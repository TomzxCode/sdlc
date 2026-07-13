---
title: "Heartbeat Execution & Adapters"
status: done
---

# Specification: Heartbeat Execution & Adapters

## Overview

A lightweight in-process scheduler wakes agents; the heartbeat execution service resolves workspace, injects secrets, loads skills, and invokes the agent's adapter. Adapters implement a common interface (`invoke`, `status`, `cancel`). Built-ins cover process, http, local CLI, and the OpenClaw gateway; external adapters are loaded as plugins with zero hardcoded core imports.

## Architecture

```
Scheduler ──► heartbeat service ──► adapter.invoke(agent, context)
   (skip rules)     (workspace, secrets, skills)        │
                                                       ├─ process: spawn, stream, SIGTERM/SIGKILL
                                                       ├─ http: outbound req, callback
                                                       ├─ local CLI: claude/codex/gemini/opencode/pi/cursor
                                                       ├─ openclaw gateway
                                                       └─ external plugin
                  heartbeat_runs (status, context_snapshot) + heartbeat_run_events
```

## Data Models

### heartbeat_runs

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id / agent_id | uuid | FK, not null | Scoping |
| invocation_source | enum | - | `scheduler \| manual \| callback` |
| status | enum | - | `queued \| running \| succeeded \| failed \| cancelled \| timed_out` |
| started_at / finished_at | timestamptz | null | Timing |
| error | text | null | Failure detail |
| external_run_id | text | null | Adapter run id |
| context_snapshot | jsonb | null | Invocation context |

Supporting tables: `heartbeat_run_events`, `heartbeat_run_watchdog_decisions`, `agent_wakeup_requests`, `agent_runtime_state`, `agent_task_sessions`.

## API Contracts

### POST /agents/:agentId/heartbeat/invoke

Triggers a heartbeat run (manual source). Returns the run record.

### Adapter interface

```ts
interface AgentAdapter {
  invoke(agent: Agent, context: InvocationContext): Promise<InvokeResult>;
  status(run: HeartbeatRun): Promise<RunStatus>;
  cancel(run: HeartbeatRun): Promise<void>;
}
```

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 409 | CONFLICT | Agent not invokable (paused/terminated/budget-blocked/active run) |

## Sequences

### Scheduled heartbeat

```
Scheduler tick → skip rules check → heartbeat service → adapter.invoke → run status + events + cost events → activity_log
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Scheduler | In-process worker | No queue infra needed for V1 |
| Adapter loading | Dynamic plugin registry | Zero hardcoded adapter imports; pure dynamic loading |

## Risks and Unknowns

1. Cheap-model profile lane must be tightly constrained to status-only recovery to avoid deliverable work on a low-cost model.

## Out of Scope

- Cloud-grade orchestration or external queue infrastructure.

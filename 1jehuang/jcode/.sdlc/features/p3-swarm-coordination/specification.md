---
title: "Swarm Multi-Agent Coordination"
status: done
---

# Specification: Swarm Multi-Agent Coordination

## Overview

Swarm coordination spans `crates/jcode-swarm-core` (message/report validation), `crates/jcode-plan` (plan DAG and mermaid/bridge helpers), `crates/jcode-task-types`, and the server-side swarm implementation in `crates/jcode-app-core/src/server/` (`swarm*.rs` and `comm_*.rs`). The coordinator agent runs in the main session; workers run as subagents. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
              coordinator agent (main session)
                        │
          plan DAG (jcode-plan, PlanItem, VersionedPlan)
                        │
   ┌────────────────────┼─────────────────────┐
   ▼                    ▼                     ▼
worker agent        worker agent          worker agent
(visible/headless/inline/auto spawn modes)
   │                    │                     │
   └──────────── typed comm channels (comm_graph, comm_plan, comm_session,
                  comm_control, comm_sync, comm_await) ────────────┘
                        │
              swarm status / plan events ──► UI (TUI / protocol)
```

## Data Models

### PlanItem / VersionedPlan (`crates/jcode-plan`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| item | PlanItem | bounded by MAX_PLAN_ITEMS = 1024 | A single task node in the plan. |
| version | int | not null | Version of the plan graph. |
| status | enum | pending/in-progress/done/failed | Progress of the item. |

### Swarm Status / Todo / Member

Shared types include `SwarmMemberStatus`, `SwarmTodoItem`, and `PlanGraphStatus` in `jcode-protocol`.

## API Contracts

### Protocol (internal)

- `RunSubagent` request — spawn a worker from the coordinator.
- `Comm*` requests — swarm message operations (send DM, broadcast, plan update).
- `ServerEvent` swarm variants — `swarm_status`, `swarm_plan`, member status snapshots.

## Sequences

### Delegate and complete a task

```
Coordinator → RunSubagent(task) → worker spawns in configured mode
Worker runs task → completion report (tldr + marker)
Server validates report (jcode-swarm-core) → sends Comm message to coordinator
Coordinator updates plan DAG → plan status events stream to UI
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Plan as versioned DAG | `VersionedPlan` in `jcode-plan` | Supports revision as tasks complete and replay/history. |
| Typed comm channels | `comm_*.rs` modules with graph/plan/session/control separation | Keeps message flows auditable and testable. |
| Report validation | tldr rule + completion marker | Prevents malformed member output from corrupting the plan. |
| Spawn modes | visible/headless/inline/auto | Lets users trade visibility against parallelism. |
| Persistence | swarm state in durable server state | Survives reloads (NFR-1). |

## Risks and Unknowns

1. Scheduling and parallelism heuristics are not fully documented in the code; inferred from module structure.
2. Plan-item limits and tldr rules may need tuning as worker counts grow.

## Out of Scope

- Cross-machine (distributed) swarm execution; workers run within one server process.
- Persistent worker identity across sessions.

---
title: "Agent Execution Engine"
status: done
---

# Specification: Agent Execution Engine

## Overview

The engine's scheduler and triage claim eligible tasks; the executor creates permission-bounded agent sessions and drives them in git worktrees; durable agents run on heartbeats with bounded auto-recovery; permission policies and sandboxes constrain commands; and every lifecycle event is recorded in the run-audit.

## Architecture

```
scheduler / triage  ── claim/lease ──►  executor (task session, worktree)
      │                                       │
      │                                 agent session
      │                                       ▼
   capacity/caps                       permission policy + sandbox backend
      │                                       │
      ▼                                       ▼
task store (advisory locks, run-audit)   agent heartbeat (durable agents)
```

## Data Models

### Agent

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Agent identifier |
| status | enum | not null | idle/active/error/paused |
| pauseReason | enum | — | error-retry-exhausted, error-unrecoverable, etc. |
| permissionPolicy | object | not null | Bounded tool/action policy |

## API Contracts

### POST /api/agents

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | yes | Agent name |
| model | string | no | Assigned model |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| agent | object | Created agent |

## Sequences

### Execution

```
triage → scheduler claim → executor creates session
   → permission check per tool → sandbox (bubblewrap/spawn) → agent runs
   → verdict → task advances (workflow graph) → run-audit events
```

### Durable recovery

```
heartbeat → error state → recoverable? → clear + retry (shared budget)
   → exhausted → park paused (pauseReason: error-retry-exhausted)
   → operator-actionable → park (pauseReason: error-unrecoverable)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Async exec for user commands | async `exec` with timeout | No blocking shellout for user config |
| superviseSpawn for children | from `@fusion/core` | Managed child processes, no nohup/detached spawn |
| Shared heartbeat budget | timer + self-healing + automation | Bounded recovery; single exhaustion point |
| Sandbox pluggable | bubblewrap / spawn-based | Command isolation backends |

## Risks and Unknowns

1. Claim/capacity accounting across lanes is detailed in scheduler tests and docs/agents.md.

## Out of Scope

- Merge mechanics (FEAT-p5) and planner oversight (FEAT-p3)
---
title: "Cron Scheduling and Subagent Delegation"
status: done
---

# Specification: Cron Scheduling and Subagent Delegation

## Overview

Cron uses a SQLite-backed job store (cron/jobs.py) and a tick loop scheduler (cron/scheduler.py). Delegation spawns child AIAgent instances with isolated context via tools/delegate_tool.py.

## Architecture

### Cron
```
Cron (cron/)
    ├── jobs.py — SQLite job store
    ├── scheduler.py — tick loop
    ├── lifecycle_guard.py — 3-minute hard interrupt
    └── suggestions.py — automated schedule suggestions
```

### Delegation
```
Delegation (tools/delegate_tool.py)
    ├── Single: task(goal, context, toolsets)
    ├── Batch: tasks([...]) — concurrent parallelism
    ├── Role: leaf (default, cannot delegate further)
    └── Role: orchestrator (can spawn sub-workers)
```

## Data Models

### Cron Job

| Field | Type | Description |
|---|---|---|
| id | TEXT | UUID |
| schedule | TEXT | Duration, every-phrase, cron expression, or ISO timestamp |
| prompt | TEXT | Job prompt |
| skills | list | Skills to load during job execution |
| model | string | Override model |
| script | string | Pre-run data collection script |
| context_from | string | Chain from another job's output |
| workdir | string | Working directory with AGENTS.md |
| platform | string | Delivery platform |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Cron storage | SQLite | Zero-dependency, simple, supports concurrent access |
| Tick loop | File lock | Prevents duplicate ticks across processes without a coordinator |
| Hard interrupt | 3-minute timeout | Prevents runaway agent loops from monopolizing the scheduler |
| Delegation | Subprocess with shared budget | Inherits parent's iteration budget, ensures total work is bounded |
| Multi-agent safety | Role: leaf | Leaf agents cannot spawn further agents, preventing cascading delegation |
| Async completion | Queue-based | Background tasks return their result to a queue that the parent checks later |

## Risks and Unknowns

1. Cron sessions skip memory (skip_memory=True) by default — long-running cron tasks lose context across job runs
2. Delegation with background=true is process-local — does not survive process restart (unlike cron)
3. The 3-minute hard interrupt may be too short for complex batch tasks

## Out of Scope

- Distributed execution across machines
- Cron job dependency graph (only chaining is supported, not DAG)
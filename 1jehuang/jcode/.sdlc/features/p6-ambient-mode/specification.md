---
title: "Ambient Mode"
status: done
---

# Specification: Ambient Mode

## Overview

Ambient mode is implemented in `crates/jcode-app-core/src/` (`ambient.rs`, `ambient_runner.rs`, `ambient_scheduler.rs`, and the `ambient/` module) with shared types in `crates/jcode-ambient-types`. The scheduler drives work cycles; the runner executes tasks; directives and safety gates control what ambient may do. CLI control lives in `src/cli/` (`jcode ambient`). This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
jcode server
└── ambient_scheduler.rs ──► work cycles
        │
        ▼
ambient_runner.rs ──► tasks (garden/scout), directives
        │
        ├── [ambient] config (directives, schedules)
        ├── safety / permissions gates (SAFETY_SYSTEM)
        └── persistence (ambient status + log, durable)
        │
        ▼
CLI: jcode ambient status|log|trigger|stop
TUI: ambient status side panel / badge
```

## Data Models

### Ambient State (`jcode-ambient-types`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| status | enum | not null | Running / idle / stopped. |
| directives | list | not null | Ambient instructions to execute. |
| log | list | append-only | Recent ambient activity. |
| schedule | config | nullable | Trigger schedule for cycles. |

## API Contracts

### CLI: `jcode ambient`

- `status` — show ambient mode state.
- `log` — show recent ambient activity.
- `trigger` — run a work cycle now.
- `stop` — stop ambient mode.
- `run-visible` (hidden) — run a cycle visibly for debugging.

## Sequences

### Work cycle

```
Scheduler ticks (or trigger) → read directives → pick tasks (garden/scout)
Runner executes task through safety/permission gates
Results logged → state persisted → status events published to UI
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Same-process scheduler | `ambient_scheduler.rs` in app-core | No separate daemon; shares server lifecycle. |
| Safety-gated runner | permissions + command-risk gates | Ambient autonomy must not bypass interactive safety (NFR-1). |
| Durable ambient state | persisted status/log | Survives reloads (NFR-3). |
| Overnight hook | overnight processing module | Long-running consolidation fits idle windows. |

## Risks and Unknowns

1. Default cycle cadence and per-cycle budgets are inferred from code; they may need operator tuning.
2. Ambient autonomy against live repositories carries inherent risk; safety coverage is critical.

## Out of Scope

- A separate ambient daemon or distributed ambient workers.
- Ambient actions on behalf of other machines or cloud services.

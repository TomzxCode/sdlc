---
title: "Scheduled Loop Engine"
status: done
---

# Specification: Scheduled Loop Engine

## Overview

The scheduler is a single in-process engine (croner) plus a per-loop one-shot timer. A tick loads the loop, guards on in-flight/open runs, decides the run role (exec / evolve / edit), creates a pending run row, and hands it to an injected `Dispatcher` (the MachineGateway in production). The pending row is the durable inbox; offline machines are handled by deferral and supersede, never by the engine failing the run.

## Architecture

```
start() ─► load enabled loops ─► schedule(loop) per loop
                                     │
                croner Cron (loop tz) │  armNextRunAt (one-shot nextRunAt)
                                     ▼
                                runLoop(id)
                                     │
            ┌─────────────┬──────────┴───────────┬──────────────┐
            │ in-flight?  │ running run?         │ role select  │
            │ (skip)      │ (skip tick)          │ edit>evolve>exec
            ▼                                 ▼
   supersede deferred pending (exec) ──► addRun(pending) ──► dispatcher.dispatch(loop, run)
```

The scheduler implements `Dispatcher`-triggered flows and a `Dispatcher` interface that is transport-agnostic. The MachineGateway implements `dispatch` in production.

## Data Models

The engine reads and writes through `store`:

### loops (relevant columns)

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Loop id |
| cron | text | not null | Cron expression |
| timezone | text | nullable | IANA timezone; null = server local |
| enabled | boolean | default true | Master schedule switch |
| nextRunAt | text (ISO) | nullable | One-shot override; consumed on fire |
| evolveDue | boolean | nullable | Marker: next tick is an evolve pass |
| evolvedRunCount | integer | nullable | Runs count at last evolution |
| editRequest | text | nullable | Pending owner edit instruction |
| machineId | text | not null | Execution machine |

### runs (created per tick)

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Run id |
| loopId | text | not null | Owning loop |
| machineId | text | not null | Bound machine |
| phase | enum | pending → running → done/error/canceled | Lifecycle |
| role | enum | exec / evolve / edit | Run kind |
| ts | text (ISO) | not null | Creation time |

## API Contracts

The engine exposes no HTTP endpoints; it is consumed through `store` and the injected Dispatcher. It provides programmatic methods on `Scheduler`: `start`, `addLoop`, `removeLoop`, `runNow`, `evolveNow`, `requestEdit`, `finishEdit`, `finishEvolution`, `maybeFlagEvolve`, `runningIds`, and the static `nextRun(expr)` cron validator.

## Sequences

### Cron tick → pending run → dispatch

```
croner fire → runLoop(id)
  ├─ getLoop; unschedule if missing
  ├─ skip if !enabled or a running run exists
  ├─ role = editRequest ? "edit" : evolveDue ? "evolve" : "exec"
  ├─ if exec pending exists: supersedePendingRun(old, reason) → skipped
  ├─ consume spent nextRunAt (≤ now + 1.5s)
  ├─ if evolveDue and !canEvolve → finishEvolution, return
  └─ addRun(pending, role) → dispatcher.dispatch(loop, run)
```

### Boot misfire catch-up

```
start() → background catchUpMissedFires(all enabled loops)
  per loop: previousRuns(1) in loop tz
    ├─ stand down if a past-due nextRunAt one-shot is present
    ├─ stand down if the occurrence predates loop creation
    └─ fire ONE compensating tick if the newest run predates the occurrence
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Cron engine | croner with `protect` + `catch` | Computes future fires only, timezone-aware, protect prevents overlap |
| Pending run as inbox | Rows in phase `pending` | Durable across restarts; machine claim is stateless |
| Deferred handling | Hold pending, supersede on next fire | Never fails an unreachable machine; queue coalesces to depth 1 |
| Supersede atomicity | `store.supersedePendingRun` phase-guard | A run claimed in the same instant is left alone |
| Evolve cadence | `EVOLVE_EVERY` runs AND `EVOLVE_MIN_INTERVAL_MS` | Prevents a fast loop from evolving many times a day |
| In-flight guard | In-process `running` set per loop | Serializes cron + one-shot landing together without DB round-trips |
| Misfire recovery | Reconstruct past occurrence at boot | croner only computes future fires; a deploy window must not lose a run |

## Risks and Unknowns

1. The in-process in-flight guard complements but never replaces the DB-level open-run check; a second scheduler process against the same DB would still double-fire (mitigated by the single-scheduler invariant).
2. `unref`'d timers can be delayed by a busy event loop; acceptable for schedule granularity.

## Out of Scope

- Executing the run (the daemon's poll claims and runs it).
- Deciding machine offline (the gateway sweep and deferral own that).
- Multi-process scheduler support (explicitly forbidden by the single-scheduler invariant).

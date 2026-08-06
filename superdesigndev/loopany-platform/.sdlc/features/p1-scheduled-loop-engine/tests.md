---
title: "Scheduled Loop Engine"
status: done
---

# Test Plan: Scheduled Loop Engine

## Scope

Testing the scheduler's tick behavior (role selection, deferral/supersede, one-shots, evolve/edit scheduling, misfire catch-up) and the run-lifecycle store operations it drives. Out of scope: the daemon's poll claim loop and agent execution (covered by the machine gateway and daemon features).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Scheduler end-to-end tick creates a pending run and dispatches | Enabled loop, dispatcher spy | One pending run created, dispatcher called with loop + run |
| TC-2 | A running run blocks the tick | Loop with a phase `running` run | No second pending run created |
| TC-3 | A deferred pending exec run is superseded on the next exec fire | Pending exec run, next exec tick | Old run outcome `skipped`, one fresh pending run remains |
| TC-4 | A non-exec fire defers rather than supersedes a pending exec | Pending exec run, evolve tick | Old pending stays, no supersede |
| TC-5 | Run-now arms a one-shot timer | `scheduler.runNow(id)` | A pending run is created through the one-shot path |
| TC-6 | Evolve-now flags evolution and fires | `scheduler.evolveNow(id)` | `evolveDue` set, pending run created |
| TC-7 | Edit request produces an `edit` role run | Loop with `editRequest` set | Next tick creates a run with role `edit` |
| TC-8 | Misfire catch-up fires one compensating tick | Loop whose newest run predates a past cron occurrence | Exactly one compensating run, coalesced |
| TC-9 | Misfire catch-up stands down for a past-due one-shot | Loop with a past-due `nextRunAt` | No double fire via catch-up |
| TC-10 | Evolve cadence respects both gates | Run counts below `EVOLVE_EVERY` or within `EVOLVE_MIN_INTERVAL_MS` | No evolve flagged |
| TC-11 | Failed dispatch marks the run error | Dispatcher throws | Run phase `error`, no unhandled rejection |
| TC-12 | Disabled loop is not scheduled; re-enable reschedules | Loop toggled `enabled` | No ticks while disabled, ticks resume after re-enable |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-13 | Scheduler drives the real store against pglite | pglite pool, seeded loop | A cron fire creates a pending row readable back through the store |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-14 | `spentNextRunAt` with a future value (the run self-rescheduled) | The future `nextRunAt` is preserved, not cleared |
| TC-15 | Cron expression that never fires again | `Scheduler.nextRun` throws; the loop is not scheduled |
| TC-16 | Dispatch throws during an edit run | Edit marker is cleared so it does not re-fire forever |

## Test Infrastructure

- vitest across both packages; server tests run against real pglite where integration is needed.
- The dispatcher is injected as a spy/fake in unit tests; `store` is exercised against pglite for integration tests.
- Scheduler consts are read at module load, so tests re-import modules to vary `LOOPANY_EVOLVE_*`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-1, TC-12 |
| FR-3 | TC-2 |
| FR-4 | TC-3, TC-4 |
| FR-5 | TC-5 |
| FR-6 | TC-5, TC-6 |
| FR-7 | TC-10 |
| FR-8 | TC-7 |
| FR-9 | TC-8, TC-9 |
| FR-10 | TC-12 |
| FR-11 | TC-14 |
| FR-12 | covered by open-runs store query used by `runningIds` |
| NFR-1 | TC-11, TC-16 |
| NFR-2 | TC-8 (background sweep) |
| NFR-3 | boot guard covered by `server/boot.test.ts` |
| NFR-5 | TC-10 |

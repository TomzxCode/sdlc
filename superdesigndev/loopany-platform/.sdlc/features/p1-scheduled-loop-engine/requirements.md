---
title: "Scheduled Loop Engine"
status: done
---

# Requirements: Scheduled Loop Engine

## Overview

The scheduled loop engine is the core of Loopany: an in-process cron scheduler that turns a loop's schedule into pending agent runs and dispatches them to the loop's bound machine. A tick creates a pending run that is the durable inbox for the machine's poll; the machine unreachable case defers rather than fails, the next fire supersedes a still-waiting run, and boot-time catch-up recovers occurrences lost inside a deploy window. The engine also schedules the self-improvement (evolve) passes, owner-requested edit runs, one-shot run-now overrides, and enforces the single-scheduler invariant.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Loop owner | Loops fire reliably on schedule, catch up after outages, and never double-fire. |
| Loop operator | A machine offline for a while loses no scheduled work; the next fire supersedes the missed one. |
| Server operator | One scheduler process per database; a deploy window does not silently drop scheduled occurrences. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The scheduler shall fire a loop on its cron expression interpreted in the loop's timezone. |
| FR-2 | Must | A tick shall create a pending run row and dispatch it to the loop's bound machine via the Dispatcher seam. |
| FR-3 | Must | A tick for a loop with a running run shall be skipped so two agents never run the same loop at once. |
| FR-4 | Must | A pending run on an unreachable machine shall be deferred, and the next exec fire shall supersede the still-waiting one as an outcome `skipped`. |
| FR-5 | Must | The scheduler shall support a one-shot `nextRunAt` override that fires once and then resumes the cron schedule. |
| FR-6 | Must | The scheduler shall support run-now (`scheduler.runNow`) and evolve-now (`scheduler.evolveNow`) triggers. |
| FR-7 | Must | The scheduler shall run a dedicated evolve pass when flagged, at most once per `EVOLVE_MIN_INTERVAL_MS` and no sooner than every `EVOLVE_EVERY` runs. |
| FR-8 | Must | The scheduler shall run a dedicated edit run when an owner `editRequest` is pending, taking precedence over a scheduled exec run. |
| FR-9 | Must | At boot, the scheduler shall detect a missed cron occurrence inside a downtime window and fire one compensating catch-up tick. |
| FR-10 | Should | A disabled loop shall not fire and its timers shall be unscheduled; re-enabling reschedules it. |
| FR-11 | Should | The scheduler shall clear the edit request and evolve marker after their runs end, preserving a future `nextRunAt` set by the run itself. |
| FR-12 | Should | The scheduler shall expose a live set of loop ids with an open run for the UI's running indicator. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | A failed dispatch (e.g. DB error) shall mark the run error and never escape as an unhandled rejection from a timer callback. |
| NFR-2 | Must | Availability | Boot readiness shall never block on the misfire catch-up sweep, so a slow catch-up cannot widen the deploy downtime window. |
| NFR-3 | Must | Availability | Exactly one process shall own the scheduler for a given database; a second process against the same DB must not double-fire. |
| NFR-4 | Should | Performance | The per-loop in-flight guard shall serialize concurrent triggers within a single scheduler process without DB round-trips. |
| NFR-5 | Should | Operability | Scheduler behavior shall be tunable via environment variables (`LOOPANY_EVOLVE_EVERY`, `LOOPANY_EVOLVE_DELAY_MS`, `LOOPANY_EVOLVE_MIN_INTERVAL_MS`). |

## Constraints

- The server executes nothing; a tick only creates rows and dispatches, never runs workflow JS or an agent.
- Overlapping ticks are skipped rather than queued for a running run.
- The pending row is the durable inbox; the engine never decides a machine is offline.
- Timers are `unref`'d so they do not hold the process open.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** a loop with cron `0 7 * * *` and timezone `Asia/Shanghai`
    - **When** the scheduler runs
    - **Then** a pending run is created at the next 07:00 in the loop's timezone
- [ ] **FR-2**
    - **Given** an enabled loop
    - **When** its cron fires
    - **Then** a pending run row exists and the Dispatcher received the loop and run
- [ ] **FR-3**
    - **Given** a loop with a run in phase `running`
    - **When** another tick fires for the same loop
    - **Then** no new pending run is created
- [ ] **FR-4**
    - **Given** a pending exec run the machine never claimed
    - **When** the next exec fire occurs
    - **Then** the old run retires as outcome `skipped` and the new pending run replaces it
- [ ] **FR-5**
    - **Given** a loop with a future `nextRunAt`
    - **When** the one-shot fires
    - **Then** one run executes and `nextRunAt` is cleared so the cron schedule resumes
- [ ] **FR-6**
    - **Given** a loop
    - **When** `runNow` or `evolveNow` is called
    - **Then** a pending run is created via the one-shot timer path
- [ ] **FR-7**
    - **Given** a loop with enough runs since the last evolve
    - **When** `maybeFlagEvolve` runs
    - **Then** an evolve pass is scheduled, but never more than once per day in steady state
- [ ] **FR-8**
    - **Given** a loop with a pending `editRequest`
    - **When** the next tick fires
    - **Then** the run role is `edit` and it takes precedence over an exec/evolve pass
- [ ] **FR-9**
    - **Given** a cron occurrence that fell inside a deploy window
    - **When** the scheduler boots
    - **Then** exactly one compensating catch-up tick fires and is coalesced
- [ ] **NFR-1**
    - **Given** a tick whose dispatch throws
    - **When** the tick completes
    - **Then** the run is marked `error` and no unhandled rejection escapes
- [ ] **NFR-3**
    - **Given** two scheduler processes against the same database
    - **When** both attempt to schedule the same loop
    - **Then** the boot guard prevents double ownership (single-scheduler invariant)

## Conflicts

None identified yet.

## Open Questions

1. None: the scheduler behavior is fully determined by the code and tests.

---
title: "Machine Gateway & BYOA Execution"
status: done
---

# Requirements: Machine Gateway & BYOA Execution

## Overview

The machine gateway is the server-side run-lifecycle core and the wire boundary to every machine. It owns the stateless HTTP poll that claims pending runs, the report that finalizes them, the sweep that reclaims stuck or deferred runs, machine enrollment and presence, delivery/prompt construction, the unified CLI dispatch router (device vs run credentials), run leases, rate limiting, and machine-scoped owner verbs (createLoop, listLoops, editLoop, loopLog). Together it implements BYOA: the server schedules and records, the machine's daemon executes, and the gateway keeps the two in lockstep without ever running code or an LLM.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Loop owner | Loops execute on their machine, results land back, and edits/logs work through both CLI and web. |
| Loop operator | A machine that sleeps or reconnects loses no work; the sweep reclaims only genuinely dead runs. |
| Server operator | Unauthenticated enrollment is closed; machine routes are rate-limited; a deploy never breaks an in-flight run. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | A machine shall poll `/api/machine/poll` with its device token to claim pending runs, receive the watch set, and stamp freshness. |
| FR-2 | Must | An idle daemon shall be able to opt into a server-held long-poll (`wait:true`, ~20s) woken by the Dispatcher when a pending run is dispatched. |
| FR-3 | Must | The gateway shall accept a run's final `report()` and retire its run lease, persisting transcript, metrics, artifacts, and cost. |
| FR-4 | Must | A run that a machine never claims or whose machine vanishes shall be reclaimed by the sweep, with a terminal-grace lease allowing one reconciling wake-report. |
| FR-5 | Must | The gateway shall support the owner verbs `new` / `loops` / `edit` / `log` / `show` / `home` over the unified `/api/machine/cli` router, keyed on credential type (device vs run). |
| FR-6 | Must | A run credential shall only exercise the run's own verbs and loop; owner-only verbs on a run credential shall be rejected. |
| FR-7 | Must | The run credential shall be a durable run lease keyed by the sha256 of the wire token, surviving deploys and long machine sleeps. |
| FR-8 | Must | Machine enrollment shall be gated: in gated mode only a token resolving to a live connect key may enroll, never an anonymous `shared` machine. |
| FR-9 | Must | Every `/api/machine/*` and `/agent-api/loop` route shall be rate-limited per IP and per token. |
| FR-10 | Must | A pending run on an unreachable machine shall be held by the sweep (deferred), never failed as "machine offline"; an online-but-unclaimed run reclaims as an error. |
| FR-11 | Should | The gateway shall deliver per-run instructions and caps (the exec/evolve/edit first-user-turn CORE) through `delivery` and `prompt`. |
| FR-12 | Should | The gateway shall expose presence (online / asleep / offline) and a per-machine watch cache with digest echo. |
| FR-13 | Should | The gateway shall run periodic `maintainStorage` (snapshot pruning + blob GC) and prune expired run leases. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Machine-route request bodies shall be capped (2MB) before parsing; per-field caps bound row bloat. |
| NFR-2 | Must | Security | The device token shall fully impersonate its machine but serialize owner-only (`tokenVisibleTo`); `loopLog` cross-scope is a flat 404. |
| NFR-3 | Must | Security | A DB leak of `run_leases` must not hand out live run credentials (hash-only storage). |
| NFR-4 | Must | Reliability | A canceled run's late `report()` shall be ignored before any loop-level write. |
| NFR-5 | Must | Availability | A deploy shall be invisible to an in-flight run; a long-sleep wake-report survives inside its grace window. |
| NFR-6 | Should | Performance | An idle poll must be read-only (`lastSeen` re-stamped at most every `LAST_SEEN_REFRESH_MS`); claim scans are targeted, never the all-open sweep. |

## Constraints

- The gateway never executes user code or an LLM; it only stores/reads bytes and computes pure functions.
- Poll is stateless HTTP; long-poll is the only server-held mechanism.
- Run self-scheduling surfaces (`reschedule`/`set-cron`) are floor-guarded on the run path only; owner `edit` is unlimited.
- Boot constructs one shared blob store handed to the gateway, sync, and CLI gateway.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**
    - **Given** a registered machine with a pending run
    - **When** it polls
    - **Then** the poll claims the pending run and returns it in the payload
- [ ] **FR-2**
    - **Given** an idle daemon polling with `wait:true`
    - **When** a new pending run is dispatched
    - **Then** the parked poll returns the run near-instantly
- [ ] **FR-3**
    - **Given** a running run that finalizes
    - **When** `report()` is called
    - **Then** the run becomes `done`, the lease retires, and transcript/metrics/artifacts persist
- [ ] **FR-4**
    - **Given** a run whose machine fell asleep mid-run
    - **When** the sweep reclaims it
    - **Then** the lease enters `terminal-grace` and exactly one late wake-report is honored (success flips it back to `done`)
- [ ] **FR-5**
    - **Given** a device token
    - **When** `loopany new/edit/log/show` posts to `/api/machine/cli`
    - **Then** the owner verb executes and returns a TOON `text` + `exitCode`
- [ ] **FR-6**
    - **Given** a run credential
    - **When** it posts an owner-only verb or a loop id outside its lease
    - **Then** the router returns 403, never a silent retarget
- [ ] **FR-7**
    - **Given** an in-flight run across a deploy
    - **When** the run reports after the restart
    - **Then** the lease still resolves and the report finalizes normally
- [ ] **FR-8**
    - **Given** gated mode and an unknown/forged device token
    - **When** it first contacts the poll route
    - **Then** it is 401'd and no `shared` machine is enrolled
- [ ] **FR-9**
    - **Given** a flood of machine-route requests
    - **When** the token bucket is exhausted
    - **Then** the route returns 429
- [ ] **FR-10**
    - **Given** a pending run on a sleeping machine
    - **When** the sweep runs
    - **Then** the run is held (deferred), never failed; an online-but-unclaimed run past the window reclaims as an error
- [ ] **NFR-1**
    - **Given** an oversized machine-route body
    - **When** the route parses it
    - **Then** it returns 413 without parsing
- [ ] **NFR-2**
    - **Given** a teammate token with machine scope
    - **When** the machine list renders
    - **Then** `token` is null and a cross-scope `loopany log` is a flat 404

## Conflicts

None identified yet.

## Open Questions

1. None: the gateway behavior is fully determined by the code and its tests.

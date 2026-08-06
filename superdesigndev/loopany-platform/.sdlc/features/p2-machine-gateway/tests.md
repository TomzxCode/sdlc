---
title: "Machine Gateway & BYOA Execution"
status: done
---

# Test Plan: Machine Gateway & BYOA Execution

## Scope

Testing the machine wire boundary: poll/claim, long-poll wake, report finalize, sweep reclaim + terminal-grace reconcile, enrollment gating, rate limiting, run leases, delivery/prompt construction, unified CLI routing, and the TOON render spine. Out of scope: daemon-side spawning and artifact byte ingress.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Poll claims a pending run for the machine | Registered machine + pending run | Claimed run returned with run token |
| TC-2 | Long-poll waiter is resolved by dispatch | Idle `wait:true` poll, new dispatch | Parked poll returns the run near-instantly |
| TC-3 | Report finalizes the run and retires the lease | Final report on an active lease | Run `done`, lease deleted, notify fired |
| TC-4 | Terminal-grace honors one reconciling wake-report | Swept run, late success report | Run flips back to `done`, no second push |
| TC-5 | Second finalize is rejected | Already-retired lease | Report ignored before any loop-level write |
| TC-6 | Enrollment is gated in gated mode | Forged/unknown device token | 401, no `shared` machine enrolled |
| TC-7 | Cross-machine id-collision re-check | Token hash mismatch on an existing machine | Enroll rejected |
| TC-8 | Rate limiter 429s when the bucket is spent | Per-IP flood | 429 after the burst/per-sec allowance |
| TC-9 | Blob-PUT and sync-POST are rate-limit-exempt | Valid device token burst | No 429 from the limiter; still 401 on an unknown token |
| TC-10 | CLI router branches on credential type | `dk_` vs run lease vs legacy bare UUID | Device verbs vs run verbs resolve correctly |
| TC-11 | Run credential rejects owner-only verbs and cross-loop ids | Run token posting `new` or a foreign loop | 403, never a silent retarget |
| TC-12 | `loopLog` cross-scope is a flat 404 | Machine B token asking for loop A's log | 404, existence never leaked |
| TC-13 | TOON serializer quotes and blocks per axi rules | Values with/without whitespace/commas | Bare vs quoted render per `gateway/toon.ts` |
| TC-14 | Presence is three-state (online/asleep/offline) | lastSeen deltas | `online` < 30s, `asleep` < 6h, else `offline` |
| TC-15 | Prompt construction builds the exec/evolve/edit CORE | Role + loop + state | First-user-turn instructions with the untrusted-data guard |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-16 | Full poll→run→report lifecycle against pglite | pglite store, seeded loop + machine | Run claims, executes (fake dispatcher), finalizes, lease retires |
| TC-17 | Machine-route body cap (2MB) | Oversized POST body | 413 before parsing |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-18 | Late report after a cancel | Ignored before any loop-level write (never advances cursor/taskFileContent) |
| TC-19 | A swept run whose wake-report is a real failure | The generic reclaim reason is replaced; no second push |
| TC-20 | Terminal-grace mutations | `agentApi`/`runCli` refuse with 409; only the final report reconciles |
| TC-21 | Deferred pending past `DEFERRED_MAX_MS` | Retires as outcome `skipped`, phase `canceled` |
| TC-22 | Alarm policy mirrors presence | Asleep (<6h) fully silent; genuinely offline gets ONE calm deferred message |

## Test Infrastructure

- vitest; the gateway takes an injectable notifier and blob store so tests observe pushes without network.
- Real pglite for integration tests; `setWebhookFetchDeps` injects DNS + fetch for notify tests.
- Rate limiting is off under vitest unless `LOOPANY_RATE_LIMIT=on` so suites never trip it.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-2 |
| FR-3 | TC-3 |
| FR-4 | TC-4, TC-19, TC-21 |
| FR-5 | TC-10 |
| FR-6 | TC-11 |
| FR-7 | durable lease + deploy survival covered by gateway/run-lease tests (TC-3, TC-16) |
| FR-8 | TC-6, TC-7 |
| FR-9 | TC-8 |
| FR-10 | TC-21, TC-22 |
| FR-11 | TC-15 |
| FR-12 | TC-14 |
| FR-13 | retention/GC covered by the artifact feature's retention tests |
| NFR-1 | TC-17 |
| NFR-2 | TC-12 |
| NFR-3 | hash-only lease storage asserted by schema tests |
| NFR-4 | TC-5, TC-18 |
| NFR-6 | lastSeen re-stamp cadence covered by gateway poll tests |

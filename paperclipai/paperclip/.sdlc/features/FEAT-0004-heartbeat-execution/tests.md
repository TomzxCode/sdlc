---
title: "Heartbeat Execution & Adapters"
status: done
session_link: "—"
---

# Test Plan: Heartbeat Execution & Adapters

## Scope

Scheduler skip rules, heartbeat run lifecycle, run control/completion, queueing, retries, recovery, execution configuration, and cost accounting are covered by the heartbeat service suite and route tests.
Out of scope: cloud-grade orchestration / external queues.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Scheduling rules | Agent state, budget, active runs | Skip/invoke verdicts (`server/src/services/heartbeat/scheduling.test.ts`) |
| TC-2 | Heartbeat queue | Pending invocations | Correct ordering/dedup (`server/src/services/heartbeat/queue.test.ts`) |
| TC-3 | Run lifecycle transitions | Run events | Correct statuses (`server/src/services/heartbeat/run-lifecycle.test.ts`) |
| TC-4 | Run control (cancel) | Running run | Graceful cancel then force-kill (`server/src/services/heartbeat/run-control.test.ts`) |
| TC-5 | Run completion | Terminal run results | Status + events recorded (`server/src/services/heartbeat/run-completion.test.ts`) |
| TC-6 | Retries and recovery | Failed runs | Retry policy + recovery (`server/src/services/heartbeat/retries.test.ts`, `server/src/services/heartbeat/recovery.test.ts`) |
| TC-7 | Run log streaming | Process stdout/stderr | Logs captured (`server/src/services/heartbeat/run-log.test.ts`) |
| TC-8 | Execution configuration | Agent + invocation context | Resolved workspace/secrets/skills (`server/src/__tests__/heartbeat-execution-configuration.test.ts`, `server/src/services/heartbeat/run-preparation.test.ts`) |
| TC-9 | Cost accounting | Run cost events | Correct ledger entries (`server/src/__tests__/heartbeat-cost-accounting.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-10 | Run runtime status | Running run | Accurate status payload (`server/src/services/heartbeat-run-runtime-status.test.ts`) |
| TC-11 | Stop metadata | Cancelled run | Stop attribution recorded (`server/src/services/heartbeat-stop-metadata.test.ts`) |
| TC-12 | Archived-company guard | Archived company agent | Invocation blocked (`server/src/__tests__/heartbeat-archived-company-guard.test.ts`) |
| TC-13 | Execution continuation | Interrupted run | Continuation or rejection (`server/src/services/execution-continuation.test.ts`) |
| TC-14 | Run cancellation service | Active run | SIGTERM then SIGKILL (`server/src/services/run-cancellation.test.ts`) |
| TC-15 | GitHub launchers lifetime | Launcher config | Correct launcher lifecycle (`server/src/services/heartbeat-github-launchers.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-16 | Scheduled heartbeat round-trip | Scheduler tick on due agent | Run invoked, status/events/costs recorded |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-17 | Agent at hard budget limit on schedule fire | No new run, skip recorded |
| TC-18 | Orphaned/stuck runs | Detected and recovered automatically |

## Test Infrastructure

- Vitest suite; dedicated `server/src/services/heartbeat/` test modules.
- PGlite dev DB; native-runtime integration tests for executor paths.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-1, TC-12, TC-17 |
| FR-03 | TC-3, TC-10 |
| FR-04 | TC-4, TC-7, TC-14 |
| FR-05 | TC-8 (related: HTTP adapter coverage in adapter tests) |
| FR-06 | TC-8 |
| FR-07 | TC-15 (plus local CLI adapter tests, e.g. `cursor-local-adapter.test.ts`) |
| FR-08 | TC-6, TC-13, TC-18 |
| NFR-01 | TC-16 (ack timing; release-gate item) |
| NFR-02 | TC-7, TC-9, TC-11 |

---
title: "Ambient Mode"
status: done
---

# Test Plan: Ambient Mode

## Scope

Covers ambient scheduler, runner, state persistence, and safety gating. Out of scope: real overnight schedules and long-running cycle behavior in CI.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Ambient state and lifecycle | `crates/jcode-app-core/src/ambient_tests.rs` | Ambient starts, runs, stops, and persists correctly |
| TC-2 | Ambient runner behavior | `crates/jcode-app-core/src/ambient_runner.rs` tests | Tasks execute through the runner |
| TC-3 | Scheduler behavior | `crates/jcode-app-core/src/ambient_scheduler.rs` tests | Cycles trigger on schedule |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Ambient e2e | `tests/e2e/ambient.rs` | Ambient work cycle runs end to end |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-5 | Ambient task requires permission | Action gated by safety system, no bypass |
| TC-6 | Server reload during ambient cycle | Ambient state recovered; cycle resumes |
| TC-7 | Risky command in ambient task | Passed through command-risk gate before execution |

## Test Infrastructure

- E2E harness under `tests/e2e/` with test support modules.
- Durable-state fixtures for reload scenarios.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-3, TC-4 |
| FR-2 | TC-2 |
| FR-3 | TC-1, TC-6 |
| FR-4 | TC-5, TC-7 |
| NFR-1 | TC-5, TC-7 |
| NFR-3 | TC-6 |

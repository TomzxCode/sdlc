---
title: "Telemetry"
status: done
---

# Test Plan: Telemetry

## Scope

Covers client-side event emission, queue behavior, opt-out, lifecycle/onboarding tracing, and server-side worker ingestion. Out of scope: production D1 data volume behavior.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Client telemetry core | `crates/jcode-telemetry-core/src/tests.rs` | Events queue and flush correctly |
| TC-2 | Lifecycle event tracing | `crates/jcode-telemetry-core/src/lifecycle.rs` tests | Session lifecycle events produced with correct end reasons |
| TC-3 | Onboarding trace | `crates/jcode-telemetry-core/src/onboarding_trace.rs` tests | Onboarding steps traced correctly |
| TC-4 | Client-side telemetry app-core | `crates/jcode-app-core/src/telemetry_tests.rs` | App-level telemetry integration works |
| TC-5 | Usage accounting | `crates/jcode-app-core/src/usage_tests.rs` | Token usage totals correct |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Worker ingestion | `telemetry-worker/test/worker.test.mjs` | Worker validates and stores events |
| TC-7 | Token-value view | `telemetry-worker/test/token-value.test.mjs` | Token-value aggregation works |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Telemetry endpoint down | Client workflow unaffected; send fails silently |
| TC-9 | Queue full | Queue bounded, no unbounded growth |
| TC-10 | Opt-out set | No events emitted |

## Test Infrastructure

- `telemetry-worker/test/*.mjs` for worker behavior.
- Client queue fixtures for boundedness.
- Opt-out env-var test scenarios.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-1, TC-8 |
| FR-3 | TC-10 |
| FR-5 | TC-6 |
| FR-7 | TC-6 |
| FR-8 | TC-2 |
| NFR-2 | TC-8 |
| NFR-3 | TC-9 |

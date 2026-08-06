---
title: "Command Center & Operational Monitoring"
status: done
---

# Test Plan: Command Center & Operational Monitoring

## Scope

Covers the Command Center fleet/health surfaces, usage and cost tracking, HMAC signal connectors, and monitor/diagnostics routes.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Signal connector route validation | valid/invalid type | 202 for valid, 401/400 otherwise |
| TC-2 | Usage/cost accounting | task tokens | Per-task usage/cost rows |
| TC-3 | Monitor route health | system snapshot | Health payload rendered |
| TC-4 | Command Center controls CSS contract | control styles | Tokens applied per contract |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Signal payload mapped to board | HMAC-signed payload | Board/command surface updated |
| TC-6 | Usage route from live store | executed tasks | Usage data served |
| TC-7 | Diagnostics routes | engine running | Diagnostics served |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Unsigned signal | Rejected 401 |
| TC-9 | Unreachable node in health | Degrades gracefully |

## Test Infrastructure

- Vitest dashboard suites; command-center component interactive tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-3, TC-4 |
| FR-2 | TC-2, TC-6 |
| FR-3 | TC-1, TC-5, TC-8 |
| FR-4 | TC-7 |
| NFR-1 | TC-8 |

## Key Test Files

- `packages/dashboard/src/routes/__tests__/register-signal-routes*.test.ts`, `codebase-metrics-route.test.ts`, `register-system-maintenance-routes.test.ts`
- `packages/dashboard/app/components/command-center/__tests__/*`, `packages/dashboard/app/__tests__/usage-*.test`
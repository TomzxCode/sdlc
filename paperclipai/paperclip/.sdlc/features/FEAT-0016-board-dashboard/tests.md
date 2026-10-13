---
title: "Board Dashboard"
status: done
session_link: "reverse-engineered during sync (no session)"
---

# Test Plan: Board Dashboard

## Scope

Dashboard aggregation endpoint and React dashboard pages are covered by existing server and UI tests.
Out of scope: p95 latency benchmarking (NFR-01) and wallboard live-refresh timing, which have no automated perf harness.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Dashboard service aggregates agent counts, spend, approvals | Company with agents, cost events | Correct counts and utilization (server/src/__tests__/dashboard-service.test.ts) |
| TC-2 | Dashboard page renders cards and handles states | Mocked dashboard payload | Cards render; loading/error states covered (ui/src/pages/Dashboard.test.ts) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-3 | Dashboard route returns scoped payload with company access checks | Seeded company, authorized caller | 200 with agentCounts/spend/pendingApprovals; 403/404 otherwise |

## End-to-End Tests

None automated for this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-4 | Budget service data missing | Dashboard degrades gracefully (NFR-02) |
| TC-5 | Disconnect/retry on dashboard stream | Covered by dashboard-disconnect-retry test |

## Test Infrastructure

- Existing vitest suites in server/src/__tests__ and ui/src/pages.
- No extra fixtures required beyond current test seeds.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2, TC-3 |
| FR-02 | TC-1, TC-2 |
| FR-03 | TC-1, TC-2 |
| FR-04 | TC-1 |
| FR-05 | TC-2 |
| FR-07 | TC-5 |
| FR-08 | TC-2 (DashboardLive.tsx exists; live-refresh timing not asserted) |
| NFR-01 | Gap: no automated p95 perf test |
| NFR-02 | TC-4 |

Real test files (4 cases in server/src/__tests__/dashboard-service.test.ts, 4 in ui/src/pages/Dashboard.test.ts, plus server/src/__tests__/dashboard-disconnect-retry.test.ts).

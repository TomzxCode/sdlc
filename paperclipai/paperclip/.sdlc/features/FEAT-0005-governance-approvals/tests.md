---
title: "Governance & Approvals"
status: done
session_link: "—"
---

# Test Plan: Governance & Approvals

## Scope

Approval types/statuses, transactional decisions, board override authority, budget hard-stops, execution policies, and scoped task-watchdog authority are covered by service and route tests.
Out of scope: multi-board governance / human RBAC granularity.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Approvals service decisions | Approve/reject/cancel payloads | Terminal states, no lost decisions (`server/src/__tests__/approvals-service.test.ts`) |
| TC-2 | Approval route idempotency | Duplicate decision requests | Single decision applied (`server/src/__tests__/approval-routes-idempotency.test.ts`) |
| TC-3 | Watchdog classifier | Watchdog run context | Scoped-mutation verdicts (`server/src/__tests__/task-watchdogs-classifier.test.ts`) |
| TC-4 | Execution policy evaluation | Issue + policy state | Gate enforcement (`server/src/__tests__/issue-execution-policy.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Watchdog scheduler | Watched subtree with stalled path | Live path restored inside subtree (`server/src/__tests__/task-watchdogs-scheduler.test.ts`) |
| TC-6 | Issue watchdog routes | Watchdog config payloads | Persisted config, scoped authority (`server/src/__tests__/issue-watchdogs-routes.test.ts`) |
| TC-7 | Issue approvals linkage | Issue + approval | Approval blocks/allows correctly (`server/src/services/issue-approvals.ts` exercised via approval tests) |
| TC-8 | Active-run watchdog policy | Active run state | Correct policy verdicts (`server/src/modules/active-run-watchdog/domain/policy.test.ts`, `server/src/modules/active-run-watchdog/application/use-cases.test.ts`) |
| TC-9 | Agent lifecycle approvals (hire/strategy gate) | Hire/CEO-strategy approvals | Board decision gates execution (`server/src/modules/agent-lifecycle/__tests__/lifecycle.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-10 | CEO strategy gate | CEO drafts delegated tasks, strategy unapproved | Tasks cannot enter active execution states |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Watchdog attempts hire/budget approval or cross-company touch | Denied, no probe issue/comment created |
| TC-12 | Decision on already-terminal approval | Rejected `409` conflict |
| TC-13 | Non-board actor attempts board-only decision | Rejected `403` |

## Test Infrastructure

- Vitest suite; watchdog scheduler/classifier and active-run-watchdog module tests.
- `doc/TASK-WATCHDOG.md` documents the scoped watchdog contract.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2 |
| FR-02 | TC-9, TC-10 |
| FR-03 | TC-1, TC-13 |
| FR-04 | Activity-log assertions in approval tests |
| FR-05 | TC-4 |
| FR-06 | TC-3, TC-5, TC-6, TC-11 |
| NFR-01 | TC-11, TC-13 |
| NFR-02 | Watchdog metadata assertions in scheduler tests |

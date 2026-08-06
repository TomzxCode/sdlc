---
title: "Planning Mode & Planner Oversight"
status: done
---

# Test Plan: Planning Mode & Planner Oversight

## Scope

Covers plan approval, planner confirmation, overseer state/events, interventions, the human-control guard, handoff recovery, and dashboard control surfaces. Board move tests belong to FEAT-p1.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Planner confirmation lifecycle | confirmation request | Pending → resolved confirmation |
| TC-2 | Planner intervention record | intervention | Timeline entry persisted |
| TC-3 | Overseer state transitions | oversight level change | State reflects override |
| TC-4 | Overseer events emitted | overseer action | Event recorded with ids/outcomes metadata |
| TC-5 | Planner recovery | interrupted handoff | Recovery enqueues continuation |
| TC-6 | Planner role is not a column | planner state | Not rendered as a board column |
| TC-7 | Oversight human-control guard | user-paused/auto-merge-off task | All oversight action withheld |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-8 | Planner overseer runtime | engine running | Overseer tick acts per level |
| TC-9 | Overseer intervention wiring | steer level + intervention | Intervention routed to operator |
| TC-10 | Overseer runtime snapshot | active planner | Snapshot reflects runtime state |
| TC-11 | Executor live overseer retry gate | execution + overseer | Retry gated by overseer |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-12 | Overseer off cleanup | Cleanup removes overseer state |
| TC-13 | Plan-review failure | Replan via plan-replan seam |

## Test Infrastructure

- Vitest in core/engine/dashboard suites; `planner-overseer-*.test.ts` family

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-13 |
| FR-2 | TC-1, TC-5 |
| FR-3 | TC-3, TC-4, TC-8, TC-9, TC-10 |
| FR-4 | TC-11 |
| FR-5 | TC-2, TC-4 |
| FR-6 | TC-7 |
| NFR-1 | TC-6 |

## Key Test Files

- `packages/core/src/__tests__/planner-confirmation.test.ts`, `planner-intervention.test.ts`, `planner-overseer-events.test.ts`, `planner-overseer-state.test.ts`, `planner-recovery.test.ts`, `overseer-emission-guard.test.ts`, `planner-role-is-not-a-column.test.ts`
- `packages/engine/src/__tests__/planner-overseer.test.ts`, `planner-overseer-off-cleanup.test.ts`, `planner-overseer-intervention-wiring.test.ts`, `planner-overseer-runtime-snapshot.test.ts`, `executor-live-overseer-retry-gate.test.ts`
- `packages/dashboard/src/routes/__tests__/tasks-overseer-controls.test.ts`, `tasks-planner-overseer-state.test.ts`, `register-planning-subtask-routes.parent-close.test.ts`
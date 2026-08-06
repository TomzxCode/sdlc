---
title: "Agent Execution Engine"
status: done
---

# Test Plan: Agent Execution Engine

## Scope

Covers triage/scheduler claiming, executor session driving, permission policy enforcement, sandbox isolation, agent heartbeat recovery, and run-audit emission. Merge and review nodes belong to FEAT-p5.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Agent permission policy | restricted action | Action blocked/prompted per policy |
| TC-2 | Agent store routing policy | agent config | Correct lane routing |
| TC-3 | Assigned-task ranking (triage) | task candidates | Ranked claim order |
| TC-4 | Sandbox audit on routine runner | sandboxed command | Sandbox applied, audit recorded |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Scheduler auto-claim invalidation | stale claim | Claim invalidated |
| TC-6 | Executor approval gate | gated task | Held until approval |
| TC-7 | Agent heartbeat procedures | durable agent | Heartbeat moves work / parks correctly |
| TC-8 | Triage column audit | triage run | Column assignment correct |
| TC-9 | Scheduler paused dispatch refusal | paused task | Dispatch refused |
| TC-10 | Scheduler fanout escalation lanes | overloaded lane | Escalation applies |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Agent heartbeat error recovery | Recoverable → retry; exhausted → parked paused |
| TC-12 | Deleted blocker wip dependent | Scheduler avoids deadlock |
| TC-13 | Node unreachable during scheduling | Claims audited, no loss |

## Test Infrastructure

- Vitest engine/core suites; PostgreSQL-backed where required; fake timers for heartbeat

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-3, TC-5, TC-8, TC-9, TC-10 |
| FR-2 | TC-6 |
| FR-3 | TC-7, TC-11 |
| FR-4 | TC-1, TC-2 |
| FR-5 | TC-4 |
| FR-7 | TC-12, TC-13 |

## Key Test Files

- `packages/engine/src/__tests__/triage-*.test.ts`, `executor-*.test.ts`, `agent-heartbeat-*.test.ts`, `scheduler-*.test.ts`, `routine-runner.test.ts`, `routine-runner-sandbox-audit.test.ts`
- `packages/core/src/__tests__/agent-permissions.test.ts`, `agent-permission-policy.test.ts`, `agent-store-routing-policy.test.ts`, `assigned-task-ranking.test.ts`
- `packages/dashboard/src/routes/__tests__/agent-core-routes.test.ts`, `agent-onboarding-routes.test.ts`
- `packages/dashboard/app/__tests__/agent-runs-ui.test.ts`, `agent-detail-settings-theme-styling.test.ts`
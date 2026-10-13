---
title: "Goal Hierarchy"
status: done
session_link: "reverse-engineered during sync 2026-10-13"
---

# Test Plan: Goal Hierarchy

## Scope

Covers goal CRUD, parent_id hierarchy, level/status enums, owner agent tracking, and goal links from issues and projects.
Out of scope: goal-based budget allocation and automatic progress rollup (per specification).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Goal validation | Create/update payload | Valid goals accepted, invalid rejected (`server/src/__tests__/project-goal-validation.test.ts`) |
| TC-2 | Runner goals service | Goal-scoped runner query | Correct goal resolution (`server/src/services/runner-goals.test.ts`) |
| TC-3 | Issue goal fallback | Issue without direct goal | Fallback goal chain resolved (`server/src/__tests__/issue-goal-fallback.test.ts`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Issues goal context routes | Issue with goal_id | Goal chain returned in context (`server/src/__tests__/issues-goal-context-routes.test.ts`) |
| TC-5 | Project goal telemetry routes | Project with goal_id | Telemetry scoped by goal (`server/src/__tests__/project-goal-telemetry-routes.test.ts`) |
| TC-6 | Runner goal control broker | Goal-gated run request | Run admitted or held per goal policy (`server/src/services/runner-goal-control-broker.test.ts`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-7 | Goal hierarchy trace | Create root goal, create child with parent_id, link issue via goal_id | Chain traceable from issue to company root |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Goal for wrong company | 403/404 on cross-company access |
| TC-9 | Invalid level or status enum | 400 INVALID_INPUT returned |

## Test Infrastructure

- Vitest suites under `server/src/__tests__/` and `server/src/services/`.
- Seeded companies, goals, issues, and projects with goal links.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-7 |
| FR-03 | TC-2 |
| FR-04 | TC-3, TC-4, TC-5, TC-7 |
| FR-05 | TC-4 |
| NFR-01 | TC-4, TC-5, TC-6 |

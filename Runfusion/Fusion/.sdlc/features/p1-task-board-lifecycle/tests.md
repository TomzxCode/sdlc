---
title: "Task Board & Task Lifecycle Management"
status: done
---

# Test Plan: Task Board & Task Lifecycle Management

## Scope

Covers task creation, lifecycle moves and guards, soft-delete/archive, comments and artifacts, search/filter, and the board/list rendering. Workflow-graph execution tests belong to FEAT-p2.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Move task while planning rejects with guard | task in planning, invalid move | Move rejected, column unchanged |
| TC-2 | Delete task while planning rejected | planning task delete | Delete blocked |
| TC-3 | Task creation persists title/column | create payload | Task row with spec doc |
| TC-4 | Task document concurrency | concurrent doc writes | One writer wins under advisory lock |
| TC-5 | Soft-delete keeps tombstone | delete task | Tombstone present, row not resurrectable |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Task workflow routes expose move bypass guards | task exists | Route returns resolved column order / guard behavior |
| TC-7 | Task-not-found 404 | missing task id | 404 response |
| TC-8 | API task mutations from the SPA | live dashboard | Task created and rendered on board |
| TC-9 | Board move across columns | multiple tasks | Board order reflects resolved column order |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-10 | Column unsupported by the workflow | Column rendered with degraded-mode flag |
| TC-11 | Concurrent lifecycle mutations on same task | Exactly one succeeds under advisory lock |
| TC-12 | Mobile viewport board | Board renders usable on mobile breakpoints |

## Test Infrastructure

- Vitest; `@fusion/core`/`@fusion/engine`/`@fusion/dashboard` package test suites
- In-memory fakes and PostgreSQL-backed suites where required

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-3, TC-8 |
| FR-2 | TC-6, TC-9, TC-12 |
| FR-3 | TC-4 |
| FR-4 | TC-1, TC-10, TC-11 |
| FR-6 | TC-2, TC-5 |
| FR-7 | TC-6, TC-7, TC-8 |
| NFR-1 | TC-4, TC-11 |
| NFR-3 | TC-12 |

## Key Test Files

- `packages/core/src/__tests__/move-task-if-planning.test.ts`, `delete-task-if-planning.test.ts`, `task-creation`, `task-document-concurrency`
- `packages/dashboard/src/routes/__tests__/register-task-workflow-routes*.test.ts`
- `packages/dashboard/app/__tests__/api-tasks.test.ts`, `board-mobile-*.test.ts`, `column-role-degraded-flags.test.ts`
- `packages/cli/src/commands/__tests__/task.test.ts`, `task-lifecycle.test.ts`, `task-lock-retry.test.ts`
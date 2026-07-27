---
title: "Session Goals (Autonomous Multi-Turn Execution)"
status: done
---

# Test Plan: Session Goals

## Scope

Server-side goal runtime logic, audit integration, session metadata persistence, and UI goal arm store.
Excludes: multi-session goals, goal templates.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Goal arm store sets armed state | setArmed(true) | armed === true, objectiveOverride === null |
| TC-2 | Goal arm store sets armed with override | setArmed(true, "custom text") | armed === true, objectiveOverride === "custom text" |
| TC-3 | Goal arm store consume clears state | consume() returns { armed: true }, then check state is reset | armed === false after consume |
| TC-4 | Goal runtime creates goal metadata | Goal payload with objective | metadata.openchamber.goal created with status active |
| TC-5 | Goal runtime pauses execution | Pause signal on active goal | status transitions to paused |
| TC-6 | Goal runtime resumes paused goal | Resume signal | status transitions to active |
| TC-7 | Audit verdict blocks after streak | 3 consecutive blocked verdicts | status transitions to blocked |
| TC-8 | Token budget enforcement | tokensUsed >= tokenBudget | status transitions to budgetLimited |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | Full goal loop: set -> auto-continue -> complete | Active session, goal set | Auto-continuations sent, goal completes |
| TC-10 | Goal persist across server restart | Active goal on session | After restart, goal status is restored |
| TC-11 | Audit uses small model configuration | Goal active, audit triggered | Audit call uses configured small model |
| TC-12 | Session compaction preserves goal | Compaction event on goal session | goal metadata preserved post-compaction |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | Audit service unavailable repeatedly | auditFailStreak increments; after limit, goal blocks |
| TC-14 | Turn cap reached before objective complete | status: complete with note "turn limit reached" |
| TC-15 | Empty objective text | Goal creation rejected or defaults to fallback |
| TC-16 | Concurrent goal set on same session | Stale-write guard prevents overwrite; operation rejected |

## Test Infrastructure

- `packages/web/server/lib/session-goal/create.test.js` — goal creation tests
- `packages/web/server/lib/session-goal/runtime.test.js` — goal runtime tests
- `packages/ui/src/stores/useSessionGoalArmStore.ts` — UI arm store (unit tested in component tests)
- Mock small model client for audit verification

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-2, TC-4 |
| FR-02 | TC-2 |
| FR-03 | TC-9, TC-14 |
| FR-04 | TC-7, TC-11 |
| FR-05 | TC-5, TC-6 |
| FR-06 | TC-8 |
| FR-07 | TC-10 |
| FR-08 | TC-6 |
| FR-09 | (UI tests) |
| FR-10 | TC-7, TC-8, TC-13 |
| FR-11 | TC-11 |
| FR-12 | TC-8 |
| FR-13 | TC-12 |
| FR-14 | Not tested (future scope) |
| NFR-01 | TC-13, TC-14 |
| NFR-02 | TC-13 |
| NFR-03 | TC-11 |

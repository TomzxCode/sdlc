---
title: "Missions, Goals, Research & Evals"
status: done
---

# Test Plan: Missions, Goals, Research & Evals

## Scope

Covers mission hierarchy and sync, mission autopilot and execution loop, goals/citations/anchoring, research orchestration and providers, and eval follow-ups. Board and merge mechanics belong to FEAT-p1/FEAT-p5.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Mission store validation diagnostics | invalid mission | Diagnostic error |
| TC-2 | Mission store sync auto-merge | mission sync | Auto-merge transition applied |
| TC-3 | Mission store sync loop transition | loop transition | State machine advances |
| TC-4 | Goal citation extraction | goals text | Citations extracted |
| TC-5 | Goal citation audit aggregation | citations | Aggregated audit output |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Mission autopilot | mission with features | Features sync to board tasks |
| TC-7 | Mission execution loop | autopilot active | Loop drives feature execution |
| TC-8 | Mission scheduler | schedulable missions | Scheduled per policy |
| TC-9 | Mission feature sync | feature changes | Board reflects sync |
| TC-10 | Mission verification | completed feature | Verification gate runs |
| TC-11 | Goal context injection | active goal | Context injected into sessions |
| TC-12 | Goal anchoring audit | goal anchors | Anchoring audit passes |
| TC-13 | Eval follow-ups | scored task | Follow-ups enqueued |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-14 | Duplicate mission feature | Deduplicated / diagnostic |
| TC-15 | Research provider failure | Step-runner handles and reports |

## Test Infrastructure

- Vitest in core/engine/dashboard; engine mission/goal/research suites

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-3 |
| FR-2 | TC-6, TC-7, TC-8, TC-9 |
| FR-3 | TC-4, TC-5, TC-11, TC-12 |
| FR-4 | TC-15 |
| FR-5 | TC-13 |
| FR-6 | TC-14 |

## Key Test Files

- `packages/core/src/__tests__/mission-store.*.test.ts`, `goal-citation-extractor.test.ts`, `goal-citation-audit-aggregation.test.ts`
- `packages/engine/src/__tests__/mission-autopilot.test.ts`, `mission-execution-loop.test.ts`, `mission-scheduler.test.ts`, `mission-feature-sync*.test.ts`, `mission-verification*.test.ts`, `goal-*.test.ts`, `eval-followups.test.ts`
- `packages/dashboard/src/routes/__tests__/mission-*.test.ts`, research route tests
- `packages/dashboard/app/__tests__/api-missions.test.ts`; `packages/cli/src/commands/__tests__/research.test.ts`
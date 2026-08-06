---
title: "Automated Code Review, Merge & PR Automation"
status: done
---

# Test Plan: Automated Code Review, Merge & PR

## Scope

Covers review-node verdicts, merge strategies and conflict resolution, merge guards (file-scope, overlap, diff-volume, lineage), post-squash audit, smart-pull/auto-prerebase, already-merged detection, and PR create/monitor/finalize.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | File-scope invariant on squash | out-of-scope files | FileScopeViolationError |
| TC-2 | Already-merged detector | landed branch | Classified landed, skipped |
| TC-3 | Empty cherry-pick | no-op commit | No empty commit created |
| TC-4 | Diff-volume gate | suspicious shrinkage | Squash blocked |
| TC-5 | Overlap guard | recent main overlap | Flip to prefer-branch when smart |
| TC-6 | Merge advance events | merge plan | Events emitted |
| TC-7 | Auto-merge retry cap settings | retryable merge | Retry up to cap then park |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-8 | Merger conflict resolution | conflict on branch | Resolved and merged |
| TC-9 | Auto-prerebase on divergence | divergent branch | Fast-forward reconciled |
| TC-10 | Commit strategy real-git | rebase vs squash | Correct commit topology |
| TC-11 | PR monitor response run | PR updated | Monitor responds and finalizes |
| TC-12 | Merge advance notice route | merge in progress | Advance notice served |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | Duplicate commits on main | Dropped before merging |
| TC-14 | Push divergence after merge | Recovery-branch safety ref; non-fatal aborted push |
| TC-15 | Contamination auto-recovery | First pass bounded; repeated escalates |

## Test Infrastructure

- Vitest engine suite; real-git tests (`merger-*.real-git.test.ts`); slow variants for dependency installs

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-2 |
| FR-2 | TC-8, TC-10 |
| FR-3 | TC-9 |
| FR-4 | TC-1, TC-4, TC-5 |
| FR-5 | TC-11 |
| FR-6 | TC-2, TC-13 |
| FR-7 | TC-6, TC-12 |
| NFR-1 | TC-1 |
| NFR-2 | TC-3, TC-13 |
| NFR-3 | TC-15 |

## Key Test Files

- `packages/engine/src/__tests__/merger-*.test.ts`, `already-merged-detector.real-git.test.ts`, `auto-merge-fact-providers.test.ts`, `auto-merge-retry-cap-settings.test.ts`, `smart-pull`/`pr-*` tests
- `packages/dashboard/src/routes/__tests__/register-task-workflow-routes.merge-advance-events.test.ts`, `...merge.test.ts`, `task-review-routes.test.ts`
- `packages/cli/src/commands/__tests__/pr-lock-retry.test.ts`, `git.test.ts`
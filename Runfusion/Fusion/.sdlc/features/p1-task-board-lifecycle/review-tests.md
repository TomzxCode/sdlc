---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Named test files that do not exist:

- Key Test Files lists `task-creation` and `task-document-concurrency` as test files under `packages/core/src/__tests__/`. Neither path exists. `task-document-concurrency` is a source module at `packages/core/src/task-document-concurrency.ts`, and its coverage sits in `packages/core/src/__tests__/postgres/taskstore-remaining.test.ts:36`.
- Key Test Files lists `packages/dashboard/src/routes/__tests__/register-task-workflow-routes*.test.ts`. The glob still matches 13 files, so the reference holds, but the file the plan leans on for TC-6 and TC-7 is `register-task-workflow-routes.move-bypassguards.test.ts` and `register-task-workflow-routes.task-not-found-404.test.ts`, and neither the name nor the count is recorded.

Test cases with no named coverage:

- TC-3 "Task creation persists title/column" has no file named in Key Test Files. The nearest coverage is `packages/core/src/__tests__/postgres/create-task-reserved-id.pg.test.ts` and `packages/core/src/__tests__/postgres/task-proposal-claim.pg.test.ts`.
- TC-5 "Soft-delete keeps tombstone" has no file named in Key Test Files. The nearest coverage is `packages/core/src/__tests__/postgres/soft-delete-resurrection-FN-5233.pg.test.ts` and `packages/core/src/__tests__/task-deleted-outbox-consumer-backoff.test.ts`.
- TC-11 "Concurrent lifecycle mutations on same task" has no file named in Key Test Files. The advisory-lock contention coverage is in the PostgreSQL-gated suites `packages/core/src/__tests__/postgres/workflow-capacity-invariant.pg.test.ts:352` and `:417`, and `packages/core/src/__tests__/postgres/archive-live-task-fence.pg.test.ts:52`. The CLI-side retry coverage is `packages/cli/src/commands/__tests__/task-lock-retry.test.ts`.
- TC-9 "Board move across columns" asserts a multi-task board move that the product does not implement, so no test can exist for it. The nearest coverage is the per-task column order in `packages/dashboard/src/routes/__tests__/register-task-workflow-routes.resolved-column-order.test.ts`.

Coverage matrix gaps:

- The Coverage Matrix has no row for FR-5, FR-8, FR-9, NFR-2, or NFR-4, so those requirements are unverified by the plan.
- FR-3 is mapped only to TC-4, which covers document concurrency. Nothing in the plan covers the persistence of comments, artifacts, dependencies, branch context, or file scope, which is what FR-3 actually requires.
- FR-7 is mapped to TC-6, TC-7, and TC-8, all of which exercise the dashboard API only. Nothing covers the CLI surface, which the requirement names.

Significant test areas the plan does not cover:

- The board, list, column, and task card component suites are absent from Key Test Files: `packages/dashboard/app/components/__tests__/Board.test.tsx`, `Column.test.tsx`, `ListView.test.tsx`, and `TaskCard.u11-merged-column.test.tsx`.
- Per-task column role identity is absent: `packages/dashboard/app/__tests__/columnRoles.test.ts` and `packages/dashboard/app/__tests__/task-detail-column-role-identity.test.ts`.
- Multi-lane board workflows are absent: `packages/dashboard/src/routes/__tests__/register-task-workflow-routes.resolved-column-order.test.ts` and `packages/dashboard/app/hooks/useBoardWorkflows.ts` have no plan entry, and no test file name covers the board workflow payload in `packages/dashboard/src/routes/board-workflows.ts`.
- Duplicate intake is absent: `packages/core/src/__tests__/duplicate-guard.test.ts` and `packages/core/src/__tests__/same-agent-duplicate-intake.test.ts` cover the guard that FR-1 does not mention.
- Archive liveness and cold storage are absent: `packages/core/src/__tests__/task-archive-liveness.test.ts`, `packages/core/src/__tests__/archive-live-task-guard.test.ts`, and `packages/core/src/__tests__/archive-all-done-lane.test.ts`.
- Cross-task overlap waits are absent: `packages/core/src/__tests__/postgres/overlap-wait-persistence.pg.test.ts` and `packages/core/src/__tests__/store-overlap-repair-lanes-resolved.test.ts`.
- Task document revisions and archived publications are absent: `packages/core/src/__tests__/postgres/artifacts-documents-evals.pg.test.ts` covers the `task_documents` and `artifacts` tables, and no plan entry names it.
- Recommendations and steering are absent: `packages/core/src/__tests__/task-recommendations-list.test.ts` and `packages/dashboard/src/routes/__tests__/task-recommendation-routes.test.ts`.
- The hard-cancel move contract has no plan entry, although the specification's Sequences section names it: `packages/core/src/__tests__/postgres/task-move-hard-cancel-ordering.pg.test.ts` and `packages/core/src/__tests__/task-move-disposer.test.ts`.

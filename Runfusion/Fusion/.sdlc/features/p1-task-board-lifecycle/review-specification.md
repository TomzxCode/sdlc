---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Architecture:

- The diagram names "Dashboard API registrars (register-tasks, register-task-workflow-routes)". `packages/dashboard/src/routes/register-tasks.ts` is an empty stub that registers nothing and states it was superseded in FN-2541. It is also absent from the mount contract in `packages/dashboard/src/routes/create-api-routes-mount-sequence.ts:8`, which lists only `registerTaskWorkflowRoutes` for this domain.
- The diagram lists the core store modules as "task-creation, mutation-ops, lifecycle-ops, moves, comments-ops, task-artifacts-ops, file-scope, branch-context, search, task-advisory-lock". The store also owns the archive lifecycle (`packages/core/src/task-store/archive-lifecycle.ts`, `archive-lifecycle-2.ts`), the branch groups (`packages/core/src/task-store/branch-group-ops.ts`), the cross-task overlap waits (`packages/core/src/task-store/overlap-wait-ops.ts`), the dependency writes (`packages/core/src/task-store/update-task-deps.ts`), the symbol locks (`packages/core/src/task-store/symbol-locks.ts`), and the per-task workflow selection (`packages/core/src/task-store/workflow-definitions.ts`). None of these appear in the diagram.
- The diagram's task-store box omits the workflow-owned column model, which now decides which columns exist and what each column means (`packages/core/src/column-roles.ts:56` to `:123`).

Data Models:

- `id | int | PK, not null` is wrong on both type and key. The column is `text("id").notNull()` (`packages/core/src/postgres/schema/project.ts:56`) and the primary key is the composite `(projectId, id)` (`packages/core/src/postgres/schema/project.ts:314`).
- `column | enum | not null | planning/todo/in-progress/in-review/done` is wrong. There is no `planning` column, the legacy set is `triage/todo/in-progress/in-review/done/archived` (`packages/core/src/types/board/board.ts:27`), and the column is validated against the task's own workflow rather than a closed enum (`packages/dashboard/src/routes/register-task-workflow-routes.ts:2530` to `:2539`).
- `status | enum | not null` is wrong. The column is a nullable text (`packages/core/src/postgres/schema/project.ts:76`).
- `userPaused | bool` is wrong. The column is `integer("user_paused").default(0)` (`packages/core/src/postgres/schema/project.ts:86`).
- `prompt / spec doc | text` is wrong. The specification is a `PROMPT.md` file in the task directory (`packages/core/src/task-store/task-creation.ts:1446`, `packages/core/src/task-store/task-update.ts:1308`). The database table `task_documents` (`packages/core/src/postgres/schema/project.ts:1274`) holds named documents with a revision counter and a revision history in `task_document_revisions`.
- `file-scope | json` names a column that does not exist. The scope is written as a "## File Scope" section in `PROMPT.md` and validated and sanitized by `packages/core/src/task-store/file-scope.ts:27` and `:41`. The persisted scope artifacts are the `declaredSymbols`, `modifiedFiles`, and `scopeAutoWiden` JSONB columns (`packages/core/src/postgres/schema/project.ts:253`, `:252`, `:248`).
- `branch-context | json` names a column that does not exist. The context is a `fusionBranchContext` key inside `tasks.sourceMetadata` (`packages/core/src/task-store/branch-context.ts:11` to `:15`, `packages/core/src/postgres/schema/project.ts:279`), while the branch assignment itself is the `branch` and `baseBranch` text columns (`packages/core/src/postgres/schema/project.ts:89` and `:90`) plus a branch-group row.
- The Task table omits the persisted fields the feature's own requirements name: `deletedAt` and `allowResurrection` (`packages/core/src/postgres/schema/project.ts:287` and `:288`), `dependencies` (`:217`), `comments` (`:223`), `attachments` (`:221`), `steeringComments` (`:222`), `enabledWorkflowSteps` (`:251`), `priority` (`:74`), `reviewLevel` (`:78`), and `lineageId` (`:71`).

API Contracts:

- The request table says `title` is required and `column` is optional. The route requires `description` and treats `title` as optional (`packages/dashboard/src/routes/register-task-workflow-routes.ts:1718` and `:1890`), and it accepts about 25 more fields including `dependencies`, `enabledWorkflowSteps`, `workflowId`, `agentId`, `autoMerge`, `priority`, `branchSelection`, `githubTracking`, `acknowledgedDuplicates`, and `bypassDuplicateCheck` (`:1681` to `:1717`).
- The response table says 200 OK with a `task` field. The route answers 201 with the bare task object (`packages/dashboard/src/routes/register-task-workflow-routes.ts:2316`) and answers 200 with the bare canonical task when a deterministic duplicate wins (`:2291`).
- The error table lists codes `INVALID_INPUT` and `TASK_NOT_FOUND`. The wire form is `{ error: message, details? }` (`packages/dashboard/src/api-error.ts:129` to `:134`). Intake duplicates answer 409 with `error: "duplicate_candidates"` (`packages/dashboard/src/routes/register-task-workflow-routes.ts:1984`), and delete conflicts answer 409 with `details.code` set to `TASK_HAS_DEPENDENTS` or `TASK_HAS_LINEAGE_CHILDREN` (`:7880` and `:7894`).
- The section documents one endpoint. The same registrar exposes about 90 task routes, including the move, delete, archive, comment, document, artifact, attachment, checkout, and steering surfaces that the feature's own requirements cover.

Sequences:

- "task-store(task-creation) → DB (advisory lock)" is wrong. Task creation takes no per-task advisory lock. `packages/core/src/task-store/task-creation.ts` has no `acquireTaskAdvisoryXactLock` call. The lock is taken by the move path (`packages/core/src/task-store/moves.ts:1164`), the mutation path (`packages/core/src/task-store/task-mutation-ops.ts:449`), the reset path (`packages/core/src/task-store/reset-lifecycle.ts:201`), the archive path (`packages/core/src/task-store/async/async-archive-lineage.ts:259`), and the audit path (`packages/core/src/task-store/audit-ops.ts:144`).

Technical Decisions:

- "Board move | `moves.ts` | Supports per-task and board-level moves with guard rails" is wrong. `moves.ts` supports per-task moves only, as its four exports show (`packages/core/src/task-store/moves.ts:258`, `:284`, `:305`, `:421`).
- The decision table omits the workflow-owned column model, which is the decision behind the move guards, the resolved column order, and the degraded role flags (`packages/core/src/column-roles.ts:56` to `:123`, `packages/core/src/types/board/board-config.ts:194`).
- "Soft-delete tombstone | keep tombstone | Preserves audit trail, prevents resurrect" is too absolute. An operator can authorize resurrection through `allowResurrection` or `forceResurrect` (`packages/core/src/task-store/task-id-integrity.ts:383` and `:420`, `packages/core/src/postgres/schema/project.ts:288`), and the delete route accepts `allowResurrection` as a query parameter (`packages/dashboard/src/routes/register-task-workflow-routes.ts:7834`).

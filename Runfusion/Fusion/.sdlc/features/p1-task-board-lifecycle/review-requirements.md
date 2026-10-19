---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Stale requirements:

- FR-5 claims the system shall "move the board itself (board-level moves)". No board-level or multi-task move exists. `packages/core/src/task-store/moves.ts` exports only per-task operations (`moveTaskImpl` line 258, `moveTaskIfImpl` line 284, `handoffToReviewImpl` line 305, `moveTaskInternalImpl` line 421). The dashboard exposes one single-task route (`POST /tasks/:id/move`, `packages/dashboard/src/routes/register-task-workflow-routes.ts:2526`) and the CLI exposes one single-task command (`runTaskMove`, `packages/cli/src/commands/task.ts:1537`).
- FR-9 claims the system shall "break work into subtasks with their own lifecycle". Subtask splitting was deleted. `packages/core/src/postgres/migrations/0062_remove_task_subtask_splitting.sql` drops `break_into_subtasks`, and the create route rejects the flag with 400 "breakIntoSubtasks is no longer supported; create one detailed task instead" (`packages/dashboard/src/routes/register-task-workflow-routes.ts:1731`).
- FR-9 names "GroupTask" as a grouping feature. The surviving grouping concept is the branch group, implemented in `packages/core/src/task-store/branch-group-ops.ts` and surfaced by `packages/dashboard/app/components/GroupTaskModal.tsx:18`, which renders a branch group and its members rather than a task group.
- FR-3 lists "subtasks" among the data the store persists. The remaining parent-child relation is task lineage (`sourceParentTaskId`, `packages/core/src/postgres/schema/project.ts:278`), not subtasks.

Missing requirements (behavior the code implements that no FR or NFR covers):

- Duplicate-task detection at intake is not covered. The create route runs a deterministic fingerprint guard, a similarity match, a near-duplicate intent guard, and an explicit `DUPLICATE: FN-####` marker check, and answers 409 `duplicate_candidates` (`packages/dashboard/src/routes/register-task-workflow-routes.ts:1984`, `:2004`, `:2122`). The shared implementation is `packages/core/src/duplicates/duplicate-guard.ts`, `packages/core/src/duplicates/near-duplicate.ts`, and `packages/core/src/duplicates/explicit-duplicate-marker.ts`. The preflight surface `POST /tasks/duplicate-check` (`:1630`) and the clone surface `POST /tasks/:id/duplicate` (`:4346`) are also uncovered.
- Checkout leasing is not covered. `POST /tasks/:id/checkout` (`:7704`), `POST /tasks/:id/release` (`:7747`), `POST /tasks/:id/force-release` (`:7780`), and `GET /tasks/:id/checkout` (`:7805`) enforce exclusive execution ownership, backed by `checkedOutBy` and `checkoutLeaseEpoch` (`packages/core/src/postgres/schema/project.ts:281`, `:286`) and `AgentStore.checkoutTask` (`packages/core/src/agents/agent-store.ts:1893`).
- Steering comments are not covered. `POST /tasks/:id/steer` (`:6289`) writes `tasks.steeringComments` (`packages/core/src/postgres/schema/project.ts:222`) through `addSteeringCommentImpl` (`packages/core/src/task-store/task-artifacts-ops.ts:788`) and wakes the assigned agent.
- Task recommendations are not covered. `GET /tasks/recommendations` (`:1603`) and `POST /tasks/:id/recommendations/:recommendationId/create` (`:2367`) create a linked child task from a recommendation and store the link in `tasks.recommendations` (`packages/core/src/postgres/schema/project.ts:162`).
- Cross-task file-scope overlap is not covered. The `task_overlap_waits` table (`packages/core/src/postgres/schema/project.ts:382`), `packages/core/src/task-store/overlap-wait-ops.ts`, `GET /tasks/:id/overlap-blocker` (`:6535`), and `POST /tasks/:id/repair-overlap-blocker` (`:6551`) serialize work that declares overlapping files. NFR-1 only covers concurrency on one task.
- Task attachments are not covered. `POST /tasks/:id/attachments` (`:4690`), `GET /tasks/:id/attachments/:filename` (`:4713`), and `DELETE /tasks/:id/attachments/:filename` (`:4732`) are a file-upload surface distinct from artifacts, stored in `tasks.attachments` (`packages/core/src/postgres/schema/project.ts:221`).
- Spec revision and rebuild are not covered. `POST /tasks/:id/spec/revise` (`:6332`) and `POST /tasks/:id/spec/rebuild` (`:6451`) change the persisted specification after creation.
- Task reset and revert are not covered. `POST /tasks/:id/reset` (`:3942`) and `POST /tasks/:id/revert` (`:2813`) return a card to an earlier lifecycle state.
- Assignment and custom fields are not covered. `PATCH /tasks/:id/assign` (`:7129`), `PATCH /tasks/:id/assign-user` (`:7186`), and `PATCH /tasks/:id/custom-fields` (`:7277`) write `assignedAgentId`, `assigneeUserId`, and `tasks.customFields` (`packages/core/src/postgres/schema/project.ts:259`, `:261`, `:290`).
- The tombstone identifier reservation is not covered. A soft-deleted identifier is never reused, and re-creation is refused with `TombstonedTaskResurrectionError` unless an operator opts in through `allowResurrection` or `forceResurrect` (`packages/core/src/task-store/task-id-integrity.ts:382` and `:420`, `packages/core/src/postgres/schema/project.ts:288`, `packages/core/src/task-store/task-creation.ts:1540`). NFR-2 covers only the sweep path and does not state the reservation rule.
- Multi-lane boards are not covered. `GET /tasks/board-workflows` (`:1537`) and `packages/dashboard/src/routes/board-workflows.ts` expose one lane per workflow, and the board renders a card in the lane of its own workflow (`packages/dashboard/app/components/Board.tsx:535`). FR-2 and FR-8 describe a single board.
- The archive lifecycle and the delete outbox are not covered. `packages/core/src/task-store/archive-lifecycle.ts` and `archive-lifecycle-2.ts` move a task to cold storage, and `packages/core/src/task-store/task-deleted-outbox-consumer.ts` consumes the `task:deleted` outbox rows recorded by `task_lifecycle_events` (`packages/core/src/postgres/schema/project.ts:678`). FR-6 names only archiving, soft-delete, and tombstones.

Acceptance criteria gaps:

- The acceptance criteria list has no entry for FR-5, FR-8, FR-9, NFR-2, or NFR-4, so five stated requirements are unverified.
- Every acceptance criterion checkbox is unchecked while the document frontmatter reads `status: done` (`requirements.md:51` to `:74`).

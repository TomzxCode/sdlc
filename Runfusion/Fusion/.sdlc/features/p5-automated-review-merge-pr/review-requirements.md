---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Stale requirements

- **FR-4** claims a diff-volume gate before the squash commit is formed. The gate was deleted on 2026-08-16 by operator decision. `packages/engine/src/merge/merger-ai-squash-gates.ts:21-27` records the removal of `checkDiffVolume`, `DiffVolumeRegressionError`, and the `merge:diff-volume-blocked` audit event, and `docs/architecture.md:2440` states that file scope is now the only pre-land guard with the post-squash audit as the shrinkage backstop.
- **FR-4** claims an overlap-guard gate before the squash commit is formed. The live merge path never calls it. `packages/engine/src/merge/merger-ai.ts:9-13` states that `runAiMerge` is the sole production merge path, `packages/engine/src/merge/merger-ai.ts` has no call to `detectMergeOverlap`, and the only call site is `packages/engine/src/merger.ts:8664` inside the soft-deprecated `aiMergeTask` path.
- **FR-4** and the FR-4 acceptance criterion state that an out-of-scope squash is rejected with `FileScopeViolationError`. The outcome depends on the resolved file-scope mode. `packages/engine/src/merge/merger-file-scope.ts:258-280` skips the check in `off` mode, and `packages/engine/src/merge/merger-file-scope.ts:290-341` only rethrows in `strict` mode while `warn` and `custom` log and continue.
- **NFR-1** states that every squash commit must overlap the task file scope and that violations fail with `FileScopeViolationError`. The same mode dependency applies, and the default resolution is a warning. `packages/engine/src/merge/merge-trait.ts:88-100` returns `fileScope: "warn"` from the settings fallback, and `packages/core/src/workflows/builtin-coding-workflow-ir.ts:67` gives the built-in default workflow a merge trait with no config, so the fallback applies.
- **FR-3** names auto-prerebase as a divergence reconciliation mechanism. It is inert in the live path. `packages/engine/src/merge/merger-ai.ts:5-7` states that `runAiMerge` does not share the legacy prerebase pipeline, `packages/core/src/types/settings/settings-scope.ts:1701-1718` marks `prerebaseAutoEnabled`, `prerebaseHotFiles`, and `prerebaseDivergenceThreshold` deprecated and inert, and the only `runAutoPrerebase` call site is `packages/engine/src/merger.ts:8200` inside the deprecated `aiMergeTask` path.
- **FR-3** names smart pull as a divergence reconciliation mechanism. `packages/engine/src/merge/smart-pull.ts:101` is exported from `packages/engine/src/index.ts:524` and has no production caller. The dashboard pull path is `POST /api/git/pull` at `packages/dashboard/src/routes/register-git-github.ts:3592`, which calls `pullGitBranch` and not `smartPull`.
- **FR-5** claims the system drives GitHub and GitLab PRs. The PR automation is GitHub only. `packages/engine/src/merge/pr-monitor.ts:4-6,45-51` uses the `gh` CLI, and `packages/engine/src/merge/pr-nodes.ts`, `packages/engine/src/merge/pr-response-run.ts`, and `packages/engine/src/merge/pr-reconcile.ts` have no GitLab branch. The GitLab surface is import only, `packages/dashboard/src/routes/register-gitlab.ts:209,244` fetch and import merge requests, and `docs/gitlab-parity-inventory.md:113,119` defers merge request lifecycle actions and forbids auto-merging merge requests.

### Missing requirements

- No FR covers the merge policy resolved from the workflow merge trait. `packages/engine/src/merge/merge-trait.ts:118-168` resolves the commit strategy, a `pr-only` route, and the file-scope mode from the task's workflow column, and `packages/engine/src/merge/merge-trait.ts:39` adds the `pr-only` strategy value.
- No FR covers the auto-merge off hold. `packages/core/src/merge/task-merge.ts:166-171` stops automatic merge processing when `settings.autoMerge` is false unless the task opts in, and `packages/engine/src/merge/merger-ai.ts:1703` refuses the direct merge under that hold.
- No FR covers shared branch group integration and group to default promotion as two separately gated merge steps. `packages/engine/src/merge/group-merge-coordinator.ts` and `packages/core/src/merge/task-merge.ts:188-218` implement both.
- No FR covers the workspace per-repository land. `packages/engine/src/merge/merger-ai.ts:1041` lands one repository at a time with a repository-scoped file scope, and `packages/engine/src/merge/workspace-land-predicate.ts` proves the landing.
- No FR covers the reviewer that runs inside the merge. `packages/engine/src/merge/merger-ai.ts:23-27` describes a fresh reviewer that audits the squash and drives corrective rounds, and `packages/core/src/types/merge/merge-policy.ts:179-182` defines `merger.maxReviewPasses`.
- No FR covers durable merge proof as a precondition for reaching done. `packages/engine/src/merge/auto-merge-finalization.ts:212` refuses to promote a loose merged result into merge proof, and `packages/core/src/workflow-merge-proof.ts:38` evaluates the proof.
- No FR covers the pre-merge approval gates or the audited operator bypass. `packages/core/src/merge/pre-merge-approval.ts`, `packages/core/src/merge/required-pre-merge-steps.ts`, and `packages/engine/src/merge/pre-merge-gate-reseed.ts` implement them.
- No FR covers the durable merge queue and merge request leasing. `packages/core/src/postgres/schema/project.ts:1079-1108` defines the tables and `packages/core/src/task-store/merge-coordination.ts:10` keeps the enqueue transactional.
- No FR covers the PR lifecycle as a first-class workflow with bounded rework cycles and an auto-merge gate. `packages/core/src/workflows/builtin-pr-workflow-ir.ts:80-172` defines the nodes and edges.
- No FR covers the recovery of a divergent push through a remote safety branch and a non-fatal aborted push. `packages/engine/src/merge/recover-confirmed-merge-push.ts` and `packages/engine/src/merge/push-after-merge-policy.ts` implement it.

---
title: "Multi-Repository Workspaces"
status: done
---

# Test Plan: Multi-Repository Workspaces

## Scope

Covers member detection, the member list file, the workspace mode toggle, member addition, per-member worktree acquisition and base resolution, the per-member review and its aggregate verdict, the per-member land loop, landed proof, the partial-land recovery sweep, the per-member revert, the main-checkout completion guard, the zero-acquire classification, and the HTTP surface for detection, the member list, and the workspace file browser.

Out of scope: the general task file routes, the file operation routes beyond list, read, and write, the dependency bootstrap, and the worktrunk worktree backend.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Detect the member repositories of a project root | A root with two Git children and one plain child | The two Git children are returned in sorted order and the plain child is not returned |
| TC-2 | Add a member repository | An eligible direct child, then the same child again | The first call reports `added` and the second reports `already-member` with the member list unchanged |
| TC-3 | Refuse an invalid member path | `../escape`, `.`, `a/..`, `group/a`, and a plain directory | The calls are refused with the reasons `invalid-path`, `not-direct-child`, `not-direct-child`, `not-direct-child`, and `not-a-git-work-tree` |
| TC-4 | Toggle workspace mode on and off | A root with detected members | The mode setting and the member list file are created and removed, and unrelated config survives |
| TC-5 | Preserve a curated member list and refuse an empty root | An existing non-empty member list, and a root with no sub-repositories | The curated list survives, and a root with no members reports the `no-sub-repositories` failure |
| TC-6 | Reconcile a failed toggle write | A failing mirror or file write | The observed member list is re-read and the mode setting is reconciled to it |
| TC-7 | Serialize concurrent toggles on one root | Two toggles on the same root | The critical sections run one after the other and the lock is released after a throwing body |
| TC-8 | Derive the owning member for a path | Repo-prefixed and unscoped paths against a member list | The longest matching member prefix wins and an unmatched path is unscoped |
| TC-9 | Resolve a member scope subset | A declared scope naming one member, resolved for a sibling | The sibling receives an empty scope and no fallback authority |
| TC-10 | Resolve a member base branch | A requestable base, a vanished recorded base, a sibling task branch, and an unresolvable base | The requestable base is used, and the other cases fall back to the member's own integration branch with the matching fallback reason |
| TC-11 | Refresh a member base | A live member checkout on a stale base | The checkout is moved onto the recorded base and the durable base commit is persisted |
| TC-12 | Skip a refresh that is dirty, conflicting, or unresolvable | A member checkout that cannot be fast-forwarded | The local checkout is kept, the result is marked skipped, and execution is not blocked |
| TC-13 | Classify a zero-acquire workspace task | An empty member map with and without a commit-free eligibility source | The classification is `unproven` without a source and `commit-free-eligible` with one |
| TC-14 | Resolve the merge readiness | A confirmed scope, a duplicate declaration, a duplicate worktree path, and a commit-free task | The ready, blocked, and no-op outcomes are returned for the matching inputs |
| TC-15 | Select the member integration target | A repository with no remote, one remote, `origin`, a configured remote, and an ambiguous remote | The local, remote, and failure outcomes are returned for the matching inputs |
| TC-16 | Qualify a member review finding | A finding id and file path without a member prefix | The id is prefixed with `member:` and the file path with `member/` |
| TC-17 | Aggregate the member review verdicts | Approved, revised, rethinking, and unavailable member verdicts | The aggregate takes the strongest severity and an approval with notes still approves |
| TC-18 | Capture a member review evidence set | A member with a recorded base commit and a task branch | The changed files come from the base-to-branch range, the file list is member-qualified, and a fingerprint is produced |
| TC-19 | Detect main-checkout work | A member main checkout with a task-attributed commit and with uncommitted changes | The attributed commit is a violation and the uncommitted change is a warning |
| TC-20 | Prove a landed member from the task trailer | An integration ref carrying a commit with the task identifier trailer and no recorded proof | The member is reported as landed and the exact commit is returned |
| TC-21 | Refuse a landed proof at or behind a revert boundary | A recorded proof behind the revert boundary | The member is not reported as landed |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-22 | Acquire every configured member | A workspace with two members and a task | One worktree per member, each with its own path, branch, and base commit |
| TC-23 | Hold a second writer off one member | A live acquire lease on one member | The second claim reports a conflict naming the holder and the caller holds |
| TC-24 | Release an acquire lease | An acquired member | The lease is released and the member can be acquired again |
| TC-25 | Keep the acquire lease authority | A lease claimed by another node or incarnation | The second claim contends instead of re-entering |
| TC-26 | Coordinate durable leases across processes | A PostgreSQL project schema | Acquire, renew, release, reclaim, and fence-ref writes all behave as one authority |
| TC-27 | Resolve a land intent | A pending intent with a live lease and one with a stale fence | The live holder resolves the intent and a stale fence is refused |
| TC-28 | Land the members of a workspace task | Two modified members | Each member advances its own integration ref and the result reports every member |
| TC-29 | Skip a member that already landed | A member with a recorded landing proof | The member is skipped and its ref is not advanced again |
| TC-30 | Land with publication disabled | The push-after-merge setting off | No fence ref is created and no remote write is attempted |
| TC-31 | Apply the member scope gates on a land | A squash that touches a file outside the member scope | The integration ref of that member does not advance |
| TC-32 | Reject a publication whose target moved | A remote target ref that moved after the fence pin was published | The atomic push is rejected and the target is not overwritten |
| TC-33 | Recover a partial land | A task in review with one landed member and one failed member | The sweep re-enqueues the task so only the unlanded member is retried |
| TC-34 | Revert the members of a workspace task | A landed member set with no conflict | Every member is reverted and committed |
| TC-35 | Roll back a conflicting workspace revert | One member whose revert conflicts | Every touched member is restored to its pre-call state and no member revert is committed |
| TC-36 | Revert through one pull request per member | A project with auto-merge off | The direct integration-branch path is refused and one pull request per member is prepared |
| TC-37 | Guard task completion on the main checkouts | A member main checkout holding a task-attributed commit | Completion is refused with the main-checkout edit reason |
| TC-38 | Prove the delivery of a workspace task | A task with a member worktree holding no commit | The acquired-worktree no-commit invariant refuses the completion |
| TC-39 | Keep the workspace root out of the routing | A task with member worktrees and stale singular routing metadata | The singular fields are cleared and every member entry survives |
| TC-40 | Resolve the workspace member list over HTTP | A registered workspace and a project that is not a workspace | The members are listed and the non-workspace project is refused with a conflict |
| TC-41 | Add a workspace member over HTTP | A valid member and an invalid member | The member is added and the invalid member is mapped to a route error |
| TC-42 | Detect the members over HTTP | An absolute path that exists and one that does not | The members and the workspace flag are returned and a missing path is refused |
| TC-43 | Browse the workspace files over HTTP | A workspace identifier of the project root and a task worktree | The listing, the read, and the write all return their payloads |
| TC-44 | Keep the member worktrees on reset | A workspace task with recorded member worktrees | Every member worktree is removed and the task returns to planning |
| TC-45 | Remove the member worktrees on archive | A workspace task with recorded member worktrees | Every member worktree is removed under a per-repository reservation |
| TC-46 | Clean up after a successful land | A merged workspace task | The member worktrees and the workspace task directory are removed |
| TC-47 | Preserve a member that holds uncommitted content | A merged workspace task with an uncommitted member | That member is preserved with its reason written to the task log |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-48 | Run a workspace task end to end | Register a workspace, create a task, execute, review, and merge | Each member is acquired, reviewed, and landed, and the task reaches done |
| TC-49 | Run the workspace pipeline smoke | A workspace project through the pipeline tier | The board, the task, and the merge report the member outcomes |
| TC-50 | Resolve a grouped workspace root in the extension | A member checkout in a grouped worktree root | The extension resolves the workspace root, not the member or the group container |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-51 | A member path leaves the workspace root | The path is rejected and never reaches a path join |
| TC-52 | A member list holds a non-string entry | The whole list is refused and the project falls back to single-repository mode |
| TC-53 | A requested base branch resolves in one member only | The other member falls back to its own integration branch and the fallback is logged |
| TC-54 | A task identifier is recycled | The trailer scan refuses to treat the older commit as this task's landing |
| TC-55 | A member is modified outside the confirmed scope | The review returns unavailable and names the out-of-scope member |
| TC-56 | A clean scoped member | The member is recorded as not reviewed and creates no landing obligation |
| TC-57 | A reviewer provider failure during a member review | The episode ends as unavailable and no partial findings are published |
| TC-58 | An approved member diff changes before the merge | The member is reported as content changed and the task is routed back to review |
| TC-59 | A lease renewal is refused during a land | The land aborts before its next durable write |
| TC-60 | An expired lease is left by a dead node | The lease is reclaimed after expiry and the reclaimed key is reported |
| TC-61 | A workspace task acquired no member | The task is classified as unproven and the review is unavailable and not retryable |
| TC-62 | A member repository cannot be prepared at registration | No project row is registered or activated |

## Test Infrastructure

- Vitest across `packages/core`, `packages/engine`, `packages/dashboard`, and `packages/cli`.
- PostgreSQL-backed tests under `packages/core/src/__tests__/postgres/` use the embedded PostgreSQL instance for the lease, land-intent, concurrent-merge, and review-evidence publication suites.
- The `*.real-git.test.ts` files build throwaway Git repositories to exercise the land, the revert, the landed predicate, and the finalize cleanup against Git itself.
- The `*.slow.test.ts` files cover the long-running merge paths and stay outside the merge gate.
- Temporary directories are created under the OS temp directory and removed after each test.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-52 |
| FR-3 | TC-4, TC-5, TC-6, TC-7 |
| FR-4 | TC-2, TC-3, TC-41 |
| FR-5 | TC-22, TC-24 |
| FR-6 | TC-10, TC-53 |
| FR-7 | TC-11, TC-12 |
| FR-8 | TC-14, TC-56 |
| FR-9 | TC-17, TC-55, TC-57 |
| FR-10 | TC-18 |
| FR-11 | TC-28, TC-30, TC-32 |
| FR-12 | TC-20, TC-21, TC-29 |
| FR-13 | TC-33 |
| FR-14 | TC-34, TC-35, TC-36 |
| FR-15 | TC-19, TC-37 |
| FR-16 | TC-13, TC-61 |
| FR-17 | TC-40, TC-41, TC-42 |
| FR-18 | TC-43 |
| FR-19 | TC-62 |
| FR-20 | TC-48 |
| FR-21 | TC-8, TC-9 |
| FR-22 | TC-30 |
| FR-23 | TC-36 |
| FR-24 | TC-45, TC-46, TC-47 |
| NFR-1 | TC-23, TC-25, TC-26, TC-59, TC-60 |
| NFR-2 | TC-39 |
| NFR-3 | TC-3, TC-51 |
| NFR-4 | TC-9, TC-14, TC-56 |
| NFR-5 | TC-20, TC-54 |
| NFR-6 | TC-59 |
| NFR-7 | TC-32 |
| NFR-8 | TC-29, TC-33 |
| NFR-9 | TC-60 |
| NFR-10 | TC-17 |
| NFR-11 | TC-18, TC-58 |
| NFR-12 | TC-10, TC-28 |
| NFR-13 | TC-7 |
| NFR-14 | TC-22, TC-45 |

## Key Test Files

- Detection, member list, and mode toggle: `packages/core/src/__tests__/workspace-add-repo.test.ts`, `packages/core/src/__tests__/workspace-mode-toggle.test.ts`, `packages/core/src/__tests__/settings-workspace-toggle-side-effect.test.ts`
- Durable coordination: `packages/core/src/__tests__/postgres/workspace-coordination-leases.pg.test.ts`, `packages/core/src/__tests__/postgres/workspace-leases.pg.test.ts`, `packages/core/src/__tests__/postgres/workspace-review-evidence-publish.pg.test.ts`, `packages/core/src/__tests__/postgres/workspace-worktrees-concurrent-merge.pg.test.ts`
- Acquisition and base resolution: `packages/engine/src/__tests__/worktree-acquisition-workspace.test.ts`, `packages/engine/src/__tests__/workspace-acquire-claim-release.test.ts`, `packages/engine/src/__tests__/workspace-acquire-contention-hold.test.ts`, `packages/engine/src/__tests__/workspace-acquire-lease-authority.test.ts`, `packages/engine/src/__tests__/workspace-base-branch.test.ts`, `packages/engine/src/__tests__/workspace-base-refresh.test.ts`
- Review: `packages/engine/src/__tests__/reviewer-workspace.test.ts`, `packages/engine/src/__tests__/workspace-review-evidence.test.ts`, `packages/engine/src/__tests__/workspace-review-complete-coverage.test.ts`, `packages/engine/src/__tests__/workspace-review-diff-base.test.ts`, `packages/engine/src/__tests__/workspace-review-findings.test.ts`, `packages/engine/src/__tests__/workspace-review-evidence-publish-fail-closed.test.ts`, `packages/engine/src/__tests__/workspace-review-remediation.test.ts`, `packages/engine/src/__tests__/workspace-review-remediation-routing.test.ts`
- Land: `packages/engine/src/__tests__/workspace-merger.test.ts`, `packages/engine/src/__tests__/workspace-merger-lease.test.ts`, `packages/engine/src/__tests__/workspace-merger-idempotency.slow.test.ts`, `packages/engine/src/__tests__/workspace-merger-scope-gates.test.ts`, `packages/engine/src/__tests__/workspace-push-after-merge.test.ts`, `packages/engine/src/__tests__/workspace-integration-target.test.ts`, `packages/engine/src/__tests__/workspace-land-predicate.revert-boundary.test.ts`, `packages/engine/src/__tests__/workspace-land-predicate-recycled-id.real-git.test.ts`
- Recovery and completion: `packages/engine/src/__tests__/self-healing-workspace.test.ts`, `packages/engine/src/__tests__/workspace-finalize-cleanup.real-git.test.ts`, `packages/engine/src/__tests__/workspace-post-landing-worktree-cleanup.test.ts`, `packages/engine/src/__tests__/executor-workspace-main-checkout-guard.test.ts`, `packages/engine/src/__tests__/executor-workspace-taskdone.test.ts`, `packages/engine/src/__tests__/workspace-zero-acquire.test.ts`
- Revert: `packages/engine/src/__tests__/task-revert.workspace.real-git.test.ts`, `packages/engine/src/__tests__/task-revert-workspace-pr.real-git.test.ts`
- HTTP surface: `packages/dashboard/src/__tests__/workspace-add-repo-route.test.ts`, `packages/dashboard/src/__tests__/settings-workspace-mode-route.test.ts`, `packages/dashboard/app/api/__tests__/workspace-files-api.test.ts`, `packages/dashboard/src/routes/__tests__/register-file-workspace-routes.test.ts`
- Documentation and lifecycle: `packages/dashboard/src/__tests__/workspace-documentation.test.ts`, `packages/dashboard/src/__tests__/task-reset-workspace-lifecycle.test.ts`, `packages/core/src/__tests__/archive-removes-workspace-worktrees.test.ts`, `packages/engine/src/__tests__/workspace-e2e.test.ts`, `packages/engine/src/__tests__/pipeline-smoke/pipeline-workspace.pipeline.test.ts`

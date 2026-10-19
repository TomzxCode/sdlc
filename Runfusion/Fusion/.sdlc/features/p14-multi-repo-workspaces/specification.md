---
title: "Multi-Repository Workspaces"
status: done
---

# Specification: Multi-Repository Workspaces

## Overview

A workspace project keeps its root browse-only and non-Git, and treats the root's direct child Git repositories as its members.
`@fusion/core` owns detection, the member list in `.fusion/workspace.json`, the mode toggle, and the durable coordination leases and land intents in PostgreSQL.
`@fusion/engine` owns the per-member worktree acquisition, the per-member base resolution and refresh, the per-member review, the per-member land loop, the partial-land recovery sweep, and the per-member revert.
The dashboard exposes detection, the member list, and the workspace file browser over HTTP.

## Architecture

```
                     ┌──────────────────────────────────────────────────────────────────────────┐
                     │ Surfaces                                                                 │
                     │ Setup Wizard / Settings    CLI (fn project, fn task)                     │
                     │ Dashboard file browser (workspace = project | task)                      │
                     └──────────────────────────────────────────────────────────────────────────┘
                                                           │  REST
         ┌──────────────────────────────────────────────────────────────────────────┐
         │ @fusion/dashboard routes                                                 │
         │ POST /projects/detect-workspace     GET|POST /git/workspace-repos        │
         │ GET  /workspaces                    GET|POST /files...                   │
         └──────────────────────────────────────────────────────────────────────────┘
                                               │
         ┌──────────────────────────────────────────────────────────────────────────┐
         │ @fusion/core                                                             │
         │ git/git-repository.ts                                                    │
         │   detectWorkspaceRepos   loadWorkspaceConfig   saveWorkspaceConfig       │
         │   addWorkspaceRepo       applyWorkspaceModeToggle                        │
         │   withWorkspaceModeLock                                                  │
         │ task-store/workspace-leases.ts   tasks/workspace-lease-types.ts          │
         │   acquire / renew / release / reclaim / fence-ref / land-intent          │
         │ postgres/schema/project.ts                                               │
         │   workspace_coordination_leases   workspace_land_intents                 │
         └──────────────────────────────────────────────────────────────────────────┘
                                               │
         ┌──────────────────────────────────────────────────────────────────────────┐
         │ @fusion/engine                                                           │
         │ worktree/   workspace-paths   workspace-base-branch                      │
         │             workspace-base-refresh   workspace-review-evidence           │
         │             worktree-acquisition (acquireWorkspaceRepoWorktree)          │
         │ executor/   workspace-review-per-repo   workspace-config-resolver        │
         │             workspace-main-checkout-guard   workspace-zero-acquire       │
         │ merge/      merger-ai.landWorkspaceTask   workspace-land-predicate       │
         │             workspace-fence-ref   workspace-merge-readiness              │
         │             workspace-merge-dispatch-lease   workspace-integration-target│
         │             workspace-land-failure                                       │
         │ execution/  task-revert (revertWorkspaceTask, prepareWorkspaceRevertPr)  │
         │ self-healing.ts  reconcileWorkspacePartialLands                          │
         └──────────────────────────────────────────────────────────────────────────┘
                                               │
         ┌──────────────────────────────────────────────────────────────────────────┐
         │ Git and PostgreSQL                                                       │
         │ ROOT/MEMBER main checkout      ROOT/.fusion/worktrees/TASKID/            │
         │ member integration ref         member remote (optional)                  │
         │ PostgreSQL project schema: leases, land intents, tasks                   │
         └──────────────────────────────────────────────────────────────────────────┘
```

## Data Models

### Workspace config file

Stored at `<workspace-root>/.fusion/workspace.json`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| repos | string[] | Required, every entry a string, every entry a normalized relative path inside the workspace root | Member repository paths relative to the workspace root, sorted |

### Workspace worktree entry

Stored per task in `tasks.workspace_worktrees`, keyed by the member path relative to the workspace root.

| Field | Type | Constraints | Description |
|---|---|---|---|
| worktreePath | string | Not null | Absolute path of the member's linked checkout |
| branch | string | Not null | The task branch checked out in that member |
| baseBranch | string | Optional | The ref the member worktree was derived from and must later target |
| baseBranchFallbackFrom | string | Optional | The operator-requested ref that could not be used in that member |
| baseCommitSha | string | Optional | The per-member fork point captured at acquisition |
| landedSha | string | Optional | The commit that landed this member on its integration ref |
| revertBoundarySha | string | Optional | The integration commit created by a completed git-mode revert |
| landFailure | object | Optional | Display-only failure breadcrumb for the member, never part of a landed predicate |

### Task repository scope

Stored per task in `tasks.repository_scope`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| repositories | string[] | Not null, no empty entry, no duplicate | The confirmed member repositories |
| state | string | Optional, only `confirmed` | The confirmation state of the scope |
| revision | number | Optional | Monotonic configuration generation that fences a stale review callback |
| confirmedAt | string | Optional | When the scope was confirmed |
| confirmedBy | string | Optional, only `workspace` | The confirmer, always the configured workspace |
| reviewEvidence | map | Optional | Per-repository approved diff fingerprint and approval time |
| reviewRemediation | object | Optional | The reviewed repository, the normalized input signature, and the scope generation of a remediation episode |
| extensions | array | Optional | Historical manual-scope acceptance and refusal records |

### Workspace coordination lease

Table `workspace_coordination_leases` in the project schema.

| Field | Type | Constraints | Description |
|---|---|---|---|
| projectId | string | Primary key part, not null | The owning project |
| leaseKey | string | Primary key part, not null | The contended resource key, `repo:MEMBER` or `merge-dispatch:TASKID` |
| kind | string | Not null, one of `acquire`, `land`, `merge-dispatch` | The tenancy type |
| ownerTaskId | string | Not null | The owning task |
| ownerNodeId | string | Not null | The owning node |
| ownerIncarnationId | string | Not null | The owning process incarnation, so a restarted process is not the same owner |
| ownerRunId | string | Optional | The owning run |
| fenceToken | bigint | Not null, increasing | The fencing authority, not a time-to-live |
| fenceRefName | string | Optional | The published fence ref name |
| fenceRefSha | string | Optional | The published fence ref commit |
| status | string | Not null, one of `held`, `released`, `expired` | The lease state |
| acquiredAt | string | Not null | When the lease was claimed |
| renewedAt | string | Not null | When the lease was last renewed, observability only |
| expiresAt | string | Not null | The only liveness clock for the lease |
| createdAt | string | Not null | Row creation time |
| updatedAt | string | Not null | Row update time |

### Workspace land intent

Table `workspace_land_intents` in the project schema.

| Field | Type | Constraints | Description |
|---|---|---|---|
| projectId | string | Primary key part, not null | The owning project |
| taskId | string | Primary key part, not null | The landing task |
| repoRelPath | string | Primary key part, not null | The member path relative to the workspace root |
| remoteUrl | string | Not null | The member remote that receives the publication |
| integrationRef | string | Not null | The member integration ref that is advanced |
| intendedSha | string | Not null | The commit the land intends to publish |
| expectedTip | string | Not null | The integration tip the land expects to replace |
| fenceRefName | string | Not null | The fence ref that guards the publication |
| fenceRefSha | string | Not null | The fence ref commit that guards the publication |
| ownerTaskId | string | Not null | The lease owner triple member for the task |
| ownerNodeId | string | Not null | The lease owner triple member for the node |
| ownerIncarnationId | string | Not null | The lease owner triple member for the incarnation |
| fenceToken | bigint | Not null | The fence token of the tenancy that wrote the intent |
| status | string | Not null, one of `pending`, `recorded`, `abandoned` | The intent state |
| resolvedSha | string | Optional | The commit proven to carry the work |
| resolution | string | Optional, one of `landed`, `not-landed` | How the intent resolved |
| createdAt | string | Not null | Row creation time |
| updatedAt | string | Not null | Row update time |
| resolvedAt | string | Optional | When the intent resolved |

### Workspace member land result

Returned in memory by `landWorkspaceTask`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| repo | string | Not null | The member path relative to the workspace root |
| repoRootDir | string | Not null | Absolute path of the member's main checkout |
| integrationBranch | string | Not null | The member's own integration branch |
| branch | string | Not null | The task branch that was landed |
| status | string | Not null, one of `landed`, `empty`, `failed` | The outcome for that member |
| landedSha | string | Optional | The squash commit when the status is `landed` |
| localSync | object | Optional | How the member checkout was reconciled |
| dependencySyncDecision | string | Optional | The clean-room dependency decision for that member |
| error | string | Optional | The failure message when the status is `failed` |
| alreadyLanded | boolean | Optional | True when the landed predicate skipped the member on a retry |

### Workspace member revert result

Returned in memory by `revertWorkspaceTask`.

| Field | Type | Constraints | Description |
|---|---|---|---|
| repo | string | Not null | The member path relative to the workspace root |
| classification | string | Not null | The per-member classification, `clean`, `reverted`, or `conflict` |
| branch | string | Optional | The member branch the revert targeted |
| revertedCommits | array | Optional | The commits the member revert addressed |

## API Contracts

The normative contract is in [`api.yaml`](api.yaml) (OpenAPI 3.1).
The table below is a summary; request and response schemas and error bodies are in `api.yaml`.

| Method | Path | Purpose |
|---|---|---|
| POST | /api/projects/detect-workspace | Detect the member repositories of a directory |
| GET | /api/git/workspace-repos | List the registered members of a workspace, and the detected candidates when asked |
| POST | /api/git/workspace-repos | Add a member repository to a workspace |
| GET | /api/workspaces | List the browsable workspaces of a project, which are the project root and the task worktrees |
| GET | /api/files | List the files and directories at a path inside a workspace |
| GET | /api/files/{filepath} | Read one file inside a workspace |
| POST | /api/files/{filepath} | Write one file inside a workspace |

Error codes shared across endpoints:

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | The request body or query is missing a required field or holds a value the route rejects |
| 400 | INVALID_WORKSPACE_REPO | The member path is not an in-root direct child Git work tree, or the name is excluded |
| 404 | NOT_FOUND | The requested file, path, or task does not exist |
| 409 | NOT_A_WORKSPACE | The project has no member list, so the route has nothing to report |
| 413 | FILE_TOO_LARGE | The file exceeds the size the file service accepts |
| 415 | UNSUPPORTED_MEDIA_TYPE | The file is binary and cannot be returned as text |
| 500 | INTERNAL_ERROR | An unexpected failure, reported with the operator-facing summary |

## Key Sequences

### Detect members and register a workspace

```
POST /api/projects/detect-workspace { path }
        │
        ▼
  path is absolute?  ──no──► 400 INVALID_INPUT
        │ yes
        ▼
  path exists?      ──no──► 400 INVALID_INPUT
        │ yes
        ▼
  detectWorkspaceRepos(root)
        │  for each direct child, skip excluded names
        │  require a .git marker, then a git rev-parse work-tree probe
        ▼
  { repos: [...sorted], isWorkspace: repos.length > 0 }
        │
        ▼  operator confirms workspace mode
  prepare every member (verifiable HEAD, managed .gitignore)
        │  failure ──► no project row is registered or activated
        ▼
  write .fusion/config.json settings.workspaceMode = true
        ▼
  write .fusion/workspace.json { repos }
```

### Land the members of a workspace task

```
merge dispatch
        │
        ▼
  claim merge-dispatch:TASKID lease ──conflict──► busy, retry later
        │
        ▼
  for each member, in sorted member order
        │
        ├─ claim repo:MEMBER lease (kind land) ──conflict──► busy, retry later
        ├─ resolve the member's integration target (local when publication is off)
        ├─ resolve the member's integration branch and expected tip
        ├─ publish the fence ref refs/fusion/workspace-lease/SLUG
        ├─ write the land intent (pending)
        ├─ squash the member branch onto the member integration ref
        ├─ push with --atomic and --force-with-lease on the target and every fence ref
        ├─ persist landedSha under a valid lease, then resolve the intent (recorded)
        └─ release the member lease
        │
        ▼
  every member landed or empty ──no──► partial land, task stays in review
        │ yes
        ▼
  finalize the task to done, then remove the member worktrees
```

### Revert the members of a workspace task

```
revert request
        │
        ▼
  resolve the per-member attributable commits
        │  squash proof first, then the member branch range
        ▼
  classify every member
        │  clean / already reverted / conflict
        ▼
  any conflict?  ──yes──► roll every touched member back, commit nothing
        │ no
        ▼
  apply the revert to every member, then commit every member
        │
        ▼
  record the member revert boundary commit
        │
        ▼
  auto-merge off ──yes──► prepare one pull request per member instead
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Member authority | `.fusion/workspace.json` is the single membership authority, the `workspaceMode` setting is a separate mirror | The executor reads the file, so the file decides execution while the setting drives the dashboard toggle and registration suppression |
| Detection depth | One level of direct children only | A workspace root is a plain directory whose immediate children are the intended members, and a deeper scan would pick up dependency artifacts |
| Member path rules | Normalized relative in-root direct child, excluded names refused | A member path is joined onto the workspace root, so an absolute path or a `..` escape would resolve outside the root |
| Mode toggle order | Write the setting mirror first on enable, remove the file first on disable | A half-written change must not leave the file enabling execution, and a partial delete must not be auto-detected back to enabled |
| Mode toggle serialization | One in-process lock per project root | The toggle reads, decides, and writes several files, and a concurrent toggle would otherwise lose a member |
| Worktree ownership | One worktree per configured member under one task directory | Agents never choose or extend checkouts, so a task sees one stable set of members for its whole lifetime |
| Root routing | The workspace root is never a checkout, a reviewer working directory, or a landing target | The root is not a Git repository, so any such use would break the member's own base and diff |
| Base pinning | The resolved member base is recorded at acquisition and wins over the task field afterwards | A later edit of the task's base branch must not retarget a checkout that already exists |
| Base fallback | The member's own integration branch when the requested ref does not resolve there | Members are independent repositories, so one member's ref cannot be assumed to exist in another |
| Scope authority | A confirmed repository scope, not the acquired checkouts, decides review and landing | Acquisition grants a checkout, and a checkout alone must not create a review or landing obligation |
| Review coverage | One reviewer per modified in-scope member, then one aggregate verdict | The reviewer runs with the member's working directory, so per-member evidence is what it can see |
| Aggregate severity | Rethink outranks revise, which outranks unavailable, which outranks the approval family | The aggregate must not depend on the order in which members are reviewed |
| Review and landing evidence | The same repository-qualified file list and the same per-member diff fingerprint | Landing must consume exactly what review approved |
| Land atomicity | Non-atomic per member, land as you go | A shared workspace integration branch would be wrong because members are independent repositories |
| Landed proof | The recorded landing commit, proven by an ancestor check | A recorded commit that is no longer reachable means the ref was rebuilt, so the member must land again |
| Lost proof fallback | The task identifier trailer on the integration history | A squash commit's parent is the integration tip, so branch ancestry cannot prove the landing, but the trailer can |
| Fence refs | A private ref per tenancy, published once per tenancy, reused on re-entry | Rotating the pin on re-entry would orphan a pending land intent that names the old pin |
| Publication | One atomic push that compares and swaps the target ref and every fence ref | A superseded owner must be rejected even when the target tip has not moved |
| Revert coverage | Classify all members, then commit all members | A half-reverted workspace is an inconsistent state, so a conflict rolls everything back |
| Recovery | A partial land re-enqueues the task and retries only the unlanded members | A partial land is recoverable state, not one atomic merge, so it must never be reported as a merge |
| Member worktree updates | One advisory-locked per-key store merge per member | A wholesale map replacement would lose a concurrent sibling acquisition, landing, or teardown entry |

## Risks and Unknowns

1. The land loop is non-atomic, so a failure after an earlier member landed leaves the workspace in a mixed state until the recovery sweep runs.
2. A member's base branch can resolve in one member and not another, which produces a mixed workspace that needs operator inspection.
3. The acquisition lease covers only the checkout creation, so two tasks can work in the same member at the same time after acquisition completes.
4. A member that is added while a task is running is not acquired by that task, so the new work needs a follow-up task.
5. The `workspaceMode` setting and `.fusion/workspace.json` are separate artifacts, so a toggle alone can leave the two out of step.
6. The code does not record whether a workspace task may be created against a member list that changes during review.

## Out of Scope

- A shared workspace integration branch, which would require the members to share one Git history.
- Root-level Git operations in a workspace, because the workspace root is not a Git repository.
- Nested member discovery, because detection stops at the direct children.
- Workspace Plan Review scripts, because the script runner cannot yet receive the multi-root boundary.
- The general file browser, the task file routes, and the file operation routes beyond the workspace file list, read, and write calls.

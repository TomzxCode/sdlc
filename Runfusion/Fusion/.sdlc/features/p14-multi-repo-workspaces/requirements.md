---
title: "Multi-Repository Workspaces"
status: done
---

# Requirements: Multi-Repository Workspaces

## Overview

A workspace is a Fusion project whose root directory is not a Git repository and whose direct child directories are Git repositories.
Fusion detects those member repositories, records them in `.fusion/workspace.json`, and gives every task one worktree per member.
Review runs once per modified member, each member lands on its own local integration ref under a durable write fence, and a partial land is recovered instead of lost.
An operator can also revert a workspace task across all of its members.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator / power user | Registers a multi-repository project, manages its member list, and reads per-repository landing and review status |
| Solo developer | Ships one change that spans several repositories from one task, one board, and one review |
| Maintainer / contributor | Keeps the multi-repository lifecycle consistent, tested, and documented |
| Git hosting remote | Receives the fenced publication of a member's integration ref when publication is enabled |

## Functional Requirements

Order rows by priority: Must first, then Should.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall detect the member repositories of a project root by scanning only its direct children, excluding `node_modules`, `.fusion`, `.git`, `.pi`, and `.worktrees`, requiring a `.git` marker and a passing Git work-tree probe, and returning the members in sorted order |
| FR-2 | Must | The system shall record the member list in `.fusion/workspace.json` and read it back, accepting only entries that are strings and normalized relative paths inside the workspace root |
| FR-3 | Must | The system shall enable and disable workspace mode for a project, writing the `workspaceMode` setting in `.fusion/config.json` and the authority file `.fusion/workspace.json` in a documented order and reconciling the two when they diverge |
| FR-4 | Must | The system shall add a member repository to an existing workspace idempotently, accepting only an in-root direct child that is a Git work tree and rejecting excluded names, absolute paths, and `..` escapes |
| FR-5 | Must | The system shall acquire one worktree per configured member repository when a task starts, under a durable per-repository lease, and record the worktree path, branch, base branch, and base commit for each member |
| FR-6 | Must | The system shall resolve a base branch for each member repository, verify it in that repository, pin the resolved ref at acquisition, and fall back to that repository's own integration branch when the requested ref does not resolve |
| FR-7 | Must | The system shall refresh every member checkout onto its recorded base branch before execution dispatches, and keep the proven local checkout when the refresh is dirty, conflicting, or unresolvable |
| FR-8 | Must | The system shall require a confirmed repository scope on a workspace task and use that scope as the authority for review and landing, so an acquired checkout alone creates no obligation |
| FR-9 | Must | The system shall review every modified in-scope member repository, qualify each finding with its repository, and return one aggregate verdict with a per-repository outcome for every scoped member |
| FR-10 | Must | The system shall capture review evidence per member from that member's recorded base commit to its task branch, including the changed file list, the repository-qualified file list, and a diff fingerprint |
| FR-11 | Must | The system shall land each member repository independently onto that member's own local integration ref under a durable write fence, and land as it goes so an earlier member can land before a later member fails |
| FR-12 | Must | The system shall record the landing proof for each member and skip a member that is already landed when a land is retried, so a retry never advances an integration ref twice |
| FR-13 | Must | The system shall recover a partial land by re-enqueuing the task and retrying only the unlanded members, and park the task for manual intervention when a member branch is gone and no landing proof exists |
| FR-14 | Must | The system shall revert a workspace task across every member repository by classifying all members before committing any of them, and roll every touched member back when one member conflicts |
| FR-15 | Must | The system shall block completion when a member's main checkout holds a commit attributed to the task, and report an uncommitted main-checkout change as a warning rather than a refusal |
| FR-16 | Must | The system shall classify a workspace task that acquired no member worktree as not applicable, commit-free eligible, or unproven, and use the same classification in review and in completion verification |
| FR-17 | Must | The system shall expose workspace detection and the member list over HTTP, and let a caller add a member repository |
| FR-18 | Must | The system shall list, read, and write files inside a workspace through the dashboard file routes, where a workspace is the project root or a task worktree |
| FR-19 | Should | The system shall prepare every configured or detected member at registration, giving each member a verifiable `HEAD` and the managed `.gitignore` rules, and register no project when preparation fails |
| FR-20 | Should | The system shall apply one operator-supplied branch name to every acquired member repository, attaching to an existing branch when one is already there |
| FR-21 | Should | The system shall interpret the declared File Scope per member repository, so a member prefix yields a member-local scope and a sibling member's declaration yields no authority |
| FR-22 | Should | The system shall publish a member's landing to that member's own remote when `pushAfterMerge` is enabled, and keep the landing on the local integration ref when it is disabled |
| FR-23 | Should | The system shall revert a workspace task through one pull request per member repository when auto-merge is off, and refuse the direct integration-branch path |
| FR-24 | Should | The system shall remove the member worktrees and the workspace task directory after a successful merge and when a workspace task is archived, and preserve a member that holds uncommitted or unverifiable content |

## Non-Functional Requirements

Order rows by priority: Must first, then Should.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Concurrency | Acquire, land, and merge dispatch shall contend on one durable project-and-repository lease key, and a fresh or reclaimed claim shall carry a higher fence token than the claim it replaces |
| NFR-2 | Must | Isolation | The workspace root shall stay browse-only and non-Git, and shall never be a task checkout, a reviewer working directory, or a landing target |
| NFR-3 | Must | Isolation | A member entry shall be a normalized relative path inside the workspace root, and an absolute path, a `..` escape, or a non-string entry shall never reach a path join |
| NFR-4 | Must | Isolation | A member's scope, review evidence, and landing obligations shall never be satisfied by another member's files |
| NFR-5 | Must | Reliability | A landing whose proof write was lost shall still be recognized as landed through the task identifier trailer on the integration history, so the retry does not squash twice |
| NFR-6 | Must | Reliability | A lost or refused lease renewal shall abort the owning land before its next durable or remote write, and the current owner and fence token shall remain the write authority |
| NFR-7 | Must | Reliability | A remote publication shall compare-and-swap the target ref and every fence ref of the tenancy in one atomic push |
| NFR-8 | Must | Recoverability | A partial land shall stay recoverable and shall never be reported as one atomic merge |
| NFR-9 | Must | Recoverability | A lease held by a dead node or a finished task shall be reclaimable once it expires, and the reclaim shall name the owner and the expected fence token |
| NFR-10 | Must | Correctness | The aggregate workspace review verdict shall be deterministic and independent of the order in which members are reviewed |
| NFR-11 | Must | Correctness | Review and landing shall consume the same repository-qualified file list and the same per-repository diff fingerprint |
| NFR-12 | Should | Observability | Base-branch decisions and land outcomes shall be written to the task log and to run audit with identifiers and fixed outcomes only, and never with ref names or file paths |
| NFR-13 | Should | Performance | The workspace configuration read shall be memoized per host, and a mode toggle shall invalidate the memo so a stale read cannot repopulate the old mode |
| NFR-14 | Should | Durability | Every per-member worktree update shall go through the advisory-locked per-key store merge, so a concurrent sibling acquisition, landing, or teardown never loses an entry |

## Constraints

- The member list lives in `.fusion/workspace.json` and the `workspaceMode` setting lives in `.fusion/config.json`, and the two are separate artifacts.
- The workspace root never becomes a Git repository to make workspace mode work.
- The `workspaceMode` setting is not itself the member list, so toggling the setting alone may not create or remove `.fusion/workspace.json`.
- Every configured member is acquired for the task, so membership changes affect later tasks rather than a running task.
- A member's base branch is pinned at acquisition, and a later edit of the task's base branch never retargets an acquired member worktree.
- The land loop is non-atomic across members, and the CLI reports a partial land with a non-zero exit code.
- The `@fusion/*` packages keep statically analyzable imports, and `@fusion/core` never imports `@fusion/engine`.
- New run-audit emitters use the bounded emitter seam so telemetry never delays a lifecycle transition.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Detect the member repositories of a project root
      Given a project root holding two direct child Git repositories and one child without a `.git` marker
      When workspace detection runs on that root
      Then the two Git repositories are returned in sorted order and the child without a marker is not returned
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Reject a member entry that escapes the workspace root
      Given a workspace configuration file holding an absolute path and a `..` escape
      When the member list is read
      Then both entries are filtered out and the remaining in-root entries are kept
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Enable workspace mode on a root with detected members
      Given a project root with no member list and two detected member repositories
      When workspace mode is enabled
      Then the mode setting is written before the member list file and the member list holds the detected repositories
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Add a member repository twice
      Given a workspace whose member list already holds the repository `api`
      When the repository `api` is added again
      Then the outcome is already a member and the member list is unchanged
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Acquire one worktree per configured member
      Given a task in a workspace configured with two member repositories
      When the task acquires its checkouts
      Then one worktree is acquired per member and each member records its worktree path, branch, and base commit
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Fall back when the requested base branch does not resolve in a member
      Given a task that requests a base branch that does not exist in one member repository
      When the base branch is resolved for that member
      Then that member's own integration branch is selected and the fallback is recorded in the task log
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Keep the local checkout when a base refresh conflicts
      Given an acquired member checkout whose recorded base cannot be fast-forwarded
      When the base refresh runs before execution
      Then the local checkout is kept unchanged and execution is not blocked
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Refuse to review a workspace task with no confirmed repository scope
      Given a workspace task whose repository scope is not confirmed
      When code review runs
      Then the verdict is unavailable and not retryable
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Aggregate one verdict across every modified member
      Given a workspace task with two modified in-scope members, one approved and one revised
      When code review completes
      Then the aggregate verdict is revised and each member carries its own outcome
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Capture the diff from the recorded base to the task branch
      Given a member whose recorded base commit is behind its task branch
      When review evidence is captured for that member
      Then the changed files are the ones between the recorded base commit and the task branch and the file list is prefixed with the member name
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Land one member and fail a later member
      Given a workspace task with two modified members where the second member's land fails
      When the land loop runs
      Then the first member's integration ref has advanced and the result reports a partial land
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Skip a member that already landed on a retry
      Given a workspace task whose first member recorded a landing proof
      When the land loop is retried
      Then the first member is skipped and its integration ref is not advanced again
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Recover a partial land by retrying the unlanded members
      Given a workspace task in review with one landed member and one member that failed to land
      When the partial-land sweep runs
      Then the task is re-enqueued so only the unlanded member is retried
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Commit no member revert when one member conflicts
      Given a workspace task whose one member revert conflicts
      When the workspace revert runs
      Then every touched member is rolled back to its pre-call state and no member revert is committed
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Block completion on a task-attributed main-checkout commit
      Given a member main checkout holding a commit that names the task identifier
      When task completion is requested
      Then completion is refused with a main-checkout edit violation
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Classify a workspace task that acquired no member worktree
      Given a workspace task with an empty member worktree map and no commit-free eligibility
      When the zero-acquire classification runs
      Then the classification is unproven
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: List the members of a registered workspace
      Given a registered workspace holding the members `api` and `web`
      When the member list route is called
      Then the response holds `api` and `web` and the request is refused with a conflict for a project that is not a workspace
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: List files in a workspace
      Given a workspace whose identifier is the project root
      When the workspace file list route is called
      Then the response holds the requested path and the directory entries
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: Refuse to register a workspace when a member cannot be prepared
      Given a detected member repository that cannot be prepared
      When project registration completes
      Then no project row is registered or activated
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Apply one operator branch to every member
      Given a workspace task with an operator-supplied branch name
      When the task acquires its checkouts
      Then every acquired member uses that branch name
    ```

- [ ] **FR-21**

    ```gherkin
    @FR-21
    Scenario: Withhold a sibling member's scope from a member
      Given a declared file scope that names only the member `api`
      When the scope is resolved for the member `web`
      Then the resolved scope for `web` is empty
    ```

- [ ] **FR-22**

    ```gherkin
    @FR-22
    Scenario: Publish a member land only when publication is enabled
      Given a workspace task whose publication setting is disabled
      When a member lands
      Then no fence ref is created and no remote write is attempted
    ```

- [ ] **FR-23**

    ```gherkin
    @FR-23
    Scenario: Revert a workspace task through one pull request per member
      Given a workspace task in a project whose auto-merge is off
      When a workspace revert is requested
      Then the direct integration-branch path is refused and one pull request per member is prepared
    ```

- [ ] **FR-24**

    ```gherkin
    @FR-24
    Scenario: Preserve a member that holds uncommitted content
      Given a merged workspace task whose member worktree holds uncommitted content
      When the cleanup runs
      Then that member worktree is preserved with its reason written to the task log
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Fence out a second writer on the same member
      Given a live lease on one member repository held by another task
      When a second task tries to acquire or land that member
      Then the claim reports a conflict naming the holder
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Never treat the workspace root as a checkout
      Given a workspace task whose member worktrees are recorded
      When the task's routing metadata is normalized
      Then the singular worktree and branch fields are cleared and every member entry is preserved
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Refuse a member path that leaves the workspace root
      Given a caller that asks to add the member `../outside-repo`
      When the member is added
      Then the request is refused with an invalid path reason
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Keep a member's landing obligation separate from its sibling
      Given a confirmed scope of two members where only one has changed files
      When the merge readiness is resolved
      Then only the member with changed files carries a landing obligation
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Prove a lost landing proof through the task identifier trailer
      Given a member whose integration ref advanced with a squash commit carrying the task identifier trailer
      When the landed predicate runs without a recorded landing proof
      Then the member is reported as landed and the proven commit is returned
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Abort a land when the lease renewal is lost
      Given a land whose lease renewal is refused
      When the land body reaches its next durable write
      Then the land aborts before that write
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Reject a publication whose target moved
      Given a remote target ref that moved after the fence pin was published
      When the fenced push runs
      Then the push is rejected and the target ref is not overwritten
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Report a partial land as a partial land
      Given a workspace land where one member failed
      When the merge result is reported to the operator
      Then the result reports that not all members landed and the task is not finalized
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: Reclaim an expired lease
      Given a held lease whose expiry has passed
      When the expired lease sweep runs
      Then the lease is reclaimed and the reclaimed key is reported
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: Keep the aggregate verdict independent of member order
      Given two members where one is revised and the other is unavailable
      When the members are reviewed in either order
      Then the aggregate verdict is revised in both runs
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: Refuse to land an approved member whose diff changed
      Given a member whose approved diff fingerprint no longer matches its current diff
      When the landing evidence is checked
      Then the member is reported as content changed and the task is routed back to review
    ```

- [ ] **NFR-12**

    ```gherkin
    @NFR-12
    Scenario: Record a base-branch decision without ref names
      Given a base-branch fallback in one member
      When the decision is audited
      Then the audit row holds the task, the member, the stage, and the fixed outcome, and no ref name
    ```

- [ ] **NFR-13**

    ```gherkin
    @NFR-13
    Scenario: Invalidate the memoized member list on a mode toggle
      Given a pending member list read for a project
      When workspace mode is toggled for that project
      Then the pending read cannot repopulate the previous mode
    ```

- [ ] **NFR-14**

    ```gherkin
    @NFR-14
    Scenario: Preserve sibling entries on a per-member update
      Given a workspace task with two member entries
      When one member entry is updated
      Then the other member entry is preserved unchanged
    ```

## Conflicts

None identified yet.

## Open Questions

1. The code does not say whether a workspace task may be created against a member list that changes while the task is in review.
   The membership snapshot is captured at acquisition, so the current behavior is that later membership changes affect only later tasks, and the intent behind that choice is not recorded.

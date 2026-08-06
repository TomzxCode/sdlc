---
title: "Automated Code Review, Merge & PR Automation"
status: done
---

# Requirements: Automated Code Review, Merge & PR

## Overview

Fusion takes finished branches through automated code review, safe merges into the default branch (squash, rebase, PR paths), and GitHub/GitLab PR creation and monitoring. The merger and PR automation apply file-scope, lineage, and diff-volume guards and resolve conflicts to land reviewed work without manual merge work.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Approves merges/PRs, monitors PRs, reads merge advance notice |
| Reviewer | Reviews the branch at the graph review node |
| VCS system | GitHub/GitLab hosting for PRs and branches |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall run code review as a workflow-graph node before merge |
| FR-2 | Must | The system shall merge finished branches into the default branch with a configurable commit strategy (squash default) |
| FR-3 | Must | The system shall resolve merge conflicts and reconcile divergent branches (auto-prerebase, smart pull) |
| FR-4 | Must | The system shall enforce file-scope, overlap-guard, and diff-volume gates before forming a squash commit |
| FR-5 | Must | The system shall drive GitHub/GitLab PRs: create, monitor, respond, finalize |
| FR-6 | Should | The system shall detect already-merged/landed branches and skip or classify accordingly |
| FR-7 | Should | The system shall expose merge advance notice and merge detail surfaces in the dashboard |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Correctness | Every squash commit must overlap the task file-scope; violations fail with FileScopeViolationError |
| NFR-2 | Must | Integrity | Empty cherry-picks are no-ops; duplicate on-main commits are dropped before merging |
| NFR-3 | Must | Reliability | Post-squash audit policy (`warn`/`block`/`off`) must be respected |
| NFR-4 | Must | Liveness | Triple-proof must protect against moving a user-paused or auto-merge-off branch backward |

## Constraints

- Prefer squash by default; history-preserving merges require opt-in strategy
- Never force-add ignored artifacts on squash merges
- GitLab parity is tracked as a first-class supported surface (`docs/gitlab-parity-inventory.md`)

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a finished branch
    - **When** the review node runs
    - **Then** a review verdict is produced before merge consideration
- [ ] **FR-2**
    - **Given** an approved branch
    - **When** merge proceeds
    - **Then** it lands in the default branch under the configured strategy
- [ ] **FR-4**
    - **Given** a branch whose changed files are out of the task file-scope
    - **When** merge runs
    - **Then** the squash is rejected with a FileScopeViolationError
- [ ] **FR-5**
    - **Given** a PR to open
    - **When** the PR monitor runs
    - **Then** a PR is created, monitored, and finalized
- [ ] **NFR-1**
    - **Given** merged changes
    - **When** the commit is formed
    - **Then** the scope/invariant holds on the squash commit

## Conflicts

None identified yet.

## Open Questions

1. Which auto-merge policies require explicit operator opt-in versus default?
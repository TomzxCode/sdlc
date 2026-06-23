---
title: "Git Worktree Management"
status: draft
---

# Requirements: Git Worktree Management

## Overview

Create, manage, and delete git worktrees from the UI. Each worktree has its own session, branch, and optionally running agent. Includes branch name generation, worktree validation, setup command execution, branch renaming/deletion, and an Agent Group view showing all worktree sessions organized by branch.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers working on multiple PRs | Isolated branches with dedicated sessions |
| Multi-agent users | Each agent runs in its own worktree |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating git worktrees with branch name generation and validation. |
| FR-02 | Must | The system shall associate worktrees with dedicated sessions. |
| FR-03 | Must | The system shall support deleting worktrees and cleaning up associated sessions. |
| FR-04 | Must | The system shall support running setup commands after worktree creation. |
| FR-05 | Should | The system shall display an Agent Group view organizing worktree sessions by branch. |
| FR-06 | Should | The system shall support branch renaming and deletion from the worktree UI. |
| FR-07 | Should | The system shall support instant draft-first worktree creation. |
| FR-08 | Should | The system shall support creating worktrees from PR heads, reusing existing local branches. |
| FR-09 | Must | The system shall allow checkout with uncommitted changes, show dirty-change warnings on deletion, provide guided conflict handling for commit integration, and support stash management. |

## Acceptance Criteria

- [ ] FR-01: Given a project, the user creates a worktree with a generated branch name
- [ ] FR-02: Given a worktree, it has its own session with isolated working directory
- [ ] FR-03: Given a worktree, the user can delete it and its session is cleaned up
- [ ] FR-04: Given a newly created worktree, a setup command runs automatically after creation
- [ ] FR-05: Given multiple worktrees, the Agent Group view shows them organized by branch
- [ ] FR-06: Given a worktree, the user can rename its branch or delete the branch from the worktree UI
- [ ] FR-07: Given a draft-first workflow, the user creates a worktree instantly without specifying a target branch
- [ ] FR-08: Given a PR, creating a worktree reuses the existing local branch if it matches
- [ ] FR-09: Given a worktree with uncommitted changes, checkout is allowed; given deletion of a dirty worktree, a warning is shown; given a merge conflict, guided conflict handling is provided

## Constraints

- Git worktree operations are performed via the `simple-git` library

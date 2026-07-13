---
title: "Git & GitHub Integration"
status: done
---

# Requirements: Git & GitHub Integration

## Overview

OpenChamber provides a full Git sidebar and GitHub-native workflows inside the app. Users can stage files, commit, push/pull, manage branches, create pull requests with AI-generated descriptions, start sessions from issues and PRs, manage worktrees for multi-run isolation, and handle GitHub authentication for multiple accounts.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | In-app Git workflows without switching to a terminal or external tool |
| Open-source contributors | PR creation, review checks, and merge actions integrated with chat |
| Teams | Multi-account GitHub auth and fork-aware PR creation |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display a Git sidebar showing changed files, staging area, and commit controls. |
| FR-02 | Must | The system shall support staging, unstaging, committing, pushing, and pulling with visual feedback. |
| FR-03 | Must | The system shall support branch creation, switching, and deletion with a searchable branch picker. |
| FR-04 | Must | The system shall support creating pull requests with AI-generated descriptions directly from the UI. |
| FR-05 | Must | The system shall display PR status checks, merge actions, and review state. |
| FR-06 | Must | The system shall support starting AI sessions from GitHub issues and pull requests with context attached. |
| FR-07 | Must | The system shall support one-click sync (pull + push) and stash management. |
| FR-08 | Should | The system shall support worktree integration for isolated sessions per branch with merge-back and conflict handling. |
| FR-09 | Should | The system shall support Git identities (multiple name/email configs) and gitmoji support. |
| FR-10 | Should | The system shall support multi-remote push and fork-aware PR creation. |
| FR-11 | May | The system shall support rebase and merge flows with conflict resolution UI. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Git status polling shall use lightweight change detection first and heavy status fetches only for changed directories. |
| NFR-02 | Must | Reliability | Large change lists shall display reliably without UI freeze. |
| NFR-03 | Should | Security | GitHub OAuth tokens shall be stored securely and refreshed automatically. |

## Constraints

- Git operations use `simple-git` library on the server side
- GitHub API uses `@octokit/rest`
- Git state is polled; no git hooks or filesystem watchers for git events
- Branch selection is hidden for non-Git draft sessions

## Acceptance Criteria

- [ ] FR-01: Given a Git repository, the sidebar shows unstaged, staged, and untracked files
- [ ] FR-02: Given staged changes, the user can commit with a message and the commit succeeds
- [ ] FR-03: Given multiple branches, the branch picker allows search and switching
- [ ] FR-04: Given a branch with commits ahead of remote, the user can create a PR with an AI-generated description
- [ ] FR-05: Given an open PR, the UI shows CI check status and merge button
- [ ] FR-06: Given a GitHub issue, the user can start a session with the issue body as context
- [ ] FR-07: Given a dirty worktree, the user can stash, sync, and pop stash
- [ ] FR-08: Given a branch with a worktree, the user can merge changes back and resolve conflicts from the UI
- [ ] FR-09: Given multiple Git identities configured, when committing, the user can select which identity to use and optionally add a gitmoji
- [ ] FR-10: Given a fork of a repository, the user can push to multiple remotes and create a PR targeting the upstream
- [ ] FR-11: Given a branch with diverged history, the user can initiate a rebase or merge and resolve conflicts inline
- [ ] NFR-01: Given a directory with no git changes, git status polling uses lightweight change detection and skips heavy status fetches
- [ ] NFR-02: Given a diff with 10,000+ changed files, the change list renders without UI freeze
- [ ] NFR-03: Given GitHub OAuth tokens stored by the app, they are stored securely and refreshed automatically when expired

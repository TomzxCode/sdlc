---
title: "Git & GitHub Integration"
status: done
---

# Specification: Git & GitHub Integration

## Overview

Git operations are handled server-side via `simple-git` and `@octokit/rest`. The UI consumes REST endpoints exposed by the Express server. Git state is polled on a schedule with lightweight change detection triggering heavier status fetches. GitHub OAuth device flow handles authentication.

## Architecture

```
Git Sidebar UI (packages/ui/src/components/)
    |
    v  REST calls
Express Server (packages/web/server/lib/git/)
    |
    +---> simple-git (local repo operations)
    |
    +---> @octokit/rest (GitHub API)
    |
    +---> GitHub OAuth Device Flow (packages/web/server/lib/github/)
```

## Data Models

### GitStatus

| Field | Type | Constraints | Description |
|---|---|---|---|
| branch | string | not null | Current branch name |
| ahead | number | not null | Commits ahead of upstream |
| behind | number | not null | Commits behind upstream |
| staged | FileEntry[] | not null | Staged file changes |
| unstaged | FileEntry[] | not null | Unstaged file changes |
| untracked | string[] | not null | New untracked files |
| stashCount | number | not null | Number of stashes |

### PullRequest

| Field | Type | Constraints | Description |
|---|---|---|---|
| number | number | PK | PR number |
| title | string | not null | PR title |
| state | enum | not null | open, closed, merged |
| mergeable | boolean | nullable | Merge compatibility |
| statusChecks | Check[] | not null | CI check results |

## API Contracts

### GET /api/git/status

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| branch | string | Current branch |
| ahead | number | Ahead count |
| behind | number | Behind count |
| files | FileEntry[] | Changed files with status codes |

### POST /api/git/commit

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| message | string | yes | Commit message |
| files | string[] | no | Specific files to stage (empty = all staged) |

### POST /api/git/pull-request

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| title | string | yes | PR title |
| body | string | no | PR description (AI-generated if omitted) |
| base | string | no | Base branch |
| head | string | no | Head branch |

## Sequences

### Create PR with AI-generated description

```
User clicks "Create PR" -> POST /api/git/pull-request
    |
    v
Server gathers commit messages since branch point
    |
    v
Server calls OpenCode to generate PR description
    |
    v
Server creates PR via GitHub API
    |
    v
Returns PR data to UI -> UI shows PR link and status
```

### One-click sync

```
User clicks "Sync" -> Server: git pull --rebase
    |
    v
If conflicts: UI shows conflict state
    |
    v
If success: Server: git push
    |
    v
UI refreshes git status
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Git library | simple-git | Mature Node.js wrapper for git CLI; handles all operations needed |
| GitHub API | @octokit/rest | Official GitHub REST client with TypeScript types |
| Auth flow | OAuth device flow | No client secret required; works for desktop and web |
| Polling strategy | Two-phase (lightweight detection + heavy fetch) | Avoids unnecessary CPU/IO for unchanged repos |
| PR description | AI-generated via OpenCode prompt | Leverages existing AI capability for PR boilerplate |

## Risks and Unknowns

1. Large repositories (10k+ files changed) may cause polling latency
2. GitHub API rate limits may affect heavy users

## Out of Scope

- GitLab, Bitbucket, or other forge support
- Interactive rebase UI
- Merge conflict resolution editor (basic handling only)

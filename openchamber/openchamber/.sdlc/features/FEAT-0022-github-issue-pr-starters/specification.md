---
title: "GitHub Issue / PR Starters"
status: done
---

# Specification: GitHub Issue / PR Starters

## Overview

Issue and PR picker dialogs (`GitHubIssuePickerDialog.tsx`, `GitHubPrPickerDialog.tsx`) use the GitHub API via `@octokit/rest` to list and fetch issues/PRs. The `GitHubIntegrationDialog.tsx` manages OAuth and connection setup.

## Architecture

```
GitHubIssuePickerDialog (packages/ui/src/components/session/)
    +---> Issue list (browse, search, URL/number input)
    |
GitHubPrPickerDialog
    +---> PR list with status checks, mergeable state
    +---> Load PR context (description, comments, checks)
    |
v  REST calls
Server GitHub API (packages/web/server/lib/github/)
    +---> @octokit/rest (list issues, list PRs, get PR details)
    +---> OAuth device flow
```

## Sequences

### Start session from GitHub issue

```
User opens issue picker -> Browses or enters issue URL/number
    |
    v
Server fetches issue details via GitHub API
    |
    v
User clicks "Start session" -> Optionally creates worktree
    |
    v
New session created with issue title + body as initial context
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Input methods | Browse, search, URL, number | Supports multiple user workflows |
| Context loading | Full issue/PR body + comments | Gives the AI maximum context for the task |

## Out of Scope

- Issue/PR creation from within the session
- Cross-repository issue linking

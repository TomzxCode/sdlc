---
title: "Git Worktree Management"
status: draft
---

# Specification: Git Worktree Management

## Overview

Worktree management is implemented in `packages/ui/src/lib/worktrees/` with `worktreeManager.ts`, `worktreeCreate.ts`, `worktreeStatus.ts`, `worktreeBootstrap.ts`, and `branchSearch.ts`. The `NewWorktreeDialog.tsx` provides creation UI. Agent groups use `useAgentGroupsStore.ts`.

## Architecture

```
NewWorktreeDialog / BranchPickerDialog (packages/ui/src/components/session/)
    |
    v
worktreeManager.ts (orchestration)
    +---> worktreeCreate.ts (creation, validation)
    +---> worktreeStatus.ts (status tracking)
    +---> worktreeBootstrap.ts (setup commands)
    +---> branchSearch.ts (branch name generation/search)
    |
    v
Agent Group View (useAgentGroupsStore.ts)
    Shows worktree sessions organized by branch
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Management | Client-side with git CLI | Worktrees are a git concept; client manages lifecycle |
| Session association | Directory-based | Each worktree has its own directory; session follows |
| Branch reuse | Match PR head to local branch | Avoids duplicate branches when creating worktrees from PRs |

## Out of Scope

- Worktree diffing between branches
- Automatic merge back (handled manually via git)

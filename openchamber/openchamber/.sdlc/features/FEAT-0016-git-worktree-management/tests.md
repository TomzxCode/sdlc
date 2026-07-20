---
title: "Git Worktree Management"
status: done
---

# Test Plan: Git Worktree Management

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Git service handles worktree creation | Worktree create request | Worktree is created in isolated directory |
| TC-2 | Session worktree store manages active worktrees | Worktree lifecycle events | Store tracks worktree state correctly |
| TC-3 | Multi-run store uses worktrees for parallel agents | Multi-run start event | Each agent gets an isolated worktree |

## Test Files

- `packages/web/server/lib/git/service.test.js`
- `packages/ui/src/sync/session-worktree-store.test.js`
- `packages/ui/src/stores/useMultiRunStore.test.ts`
- `packages/vscode/src/gitService.worktree-bootstrap.test.js`
- `packages/vscode/src/bridge-git-runtime.test.js`

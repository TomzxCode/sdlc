---
title: "Git & GitHub Integration"
status: done
---

# Test Plan: Git & GitHub Integration

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Git service handles branch operations | Branch name, repo path | Correct branch created/switched |
| TC-2 | Git graph renders correctly | Commit history data | Properly rendered graph |
| TC-3 | GitHub credential helper works | GitHub token | Correct credential resolution |

## Test Files

- `packages/web/server/lib/git/service.test.js`
- `packages/web/server/lib/github/gh-cli-credential.test.js`
- `packages/ui/src/components/views/git/gitGraph.test.ts`
- `packages/ui/src/components/views/git/gitIndexMutationQueue.test.ts`
- `packages/ui/src/stores/useGitStore.test.ts`
- `packages/ui/src/stores/useGitStore.repro.test.ts`
- `packages/web/src/api/git.test.ts`
- `packages/vscode/src/bridge-git-runtime.test.js`
- `packages/vscode/src/bridge-git-special-runtime.test.js`

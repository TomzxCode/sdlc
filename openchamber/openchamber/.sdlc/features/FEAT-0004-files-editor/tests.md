---
title: "Files & Editor"
status: done
---

# Test Plan: Files & Editor

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | File system routes handle CRUD | File paths, content | Correct read/write/delete responses |
| TC-2 | File search store works | Search query | Filtered file results |

## Test Files

- `packages/web/server/lib/fs/routes.test.js`
- `packages/web/src/api/files.test.ts`
- `packages/ui/src/stores/useFilesViewTabsStore.test.ts`
- `packages/ui/src/stores/useFilesViewTabsStore.windows.test.ts`
- `packages/ui/src/stores/useFileSearchStore.test.ts`
- `packages/vscode/src/bridge-fs-runtime.test.js`

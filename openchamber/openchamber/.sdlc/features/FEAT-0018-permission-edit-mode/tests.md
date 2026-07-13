---
title: "Permission & Edit Mode"
status: done
---

# Test Plan: Permission & Edit Mode

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Permission store manages requests | Permission request data | Correct approve/deny/reject |
| TC-2 | Auto-accept runtime persists correctly | Auto-accept config | Correct persistence and retry |

## Test Files

- `packages/ui/src/stores/permissionStore.test.ts`
- `packages/web/server/lib/permission-auto-accept/runtime.test.js`
- `packages/ui/src/stores/utils/permissionAutoAccept.test.ts`
- `packages/ui/src/sync/scoped-blocking-requests.test.ts`

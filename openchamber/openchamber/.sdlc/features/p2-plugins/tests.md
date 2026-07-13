---
title: "Plugins"
status: done
---

# Test Plan: Plugins

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Plugin store manages plugins | Plugin data | Correct add/remove/toggle |
| TC-2 | Plugin routes work | Plugin config | Correct registration and execution |

## Test Files

- `packages/ui/src/stores/usePluginsStore.test.ts`
- `packages/web/server/lib/opencode/plugins.test.js`
- `packages/web/server/lib/opencode/plugin-routes.test.js`
- `packages/web/server/lib/opencode/plugin-spec.test.js`

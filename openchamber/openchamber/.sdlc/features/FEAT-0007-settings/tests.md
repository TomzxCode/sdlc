---
title: "Settings"
status: done
---

# Test Plan: Settings

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Settings helpers normalize correctly | Raw settings | Correctly normalized settings |
| TC-2 | Theme sync payload creates correctly | Theme data | Correct sync payload |

## Test Files

- `packages/web/server/lib/opencode/settings-helpers.test.js`
- `packages/web/server/lib/opencode/settings-runtime.test.js`
- `packages/web/server/lib/opencode/settings-normalization-runtime.test.js`
- `packages/ui/src/contexts/theme-sync-payload.test.ts`
- `packages/ui/src/contexts/ThemeSystemContext.test.ts`

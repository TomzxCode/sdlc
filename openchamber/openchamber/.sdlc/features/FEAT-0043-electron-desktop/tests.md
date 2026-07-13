---
title: "Electron Desktop"
status: done
---

# Test Plan: Electron Desktop

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Updater feed parses correctly | Feed URL | Correct update manifest |
| TC-2 | SSH manager works in Electron | SSH config | Correct connection management |
| TC-3 | Runtime request headers correct | HTTP request | Properly forwarded headers |

## Test Files

- `packages/electron/updater-feed.test.mjs`
- `packages/electron/updater-check.test.mjs`
- `packages/electron/updater-capability.test.mjs`
- `packages/electron/ssh-manager.test.mjs`
- `packages/electron/runtime-request-headers.test.mjs`
- `packages/electron/opencode-cwd.test.mjs`
- `packages/electron/scripts/target-architecture.test.mjs`
- `packages/electron/scripts/verify-update-manifest.test.mjs`
- `packages/electron/scripts/updater-e2e-fixture.test.mjs`
- `packages/electron/scripts/verify-linux-appimage.test.mjs`

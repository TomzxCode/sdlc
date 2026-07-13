---
title: "Tunnel & Remote Access"
status: done
---

# Test Plan: Tunnel & Remote Access

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Tunnel types resolve correctly | Provider config | Correct tunnel provider instance |
| TC-2 | Executable search finds binaries | Binary name | Correct path or not found |
| TC-3 | ngrok tunnel starts and stops | ngrok config | Correct lifecycle events |

## Test Files

- `packages/web/server/lib/tunnels/types.test.js`
- `packages/web/server/lib/tunnels/index.test.js`
- `packages/web/server/lib/tunnels/executable-search.test.js`
- `packages/web/server/lib/tunnels/install-help.test.js`
- `packages/web/server/lib/ngrok-tunnel.test.js`

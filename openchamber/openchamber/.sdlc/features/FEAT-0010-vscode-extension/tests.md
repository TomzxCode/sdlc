---
title: "VS Code Extension"
status: done
---

# Test Plan: VS Code Extension

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Bridge proxy routes correctly | API requests from webview | Correctly proxied to server |
| TC-2 | SSE proxy forwards events | SSE event stream | Correctly forwarded to webview |

## Test Files

- `packages/vscode/src/bridge-proxy-runtime.test.js`
- `packages/vscode/src/bridge-proxy-runtime.test.ts`
- `packages/vscode/src/bridge-localfs-proxy-runtime.test.js`
- `packages/vscode/src/bridge-config-runtime.test.js`
- `packages/vscode/src/sseProxy.test.js`
- `packages/vscode/src/opencode-ready.test.ts`
- `packages/vscode/src/workspaceResolver.test.js`
- `packages/vscode/webview/api/bridge.test.ts`
- `packages/vscode/webview/requestBodyTransport.test.ts`

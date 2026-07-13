---
title: "Integrated Terminal"
status: done
---

# Test Plan: Integrated Terminal

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Terminal WS protocol handles frames | WS message frames | Correctly parsed protocol messages |
| TC-2 | Output replay buffer stores frames | PTY output chunks | Correctly ordered and bounded buffer |

## Test Files

- `packages/web/server/lib/terminal/terminal-ws-protocol.test.js`
- `packages/web/server/lib/terminal/runtime.test.js`
- `packages/web/server/lib/terminal/output-replay-buffer.test.js`

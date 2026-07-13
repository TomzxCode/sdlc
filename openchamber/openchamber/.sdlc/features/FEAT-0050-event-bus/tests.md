---
title: "Event Bus"
status: done
---

# Test Plan: Event Bus

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Global hub handles replay | SSE event stream | Correct replay for reconnecting clients |
| TC-2 | Upstream reader reconnects on stall | Stalled connection | Correct reconnect with Last-Event-ID |

## Test Files

- `packages/web/server/lib/event-stream/global-hub.test.js`
- `packages/web/server/lib/event-stream/upstream-reader.test.js`
- `packages/web/server/lib/event-stream/protocol.test.js`
- `packages/web/server/lib/event-stream/runtime.test.js`

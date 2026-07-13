---
title: "Event Bus"
status: done
---

# Specification: Event Bus

## Overview

The event bus is implemented as a two-leg relay: OpenCode CLI emits SSE events, the Express server subscribes and rebroadcasts to browser clients over WebSocket.
The server side lives in `packages/web/server/lib/event-stream/` and the client side in `packages/ui/src/sync/`.
Transport concerns are separated into protocol helpers, upstream readers, hub/bridge modules, and a client-side pipeline with event reduction.

## Architecture

```
                          SERVER SIDE
                          (packages/web/server/lib/event-stream/)

OpenCode CLI
    |
    | SSE /global/event
    v
UpstreamSseReader (upstream-reader.js)
    |
    v
GlobalMessageStreamHub (global-hub.js)
    |  bounded replay buffer (2048 events, keyed by eventId)
    |  server-side subscribers (OpenCode watcher)
    |
    +---> GlobalWsBridge (global-ws-bridge.js)
    |        |  fans out to all WS clients
    |        v
    |     Browser WS clients on /api/global/event/ws
    |
    v
Server-side event subscribers

---

OpenCode CLI
    |
    | SSE /event?directory=X
    v
UpstreamSseReader (per-connection)
    |
    v
DirectoryWsBridge (directory-ws-bridge.js)
    |
    v
Browser WS client on /api/event/ws?directory=X

---

                          CLIENT SIDE
                          (packages/ui/src/sync/)

Browser WebSocket or SSE connection
    |
    v
EventPipeline (event-pipeline.ts)
    |  auto transport (WS primary, SSE fallback)
    |  reconnect with exponential backoff
    |  coalescing within flush frame (33ms)
    |  backpressure-aware flush interval
    |
    v
EventReducer (event-reducer.ts)
    |  transforms raw events into state mutations
    |  global events: refresh, project.update
    |  directory events: session/message/part/permission/question/todo/vcs
    |
    v
SyncContext (sync-context.tsx)
    |  handleDirectoryEvent clones only affected state branches
    |  dispatches to split Zustand stores
    |
    v
React components (re-render on leaf selector changes only)
```

## Data Models

### SSE Event Envelope

| Field | Type | Constraints | Description |
|---|---|---|---|
| eventId | string | nullable | SSE `id` field for replay tracking |
| directory | string | nullable | Target directory scope; `"global"` if absent |
| payload | object | not null | Event payload from OpenCode |

### WebSocket Frame (server-to-client)

| Field | Type | Constraints | Description |
|---|---|---|---|
| type | enum | not null | `ready`, `event`, `error`, `backpressure` |
| payload | object | nullable | Event payload (for `event` type) |
| eventId | string | nullable | Last-Event-ID for replay tracking |
| directory | string | nullable | Target directory |
| scope | string | nullable | `global` or `directory` (for `ready` frames) |
| message | string | nullable | Error description (for `error` frames) |
| bufferedBytes | number | nullable | Current buffer size (for `backpressure` frames) |
| maxBytes | number | nullable | Buffer limit (for `backpressure` frames) |

### Client State (per directory)

| Field | Type | Description |
|---|---|---|
| session | Session[] | Ordered session list |
| message | Record<string, Message[]> | Messages indexed by session ID |
| part | Record<string, Record<string, Part[]>> | Parts indexed by session ID then message ID |
| permission | Record<string, PermissionRequest[]> | Pending permission requests by session ID |
| question | Record<string, QuestionRequest[]> | Pending questions by session ID |
| todo | Record<string, Todo[]> | Todos by session ID |
| session_status | Record<string, SessionStatus> | Live status by session ID |
| session_diff | Record<string, FileDiff[]> | Diff snapshots by session ID |
| vcs | object | Branch/version control state |
| lsp | object | LSP diagnostics |

### Reconnect Configuration

| Parameter | Default | Description |
|---|---|---|
| stallTimeoutMs | 20,000 | Upstream idle timeout before reconnect |
| reconnectDelayMs | 250 | Base delay between reconnect attempts |
| replayLimit | 2,048 | Max events in global replay buffer |
| heartbeatIntervalMs | 15,000 | WS heartbeat ping interval |
| flushFrameMs | 33 | Client-side event coalescing window |
| wsReadyTimeoutMs | 2,000 | Time to wait for WS before SSE fallback |
| heartbeatTimeoutMs | 30,000 | Client-side heartbeat timeout |
| wsMaxBufferedBytes | 16,777,216 (16MB) | Per-client buffer limit before disconnect |
| wsBackpressureWarnBytes | 12,582,912 (12MB) | Per-client warning threshold |

## API Contracts

### WebSocket /api/global/event/ws

Client connects with query parameter `lastEventId` for replay recovery.

**Client -> Server (ready frame)**

After connection, client sends a `ready` message indicating it is ready to receive events.

**Server -> Client frames**

| Frame type | Description |
|---|---|
| `ready` | Confirms connection is established; includes `scope: "global"` |
| `event` | Relayed OpenCode event with `eventId`, `directory`, and `payload` |
| `error` | Upstream failure notification with `message` |
| `backpressure` | Warning that client is falling behind; includes `bufferedBytes` and `maxBytes` |

### WebSocket /api/event/ws?directory=X

Same frame protocol as global, but scoped to one directory.
Each connection owns its own upstream SSE reader.

### SSE /global/event (upstream, OpenCode -> Express)

Standard SSE stream from OpenCode CLI. Each event has:
- `id:` line for event tracking
- `data:` line(s) with JSON payload containing `directory` and `payload` fields

### SSE /event?directory=X (upstream, OpenCode -> Express)

Directory-scoped SSE stream from OpenCode CLI.

## Sequences

### Global event fan-out

```
OpenCode emits SSE event (id: "abc123", data: { directory: "/project", payload: { type: "session.created", ... } })
    |
    v
UpstreamSseReader parses SSE block -> calls onEvent callback
    |
    v
GlobalMessageStreamHub receives event
    |-- appends to bounded replay buffer (drops oldest if over limit)
    |-- notifies server-side subscribers (watcher, etc.)
    |-- notifies GlobalWsBridge
    |
    v
GlobalWsBridge fans out to all ready WS clients
    |-- each client: sendMessageStreamWsEvent(socket, payload, { eventId, directory })
    |-- if socket.bufferedAmount > 16MB: close with 1013
    |
    v
Browser EventPipeline receives WS frame
    |-- coalesces into flush queue
    |-- after 33ms flush frame: batch-dispatch to event reducer
    |
    v
EventReducer applies event to directory state draft
    |-- event.type === "session.created": insert into sorted session array
    |
    v
SyncContext.handleDirectoryEvent clones only affected branches
    |-- session.created clones: session, permission, todo, part
    |-- other branches keep same reference (no re-render for their subscribers)
    |
    v
Zustand store subscribers re-evaluate selectors
    |-- only components selecting mutated state branches re-render
```

### Upstream stall recovery

```
UpstreamSseReader detects no data for 20s (stallTimeoutMs)
    |
    v
AbortController.abort() on current fetch
    |
    v
Wait reconnectDelayMs (250ms base, exponential on consecutive failures)
    |
    v
Re-fetch upstream SSE with Last-Event-ID header
    |
    v
OpenCode resumes stream from last received event
    |
    v
Browser WS clients remain connected throughout (no disruption)
```

### Client reconnect with backoff

```
EventPipeline detects disconnect (heartbeat timeout, network error, transport failure)
    |
    v
Determine backoff based on:
    |-- navigator.onLine: offline -> long cap (60s)
    |-- document.visibilityState: hidden -> long cap (60s)
    |-- HTTP status: permanent 4xx -> long cap (60s)
    |-- Otherwise: exponential (250ms * 2^failures, cap 5s visible / 60s hidden)
    |
    v
Wait backoff duration (interruptible by online event, visibility change, or abort signal)
    |
    v
Attempt reconnect with same transport preferences
    |
    v
On success: dispatch buffered events, resume normal flow
On failure: increment failure count, recalculate backoff, retry
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Transport | SSE upstream (OpenCode), WS downstream (browser) | OpenCode is SSE-only; WS gives full-duplex for browser with lower overhead than SSE-over-HTTP |
| Global hub sharing | Single upstream SSE reader shared by all global WS clients | Avoids N duplicate upstream connections for N browser clients |
| Directory bridge | One upstream reader per WS connection | Directory streams are scoped; cannot share across clients with different directory filters |
| Replay buffer | Bounded in-memory ring (2048 events) | Handles brief disconnects without refetch; bounded to prevent unbounded growth |
| Client event coalescing | 33ms flush frame | Batches high-frequency deltas (60/sec) into fewer store updates; reduces render count |
| Store splitting | Separate Zustand stores by change frequency and subscriber set | Prevents streaming state from causing re-renders in unrelated components |
| Targeted cloning | Only clone state branches the event type mutates | Zustand referential equality prevents re-renders for unchanged branches; ~7x render reduction |
| Backpressure | Per-client buffer tracking with warning + disconnect | Prevents one slow client from degrading server performance; 12MB warning, 16MB hard disconnect |
| Transport fallback | WS primary with SSE fallback after 2s timeout | WS is more efficient but SSE is more reliable in some network environments |
| Reconnect pacing | Exponential backoff with visibility/online/status signals | Hidden/offline tabs use long cap to reduce battery and server load; visible tabs recover fast |

## Risks and Unknowns

1. Replay buffer (2048 events) may be insufficient for very long agent sessions with many tool calls; events beyond the buffer require full refetch
2. The in-memory replay buffer is lost on server restart; all connected clients must do a full bootstrap
3. No binary frame support; large payloads (file contents) are JSON-encoded which may hit memory limits
4. No horizontal scaling support; the in-memory hub and replay buffer are per-process
5. The WS backpressure mechanism relies on `bufferedAmount` which may behave differently across browser implementations

## Out of Scope

- Binary WebSocket frames
- Persisted replay buffer (disk-backed)
- Horizontal scaling (multi-server event distribution)
- Compression of WebSocket frames
- Client authentication on WebSocket beyond initial HTTP upgrade

---
title: "Event Bus"
status: draft
---

# Requirements: Event Bus

## Overview

The event bus is the cross-cutting real-time communication infrastructure that relays OpenCode session events to the browser UI.
It spans two transport legs: SSE from the OpenCode CLI to the Express server, then WebSocket from the Express server to the browser.
Every runtime (web, desktop, VS Code) depends on this pipeline for live session updates, streaming deltas, permission prompts, notifications, and status changes.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All OpenChamber runtimes (web, desktop, VS Code) | Real-time session and streaming data |
| Chat feature | Message deltas, part updates, session status |
| Git feature | Branch change notifications |
| Terminal feature | Session-scoped activity signals |
| Notifications feature | Push and browser notification triggers |
| Multi-run feature | Parallel session status across directories |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall subscribe to the OpenCode global event stream (`/global/event`) via SSE and relay events to connected browser clients via WebSocket. |
| FR-02 | Must | The system shall subscribe to per-directory event streams (`/event?directory=X`) via SSE with one upstream reader per WebSocket connection. |
| FR-03 | Must | The system shall maintain a bounded replay buffer keyed by `eventId` so reconnecting clients can recover missed events without refetching. |
| FR-04 | Must | The system shall detect upstream SSE stalls (no data within configurable timeout) and automatically reconnect with `Last-Event-ID` while keeping browser WebSocket connections alive. |
| FR-05 | Must | The system shall fan out global events to all connected WebSocket clients via a shared global hub. |
| FR-06 | Must | The system shall generate and relay synthetic events (`openchamber:session-status`, `openchamber:session-activity`, `openchamber:notification`, `openchamber:heartbeat`) from the server to connected clients. |
| FR-07 | Must | The client-side event pipeline shall support automatic transport selection (WebSocket primary, SSE fallback) with configurable timeouts. |
| FR-08 | Must | The client-side event pipeline shall coalesce incoming events within a flush frame (~33ms) and batch-dispatch them to Zustand stores to minimize render cascades during streaming. |
| FR-09 | Must | The client-side event reducer shall apply targeted state mutations, cloning only the Zustand store fields affected by each event type. |
| FR-10 | Must | The system shall support reconnect with exponential backoff that respects `navigator.onLine`, `document.visibilityState`, and upstream HTTP status codes (permanent 4xx errors use long cap; retryable errors use normal backoff). |
| FR-11 | Must | The system shall enforce backpressure by tracking per-client buffered bytes and disconnecting slow clients that exceed the buffer limit (16MB). |
| FR-12 | Must | The system shall emit backpressure warning frames (12MB threshold) so clients can proactively shed low-priority updates before hitting the hard disconnect. |
| FR-13 | Must | The system shall handle directory-scoped session data separately from global session data, with distinct sync stores and update rules for each scope. |
| FR-14 | Should | The system shall support server-side event subscribers (e.g., OpenCode watcher) that share the same global hub as browser clients, avoiding duplicate upstream connections. |
| FR-15 | Should | The system shall heartbeat on the WebSocket path only while an upstream SSE stream is actively attached. |
| FR-16 | Should | The client shall preserve Zustand referential equality by returning the same object reference for state branches that an event did not mutate. |
| FR-17 | May | The system shall support a debug/trace mode for the client-side event pipeline to aid development and troubleshooting. |
| FR-18 | Must | The system shall maintain the replay buffer in-memory only; on server restart, all connected clients must perform a full bootstrap. |
| FR-19 | Should | The system shall encode all WebSocket payloads as JSON without binary frame support. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | The event pipeline shall handle 60+ events/sec during streaming without causing render cascades in unrelated UI components. |
| NFR-02 | Must | Reliability | Reconnecting clients shall recover missed events via the replay buffer without full page reload. |
| NFR-03 | Must | Performance | Targeted event cloning shall limit re-renders to only components subscribed to mutated state branches. |
| NFR-04 | Must | Availability | Background/offline tabs shall use long backoff (~60s) to avoid burning battery and server resources. |
| NFR-05 | Must | Security | WebSocket endpoints shall respect the same authentication as HTTP API routes. |
| NFR-06 | Should | Reliability | The replay buffer size shall be bounded (2048 events) to prevent unbounded memory growth. |
| NFR-07 | Should | Performance | Backpressure detection and client disconnect shall prevent a single slow client from degrading performance for others. |

## Constraints

- OpenCode upstream transport is SSE only; this cannot be changed from the OpenChamber side
- The Express server is the sole relay between OpenCode and the browser; browser clients never connect to OpenCode directly
- One active upstream SSE reader per global hub (shared across all global WS clients)
- One upstream SSE reader per directory-scoped WS connection

## Acceptance Criteria

- [ ] FR-01: Given a running server, a browser client connects to `/api/global/event/ws` and receives real-time global events
- [ ] FR-02: Given a directory-scoped WS connection to `/api/event/ws?directory=X`, the client receives events scoped to that directory
- [ ] FR-03: Given a client that disconnects and reconnects with a `Last-Event-ID`, the server replays buffered events since that ID
- [ ] FR-04: Given an upstream SSE stall (no data for 20s), the server reconnects upstream while keeping browser WS alive
- [ ] FR-05: Given two browser clients connected to the global hub, both receive the same event
- [ ] FR-06: Given the server is running, it emits synthetic events (`openchamber:session-status`, `openchamber:session-activity`, `openchamber:notification`, `openchamber:heartbeat`) to connected WS clients
- [ ] FR-07: Given a browser client, the pipeline attempts WebSocket first and falls back to SSE after timeout
- [ ] FR-08: Given a burst of 60 delta events in one second, the pipeline coalesces and batch-dispatches within flush frames
- [ ] FR-09: Given a `message.part.delta` event, only the `part` state branch is cloned; `session`, `permission`, `message` references are preserved
- [ ] FR-10: Given the browser tab is hidden, reconnect backoff uses the long cap (~60s); given the tab is visible, it uses the short cap (~5s)
- [ ] FR-11: Given a client whose buffered bytes exceed 16MB, the server closes the connection with code 1013
- [ ] FR-12: Given a client whose buffered bytes exceed 12MB, the server emits a backpressure warning frame before the hard disconnect at 16MB
- [ ] FR-13: Given two directories with active sessions, each directory's sync store is updated independently
- [ ] FR-14: Given a server-side event subscriber (e.g., OpenCode watcher), it receives events from the same global hub as browser clients without a separate upstream connection
- [ ] FR-15: Given a WebSocket client with no attached upstream SSE stream, no heartbeat is sent on that connection
- [ ] FR-16: Given a `message.part.delta` event, the client reducer returns the same object reference for state branches that were not mutated
- [ ] FR-17: Given debug mode is enabled, the event pipeline logs each event type, dispatch batch, and coalesce frame to the console
- [ ] FR-18: Given a server restart, all connected clients perform a full bootstrap and replay buffer events are lost
- [ ] FR-19: Given a WebSocket payload, it is JSON-encoded without binary frame support
- [ ] NFR-01: Given a stream of 60+ events per second, unrelated UI components do not re-render
- [ ] NFR-02: Given a disconnected client with a valid `Last-Event-ID`, the replay buffer delivers missed events without requiring a full page reload
- [ ] NFR-03: Given a `message.part.delta` event, the Zustand store clones only the `part` branch, preserving references to `session`, `message`, and `permission`
- [ ] NFR-04: Given a background tab or offline browser, the reconnect interval uses ~60s backoff; given a visible tab, it uses ~5s
- [ ] NFR-05: Given a WebSocket connection attempt without valid authentication, the server rejects the connection
- [ ] NFR-06: Given more than 2048 events in the replay buffer, the oldest events are evicted to stay within the limit
- [ ] NFR-07: Given a slow client with buffered bytes approaching 16MB, the server disconnects it without affecting other clients' performance

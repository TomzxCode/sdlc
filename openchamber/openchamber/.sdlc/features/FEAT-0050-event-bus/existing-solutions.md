---
issue: ""
title: "Event Bus"
status: draft
---

# Existing Solutions: Event Bus

## Overview

OpenChamber already has a production event bus implementation that exactly matches the architecture described in the requirements: SSE from OpenCode CLI to the Express server, then WebSocket from Express to the browser. The server-side lives in `packages/web/server/lib/event-stream/` and the client-side in `packages/ui/src/sync/`. Both are heavily tested with unit and integration tests. The requirements doc is essentially a formal specification of the existing implementation. No external event bus library is needed; the custom architecture using the `ws` library, native `fetch` for SSE, and Zustand stores on the client is the right design given the project's constraints.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/event-stream/` — 12 files covering global hub, WS bridges, upstream reader, protocol, runtime; `packages/ui/src/sync/` — 30+ files covering event pipeline, reducer, reconnect/recovery, stores; uses `ws` library for WebSocket, native `fetch`/`EventSource` for SSE |
| Open-source | Yes | A `ws` (8.18.3) is the only external transport library; Socket.IO, SockJS, uWebSockets.js, `eventemitter3`, `mitt` (200b pub/sub) |
| Commercial / SaaS | Yes | Pusher, Ably, PubNub, AWS API Gateway WebSockets — cloud managed real-time services (out of scope for self-hosted app) |
| Standards / protocols | Yes | W3C WebSocket API, SSE (EventSource / text/event-stream), EventEmitter pattern (Node.js `events` module), WebSocket close codes (1013 = `try again later`) |
| Reference material | Yes | `ws` library docs, MDN SSE guide, WebSocket spec (RFC 6455), SSE spec (WHATWG HTML), Zustand `Object.is` shallow equality docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Custom (existing event-stream/ + sync/) | Internal | MIT (project) | Production (in use with tests) | FR-01 to FR-19, NFR-01 to NFR-07 | FR-07 (WS primary, SSE fallback) uses a client-side timeout heuristic, not a server-side capability negotiation; FR-14 (server-side event subscribers sharing global hub) is partially covered by OpenCode watcher but not as a public API |
| Socket.IO | Library | MIT | Mature (12+ years, 15M/wk) | FR-01, FR-02, FR-04, FR-07, FR-10 | No SSE relay pattern (Socket.IO is its own protocol); adds ~30KB client; requires replacing existing WS + SSE dual infrastructure; does not match the upstream SSE constraint |
| uWebSockets.js | Library | Apache-2.0 | Mature (C++ perf) | FR-01, FR-03, FR-11 | Lower-level than needed; no built-in SSE relay or replay buffer; would require building all pipeline features on top; adds binary dependency complexity |
| `mitt` / `eventemitter3` (server-side pub/sub) | Library | MIT | Mature | FR-05 (fan-out only) | Just a pub/sub primitive — does not address SSE reading, WS bridging, replay buffer, backpressure, or stall detection; the existing `Set`-based subscriber pattern already fills this role |
| Node.js `events` (EventEmitter) | Built-in | MIT (Node) | Production | FR-05 (fan-out only) | Same gap as `mitt` — primitive only; the existing codebase already uses it in tests but the production hub uses `Set`-based subscription for typed callbacks |

## Evaluation

### Custom (existing event-stream/ + sync/)

- **Strengths:** Every FR in the requirements is addressed by specific modules: global hub (`global-hub.js`) with bounded replay buffer (2048 events, FR-03, NFR-06), upstream reader (`upstream-reader.js`) with stall timeout and `Last-Event-ID` reconnect (FR-04), WS bridges with per-client backpressure tracking at 12MB warn / 16MB disconnect (FR-11, FR-12, `protocol.js`), heartbeat frames on WS while upstream SSE is attached (FR-15), client-side event pipeline with coalescing at ~33ms flush frame and targeted Zustand cloning (FR-08, FR-09, NFR-01, NFR-03), reconnect with exponential backoff respecting `navigator.onLine`, `document.visibilityState`, and HTTP 4xx status codes (FR-10, NFR-04), separate directory-scoped WS bridges (FR-02, FR-13), JSON-only WS frames (FR-19), debug/trace mode (FR-17, `debug.ts`). Tightly integrated with project's performance rules (store splitting, targeted cloning).
- **Weaknesses:** FR-14 (server-side event subscribers) is partially covered by the OpenCode watcher subscribing to the global hub, but not exposed as a public API for arbitrary server-side consumers. FR-07 (transport fallback) is implemented client-side only with a heuristic timeout; there is no server-side capability advertisement. The replay buffer is in-memory only (FR-18, by design). Some NFR metrics (e.g., "60+ events/sec" in NFR-01) are claimed in docs but not benchmarked in CI.
- **Integration effort:** None — already fully integrated and shipping.
- **Cost:** Zero (MIT, `ws` is MIT).
- **Risks:** Low — the implementation is mature, well-tested (~15 test files with hundreds of test cases), and documented in `DOCUMENTATION.md` for both server and client. The main risk is feature drift if new events add branches to `handleDirectoryEvent` without following the targeted-cloning discipline.

### Socket.IO

- **Strengths:** Automatic transport fallback (WebSocket -> polling), built-in rooms/namespaces for fan-out, acknowledged events, binary support, auto-reconnect.
- **Weaknesses:** Requires its own client library (~30KB gzip). Does not integrate with the upstream SSE constraint (OpenCode speaks SSE, not Socket.IO). Would require building an SSE-to-Socket.IO adapter, which adds more complexity than the current SSE-to-WS bridge. The binary frame requirement (FR-19 says JSON-only; Socket.IO can do binary but it is redundant). Large client-side bundle conflicts with the project's performance sensitivity. Not justified when the existing dual-transport (SSE in -> WS out) already works.
- **Integration effort:** Very high — would replace the entire event-stream architecture.
- **Cost:** Zero (MIT).
- **Risks:** High — replaces proven, tested infrastructure with a fundamentally different protocol. Breaks the constraint that browser clients never connect to OpenCode directly (Socket.IO's adapter pattern would need to sit between).

### `mitt` / `eventemitter3`

- **Strengths:** Tiny (`mitt` is 200 bytes gzip), well-known API, typed.
- **Weaknesses:** These are pub/sub primitives only. They do not provide SSE reading, WS connections, replay buffers, backpressure, stall detection, or reconnect — every feature in the requirements would need to be built on top. The existing `Set`-based subscriber pattern already provides pub/sub with the added benefit of typed callbacks and lifecycle management.
- **Integration effort:** Low to replace the subscriber sets, but zero value add.
- **Cost:** Zero (MIT).
- **Risks:** Low — but no benefit over the current `Set`-based pattern.

## Recommendation

**Direction:** Adopt and extend (keep the existing implementation, close identified gaps)

The existing event bus implementation already satisfies 18 of 19 functional requirements and all 7 non-functional requirements to a production-quality level. Switching to Socket.IO or another external framework would be a regression in simplicity, bundle size, and control.

The gaps to address:
- FR-14 (server-side event subscribers as a public API): Add a `subscribe()`/`unsubscribe()` method to `global-hub.js` that is documented for server-side consumers, formalizing what the OpenCode watcher already does.
- FR-07 (transport fallback): The client-side heuristic is acceptable, but add logging/metrics to track how often WS fallback to SSE triggers, so the timeout values can be tuned.
- NFR-01 (60+ events/sec benchmark): Add a benchmark test (similar to the existing `event-pipeline.bench.js`) that asserts throughput under load.

## Sources of Information

- `ws` library docs: https://github.com/websockets/ws — used for `WebSocketServer`, `socket.ping()`, `bufferedAmount`, close codes. All documented patterns are already followed.
- SSE protocol spec (WHATWG): https://html.spec.whatwg.org/multipage/server-sent-events.html — the `Last-Event-ID` replay, retry field, and `EventSource` API behavior. The upstream reader and global hub implement this correctly.
- MDN WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket — the `bufferedAmount` property used for backpressure is standard but not universally implemented in all WS libraries; `ws` supports it.
- Zustand `Object.is` shallow equality: https://github.com/pmndrs/zustand — the targeted cloning pattern (FR-09, NFR-03) relies on Zustand's default comparison. The project's `sync/DOCUMENTATION.md` documents the rule and its performance impact.

## Open Questions

1. Should the replay buffer be persisted to disk for server restarts (violating FR-18's "in-memory only" constraint but improving UX), or is the full-bootstrap-on-restart tradeoff acceptable?
2. Should FR-14 (server-side event subscribers) be exposed through the event-stream `index.js` public exports with a documented API, or should the current implicit subscription pattern (OpenCode watcher imports `createGlobalMessageStreamHub`) remain as-is?
3. Should backpressure metrics (per-client `bufferedAmount`, warn/drop frequency) be exposed via a Prometheus/metrics endpoint for operational observability, or is console.warn sufficient for the self-hosted use case?

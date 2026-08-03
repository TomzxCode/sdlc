---
title: "Session Server"
status: done
---

# Specification: Session Server

## Overview

`pi-server` hosts the experimental `PiServer` session server.
A `PiServer` is constructed with a `PiSessionBackend` (session storage) and one or more listeners; `createUnixServer` wires a Unix socket transport.
Connections authenticate via the protocol `hello` token, then exchange request/response and event envelopes.
`LiveSessionManager` tracks active sessions and publishes snapshots.

## Architecture

```
+----------------------------+
|        PiServer            |
| - backend (PiSessionBackend)|
| - listeners                |
+------------+---------------+
             | accepts connections (e.g. Unix socket via createUnixServer)
             v
+------------+---------------+
|      connection.ts         |
| hello/auth, protocol.ts    |
+------------+---------------+
             |
             v
+------------+---------------+
|  LiveSessionManager        |
| sessions.ts, snapshots.ts  |
+----------------------------+
```

`server.ts` is the entry point; `listener.ts` defines listeners; `transports/unix/` the Unix transport; `sessions.ts`/`snapshots.ts` live-session and snapshot management; `testing/` in-memory server/client helpers.

## Data Models

### PiSessionBackend

| Method | Signature | Description |
|---|---|---|
| listSessions | `() => Promise<SessionSummary[]>` | List known sessions |
| listModels | `() => Promise<ModelInfo[]>` | List available models |
| createSession | `(options) => Promise<Session>` | Create and open a session |
| openSession | `(sessionId) => Promise<Session>` | Open an existing session |

## API Contracts

### `createUnixServer(backend, options)`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| backend | PiSessionBackend | yes | Session storage adapter |
| options.token | string | yes | Bearer token |
| options.path | string | yes | Unix socket path |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| server | PiServer | Started server instance |

## Sequences

### Client connect

```
Client → createUnixServer → server.start()
Client connects (Unix socket)
Client → hello {version, token} → server validates → session established
Client → createSession/openSession → LiveSessionManager → snapshots → client
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Auth | bearer token in `hello` | Reuses protocol handshake, no extra round trips |
| Session management | `LiveSessionManager` | Single owner of live session lifecycle |
| Snapshot publication | server + session snapshots | Clients render from authoritative state |
| Backend abstraction | `PiSessionBackend` | Decouples transport from session storage |
| Package layout | new `PiServer` + `legacy/` supervisor | Additive migration; legacy CLI kept |

## Risks and Unknowns

1. Experimental; the API may change or be removed without notice.
2. Only a Unix socket preset ships; other transports are future work.
3. Relationship to the legacy supervisor is transitional.

## Out of Scope

- The wire protocol (`pi-protocol`).
- The client (`pi-client`).
- SQLite session persistence (separate feature in `pi-storage-sqlite-node`).

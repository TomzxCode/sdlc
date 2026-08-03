---
title: "Remote Session Client"
status: done
---

# Specification: Remote Session Client

## Overview

`pi-client` is the transport-neutral remote-session client.
`PiClient` connects through a `ByteTransportFactory`, authenticates via the protocol `hello` handshake, and exchanges request/response envelopes with the server.
Session access is mediated by `SessionLease` objects with exclusive/shared ownership semantics.

## Architecture

```
+----------------------+
|      PiClient        |
| - connect()          |
| - createSession()    |
| - attachSession()    |
| - acquireSession()   |
| - listSessions()     |
| - reconnect()        |
+---------+------------+
          | ByteTransportFactory (one fresh transport per attempt)
          v
+----------------------+
|     ByteTransport    |
| send(chunk), close() |
| onData/onClose/onErr |
+----------------------+
```

`connection.ts` owns transport lifecycle, `state.ts` the connection/session state machine, `session-handle.ts` the lease model, `promise.ts` request correlation, and `client.ts` the public `PiClient` API.

## Data Models

### SessionLease

| Field | Type | Constraints | Description |
|---|---|---|---|
| mode | `"exclusive" \| "shared"` | not null | Ownership mode |
| session | session handle | not null | Underlying remote session |
| release | function | — | Releases the lease |

Leases cannot be constructed directly; they come from `createSession()` (exclusive) or `acquireSession()`/`attachSession()`.

## API Contracts

### `client.createSession({ cwd })`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| cwd | string | yes | Working directory for the session |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| lease | SessionLease | New exclusive lease for the created session |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 409 | SESSION_OWNERSHIP | Ownership conflict during acquisition |

### `client.acquireSession({ mode })`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| mode | "exclusive" \| "shared" | yes | Desired lease mode |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| lease | SessionLease | Lease in the requested mode |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 409 | SESSION_OWNERSHIP | Exclusive requested while a lease exists, or shared while exclusive held |

## Sequences

### Session create flow

```
PiClient → encodeClientMessage(create_session) → server
server → session created → response snapshot
PiClient → SessionLease (exclusive) → caller
```

### Ownership enforcement

```
caller acquires exclusive (ok)
caller attempts shared   → PiSessionOwnershipError
caller releases exclusive
caller acquires shared   (ok)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Transport abstraction | `ByteTransportFactory` | Fresh transport per attempt; keeps client Node-agnostic |
| Ownership | `SessionLease` exclusive/shared | Guards mutation vs. observation; single coordinator |
| Request correlation | per-request ID + promises | Correct handling of out-of-order responses |
| Snapshot model | authoritative snapshots, transient progress | No optimistic mutation of authoritative state |

## Risks and Unknowns

1. No automatic reconnect; long-lived connections must manage `reconnect()` explicitly.
2. Experimental API may change without notice.

## Out of Scope

- The wire protocol (`pi-protocol`).
- The server (`pi-server`).
- Concrete transports beyond the `ByteTransport` contract.

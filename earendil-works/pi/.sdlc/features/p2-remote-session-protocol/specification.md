---
title: "Remote Session Protocol"
status: done
---

# Specification: Remote Session Protocol

## Overview

`pi-protocol` is the wire boundary for remote pi sessions.
Messages are schema-validated objects encoded as a single definite-length CBOR item and framed with a four-byte big-endian length prefix.
The package ships a self-contained CBOR encoder/decoder, incremental decoders tolerant of arbitrary fragmentation, and a validated message API (`encodeClientMessage`/`encodeServerMessage`).

## Architecture

```
Client messages            Server messages
+----------------+         +----------------+
| hello (v2)     |         | session events |
| request/       |<------->| server events  |
| response env.  | framed   | response env.  |
+--------+-------+ CBOR     +--------+-------+
         |                           |
         v                           v
  length-prefixed framed bytes  incremental decoders
```

The protocol is runtime-neutral: no Node-specific imports.
`framing.ts` owns the length-prefix layout; `cbor/` owns encode/decode; `schemas.ts` owns the message definitions; `codec.ts` ties validation + framing into the message API.

## Data Models

### ClientHello

| Field | Type | Constraints | Description |
|---|---|---|---|
| type | string | `"hello"` | Message discriminator |
| version | number | `PROTOCOL_VERSION` | Protocol version |
| token | string | not null | Bearer token for authentication |

### Framed message

| Field | Type | Constraints | Description |
|---|---|---|---|
| length | uint32 | big-endian | Byte length of the CBOR payload |
| payload | CBOR | definite-length | One schema-validated message |

## API Contracts

### `encodeClientMessage(message)`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| message | ClientMessage | yes | Message to validate and frame |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| Uint8Array | framed bytes | Complete framed message ready to send |

### `createServerMessageDecoder()`

**Request**

None; incremental state is held in the returned decoder.

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| decoder | object | Accepts arbitrary chunks and emits decoded messages |

## Sequences

### Hello handshake

```
Client → encodeClientMessage(hello) → transport
Server → decoder → validate hello (version + token) → accept connection
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Payload format | CBOR | Compact, schema-validated, binary-safe |
| Framing | 4-byte BE length prefix | Cheap incremental parsing, exact boundaries |
| CBOR implementation | Self-contained encoder/decoder | No runtime dependency, full control |
| Message validation | typebox schemas | Shared schema + validate pipeline |
| Versioning | `PROTOCOL_VERSION` constant | Single source of truth for wire compatibility |

## Risks and Unknowns

1. Experimental protocol surface may change; consumers must pin the package.
2. Snapshot-authoritative semantics depend on server cooperation; progress events must never be reduced into authoritative state.

## Out of Scope

- The client implementation itself (`pi-client`).
- The server implementation (`pi-server`).
- Transport plumbing (sockets, WebSocket adapters) beyond the framing/decoder layer.

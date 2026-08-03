---
title: "Remote Session Protocol"
status: done
---

# Requirements: Remote Session Protocol

## Overview

`@earendil-works/pi-protocol` defines a runtime-neutral wire protocol for remote pi sessions.
It provides schemas, types, CBOR encoding/decoding, and byte-stream framing so that a client and a server can exchange messages over any ordered byte transport.
The protocol is versioned (currently `2`) and message-correlated (request/response envelopes plus server event envelopes), with authoritative server/session snapshots and transient progress events.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Remote session client (`pi-client`) | A validated, framed message API plus incremental decoders that tolerate arbitrary fragmentation or coalescing |
| Session server (`pi-server`) | Matching encode/decode on the server side with an authoritative snapshot model |
| Transport authors | A wire format that is transport-agnostic (streams, sockets, custom byte transports) |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall define runtime-neutral schemas and types for all protocol messages (client and server). |
| FR-02 | Must | The system shall encode messages as one definite-length CBOR item framed by a four-byte unsigned big-endian payload length. |
| FR-03 | Must | The system shall provide `encodeClientMessage()` and `encodeServerMessage()` that validate a message and return a complete framed `Uint8Array`. |
| FR-04 | Must | The system shall provide incremental decoders that accept arbitrary fragmentation or coalescing of framed bytes. |
| FR-05 | Must | The system shall require the first client message to be `hello`, carrying `PROTOCOL_VERSION` and a bearer token. |
| FR-06 | Must | The system shall correlate subsequent messages by request/response envelopes and server event envelopes. |
| FR-07 | Must | The system shall expose a version constant (`PROTOCOL_VERSION`) used by both client and server. |
| FR-08 | Should | The system shall treat server and session snapshots as authoritative, and progress events as transient UI hints. |
| FR-09 | Should | The system shall ship a self-contained CBOR encoder/decoder (no external CBOR dependency). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Compatibility | The protocol shall be versioned so incompatible wire changes bump `PROTOCOL_VERSION`. |
| NFR-02 | Must | Security | The `hello` handshake shall carry a bearer token before any session operations are allowed. |
| NFR-03 | Should | Performance | Framing shall use a fixed-length length prefix for cheap incremental parsing. |
| NFR-04 | Should | Portability | The package shall be runtime-neutral with no Node-specific imports. |

## Constraints

- Depends on `typebox` for schema definitions.
- Protocol version `2` is the current wire layout; version `1` is not preserved.
- Experimental; the message surface may change without notice.

## Acceptance Criteria

- [ ] **FR-02**
    - **Given** a protocol message
    - **When** encoded to bytes
    - **Then** the result is a four-byte big-endian length prefix followed by one definite-length CBOR item.
- [ ] **FR-04**
    - **Given** a framed byte stream delivered in arbitrary chunk boundaries
    - **When** fed to the incremental decoder
    - **Then** the original messages are recovered exactly.
- [ ] **FR-05**
    - **Given** a client that has not sent `hello`
    - **When** it sends a session operation
    - **Then** the server rejects the message until a valid `hello` with a matching token is received.
- [ ] **NFR-04**
    - **Given** the package source
    - **When** scanned for Node imports
    - **Then** none are present.

## Conflicts

None identified yet.

## Open Questions

1. Should the protocol expose a negotiation mechanism for future wire-version migration beyond bumping `PROTOCOL_VERSION`?

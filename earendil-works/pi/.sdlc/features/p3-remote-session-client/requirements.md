---
title: "Remote Session Client"
status: done
---

# Requirements: Remote Session Client

## Overview

`@earendil-works/pi-client` is a transport-neutral client for remote pi sessions.
`PiClient` exchanges length-prefixed CBOR messages through a small `ByteTransport` interface, so it works over Unix sockets, WebSockets, or any ordered byte transport without Node-specific imports.
It provides session acquisition with exclusive/shared leases, session creation/attachment, snapshot subscriptions, and request correlation by ID.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Coding agent (`pi-coding-agent`) | Attach to remote pi sessions (create, resume, subscribe) from the CLI |
| Server operators | A client that authenticates with a bearer token and honors exclusive/shared session ownership |
| Transport authors | A minimal `ByteTransport` contract that is easy to implement |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a `PiClient` that connects to a server via a `ByteTransportFactory` and authenticates with a bearer token. |
| FR-02 | Must | The system shall support creating a session (`createSession({ cwd })`) and returning a new session lease. |
| FR-03 | Must | The system shall support attaching to an existing session (`attachSession()`) as a shared acquisition. |
| FR-04 | Must | The system shall support acquiring sessions with explicit lease modes: `{ mode: "exclusive" }` or `{ mode: "shared" }`. |
| FR-05 | Must | The system shall enforce ownership: exclusive acquisition fails while any lease exists; shared acquisition fails while an exclusive lease exists. |
| FR-06 | Must | The system shall correlate requests by ID and deliver responses to the right caller. |
| FR-07 | Must | The system shall publish session snapshots to subscribers and list sessions (`listSessions()`). |
| FR-08 | Should | The system shall support `reconnect()` after disconnection (no automatic reconnect). |
| FR-09 | Should | The system shall expose cached session summaries from the latest snapshot. |
| FR-10 | Should | The system shall drive a session with `session.prompt(...)` and stream events to subscribers. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Portability | The package shall have no Node-specific imports; all byte movement goes through `ByteTransport`. |
| NFR-02 | Must | Correctness | A transport factory must create a fresh transport for every connection attempt. |
| NFR-03 | Must | Security | The client shall send the bearer token only through the `hello` handshake. |
| NFR-04 | Should | Reliability | On transport close/error the client shall surface the failure to callers and support explicit reconnect. |

## Constraints

- No automatic reconnect; callers must call `reconnect()`.
- One connection can attach several sessions.
- Experimental; API may change without notice.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a `PiClient` with a token and transport factory
    - **When** `connect()` is called
    - **Then** the client authenticates via `hello` and becomes ready.
- [ ] **FR-04**
    - **Given** a session with no active leases
    - **When** an exclusive acquisition is requested
    - **Then** an exclusive lease is returned and shared acquisitions now fail.
- [ ] **FR-05**
    - **Given** an exclusive lease already held
    - **When** a second exclusive acquisition is requested
    - **Then** `PiSessionOwnershipError` is thrown.
- [ ] **FR-06**
    - **Given** multiple in-flight requests
    - **When** responses arrive out of order
    - **Then** each caller receives the response matching its request ID.
- [ ] **NFR-01**
    - **Given** the package source
    - **When** scanned for Node imports
    - **Then** none are present.

## Conflicts

None identified yet.

## Open Questions

1. Should automatic reconnect with backoff be added, or does explicit `reconnect()` suffice?

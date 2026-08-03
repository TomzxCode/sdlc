---
title: "Session Server"
status: done
---

# Requirements: Session Server

## Overview

`@earendil-works/pi-server` provides the experimental `PiServer` session server for remote pi sessions.
It is token-authenticated, listens on listeners (including a `createUnixServer` preset), manages live sessions via `LiveSessionManager`, publishes server and session snapshots, and ships a `testing` harness for building servers/clients in tests.
The legacy child-process supervisor (`server` CLI) coexists in the same package under `legacy/`.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Remote session users | Host a pi session server that accepts authenticated clients over Unix sockets |
| Coding agent (`pi-coding-agent`) | A server-side counterpart to `PiClient` for remote sessions |
| Test authors | A `testing` harness for driving server/client pairs in tests |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a `PiServer` class that serves authenticated remote sessions over listeners. |
| FR-02 | Must | The system shall require a bearer token before accepting session operations (validated in the `hello` handshake). |
| FR-03 | Must | The system shall support a Unix socket transport preset (`createUnixServer`) with a configurable socket path. |
| FR-04 | Must | The system shall manage live sessions through a `LiveSessionManager`. |
| FR-05 | Must | The system shall publish authoritative server snapshots and session snapshots to connected clients. |
| FR-06 | Must | The system shall route client requests (create/open/list sessions, prompt, subscribe) through the protocol. |
| FR-07 | Should | The system shall expose a `PiSessionBackend` interface decoupling the server from concrete session storage. |
| FR-08 | Should | The system shall ship a `testing` entrypoint with in-memory server/client helpers for tests. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Access shall require the configured bearer token; no anonymous sessions. |
| NFR-02 | Must | Reliability | The server shall remain functional across client connect/disconnect cycles. |
| NFR-03 | Should | Compatibility | The `legacy` supervisor CLI and exports shall remain available while the new server is additive. |
| NFR-04 | Should | Maintainability | Server behavior shall be covered by a conformance suite plus per-component tests. |

## Constraints

- Experimental; APIs may change or be removed without notice.
- Unix socket transport only for the built-in preset.
- Same package hosts both the new `PiServer` and the legacy supervisor (`server` CLI).

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a `PiServer` with a backend and a Unix listener
    - **When** started
    - **Then** it accepts connections on the configured socket path.
- [ ] **FR-02**
    - **Given** a connection without a valid token
    - **When** it sends a session operation
    - **Then** the server rejects it.
- [ ] **FR-05**
    - **Given** connected clients and a live session
    - **When** session state changes
    - **Then** authoritative snapshots are published to subscribers.
- [ ] **NFR-01**
    - **Given** no configured token client
    - **When** connecting
    - **Then** the handshake fails.

## Conflicts

None identified yet.

## Open Questions

1. Will the legacy supervisor eventually be removed in favor of `PiServer` alone?

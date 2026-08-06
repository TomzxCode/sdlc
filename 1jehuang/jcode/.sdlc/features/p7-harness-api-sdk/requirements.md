---
title: "Harness API and SDKs"
status: done
---

# Requirements: Harness API and SDKs

## Overview

The harness API exposes jcode's agent runtime to external programs through a stable, versioned client API. A Unix-socket bridge (`jcode api-bridge`) translates versioned API requests onto the internal protocol, and Rust and TypeScript SDKs let applications launch jcode, drive sessions, and stream events. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Application developers | A stable API to embed or script the jcode agent runtime |
| Maintainer | A versioned API surface that can evolve without breaking SDK clients |
| Desktop/iOS app teams | Consume sessions and events through the harness API |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall expose a stable, versioned harness API for launching jcode, driving sessions, and streaming events. |
| FR-2 | Must | The system shall serve the API through a Unix-socket bridge (`jcode api-bridge`) built into the released binary. |
| FR-3 | Must | The system shall provide a Rust SDK (`jcode-sdk`) for the harness API. |
| FR-4 | Must | The system shall provide a TypeScript SDK (`@1jehuang/jcode-sdk`) published to npm. |
| FR-5 | Must | The system shall ship platform launcher packages that let SDK clients launch jcode without a Rust toolchain. |
| FR-6 | Should | The system shall keep SDK and API behavior consistent (schema parity) between Rust and TypeScript clients. |
| FR-7 | Should | The system shall expose session control (start, send message, cancel) and structured events. |
| FR-8 | May | The system shall expose capability coverage and schema snapshots for client-server negotiation. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Compatibility | The API shall be versioned so breaking changes do not silently break existing clients. |
| NFR-2 | Must | Usability | SDK clients must not need a Rust toolchain to use the API. |
| NFR-3 | Should | Performance | Event streaming over the bridge shall be low-overhead (Unix socket framing). |

## Constraints

- The bridge is Unix-only (listens on a Unix socket); Windows uses the pipe transport behind the same API.
- The bridge ships inside the released binary as `jcode api-bridge`.

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** a running `jcode api-bridge`
    - **When** a client opens a session and sends a message
    - **Then** events stream back to the client
- [ ] **FR-2**
    - **Given** the released binary
    - **When** the user runs `jcode api-bridge`
    - **Then** the bridge listens and serves versioned API clients
- [ ] **FR-3**
    - **Given** the Rust SDK
    - **When** a client drives a session
    - **Then** it connects and receives events
- [ ] **FR-4**
    - **Given** the TypeScript SDK package
    - **When** installed from npm and used
    - **Then** it drives sessions against a live bridge
- [ ] **FR-5**
    - **Given** an SDK client on a supported platform
    - **When** it launches jcode
    - **Then** the platform launcher binary is used, no toolchain required
- [ ] **FR-6**
    - **Given** Rust and TypeScript SDKs
    - **When** schema parity tests run
    - **Then** both clients agree on types and behaviors
- [ ] **FR-7**
    - **Given** an active session via the API
    - **When** the client cancels
    - **Then** the cancel is honored
- [ ] **FR-8**
    - **Given** a client and server
    - **When** they negotiate capabilities
    - **Then** incompatible surfaces are detected via schema snapshots
- [ ] **NFR-1**
    - **Given** a versioned API
    - **When** a breaking change is introduced
    - **Then** the version is bumped and old clients are not silently broken
- [ ] **NFR-2**
    - **Given** a machine without a Rust toolchain
    - **When** an SDK client runs
    - **Then** it works using the released binary bridge
- [ ] **NFR-3**
    - **Given** a streaming session
    - **When** events flow over the socket
    - **Then** latency stays low with framed messages

## Conflicts

None identified yet.

## Open Questions

1. Which API version is currently current, and what is the deprecation policy for older versions? Versioning exists but the policy is inferred from code.

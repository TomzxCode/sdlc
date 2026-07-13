---
title: "Gateway Server"
status: done
---

# Requirements: Gateway Server

## Overview

The Gateway Server is the core HTTP/WebSocket server that handles authentication, session lifecycle, API endpoints, and message routing between channels and the agent runtime. It is the primary control plane that users and channel plugins connect to.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Reliable, always-available gateway for messaging their assistant |
| Plugin developers | Stable API surface for channel and node integrations |
| Operators | Manageable startup, shutdown, health monitoring, and configuration reload |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The gateway shall serve HTTP and WebSocket endpoints for client and channel communication |
| FR-2 | Must | The gateway shall authenticate requests using bearer tokens, device pairing, or pre-auth tokens |
| FR-3 | Must | The gateway shall manage agent sessions (create, list, read, update, delete, reset) |
| FR-4 | Must | The gateway shall support hot-reload of configuration without full restart |
| FR-5 | Must | The gateway shall expose a health check endpoint |
| FR-6 | Must | The gateway shall support graceful shutdown with active session drain |
| FR-7 | Must | The gateway shall enforce rate limiting on auth endpoints |
| FR-8 | Should | The gateway shall support node pairing for external agent runtime hosts |
| FR-9 | Should | The gateway shall broadcast server state changes to connected clients |
| FR-10 | May | The gateway shall support plugin-provided HTTP endpoints |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Availability | The gateway shall recover from crashes with minimal session data loss |
| NFR-2 | Must | Security | The gateway shall not expose secrets or credentials in logs or error messages |
| NFR-3 | Should | Performance | The gateway shall handle concurrent channel connections without significant latency degradation |

## Constraints

- Single-user architecture: no multi-tenant isolation required
- Must run on Node.js 22.19+ (Node 24 recommended)
- Must support self-hosted deployment (bare metal, Docker, fly.io)

## Acceptance Criteria

- [ ] **FR-1**: Given a running gateway, when a client connects via WebSocket, then the connection is established and messages can be exchanged
- [ ] **FR-2**: Given a request with an invalid token, when it reaches the gateway, then it is rejected with 401
- [ ] **FR-3**: Given a session create request, when the gateway processes it, then a new session is created and persisted
- [ ] **FR-4**: Given a running gateway, when the config file changes, then the gateway detects and applies the changes without restart
- [ ] **FR-5**: Given a health check request, when the gateway responds, then it returns 200 with status information
- [ ] **FR-6**: Given a shutdown signal, when the gateway receives it, then it drains active sessions before exiting
- [ ] **NFR-1**: Given a gateway crash, when it restarts, then existing sessions are recoverable from persistent storage
- [ ] **NFR-2**: Given an error response, when inspected, then no API keys or credentials are present in the response body

## Conflicts

None identified yet.

## Open Questions

1. What is the target maximum number of concurrent WebSocket connections?

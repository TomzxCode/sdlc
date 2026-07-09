---
title: "Gateway Server"
status: draft
---

# Specification: Gateway Server

## Overview

The Gateway Server is built on Hono (a lightweight HTTP framework) with WebSocket support. It uses a plugin-based architecture for method handlers and middleware. Auth uses bearer tokens, device-pairing handshake, or pre-configured bootstrap tokens. Session state is persisted to SQLite via Kysely.

## Architecture

```
HTTP/WS Clients → Hono Router → Auth Middleware → Method Dispatch
                                                      │
                                          ┌───────────┴───────────┐
                                          ▼                       ▼
                                    Session Methods          Plugin Methods
                                          │                       │
                                          ▼                       ▼
                                    SQLite Store            Plugin Registry
```

## Data Models

### Session

| Field | Type | Constraints | Description |
|---|---|---|---|
| sessionId | string | PK | Unique session identifier |
| agentId | string | not null | The agent this session belongs to |
| createdAt | timestamp | not null | Session creation time |
| updatedAt | timestamp | not null | Last activity time |
| metadata | JSON | nullable | Session metadata |
| state | string | not null | Session lifecycle state |

## API Contracts

### POST /api/sessions

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| agentId | string | yes | Target agent ID |
| channelId | string | yes | Originating channel |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| sessionId | string | Created session ID |
| token | string | Session access token |

### GET /health

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| status | string | `ok` or `degraded` |
| uptime | number | Server uptime in seconds |

## Sequences

### Session Creation Flow

```
Client → Gateway: POST /api/sessions { agentId, channelId }
Gateway → Auth: validate bearer token
Gateway → Store: INSERT session
Gateway → Client: { sessionId, token }
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| HTTP framework | Hono | Lightweight, fast, good WebSocket support, TypeScript-native |
| Auth model | Bearer token + device pairing | Simple for single-user, extends to node pairing |
| State storage | SQLite via Kysely | Durable, no external DB dependency, good query capabilities |
| Config reload | File watcher + hot-reload | Zero-downtime config updates without process restart |

## Risks and Unknowns

1. WebSocket scaling with many concurrent connections needs benchmarking
2. Plugin-provided HTTP endpoints may have security implications for auth enforcement

## Out of Scope

- Multi-tenant/multi-user support
- Horizontal scaling / load balancing
- External database support (PostgreSQL, etc.)

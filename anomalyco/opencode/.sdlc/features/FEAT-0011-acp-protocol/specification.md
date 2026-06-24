---
title: "Agent Client Protocol (ACP)"
status: draft
---

# Specification: Agent Client Protocol (ACP)

## Architecture

```
External Agent / Automation ──ACP──▶ ACP Handler (packages/opencode/src/acp/)
                                         │
                                         ▼
                                   Session Runtime (FEAT-0001)
                                   Tool Registry (FEAT-0002)
                                   Provider Layer (FEAT-0003)
```

ACP handlers translate ACP protocol operations into internal runtime calls, providing a structured interface for external agents.

## Data Models

### AcpAgent

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Agent identity |
| name | text | not null | Display name |
| capabilities | array | not null | Supported operations |

### AcpSession

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Session identity |
| status | enum | not null | active, paused, completed, aborted |

## API Contracts

The ACP module exposes Effect-based handlers for each operation domain.
Wire protocol is JSON over stdin/stdout or TCP (matching MCP transport patterns).

### Agent operations

List, get, describe, delete agents.

### Session operations

Start session, send message (streaming), list sessions, get session details, abort session.

### Tool operations

Discover tools, invoke tools, get tool status.

### Event operations

Subscribe to session events, stream events.

## Sequences

### Drive a session via ACP

```
ACP Client -> agent:list -> ACP handler -> agent list
ACP Client -> session:start -> handler -> new session
ACP Client -> session:send -> handler -> stream response
ACP Client -> session:events -> handler -> event stream (tool calls, completion)
ACP Client -> session:abort -> handler -> session aborted
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Transport | JSON over stdio/TCP (same as MCP) | Familiar pattern; easy to integrate |
| Separation | ACP lives in its own module independent from MCP | Avoids conflating agent control with context protocol |
| Session binding | ACP sessions map to internal Session IDs | Reuses existing durable session infrastructure |

## Risks and Unknowns

1. ACP is a newer protocol with limited adoption; API stability is not guaranteed.
2. Permission model for external agents needs careful design to prevent privilege escalation.

## Out of Scope

- MCP implementation and servers (see FEAT-0008).
- HTTP API surface for ACP (goes through the existing server if at all).

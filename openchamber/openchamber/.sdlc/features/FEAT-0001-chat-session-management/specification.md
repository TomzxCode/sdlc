---
title: "Chat & Session Management"
status: draft
---

# Specification: Chat & Session Management

## Overview

The chat system uses a Zustand-based state architecture with SSE-driven event pipeline for real-time streaming. Sessions are persisted by the OpenCode server and synced to the UI via bootstrap + incremental SSE events. The shared UI components in `packages/ui/src/components/chat/` render messages, tool output, and timeline controls.

## Architecture

```
User Input
    |
    v
ChatInput component (packages/ui/src/components/chat/)
    |
    v  HTTP POST
Express Server (packages/web/server/index.js)
    |
    v  SDK call
OpenCode Server (external)
    |
    v  SSE stream
Event Pipeline (packages/ui/src/sync/event-pipeline.ts)
    |
    v  dispatch
Zustand Stores (packages/ui/src/stores/)
    |
    v  React re-render
ChatMessage components (packages/ui/src/components/chat/message/)
```

## Data Models

### Session

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Unique session identifier |
| title | string | nullable | Display title |
| createdAt | timestamp | not null | Creation time |
| directory | string | not null | Working directory |
| parentId | string | nullable | Parent session for forks/sub-sessions |
| archivedAt | timestamp | nullable | Archive time |
| status | enum | not null | active, idle, streaming, error |

### Message

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Unique message identifier |
| sessionId | string | FK | Parent session |
| role | enum | not null | user, assistant, system |
| parts | MessagePart[] | not null | Ordered content parts |
| finishReason | enum | nullable | end_turn, tool_call, error |
| createdAt | timestamp | not null | Timestamp |

### MessagePart

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Part identifier |
| type | enum | not null | text, tool_call, tool_result, thinking |
| delta | string | nullable | Streaming text content |
| metadata | object | nullable | Tool call details, diff stats, etc. |

## API Contracts

### POST /api/sessions/:sessionId/prompt

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| content | string | yes | User message text |
| messageID | string | no | Client-generated ID for optimistic rendering |
| attachments | string[] | no | File URLs to attach |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| messageId | string | Server-assigned message ID |
| sessionId | string | Session ID |

### GET /api/sessions/:sessionId/events

SSE stream. Events include `message.part.delta`, `message.part.updated`, `session.status`, `permission.request`.

## Sequences

### Send message and stream response

```
User types message -> ChatInput -> POST /prompt -> Express -> OpenCode SDK
                                                            |
SSE: message.part.delta (x60/sec) <- Event Pipeline <- OpenCode SSE
       |
       v
  Zustand store update -> React re-render (memoized ChatMessage)
```

### Fork from earlier turn

```
User clicks fork on turn N -> POST /api/sessions/:id/fork with afterMessageID
       |
       v
Server creates new session with messages[0..N] -> SSE event: session.created
       |
       v
UI adds new session to store, navigates to it
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| State management | Zustand with split stores | Avoids render cascades from high-frequency streaming events |
| Transport | SSE (primary), WebSocket (terminal only) | SSE is simpler for unidirectional event streaming; WebSocket adds complexity without benefit for chat |
| Virtualization | @tanstack/react-virtual | Handles large message lists without DOM bloat |
| Optimistic updates | Shadow Map pattern with client-generated IDs | Enables instant UI while preventing duplicates on server echo |
| Message parts | Array of typed parts per message | Supports mixed content (text + tool calls + thinking) in a single message |

## Risks and Unknowns

1. Very large sessions (1000+ messages) may still cause performance issues despite virtualization
2. Concurrent edits to the same session from multiple tabs/devices are not explicitly handled

## Out of Scope

- Collaborative multi-user sessions
- End-to-end encryption of message content

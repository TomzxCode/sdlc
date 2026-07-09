---
title: "Channel Integration"
status: draft
---

# Specification: Channel Integration

## Overview

Each channel is a self-contained plugin under `extensions/<channel-name>/` that implements the channel contract. The channel system in `src/channels/` provides the shared runtime: inbound event handling, draft streaming, typing indicators, session binding, and message access control.

## Architecture

```
Channel Plugin (WhatsApp, Telegram, etc.)
       │
       ▼
src/channels/ (shared channel runtime)
  ├── inbound-event/    → inbound message processing
  ├── message/          → message formatting and delivery
  ├── status/           → status reactions
  ├── transport/        → transport abstractions
  └── turn/             → turn lifecycle management
       │
       ▼
Gateway Server → Agent Runtime
```

## Data Models

### ChannelMessage

| Field | Type | Constraints | Description |
|---|---|---|---|
| messageId | string | PK | Platform message ID |
| channelId | string | not null | Channel identifier |
| sessionId | string | FK, not null | Bound session |
| text | string | nullable | Message text content |
| attachments | JSON | nullable | File/image attachments |
| timestamp | timestamp | not null | Message timestamp |

## Sequences

### Message Receive Flow

```
Platform → Channel Plugin: webhook/poll
Channel Plugin → Channel Runtime: normalized envelope
Channel Runtime → Gateway: route to agent session
Agent → Channel Runtime: response with text + attachments
Channel Runtime → Channel Plugin: formatted response
Channel Plugin → Platform: send message
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Plugin contract | Channel SDK interface in `@openclaw/plugin-sdk` | Consistent integration seam for all channels |
| Streaming | Chunked draft delivery via draft-stream-loop | Responsive UX; channels display text incrementally |
| Thread binding | Session-to-thread ID mapping | Recovery and continuity across gateway restarts |
| Attachment handling | Managed media pipeline | Consistent upload/download across heterogeneous platforms |

## Risks and Unknowns

1. Each platform has unique rate limits and API quirks that require per-channel handling
2. Webhook vs polling delivery models affect reliability and resource usage
3. Platform API deprecations can break channels without warning

## Out of Scope

- Building a new universal messaging protocol
- Cross-channel message synchronization
- Archiving platform-specific message history beyond transcript storage

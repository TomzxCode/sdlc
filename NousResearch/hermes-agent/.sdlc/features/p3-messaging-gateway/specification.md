---
title: "Messaging Gateway"
status: draft
---

# Specification: Messaging Gateway

## Overview

The gateway is an asyncio-based Python service that loads platform adapters, manages their lifecycle, and routes messages to and from the synchronous AIAgent. The architecture uses a base adapter class that each platform extends, with common functionality (session management, slash command dispatch, approval flow) in the gateway runner.

## Architecture

```
Gateway runner (gateway/run.py)
    │
    ├── PlatformManager (start/stop/lifecycle)
    ├── SessionManager (session create/switch/list/resume)
    ├── SlashDispatcher (commands bypassing agent)
    ├── ApprovalFlow (prompt/inline + approve/deny)
    └── StreamDispatcher (real-time streaming)
         │
         ├── TelegramAdapter
         ├── DiscordAdapter
         ├── SlackAdapter
         ├── WhatsAppAdapter
         ├── SignalAdapter
         ├── ... (20+ adapters)
         └── API Server Adapter
```

## Data Models

No custom data models beyond standard messaging types (message ID, chat ID, user ID, text content). Sessions are tracked via session_key derived from platform + chat/user ID.

## API Contracts

The gateway does not expose external HTTP APIs (except the API server adapter, which provides an OpenAI-compatible HTTP endpoint). Communication between adapters and the gateway runner is in-process method calls.

## Sequences

### Message processing flow
```
Platform → Adapter receives message
    │
    ├── pre-processing (rate limiting, identity check)
    │
    ├── known command? ──→ SlashDispatcher ──→ handler
    │
    └── agent message ──→ SessionManager
                │
                └── AIAgent.run_conversation()
                        │
                        └── Response → Adapter → Platform message
```

### Approval flow
```
Agent → Dangerous action detected
    → ApprovalFlow → Adapter → User (inline buttons)
    → User approves/denies
    → ApprovalFlow → Agent (approve) or abort (deny)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | asyncio | Allows concurrent handling of multiple platforms while maintaining sequential processing per session |
| Base adapter | ABC in gateway/platforms/base.py | Shared session/approval/command logic; minimal per-adapter code |
| Platform lifecycle | Explicit start/stop/disconnect | Token locks prevent credential reuse across profiles |
| Rate limiting | Per-platform config | Each platform has different API limits and we respect them individually |

## Risks and Unknowns

1. Adapter count is ~25 and growing — maintenance burden increases with each new platform
2. Session lifecycle across restarts and scale-to-zero transitions can lose in-flight messages
3. Approval flow requires tight coupling between the platform adapter and the gateway runner's interruption mechanism

## Out of Scope

- Webhook adapter (for incoming webhooks from external services) is a separate tool
- The gateway does not provide a web UI for configuration
---
title: "Session Assist (Recap and Suggestions)"
status: draft
---

# Specification: Session Assist

## Overview

Session Assist is a purely event-driven server-side watcher. It subscribes to the global SSE fan-out and monitors session status transitions. When a session goes idle, a 60-second timer arms; if no new activity occurs, a small model call generates a recap and suggestion, which are PATCHed onto the session metadata.

## Architecture

```
OpenCode SSE stream
    |
    v
session-assist/runtime.js (subscribes via global SSE fan-out)
    |
    +-- session.status: idle → arm 60s timer
    +-- session.status: busy/retry → clear timer
    +-- message.updated → clear timer
    |
    v  Timer fires
small-model/call.js → generate recap + suggestion
    |
    v  PATCH session metadata
OpenCode session API (metadata.openchamber.assist)
    |
    v  SSE event
UI hook (useSessionAssist.ts) → freshness check
    |
    v  Render
SessionRecapSpacer.tsx + SessionSuggestionChip.tsx
```

## Data Models

### Session Assist Metadata

| Field | Type | Constraints | Description |
|---|---|---|---|
| metadata.openchamber.assist.recap | string | max 500 chars | Recap of the last assistant reply |
| metadata.openchamber.assist.suggestion | string | max 200 chars | Suggested user follow-up |
| metadata.openchamber.assist.forMessageID | string | not null | ID of the last assistant message |
| metadata.openchamber.assist.generatedAt | ISO timestamp | not null | When the assist was generated |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Generation trigger | 60-second idle timer after busy→idle | Avoids generation during rapid back-and-forth |
| Small model reuse | Session's own provider/model, then small model resolution | Uses user's existing credentials, no extra auth setup |
| Freshness model | Client-side check of `forMessageID` vs last message | No delete writes needed; stale data is visually hidden |
| Settings gate | Hard toggle checked at fire time | Prevents server-side resource use when feature is disabled |

## Risks and Unknowns

1. The watcher lives only in the web server process. VS Code extension-only mode does not generate assists; it can still render them from a web/desktop instance.
2. Small model resolution may fail for unauthenticated providers (e.g., users on free OpenCode plans without API keys).

## Out of Scope

- Backfill generation for existing sessions
- Multi-language recap/suggestions
- User-customizable generation prompts

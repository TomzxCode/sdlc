---
title: "Notifications & Updates"
status: done
---

# Specification: Notifications & Updates

## Overview

The notification system is split across three layers: server-side notification preparation (`packages/web/server/lib/notifications/`), push delivery (`packages/web/server/lib/notifications/push-runtime.js`), and client-side rendering. Desktop notifications use the Electron callback. Update checks query the OpenCode release endpoint.

## Architecture

```
Server (packages/web/server/lib/notifications/)
    +---> index.js (prepareNotificationLastMessage - text truncation, summarization)
    +---> emitter-runtime.js (event -> notification dispatch)
    +---> push-runtime.js (web-push VAPID delivery)
    +---> routes.js (/api/notifications/* endpoints)
    +---> runtime.js (notification trigger logic)
    +---> template-runtime.js (notification text templates)

Desktop (packages/electron/main.mjs)
    +---> onDesktopNotification callback -> Electron Notification API

VS Code (packages/vscode/src/extension.ts)
    +---> vscode.window.showInformationMessage

Client (packages/ui/src/)
    +---> Cross-tab tracking via BroadcastChannel + SSE
    +---> Update toast (packages/ui/src/components/update/OpenCodeUpdateToast.tsx)
```

## Data Models

### NotificationEvent

| Field | Type | Constraints | Description |
|---|---|---|---|
| type | enum | not null | session_complete, permission_request, agent_message |
| sessionId | string | not null | Target session |
| title | string | not null | Notification title |
| body | string | not null | Notification body (truncated) |

### UpdateState

| Field | Type | Constraints | Description |
|---|---|---|---|
| currentVersion | string | not null | Installed OpenCode version |
| latestVersion | string | nullable | Available version |
| dismissed | boolean | not null | Whether user dismissed the prompt |

## Sequences

### Browser push notification flow

```
Agent completes -> SSE event arrives at server
    |
    v
Notification emitter -> prepareNotificationLastMessage (truncate body)
    |
    v
Push runtime -> web-push.sendNotification (VAPID)
    |
    v
Service worker in browser -> showNotification
    |
    v
User clicks notification -> Navigate to session
```

### OpenCode update check

```
App starts / periodic check -> GET OpenCode releases API
    |
    v
Compare current vs latest version
    |
    v
If update available -> Show OpenCodeUpdateToast
    |
    v
User clicks "Update" -> POST /api/opencode/update
    |
    v
Server runs update -> Restarts OpenCode
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Push | web-push with VAPID | Standard web push protocol; works with all modern browsers |
| Desktop | Electron Notification API | Native OS integration; no additional libraries |
| Dismissal | Persisted state | Prevents annoying repeated prompts |
| Deduplication | Suppress across panels | VS Code has multiple webviews; dedup prevents notification spam |

## Risks and Unknowns

1. Push notification subscription may expire if the browser is closed for extended periods
2. OpenCode update process may fail on some platforms

## Out of Scope

- Notification history or log viewer
- Email or SMS notifications
- Custom notification sounds

---
title: "Mini Chat (Electron)"
status: draft
---

# Specification: Mini Chat (Electron)

## Overview

The mini chat window is an Electron BrowserWindow managed by `packages/electron/mini-chat.mjs`. It loads a lightweight view that connects to the same local web server as the main window, sharing all state through the shared server.

## Architecture

```
Mini Chat BrowserWindow (packages/electron/mini-chat.mjs)
    +---> Always-on-top, frameless or minimal chrome
    +---> Persistent bounds (position, size via electron-store)
    +---> Keyboard shortcut toggle
    |
Lightweight UI (loads from same web server)
    +---> Chat input + response area
    +---> Shares sessions via same API
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Window type | Electron BrowserWindow | Native OS integration; always-on-top, custom bounds |
| State sharing | Same web server | No state sync needed; both windows hit the same backend |

## Out of Scope

- Independent operation without main window
- Multi-session tabs in mini chat
- Mini chat for web or VS Code runtimes

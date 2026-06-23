---
title: "Electron Desktop App"
status: draft
---

# Specification: Electron Desktop App

## Overview

The Electron desktop app lives in `packages/electron/`. The main process (`main.mjs`) imports `startWebUiServer` from `@openchamber/web/server/index.js`, boots the server in-process, and loads the web UI from `http://127.0.0.1:<port>`. The preload script (`preload.mjs`) exposes a `__TAURI__` IPC shim so the shared UI works with both Electron and legacy Tauri shells. Native integrations use Electron APIs directly.

## Architecture

```
Electron Main Process (packages/electron/main.mjs)
    |
    +---> startWebUiServer() from @openchamber/web (in-process)
    |         |
    |         v  http://127.0.0.1:<port>
    +---> BrowserWindow loads web UI
    |
    +---> Native integrations:
          +-- Menu (macOS app menu)
          +-- Dialog (open folder)
          +-- Notifications (onDesktopNotification callback)
          +-- Auto-update (electron-updater)
          +-- Deep-links (protocol handler)
          +-- Mini Chat (separate BrowserWindow)
          +-- SSH connections (desktop SSH store)
```

## Data Models

### DesktopInstance

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Instance identifier |
| name | string | not null | Display name |
| host | string | not null | SSH hostname |
| port | number | not null | SSH port |
| sshKey | string | nullable | SSH key path |

## Sequences

### App startup with Mini Chat

```
Electron main starts -> boot splash window
    |
    v
startWebUiServer() in same process
    |
    v  server ready
Create main BrowserWindow -> load http://127.0.0.1:<port>
    |
    v
If Mini Chat was active -> create Mini Chat BrowserWindow
    |
    v
Register menu, deep-links, notification handlers
```

### SSH remote connection

```
User configures remote instance in settings
    |
    v
Electron main spawns SSH tunnel
    |
    v
BrowserWindow loads remote OpenChamber URL
    |
    v
Shared UI connects via SSE to remote instance
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Server in-process | Import and call startWebUiServer() directly | Eliminates sidecar complexity; shared Node.js event loop |
| Tauri shim | __TAURI__ object in preload | Shared UI checks for __TAURI__ for native features; this keeps both shells working |
| Auto-update | electron-updater with GitHub releases | Standard Electron update flow; no custom update server needed |
| Mini Chat | Separate BrowserWindow | OS-level window management; always-on-top support |

## Risks and Unknowns

1. In-process server means an Electron crash also kills the server
2. Tauri-to-Electron migration must handle existing auto-update channels

## Out of Scope

- Windows and Linux builds (on roadmap)
- Browser-based remote desktop (SSH handles remote access)

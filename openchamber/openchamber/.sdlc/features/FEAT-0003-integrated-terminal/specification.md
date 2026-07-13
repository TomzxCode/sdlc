---
title: "Integrated Terminal"
status: done
---

# Specification: Integrated Terminal

## Overview

The terminal system uses a WebSocket relay between the ghostty-web renderer in the UI and a PTY process on the server. Input normalization, control frame parsing, and rate limiting are handled by server-side utilities in `packages/web/server/lib/terminal/`.

## Architecture

```
Terminal UI (packages/ui/src/components/terminal/)
    uses ghostty-web renderer
    |
    v  WebSocket (binary + text frames)
Express Server (packages/web/server/lib/terminal/)
    |
    v  PTY
bun-pty or node-pty (OS process)
    |
    v  /bin/bash (or user's shell)
```

## Data Models

### TerminalSession

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Session identifier |
| directory | string | not null | Working directory |
| shell | string | nullable | Shell binary path |
| createdAt | timestamp | not null | Creation time |

## API Contracts

### WebSocket /api/terminal

Binary and text frames. Protocol documented in `packages/web/server/TERMINAL_WS_PROTOCOL.md`.

**Client -> Server frames:**

| Frame Type | Description |
|---|---|
| Input | Keystrokes, paste content |
| Resize | Terminal dimensions (cols, rows) |
| Close | Terminate PTY session |

**Server -> Client frames:**

| Frame Type | Description |
|---|---|
| Output | PTY stdout/stderr output |
| Exit | PTY process exit code |

## Sequences

### Terminal session lifecycle

```
User opens terminal -> UI sends WebSocket upgrade request with directory param
    |
    v
Server creates PTY session via bun-pty/node-pty in the specified directory
    |
    v
Bi-directional relay: keystrokes -> PTY stdin, PTY stdout -> WebSocket frames
    |
    v
On close: Server kills PTY, cleans up WebSocket
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Renderer | ghostty-web | Modern, performant terminal renderer with good Unicode support |
| PTY | bun-pty (primary), node-pty (fallback) | bun-pty offers better performance; node-pty is the stable fallback |
| Transport | WebSocket (not SSE) | Terminal requires bidirectional binary-capable transport |
| Input handling | Server-side normalization and rate limiting | Prevents malformed or flood input from corrupting PTY state |

## Risks and Unknowns

1. Android/iOS virtual keyboard behavior varies significantly across devices
2. UTF-8 locale detection may fail on minimal Docker containers

## Out of Scope

- Terminal split panes
- SSH sessions (handled separately by the desktop SSH feature)
- Terminal recording/playback

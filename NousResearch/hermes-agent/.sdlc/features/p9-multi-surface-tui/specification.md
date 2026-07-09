---
title: "Multi-Surface TUI and Desktop"
status: draft
---

# Specification: Multi-Surface TUI and Desktop

## Overview

The TUI is an Ink (React for terminal) frontend communicating with a Python JSON-RPC backend over stdio. The desktop app is a separate Electron application using React + nanostores talking to a headless hermes serve backend. The dashboard embeds the real hermes --tui process through a PTY bridge.

## Architecture

```
TUI (hermes --tui):
    Ink frontend (ui-tui/src/) ← stdio JSON-RPC → tui_gateway (Python backend)
        │                                               │
        │  UI Components:                              ├── AIAgent wrapper
        │  ├── app.tsx (main composer)                  ├── SlashWorker (subprocess)
        │  ├── messageLine.tsx (streaming)              ├── Transport (stdio)
        │  ├── thinking.tsx (tool activity)               └── Gateway client
        │  ├── prompts.tsx (approvals)
        │  ├── sessionPicker.tsx
        │  └── theme.ts / branding.tsx

Desktop (hermes serve --headless):
    Electron app (apps/desktop/) ← WebSocket/JSON-RPC → AIAgent + gateway
        │                                               
        ├── apps/desktop/src/lib/desktop-slash-commands.ts
        ├── app/composer/hooks/use-slash-completions.ts
        └── app/session/hooks/use-prompt-actions.ts (runSlash)

Dashboard (hermes dashboard):
    Browser (web/) ───WebSocket/PTY─── hermes --tui (headless)
        │                                   
        ├── chat page with xterm.js
        ├── sidebar widgets (optional React UI)
        └── REST API for session browse, model switching, tool config
```

## Data Models

### JSON-RPC Methods

| Method | Direction | Description |
|---|---|---|
| prompt.submit | Request → | User submits a message |
| message.delta | Event → UI | Response stream chunk |
| message.complete | Event → UI | Response complete |
| tool.start | Event → UI | Tool execution started |
| tool.progress | Event → UI | Tool progress update |
| tool.complete | Event → UI | Tool execution complete |
| approval.request | Event → UI | Dangerous action needs approval |
| approval.respond | Request → | User approves/denies |
| session.list | Request → | List available sessions |
| slash.exec | Request → | Execute slash command |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| TUI frontend | Ink (React) | Familiar React patterns with terminal rendering |
| TUI transport | stdio JSON-RPC | Simple, no network dependency, reliable |
| Desktop backend | hermes serve (headless) | Same agent core, no terminal UI overhead |
| Dashboard PTY | ptyprocess | Embeds real TUI without re-implementation |
| Desktop state | nanostores | Lightweight, colocated, subscription-based |

## Risks and Unknowns

1. The TUI and classic CLI are separate implementations — feature parity requires maintaining both
2. The dashboard's PTY bridge adds latency and a failure point (terminal process crash)
3. Desktop app's slash command pipeline curates commands client-side — skill commands may be hidden if the curation is too aggressive

## Out of Scope

- Mobile native app (React Native / Swift / Kotlin)
- Voice-only interface
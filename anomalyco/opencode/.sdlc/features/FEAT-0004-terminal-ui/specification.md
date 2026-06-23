---
title: "Terminal UI"
status: draft
---

# Specification: Terminal UI

## Overview

The TUI is a SolidJS application rendered to the terminal via opentui.
It connects to the core server (local socket by default) and projects sessions, messages, tool activity, and permissions, with keyboard-driven navigation.

## Architecture

```
opentui (terminal renderer) ◀── SolidJS UI (packages/tui + cli/cmd/tui)
                                        │
                                        ▼
                              core server (local) ── sessions, tools, providers
```

## Data Models

The TUI consumes server-projected `Message` and `Part` shapes; it holds no durable model of its own.

## API Contracts

The TUI consumes the HTTP API (see FEAT-0006), notably session, message, and permission routes.

## Sequences

### Streaming a response

```
TUI -> POST message -> server
server -> SSE/event stream -> TUI
TUI -> incrementally render parts (text, tool calls, tool output)
TUI -> inline permission prompt when required
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | SolidJS on opentui | Reactive UI in the terminal; shared mental model with web app |
| Dev server | Worker thread under `bun dev` | Keeps TUI and server in one process; `spawn` variant for debugging |

## Risks and Unknowns

1. Worker-thread debugging can mis-map breakpoints; documented workarounds use `bun dev spawn` or a separately debugged server.
2. The split between `packages/tui` and in-repo TUI code may need consolidation.

## Out of Scope

- Web and desktop frontends (see FEAT-0005).
- Server-side session execution (see FEAT-0001).

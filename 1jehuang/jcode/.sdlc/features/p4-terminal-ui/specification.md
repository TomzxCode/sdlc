---
title: "Terminal UI"
status: done
---

# Specification: Terminal UI

## Overview

The TUI lives in `crates/jcode-tui` (the presentation layer of the crate spine: base → app-core → tui → root) with rendering helpers in `jcode-tui-mermaid`, `jcode-tui-anim`, `jcode-fuzzy`, `jcode-math`, and a shared render model in `jcode-render-core`. It subscribes to server events over the protocol socket and renders streaming messages, panels, and diagrams. Offline replay/video export lives in `jcode-tui`'s video export module and is reachable via `jcode replay`. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
jcode-tui (ratatui + crossterm)
├── tui/app/            — main app state machine, keybindings, input handling
├── tui/ui_*            — widget implementations (info widgets, side panels)
├── tui/session_picker  — session browse/resume
├── tui/mermaid         — Mermaid rendering (PNG via ratatui-image, kitty/sixel/iTerm2/halfblock)
├── tui/video_export    — offline replay + video export (jcode replay)
├── tui/keybind         — configurable keybindings
└── jcode-render-core   — backend-neutral document/render model shared with desktop
        │
        ▼
jcode-protocol (ServerEvent stream over socket)
```

## Data Models

### UI State

TUI state is decomposed into widgets via the TUISTATE trait (see `docs/TUISTATE_TRAIT_DECOMPOSITION.md`), which keeps rendering logic testable headlessly.

### Config Surface

| Section | Keys | Description |
|---|---|---|
| `[display]` | display modes, centered mode, timestamps, message timestamps | Rendering preferences. |
| `[keybindings]` | per-action bindings | User-overridable keymaps. |
| `[features]` | mermaid, idle animation, etc. | Feature toggles. |

## API Contracts

### CLI: `jcode replay [session]`

Flags: `--swarm`, `--export`, `--video`, `--auto-edit`, `--timeline`, `--speed`, `--fps`.

**Behavior** | Description
|---|---|
| `--video` | Exports an offline video of the session replay. |

## Sequences

### Render a streaming turn

```
Server sends ServerEvent (TextDelta, ToolUseStart/End, ...) over socket
TUI app receives event → updates document model (jcode-render-core)
Redraw triggered → widgets render cells → crossterm frame flush
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| ratatui + crossterm | Industry-standard terminal rendering | Mature, fast, cross-platform. |
| Render stack pinned to opt-level 3 | ratatui/unicode/image/etc. pinned in profiles | Prevents ~12 ms→21 ms full-frame slowdowns in dev builds. |
| Backend-neutral render model | `jcode-render-core` | Shares document rendering with the desktop GPU app. |
| Offline video export | `video_export` module + `jcode replay --video` | Reproducible session review without a live terminal. |
| TUISTATE decomposition | trait-based widget state | Headless testability (NFR-4). |

## Risks and Unknowns

1. Image/Mermaid rendering depends on terminal protocol support; fallbacks degrade to text or halfblock rendering.
2. Idle animations must stay CPU-light (math kernels pinned to `opt-level = 3` to bound CPU use).

## Out of Scope

- The desktop GPU UI (a separate feature; shares `jcode-render-core` only).
- Terminal-agnostic rendering of exotic diagrams beyond Mermaid.

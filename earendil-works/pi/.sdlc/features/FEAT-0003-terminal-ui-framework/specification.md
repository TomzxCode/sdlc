---
title: "Terminal UI Framework"
status: draft
---

# Specification: Terminal UI Framework

## Overview

`pi-tui` is an imperative terminal UI framework.
Components return arrays of pre-styled strings; the `TUI` manager diffs the new array against the previous frame and emits minimal escape sequences wrapped in synchronized output.
There is no virtual DOM; callers mutate components then request a render.

## Architecture

```
+-------------------+   mutate + requestRender
| Application code  |-------------------------+
+-------------------+                         |
        | uses                                 |
        v                                      v
+-------------------+   render(width)   +-------------+
|   Components      |------------------>|    TUI      |
| (Editor, Text,    |                   | (manager)   |
|  Markdown, ...)   |                   +------+------+
+-------------------+                          | composites overlays
                                               | diffs vs previousLines
                                               v
                                    +---------------------+
                                    |  differential write |
                                    |  (sync output, ~60fps)|
                                    +----------+----------+
                                               |
                                               v
                                    +---------------------+
                                    | Terminal interface  |
                                    | (ProcessTerminal /  |
                                    |  VirtualTerminal)   |
                                    +---------------------+
```

## Data Models

### Component

| Field | Type | Constraints | Description |
|---|---|---|---|
| render | (width: number) => string[] | required | Returns styled lines, each <= width |
| handleInput | (data) => boolean | optional | Returns true if input consumed |
| wantsKeyRelease | boolean | optional | Claims key release |
| invalidate | () => void | required | Marks the component dirty |

### OverlayOptions

| Field | Type | Constraints | Description |
|---|---|---|---|
| anchor | object | optional | Positioning anchor |
| margins | object | optional | Edge margins |
| visible | () => boolean | optional | Visibility callback |
| nonCapturing | boolean | optional | Does not capture focus |

### Key

| Field | Type | Constraints | Description |
|---|---|---|---|
| key | string | optional | Logical key name |
| ctrl/alt/shift | boolean | optional | Modifiers |
| paste | boolean | optional | Bracketed paste flag |

## API Contracts

### TUI.start() / TUI.stop()

Begins/ends raw mode, Kitty keyboard negotiation, and the render loop.
`requestRender()` schedules a throttled render; `setFocus`, `showOverlay`/`hideOverlay` manage composition.

### Keybindings

`matchesKey(keyData, binding)` compares parsed keys against configurable bindings.
Defaults live in `TUI_KEYBINDINGS`; consumers override via `setKeybindings`.

## Sequences

### Differential render

```
application -> component.invalidate() / TUI.requestRender()
TUI (next tick, if >= MIN_RENDER_INTERVAL_MS):
  render each focused component -> lines[]
  composite overlays into lines[]
  extract cursor marker -> compute hardware cursor position
  if first render:       output all lines (no scrollback clear)
  elif full re-render:   clear screen + home + clear scrollback; delete Kitty images
  else (differential):
    find first/last changed line vs previousLines
    move cursor to first changed line; clear to end
    write only changed range
  wrap all output in synchronized output escapes
  handle appended/deleted lines and viewport scroll
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Rendering model | Imperative, string-line diff | No VDOM overhead; minimal escape output |
| Atomicity | Synchronized output (`?2026h/l`) | Flicker-free even across slow connections |
| Throttling | ~60fps with nextTick coalescing | Bounding CPU while staying responsive |
| IME cursor | Zero-width APC marker | Keeps fake cursor while positioning hardware cursor for IME |
| Line resets | Full SGR + OSC 8 reset per line | Prevents style/hyperlink leakage across lines |
| Terminal abstraction | `Terminal` interface | `ProcessTerminal` prod, `VirtualTerminal` tests |

## Risks and Unknowns

1. Differential rendering correctness depends on accurate change detection; subtle bugs (Kitty image ranges, overlay compositing above viewport) require regression tests.
2. Terminal compatibility variance (Kitty support, synchronized output, color scheme reporting) means fallback paths must be exercised.
3. The overlay focus-restore state machine has many states ("eligible"/"blocked") and is a likely source of regressions.

## Out of Scope

- LLM streaming and provider abstraction (FEAT-0001).
- Agent loop and tool execution (FEAT-0002).
- The interactive coding agent product built on top of this framework (FEAT-0004).

---
title: "Terminal UI Framework"
status: draft
---

# Requirements: Terminal UI Framework

## Overview

`pi-tui` is a minimal terminal UI framework with differential rendering and synchronized output for flicker-free interactive CLI applications.
It is custom-built (no React/Ink/VDOM): components are plain classes that return styled strings, and a hand-written renderer diffs the new frame against the previous one and writes minimal escape sequences.
It powers the coding agent's interactive mode and is reusable by any terminal application.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Coding agent interactive mode | Primitive components (editor, text, markdown, lists, overlays) and flicker-free rendering |
| SDK / library users | A terminal-agnostic component framework they can target |
| End users | Smooth, responsive terminal rendering across platforms and terminals |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a `Component` model where components implement `render(width): string[]` and optional `handleInput`. |
| FR-02 | Must | The system shall provide a `TUI` manager that composes components, manages focus, overlays, and drives rendering. |
| FR-03 | Must | The system shall perform differential rendering, writing only changed line ranges between frames. |
| FR-04 | Must | The system shall wrap updates in synchronized output escape sequences for atomic, flicker-free rendering. |
| FR-05 | Must | The system shall throttle rendering to a capped frame rate and coalesce multiple invalidations per tick. |
| FR-06 | Must | The system shall provide reusable components: `Editor`, `Text`, `TruncatedText`, `Input`, `Box`, `Markdown`, `SelectList`, `SettingsList`, `Loader`, `CancellableLoader`, `Image`, `Spacer`. |
| FR-07 | Must | The system shall provide an `Overlay` system with anchor-based, percentage, and absolute positioning, plus focus restore. |
| FR-08 | Must | The system shall provide key handling with Kitty keyboard protocol negotiation and legacy sequence fallback. |
| FR-09 | Must | The system shall provide column-aware string utilities (`visibleWidth`, `truncateToWidth`, `sliceByColumn`, `wrapTextWithAnsi`) handling ANSI codes and wide/CJK characters. |
| FR-10 | Must | The system shall be terminal-agnostic via a `Terminal` interface, with `ProcessTerminal` for production. |
| FR-11 | Should | The system shall support terminal image protocols (Kitty and iTerm2 inline images) with capability detection. |
| FR-12 | Should | The system shall support IME candidate windows by emitting a zero-width cursor marker and positioning the hardware cursor. |
| FR-13 | Should | The system shall provide a keybindings manager with default TUI keybindings. |
| FR-14 | Should | The system shall detect terminal color scheme (light/dark) via OSC 11. |
| FR-15 | Should | The system shall provide fuzzy match/filter and autocomplete providers (slash commands + file paths). |
| FR-16 | May | The system shall ship native addons for win32 and darwin to report modifier-key state. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Correctness | Components shall return lines that do not exceed the provided width; the framework shall error otherwise. |
| NFR-02 | Must | Performance | First render and full re-render strategies shall clear scrollback correctly; differential updates shall never leave stale content. |
| NFR-03 | Must | Compatibility | Each rendered line shall append a full SGR reset and OSC 8 hyperlink reset so styles do not carry across lines. |
| NFR-04 | Should | Testability | The framework shall be testable against a virtual terminal (xterm headless) for deterministic render assertions. |
| NFR-05 | Should | Performance | Rendering shall be capped at approximately 60 fps (`MIN_RENDER_INTERVAL_MS = 16`). |

## Constraints

- No React, no Ink, no virtual DOM; imperative component model.
- Dependencies kept minimal (`get-east-asian-width`, `marked`).
- Erasable TypeScript syntax only; ESM only.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-03**
    - **Given** a previous frame and a new frame differing on a contiguous range of lines
    - **When** a render is requested
    - **Then** only the changed range is written, with the cursor moved to the first changed line and clear-to-end applied.
- [ ] **FR-04**
    - **Given** any render update
    - **When** the update is written to the terminal
    - **Then** the bytes are wrapped in synchronized output (`\x1b[?2026h` ... `\x1b[?2026l`).
- [ ] **FR-07**
    - **Given** a focused overlay that is temporarily replaced by another overlay
    - **When** the replacement releases focus
    - **Then** the original overlay reclaims focus via the focus-restore state machine.
- [ ] **FR-09**
    - **Given** a string containing ANSI codes and wide CJK characters
    - **When** `visibleWidth` and `truncateToWidth` are applied
    - **Then** the visible width and truncation account for display columns, not raw character count.
- [ ] **NFR-01**
    - **Given** a component that returns a line longer than `width`
    - **When** rendered
    - **Then** the framework raises an error rather than overflowing the terminal.
- [ ] **NFR-03**
    - **Given** consecutive rendered lines with different styling
    - **When** composited
    - **Then** each line resets SGR state so no style leaks into the next line.

## Conflicts

None identified yet.

## Open Questions

1. Is the native modifier-key addon (`native-modifiers.ts`) expected to gain a Linux path, or is the protocol fallback sufficient there?
2. What is the policy for adding new built-in components versus leaving them to consumers?

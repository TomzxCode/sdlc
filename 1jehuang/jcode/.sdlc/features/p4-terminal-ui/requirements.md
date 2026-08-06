---
title: "Terminal UI"
status: done
---

# Requirements: Terminal UI

## Overview

The terminal UI is jcode's primary interface: a fast, memory-efficient TUI built with ratatui that renders streaming agent output, session pickers, info widgets, side panels, inline images, and Mermaid diagrams. It also powers the offline `jcode replay` video export of past sessions. The TUI is the presentation layer and shares a backend-neutral render model with the desktop app. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Low-latency, readable streaming output, discoverable keybindings, and useful side panels |
| Maintainer | Performant rendering under heavy streams, themeable output, and testable UI logic |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall render streaming agent output in a terminal UI with low input latency. |
| FR-2 | Must | The system shall provide a session picker to browse and resume past sessions. |
| FR-3 | Must | The system shall display info widgets (session info, model, provider, usage) in the UI. |
| FR-4 | Must | The system shall support configurable keybindings and display options (e.g. centered mode, message timestamps, theme detection). |
| FR-5 | Should | The system shall render side panels such as the session list and usage overlay. |
| FR-6 | Should | The system shall render Mermaid diagrams and inline images in the transcript where the terminal supports it. |
| FR-7 | Should | The system shall support offline replay of sessions, including video export. |
| FR-8 | Should | The system shall run an onboarding walkthrough for first-time users. |
| FR-9 | May | The system shall show idle animations (e.g. a donut) that stay CPU-light. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | The TUI shall keep full-frame render time low while streaming (render stack pinned to optimized profiles). |
| NFR-2 | Must | Performance | RAM usage shall stay low; additional clients shall scale memory gracefully. |
| NFR-3 | Should | Usability | Keybindings must be discoverable and configurable without editing source. |
| NFR-4 | Should | Reliability | TUI state must be testable without a live terminal (headless test harness). |

## Constraints

- Terminal-first: the TUI must degrade gracefully across terminals without kitty/iterm2 image support.
- Config via `[keybindings]` and `[display]` sections in `~/.jcode/config.toml`.

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** a streaming session
    - **When** output arrives rapidly
    - **Then** the UI keeps the input line responsive (no visible input lag)
- [ ] **FR-2**
    - **Given** past sessions
    - **When** the user opens the session picker
    - **Then** sessions are listed and selectable for resume
- [ ] **FR-3**
    - **Given** an active session
    - **When** info widgets are enabled
    - **Then** session, model, provider, and usage information is visible
- [ ] **FR-4**
    - **Given** a customized keybinding or display setting
    - **When** jcode starts
    - **Then** the UI honors the configuration
- [ ] **FR-5**
    - **Given** an active session
    - **When** the session list or usage side panel is toggled
    - **Then** the panel renders the expected content
- [ ] **FR-6**
    - **Given** a transcript containing a Mermaid diagram or an inline image
    - **When** the terminal supports the rendering path
    - **Then** the diagram/image renders inline
- [ ] **FR-7**
    - **Given** a recorded session
    - **When** the user runs `jcode replay --video`
    - **Then** an offline video export is produced
- [ ] **FR-8**
    - **Given** a first-time user
    - **When** onboarding is enabled
    - **Then** a guided walkthrough is shown
- [ ] **FR-9**
    - **Given** idle time in the UI
    - **When** the idle animation is enabled
    - **Then** CPU usage stays low during animation
- [ ] **NFR-1**
    - **Given** a streaming session
    - **When** frames are rendered
    - **Then** p50/p95 frame time stays within the performance budget
- [ ] **NFR-2**
    - **Given** multiple clients on the same server
    - **When** memory is measured
    - **Then** incremental memory per additional client stays low
- [ ] **NFR-3**
    - **Given** the default keybinding set
    - **When** a user presses `?` or consults help
    - **Then** bindings are shown and overridable via config
- [ ] **NFR-4**
    - **Given** the TUI test harness
    - **When** UI logic tests run in CI
    - **Then** they pass without a real terminal

## Conflicts

None identified yet.

## Open Questions

1. What is the exact frame-time budget enforced for the TUI render stack? Profile comments reference ~12 ms p50 / ~21 ms p95 for full frames, but a formal number is not documented.

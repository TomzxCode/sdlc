---
title: "Multi-Surface TUI and Desktop"
status: done
---

# Requirements: Multi-Surface TUI and Desktop

## Overview

Hermes provides three additional user surfaces beyond the classic CLI: a Terminal UI (TUI) built with Ink/React and a Python JSON-RPC backend, an Electron desktop application with its own React frontend, and a web dashboard that embeds the real TUI via xterm.js PTY bridge. These surfaces share the same agent core and gateway backend.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Terminal users | Want a richer terminal experience than the classic CLI with session picker and streaming output |
| Desktop users | Want a standalone app with proper window management, notifications, and native feel |
| Dashboard users | Want browser-based access to the agent via web UI |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The TUI shall provide chat streaming with real-time tool activity display |
| FR-2 | Must | The TUI shall provide a session picker for switching between conversations |
| FR-3 | Must | The TUI shall support approval prompts, clarifying questions, and masked input (sudo/secret) |
| FR-4 | Must | The TUI shall support slash commands with completions |
| FR-5 | Must | The TUI shall support file path autocompletion |
| FR-6 | Must | The desktop app shall provide its own composer, transcript, and slash-command pipeline |
| FR-7 | Must | The desktop app shall communicate with a headless hermes serve backend over WebSocket/JSON-RPC |
| FR-8 | Must | The web dashboard shall embed the real TUI (not a rewrite) via xterm.js |
| FR-9 | Should | The TUI shall support skimming (theming) via the same skin data as the CLI |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | TUI input latency shall be under 50ms |
| NFR-2 | Should | Compatibility | The web dashboard shall support modern browsers (Chrome, Firefox, Safari, Edge) |

## Constraints

- The web dashboard MUST embed the real hermes --tui via PTY bridge — not reimplement the chat experience in React
- The desktop app is a completely separate surface from the TUI (its own pipeline, not an embedded TUI)
- TypeScript frontends use nanostores for shared state

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the TUI is running
    - **When** the agent responds
    - **Then** the response streams character-by-character through message.delta events
- [ ] **FR-8**
    - **Given** the dashboard is running
    - **When** a user navigates to /chat
    - **Then** the page shows the real hermes --tui embedded via xterm.js
- [ ] **FR-6**
    - **Given** the desktop app is running
    - **When** the user types a message
    - **Then** it is sent to the backend and the response appears in the desktop transcript

## Conflicts

None identified yet.

## Open Questions

1. Eventually the TUI could replace the classic CLI entirely — what is the migration path?
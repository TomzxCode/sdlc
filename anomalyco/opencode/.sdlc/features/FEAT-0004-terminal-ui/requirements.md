---
title: "Terminal UI"
status: done
---

# Requirements: Terminal UI

## Overview

The Terminal UI (TUI) is OpenCode's primary interactive surface, rendering the agent conversation, tool output, permissions, and session controls inside the terminal.
It is built with SolidJS on opentui and runs against the core server, optionally in a worker thread during development.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Fast, responsive terminal experience with keyboard-driven controls |
| Core team | Stable rendering pipeline; correct worker-thread rejection handling |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall render an interactive conversation view with streaming model output. |
| FR-02 | Must | The system shall let users switch between agents (e.g. via the Tab key). |
| FR-03 | Must | The system shall surface permission prompts and tool activity inline. |
| FR-04 | Must | The system shall scope file autocomplete to the active session. |
| FR-05 | Should | The system shall provide a thinking-mode toggle for reasoning model output. |
| FR-06 | Should | The system shall preserve worker-thread rejection handling when run via `bun dev`. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Usability | Primary interactions shall be keyboard-driven. |
| NFR-02 | Should | Performance | Streaming output shall render without blocking input. |

## Constraints

- TUI code lives in `packages/opencode/src/cli/cmd/tui/` and the `packages/tui` package.
- During development the server may run in a worker thread; `bun dev spawn` or a separately debugged server may be needed for breakpoints.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** an active session
    - **When** the model streams a response
    - **Then** tokens render incrementally in the conversation view
- [ ] **FR-04**
    - **Given** the user is entering a file path in a session
    - **When** autocomplete triggers
    - **Then** only files relevant to the active session's scope are suggested
- [ ] **FR-06**
    - **Given** the TUI runs via `bun dev` with a worker-thread server
    - **When** the worker rejects a promise
    - **Then** the rejection is handled and does not crash the TUI

## Conflicts

None identified yet.

## Open Questions

1. What is the long-term split between `packages/tui` and the in-repo `cli/cmd/tui` code?

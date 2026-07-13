---
title: "Mini Chat (Electron)"
status: done
---

# Requirements: Mini Chat (Electron)

## Overview

A compact, always-on-top mini chat window for the Electron desktop app that provides quick access to AI chat without opening the main window. Supports persistent window position, keyboard shortcuts, and shared state with the main application.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Desktop users | Quick AI access without context-switching to the main window |
| Power users | Keep a small chat window alongside their editor |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a compact always-on-top chat window. |
| FR-02 | Must | The system shall support persistent window position and size. |
| FR-03 | Must | The system shall share state with the main application. |
| FR-04 | Must | The system shall support keyboard shortcut to toggle visibility. |
| FR-05 | Should | The system shall support docking to screen edges. |
| FR-06 | Should | The system shall have a minimal UI with input and response area only. |
| FR-07 | Must | The system shall require the main window's web server for mini chat operation. |
| FR-08 | Must | The system shall support one session per mini chat window with no tabs, allowing multiple windows simultaneously. |

## Constraints

## Acceptance Criteria

- [ ] FR-01: Given the desktop app, the user opens the mini chat window
- [ ] FR-02: Given a repositioned mini chat, it opens at the same position next time
- [ ] FR-03: Given an active session in the main window, the mini chat can continue it
- [ ] FR-04: Given the keyboard shortcut, the mini chat toggles visibility
- [ ] FR-05: Given the mini chat window, dragging it to a screen edge docks it to that edge
- [ ] FR-06: Given the mini chat is open, it shows only the chat input and response area without chrome
- [ ] FR-07: Given the main window is closed, the mini chat cannot function independently
- [ ] FR-08: Given multiple mini chat windows, each displays one session with no tabs

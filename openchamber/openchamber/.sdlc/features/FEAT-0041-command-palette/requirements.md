---
title: "Command Palette"
status: draft
---

# Requirements: Command Palette

## Overview

OpenChamber provides a keyboard-activated command palette with fuzzy search for navigating to sessions, files, branches, settings pages, and executing actions. It serves as a power-user shortcut for any operation in the app.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Power users | Quick navigation and action execution without mouse |
| Keyboard-first users | Full app control via keyboard shortcuts |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a keyboard-activated command palette with fuzzy search. |
| FR-02 | Must | The system shall support searching and switching to sessions. |
| FR-03 | Must | The system shall support searching and opening files. |
| FR-04 | Must | The system shall support searching and switching git branches. |
| FR-05 | Must | The system shall support navigating to settings pages. |
| FR-06 | Should | The system shall support executing action commands (new session, toggle panel, etc.). |
| FR-07 | Should | The system shall support keyboard navigation within the palette (arrow keys, enter, escape). |
| FR-08 | Must | The system shall use Cmd+P (macOS) / Ctrl+P (Linux/Windows) as the default keyboard shortcut, with customization support. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Search results shall appear within 100ms for typical project sizes. |

## Constraints

- Uses `cmdk` library for the palette UI
- Fuzzy search uses `fuse.js`
- Palette activation via configurable keyboard shortcut


## Acceptance Criteria

- [ ] FR-01: Given the keyboard shortcut, the command palette opens
- [ ] FR-02: Given a partial session name, fuzzy search shows matching sessions
- [ ] FR-03: Given a partial filename, fuzzy search shows matching files
- [ ] FR-04: Given a partial branch name, fuzzy search shows matching branches
- [ ] FR-05: Given a settings page name, selecting it navigates to that page
- [ ] FR-06: Given the command palette open, typing an action command name executes that action
- [ ] FR-07: Given the command palette open, arrow keys move focus between results and Escape closes the palette
- [ ] FR-08: Given the default state, Cmd+P (macOS) / Ctrl+P (Linux/Windows) opens the palette; given a custom shortcut, the new shortcut opens the palette instead
- [ ] NFR-01: Given a project with 500+ searchable items, fuzzy search results appear within 100ms of keystroke

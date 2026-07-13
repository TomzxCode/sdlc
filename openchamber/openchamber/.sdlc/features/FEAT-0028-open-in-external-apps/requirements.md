---
title: "Open In External Apps"
status: done
---

# Requirements: "Open In" External Apps

## Overview

Users can configure a preferred external application (from a catalog of 23+ supported apps: VS Code, IntelliJ, Xcode, Terminal, iTerm2, Ghostty, Cursor, Zed, etc.) to open project directories. The system detects installed apps and lets users select their preferred one.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Desktop users | Open project in preferred editor or terminal |
| Multi-tool developers | Switch between IDEs for different tasks |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support opening project directories in a configured external application. |
| FR-02 | Must | The system shall provide a catalog of 23+ supported applications. |
| FR-03 | Must | The system shall detect which apps are installed on the system. |
| FR-04 | Should | The system shall allow the user to select their preferred app. |
| FR-05 | Should | The system shall support the "Open In" action from the header and file viewer. |
| FR-06 | Must | The system shall provide a fixed catalog of 23 supported apps without the ability to add custom apps. |
| FR-07 | Should | The system shall store app preference globally, not scoped per-project. |

## Acceptance Criteria

- [ ] FR-01: Given a configured app, clicking "Open In" launches it with the project directory
- [ ] FR-02: Given the app catalog, 23+ apps are available for selection
- [ ] FR-03: Given the system, installed apps are detected and shown as available
- [ ] FR-04: Given the app catalog, the user can select their preferred external app
- [ ] FR-05: Given the header or file viewer, the user can trigger the "Open In" action
- [ ] FR-06: Given the app catalog, the user cannot add custom apps beyond the 23 provided
- [ ] FR-07: Given app preference set in one project, the same preference applies across all projects

## Constraints

- App preference is stored in localStorage

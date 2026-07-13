---
title: "Web & Desktop Apps"
status: done
---

# Requirements: Web & Desktop Apps

## Overview

OpenCode ships a SolidJS web app of shared UI components and an Electron desktop application that wraps it.
The web app lets users interact with sessions through a browser against a running server, while the desktop app packages that experience as a native application with cross-platform installers.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | A polished graphical experience without a terminal |
| Desktop users | Native installers (dmg, exe, deb/rpm/AppImage) and auto-update |
| Core team | Shared component library between web and desktop |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The web app shall connect to a running OpenCode server and render sessions, messages, and tool activity. |
| FR-02 | Must | The desktop app shall wrap the web UI in Electron and run a local server. |
| FR-03 | Must | The desktop app shall be packaged for macOS (Apple Silicon + Intel), Windows, and Linux. |
| FR-04 | Should | The web app shall share UI components with other surfaces via `packages/app` and `packages/ui`. |
| FR-05 | Should | The desktop app shall be installable via Homebrew Cask and Scoop extras. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Usability | The graphical experience shall match TUI capabilities for core session flows. |
| NFR-02 | Should | Performance | The web dev server shall hot-reload UI changes independently of the core server. |

## Constraints

- UI/core product features require design review with the core team before implementation.
- The web app requires a separately running server for full functionality.
- Desktop packaging uses Electron; `trustedDependencies` includes `electron`.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** a server is running
    - **When** the web app loads
    - **Then** sessions render and new prompts can be submitted
- [ ] **FR-02**
    - **Given** the desktop app is launched
    - **When** it starts
    - **Then** a local server is available and the web UI is displayed
- [ ] **FR-03**
    - **Given** a desktop release build
    - **When** packaged
    - **Then** dmg (mac arm64/x64), Windows exe, and Linux deb/rpm/AppImage artifacts are produced

## Conflicts

None identified yet.

## Open Questions

1. What is the update mechanism and cadence for desktop auto-updates across platforms?

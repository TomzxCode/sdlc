---
title: "Desktop App"
status: done
---

# Requirements: Desktop App

## Overview

The desktop app wraps the agentsview web server in a native application using Tauri, providing a native title bar, system tray integration, auto-start, and auto-update. It targets macOS (DMG) and Windows, with the Go binary bundled as a sidecar process.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Install and run agentsview as a native desktop application |
| macOS user | Prefer DMG installation with automatic updates |
| Windows user | Native Windows experience |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a Tauri-based desktop wrapper for agentsview |
| FR-2 | Must | The system shall bundle the Go server binary as a Tauri sidecar |
| FR-3 | Must | The system shall support auto-start on login |
| FR-4 | Must | The system shall support system tray integration with status icon |
| FR-5 | Must | The system shall support auto-update checking and installation |
| FR-6 | Should | The system shall provide a macOS DMG installer |
| FR-7 | Should | The system shall provide a Windows installer |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Desktop app should use minimal system resources when idle |

## Acceptance Criteria

- **FR-1**
  - Given the desktop app is installed
  - When the app is launched
  - Then the agentsview web UI opens in the default browser
- **FR-3**
  - Given the desktop app is installed
  - When the user logs in
  - Then agentsview starts automatically

## Open Questions

1. Should there be a Linux desktop build or is web-only sufficient?

---
title: "Electron Desktop App"
status: draft
---

# Requirements: Electron Desktop App

## Overview

The Electron desktop app (packages/electron/) is the forward desktop runtime for OpenChamber. It boots the web server in the same Node process, loads the web UI from localhost, and provides native integrations: macOS menu, dialogs, notifications, auto-update, deep-links, multi-window support, Mini Chat windows, and SSH remote connections.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| macOS developers | Native desktop experience for AI-assisted coding |
| Remote workers | SSH connections to remote OpenChamber instances |
| Multi-taskers | Mini Chat and multi-window for parallel workflows |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall boot the web server in-process (no sidecar subprocess) and load the UI from localhost. |
| FR-02 | Must | The system shall provide native macOS menu integration with app actions. |
| FR-03 | Must | The system shall support auto-update via electron-updater with GitHub releases. |
| FR-04 | Must | The system shall support deep-link handling for opening projects and sessions. |
| FR-05 | Must | The system shall support Mini Chat windows for focused conversations. |
| FR-06 | Must | The system shall support connecting to remote OpenChamber instances over SSH. |
| FR-07 | Should | The system shall support multi-window for parallel project/session workflows. |
| FR-08 | Should | The system shall support "Open In" shortcuts for Finder, Terminal, and preferred editor. |
| FR-09 | Should | The system shall support workspace-first startup flow with directory picker. |
| FR-10 | Should | The system shall support system notifications via desktop notification callback. |
| FR-11 | May | The system shall support Windows and Linux (on roadmap). |
| FR-12 | Must | The system shall support in-place migration from Tauri to Electron by packaging the Electron app into a Tauri-compatible format for auto-update. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | The Electron app shall use hardened runtime and notarization on macOS. |
| NFR-02 | Should | Performance | The splash window shall appear early while the server starts. |
| NFR-03 | Should | Reliability | Window state (size, position) shall be restored across launches. |

## Constraints

- Electron 41 is the current version
- Builds are distributed as DMG and ZIP for macOS (arm64)
- The preload script exposes `__TAURI__` IPC shim for backward compatibility with shared UI
- Notarization requires an Apple Developer certificate
- Tauri-to-Electron migration is documented in docs/TAURI_TO_ELECTRON_CUTOVER.md

## Acceptance Criteria

- [ ] FR-01: Given the app launches, the web server starts in-process and the UI loads
- [ ] FR-02: Given the app is running, the macOS menu bar shows OpenChamber actions
- [ ] FR-03: Given a new release on GitHub, the app detects, downloads, and applies the update
- [ ] FR-04: Given a deep link URL for a project or session, the app opens the correct resource
- [ ] FR-05: Given the Mini Chat is opened, it shows a compact session view independent of the main window
- [ ] FR-06: Given SSH credentials, the app connects to a remote OpenChamber instance
- [ ] FR-07: Given multiple projects, the user opens them in separate windows for parallel workflows
- [ ] FR-08: Given a file or folder, the user opens it in Finder, Terminal, or preferred editor via "Open In"
- [ ] FR-09: Given first launch, the app shows a directory picker to select a workspace
- [ ] FR-10: Given a system notification event, the app displays it via the desktop notification callback
- [ ] FR-11: Given Windows or Linux, the app runs with platform-appropriate menus and behavior
- [ ] FR-12: Given a Tauri installation, the Electron update is packaged as a Tauri-compatible .app.tar.gz and auto-updates in-place
- [ ] NFR-01: Given the macOS build, the app is notarized with hardened runtime enabled
- [ ] NFR-02: Given app startup, the splash window appears before the server is ready
- [ ] NFR-03: Given the app is resized and repositioned, it opens at the same window state on next launch

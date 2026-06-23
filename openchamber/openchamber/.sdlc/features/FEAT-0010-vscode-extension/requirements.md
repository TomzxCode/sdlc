---
title: "VS Code Extension"
status: draft
---

# Requirements: VS Code Extension

## Overview

OpenChamber ships as a VS Code extension that embeds the shared UI in a sidebar webview. It provides editor-native AI assistance: chat alongside code, agent manager for parallel runs, right-click actions (explain, improve, add context), and session management in an editor panel.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| VS Code users | AI coding assistance without leaving the editor |
| Extension marketplace users | Easy installation from VS Code Marketplace |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a sidebar webview with the shared OpenChamber chat UI. |
| FR-02 | Must | The system shall support opening files from tool output directly in the editor. |
| FR-03 | Must | The system shall support right-click context menu actions: Explain, Improve Code, Add to Context. |
| FR-04 | Must | The system shall support the Agent Manager for parallel multi-model runs. |
| FR-05 | Must | The system shall support an editor panel for session viewing alongside code. |
| FR-06 | Should | The system shall map VS Code theme colors to OpenChamber theme tokens. |
| FR-07 | Should | The system shall support settings sync (API URL, binary path) between VS Code and the extension. |
| FR-08 | Should | The system shall support responsive layout that adapts to sidebar width. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | SSE cleanup and reconnection shall not leak listeners or get stuck. |
| NFR-02 | Must | Reliability | Extension startup shall handle delayed API readiness with retries. |
| NFR-03 | Should | Performance | Extension shall not impact editor performance during idle state. |

## Constraints

- Extension host runs in Node.js; webview runs the shared React UI
- Webview communicates with extension host via VS Code message API
- Published under publisher ID `fedaykindev` on VS Code Marketplace
- Requires VS Code >= 1.85.0

## Acceptance Criteria

- [ ] FR-01: Given the extension is installed, the sidebar shows the OpenChamber chat UI
- [ ] FR-02: Given an assistant tool output referencing a file, clicking it opens the file in the editor
- [ ] FR-03: Given selected code in the editor, right-clicking shows OpenChamber actions
- [ ] FR-04: Given the Agent Manager, the user can start a multi-model run from the sidebar
- [ ] FR-05: Given an active session, the user can open it in an editor panel alongside code
- [ ] FR-06: Given a dark VS Code theme, the OpenChamber UI adapts its colors accordingly
- [ ] FR-07: Given VS Code settings are configured for API URL and binary path, the extension reads and applies these settings on startup
- [ ] FR-08: Given the VS Code sidebar width is resized, the extension webview layout adapts accordingly without horizontal scroll
- [ ] NFR-01: Given an SSE connection from the extension, when the webview is closed or reloaded, all listeners are cleaned up and reconnection does not leak resources
- [ ] NFR-02: Given the extension starts before the API server is ready, it retries the connection with bounded intervals until the API responds
- [ ] NFR-03: Given the extension is installed but the webview is not visible, it does not consume noticeable CPU or memory in the editor

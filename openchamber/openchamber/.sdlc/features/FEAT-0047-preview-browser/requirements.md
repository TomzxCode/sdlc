---
title: "Preview & Embedded Browser"
status: done
---

# Requirements: Preview & Embedded Browser

## Overview

OpenChamber can embed a live preview of running dev servers within the app. The preview runs in an iframe with a URL bar, reload button, external open action, and inspect mode for clicking elements to annotate. On Electron desktop, a full embedded browser tab is available. The console overlay shows browser logs with filter, copy, and attach-to-session capabilities.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Frontend developers | Preview running apps alongside AI-assisted coding |
| Electron desktop users | Full embedded browser with inspect and annotation tools |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall embed an iframe preview of a running dev server within the app. |
| FR-02 | Must | The system shall provide a URL bar with reload and external open controls. |
| FR-03 | Must | The system shall proxy absolute same-origin requests and WebSocket URLs correctly. |
| FR-04 | Must | The system shall provide a console overlay showing browser logs with filter and copy. |
| FR-05 | Should | The system shall support inspect mode: click an element to annotate it. |
| FR-06 | Should | The system shall support attaching console output to the chat session. |
| FR-07 | Should | The system shall auto-detect dev server URLs from project actions. |
| FR-08 | May | The system shall provide a full embedded browser tab on Electron desktop with URL bar, navigation, and inspect mode. |
| FR-09 | May | The system shall support annotation screenshots from the preview. |
| FR-10 | Must | The system shall auto-detect dev servers based on package.json script name patterns, not specific frameworks. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Preview iframe shall not have access to OpenChamber's own cookies or storage. |
| NFR-02 | Should | Reliability | Preview proxy shall not launch unrelated project actions when no dev-server is detected. |

## Constraints

- Preview runs in a sandboxed iframe with proxy middleware on the server
- URL rewriting handles absolute same-origin paths and WebSocket upgrade URLs
- Electron browser tab uses Electron's webview or BrowserView API
- Dev server auto-detection is based on package.json script name patterns (dev, start, preview, serve, develop); the proxy handles Vite/HMR and webpack-dev-server

## Acceptance Criteria

- [ ] FR-01: Given a running dev server, the preview iframe loads the app
- [ ] FR-02: Given the preview, the URL bar shows the current URL with reload and external open buttons
- [ ] FR-03: Given a preview with same-origin fetch calls, they are proxied correctly
- [ ] FR-04: Given the console overlay, browser logs appear with filter and copy controls
- [ ] FR-05: Given inspect mode is active, clicking a page element highlights it and captures its coordinates for annotation
- [ ] FR-06: Given the console overlay, the user can attach selected log entries to the active chat session
- [ ] FR-07: Given a project with a dev server action, the preview auto-opens the detected URL
- [ ] FR-08: Given the Electron desktop app, the embedded browser tab shows with full URL bar, navigation controls, and inspect mode
- [ ] FR-09: Given an annotation is captured, the system saves a screenshot with the annotation overlay
- [ ] FR-10: Given a package.json with a "dev" or "start" script, the system detects the dev server regardless of framework
- [ ] NFR-01: Given a dev server preview in an iframe, the embedded page cannot access OpenChamber's cookies or localStorage
- [ ] NFR-02: Given a project without a dev server script, activating the preview does not launch any project action

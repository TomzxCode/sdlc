---
title: "Integrated Terminal"
status: done
---

# Requirements: Integrated Terminal

## Overview

OpenChamber includes a fully integrated terminal emulator within the app UI, supporting per-directory sessions, tabbed interface, and stable performance under heavy output. The terminal uses ghostty-web for rendering and bun-pty/node-pty for PTY management on the server.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Run commands, dev servers, and scripts without leaving the app |
| Mobile/PWA users | Terminal access from mobile devices |
| Desktop users | Native-quality terminal experience |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide an integrated terminal with PTY sessions connected via WebSocket. |
| FR-02 | Must | The system shall support per-directory terminal sessions that persist across navigations. |
| FR-03 | Must | The system shall handle UTF-8 input and output correctly across platforms. |
| FR-04 | Must | The system shall support control-key shortcuts (Ctrl+C, Ctrl+D, etc.). |
| FR-05 | Should | The system shall support tabbed terminal interface with multiple concurrent sessions. |
| FR-06 | Should | The system shall maintain stable performance on heavy output (build logs, test runs). |
| FR-07 | May | The system shall support mobile keyboard handling including control keys on tablets. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | WebSocket connections shall be cleaned up reliably during shutdown and reconnects. |
| NFR-02 | Must | Reliability | Idle WebSocket connections shall be cleaned up to prevent resource leaks. |
| NFR-03 | Should | Performance | Terminal viewport shall stay above the mobile keyboard on touch devices. |
| NFR-04 | Must | Capacity | The system shall support up to 20 concurrent terminal sessions; requests exceeding this limit shall receive HTTP 429. |

## Constraints

- Uses ghostty-web renderer in the browser/webview
- Server uses bun-pty (preferred) or node-pty for PTY management
- Input/output relayed over WebSocket with a defined protocol (see `TERMINAL_WS_PROTOCOL.md`)
- File paths are rejected as terminal working directories

## Acceptance Criteria

- [ ] FR-01: Given the app is open, the user can open a terminal and type commands
- [ ] FR-02: Given a terminal session in directory A, navigating away and back preserves the session
- [ ] FR-03: Given UTF-8 output (e.g., git log with non-ASCII characters), the terminal renders correctly
- [ ] FR-04: Given Ctrl+C is pressed, the running process receives SIGINT
- [ ] FR-05: Given multiple terminal tabs, each maintains its own PTY session
- [ ] NFR-04: Given 20 active terminal sessions, when a 21st session is requested, the response returns HTTP 429
- [ ] FR-06: Given a terminal running a build or test with heavy output, the terminal renders without significant lag or stuttering
- [ ] FR-07: Given a tablet device, the on-screen keyboard includes control keys (Ctrl, Alt, Tab)
- [ ] NFR-01: Given a terminal session active during app shutdown, the WebSocket connection is closed cleanly without resource leaks
- [ ] NFR-02: Given a terminal session idle for the timeout period, the WebSocket connection is closed and the PTY session is cleaned up
- [ ] NFR-03: Given a mobile device with an open terminal, the viewport adjusts so the input line remains visible above the keyboard

---
title: "Terminal and Browser Automation"
status: done
---

# Requirements: Terminal and Browser Automation

## Overview

Hermes provides real terminal access through six backends (local, Docker, SSH, Modal, Daytona, Singularity) and full browser automation through Playwright-based CDP control. These are the agent's primary environment interaction tools, enabling it to execute commands, run code, navigate websites, and interact with web applications.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Power users | Want the agent to perform real work on their system (install packages, run scripts, edit files) |
| Browser users | Want the agent to navigate websites, fill forms, and extract information |
| Developers | Need configurable remote execution environments (Docker, SSH, cloud) |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The agent shall execute shell commands in the user's terminal via local backend |
| FR-2 | Must | The agent shall support Docker, SSH, Modal, Daytona, and Singularity as alternative terminal backends |
| FR-3 | Must | The agent shall support background terminal processes with completion notification |
| FR-4 | Must | The agent shall navigate web pages, click elements, type text, scroll, and extract content via browser |
| FR-5 | Must | The agent shall take screenshots/snapshots of browser pages |
| FR-6 | Must | The agent shall support browser dialog handling (alert, confirm, prompt) |
| FR-7 | Should | The agent shall support Chrome DevTools Protocol (CDP) for advanced browser features |
| FR-8 | Should | The agent shall support hold-click and alternative click methods for complex web apps |
| FR-9 | Should | The agent shall support file sync between the host and remote backends |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Terminal commands must pass through security checks (dangerous command detection, path validation) |
| NFR-2 | Must | Security | Browser automation must connect to a sandboxed/containerized Chromium instance |
| NFR-3 | Should | Performance | Terminal operations should timeout gracefully with configurable per-command timeouts |

## Constraints

- Browser automation requires Playwright and a Chromium binary
- Remote backends (SSH, Docker, Modal, Daytona, Singularity) require external credentials or infrastructure
- Background processes with notification require a watcher in the gateway

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the agent is running
    - **When** the user asks the agent to run ls
    - **Then** the agent executes ls in the local terminal and returns the output
- [ ] **FR-4**
    - **Given** the agent is running with browser access
    - **When** the user asks the agent to navigate to example.com
    - **Then** the agent opens the browser, loads the page, and returns a snapshot
- [ ] **FR-3**
    - **Given** the agent is running with background terminal support
    - **When** the user asks the agent to run a long process in the background
    - **Then** the process starts running and the agent is notified when it completes

## Conflicts

None identified yet.

## Open Questions

1. Should we support headless-only browser mode? Currently requires a display/X environment for full mode.
---
title: "Control UI"
status: draft
---

# Requirements: Control UI

## Overview

The Control UI is a web-based dashboard for interacting with the assistant and managing the gateway. It provides a chat interface, session management, configuration access, system status monitoring, and plugin management.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Intuitive web interface for chatting with the assistant and managing the system |
| Operators | Quick access to system status, logs, and configuration |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The Control UI shall provide a chat interface for sending messages and viewing responses |
| FR-2 | Must | The Control UI shall display message streaming in real-time |
| FR-3 | Must | The Control UI shall support rich message rendering (markdown, code blocks, images) |
| FR-4 | Must | The Control UI shall provide session management (create, list, switch, delete) |
| FR-5 | Must | The Control UI shall display gateway status and health |
| FR-6 | Must | The Control UI shall be served by the gateway over HTTP/HTTPS |
| FR-7 | Should | The Control UI shall support viewing and editing configuration |
| FR-8 | Should | The Control UI shall support file and image upload |
| FR-9 | Should | The Control UI shall provide plugin management interface |
| FR-10 | May | The Control UI shall support dark mode |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The Control UI shall be accessible only to authenticated users |
| NFR-2 | Must | Security | The Control UI shall enforce Content Security Policy headers |
| NFR-3 | Should | Performance | The Control UI page load shall be under 2 seconds |

## Constraints

- Built as a single-page application served by the gateway
- Uses Lit web components (legacy decorators)
- Must work on modern browsers (Chrome, Firefox, Safari, Edge)

## Acceptance Criteria

- [ ] **FR-1**: Given the Control UI loaded in a browser, when the user types a message and sends it, then the message appears in the chat and the assistant responds
- [ ] **FR-2**: Given an assistant response in progress, when the response streams, then the text appears incrementally
- [ ] **FR-6**: Given a running gateway, when the user navigates to the Control UI URL in a browser, then the page loads
- [ ] **NFR-1**: Given an unauthenticated request to the Control UI, when it reaches the gateway, then it is redirected or rejected
- [ ] **NFR-2**: Given the Control UI response headers, when inspected, then Content-Security-Policy is set

## Conflicts

None identified yet.

## Open Questions

1. Should the Control UI support multiple simultaneous chat sessions?
2. What is the target mobile browser support for the Control UI?

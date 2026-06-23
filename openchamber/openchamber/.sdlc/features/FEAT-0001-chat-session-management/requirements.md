---
title: "Chat & Session Management"
status: draft
---

# Requirements: Chat & Session Management

## Overview

The core chat interface provides a branchable timeline for AI coding sessions. Users can send messages, receive streamed AI responses, fork conversations at any point, undo/redo turns, and manage multiple sessions across projects. This is the primary interaction surface for all OpenChamber runtimes.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users (developers) | Fluid, reliable chat experience with undo/redo and session persistence |
| Mobile/PWA users | Responsive chat controls on small screens |
| VS Code users | In-editor chat alongside code |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display a chat timeline with user and assistant messages, supporting streaming of assistant responses in real time via SSE. |
| FR-02 | Must | The system shall support undo and redo of chat turns (message-level branching) so users can explore different approaches. |
| FR-03 | Must | The system shall support forking a conversation from any earlier turn, creating a new branch that preserves the original timeline. |
| FR-04 | Must | The system shall persist session state so that reopening a session restores the full message history and scroll position. |
| FR-05 | Must | The system shall support creating new sessions, switching between sessions, and archiving or deleting sessions. |
| FR-06 | Must | The system shall render tool output (file diffs, file operations, permissions, long-running task progress) with dedicated UI components. |
| FR-07 | Must | The system shall support a header session switcher with project, branch, diff, active, unread, and sub-session context. |
| FR-08 | Should | The system shall support queued messages that auto-send one at a time in FIFO order. |
| FR-09 | Should | The system shall render inline comment drafts on diffs, files, and plans that can be sent back to the agent. |
| FR-10 | Should | The system shall support session folders and subfolders with drag-to-reorder. |
| FR-11 | Should | The system shall render Mermaid diagrams inline with copy/download actions. |
| FR-12 | May | The system shall support sharing messages as images. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Streaming deltas shall update the UI at up to 60 events/sec without visible jank, using virtualized rendering for large timelines. |
| NFR-02 | Must | Reliability | The SSE event pipeline shall reconnect with exponential backoff, respecting navigator.onLine and visibility state. |
| NFR-03 | Must | Reliability | Fetch failure must be signaled distinctly from successful-but-empty responses to prevent state corruption. |
| NFR-04 | Should | Performance | Scroll position shall be preserved across session switches, hydration, and draft-to-session transitions using synchronous layout effects. |
| NFR-05 | Must | Performance | The system shall paginate messages with an initial page of 150 messages (30 for VS Code/mobile) and history pages of 200. |
| NFR-06 | Must | Performance | The system shall cap the session list per directory with LRU trimming. |

## Constraints

- Chat state is managed in Zustand stores split by change frequency (streaming vs. metadata)
- SSE is the primary transport; WebSocket is used only for terminal
- The shared UI must work identically across web, desktop, and VS Code

## Acceptance Criteria

- [ ] FR-01: Given an active session, when the assistant streams a response, the user sees tokens appear in real time
- [ ] FR-02: Given a chat with multiple turns, when the user triggers undo, the last turn is removed and the timeline branches
- [ ] FR-03: Given a chat with 5+ turns, when the user clicks fork on turn 3, a new branch is created from that point
- [ ] FR-04: Given an active session with messages, when the user closes and reopens the session, all messages and scroll position are restored
- [ ] FR-05: Given the session list, when the user creates, switches to, archives, or deletes a session, the action completes and the UI reflects the change
- [ ] FR-06: Given an assistant message with tool output, when rendered, it shows a dedicated UI for the tool type (diff, file operation, etc.)
- [ ] FR-07: Given multiple sessions across projects, the header switcher shows project, branch, diff stats, and unread indicators
- [ ] FR-08: Given a queue of 3 messages, when the first response completes, the next message sends automatically
- [ ] NFR-05: Given a session with 300+ messages, when loading, only the initial page of 150 messages (30 for VS Code/mobile) is fetched
- [ ] NFR-06: Given a directory with 60+ sessions, when sessions exceed the cap, the least recently used sessions are trimmed
- [ ] FR-09: Given a diff, file, or plan with comment drafts, when the user sends the comment, it is delivered to the agent
- [ ] FR-10: Given the session list, the user can create folders, move sessions into subfolders, and reorder them via drag-and-drop
- [ ] FR-11: Given a message containing a Mermaid diagram, the diagram renders inline with copy and download buttons
- [ ] FR-12: Given a chat message, when the user triggers share as image, a PNG screenshot of the message is generated and downloaded
- [ ] NFR-01: Given a streaming assistant response, the UI updates at up to 60 deltas/sec without visible jank or layout thrash
- [ ] NFR-02: Given an SSE connection drop, the client reconnects with exponential backoff and respects navigator.onLine and document.visibilityState
- [ ] NFR-03: Given a failed API fetch returning an error, the error is not treated as an empty successful response
- [ ] NFR-04: Given a session with scroll position, when switching sessions and returning, the scroll position is restored

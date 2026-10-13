---
title: "Chat Rooms & Messaging"
status: done
---

# Requirements: Chat Rooms & Messaging

## Overview

Operators and agents need persistent, multi-participant conversation spaces outside of task-scoped planning chat. Chat rooms provide team discussion with membership, message history with pagination, file attachments, and AI-generated replies, while saved messaging scripts let operators reuse canned commands. This feature was reverse-engineered from shipped code during sync-sdlc.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Solo developer | Discusses work with agents in a persistent room instead of ephemeral task comments |
| Operator / power user | Reuses saved scripts and reviews room history across sessions |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let operators create, read, update, and delete chat rooms with slug-collision protection. |
| FR-2 | Must | The system shall manage room membership (list, add, and remove agent members). |
| FR-3 | Must | The system shall store and paginate room messages and support deleting a single message or clearing a room. |
| FR-4 | Should | The system shall support file attachments on rooms and messages with MIME-type and size validation and path-traversal protection. |
| FR-5 | Should | The system shall generate AI replies in rooms and surface generation failures as typed errors. |
| FR-6 | Should | The system shall let operators save, list, and run named messaging scripts (name to command mappings). |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall validate attachment paths so a crafted filename cannot escape the room attachment directory. |
| NFR-2 | Should | Performance | Mutating chat endpoints shall be rate-limited separately from read endpoints. |

## Constraints

- Room attachment storage lives under the project `.fusion/chat-room-attachments` directory.
- Chat message metadata is validated against the core message schema.

## Acceptance Criteria

- [ ] **FR-1**

```gherkin
@FR-1
Scenario: Create a room with a duplicate slug
Given a room with slug "standup" exists
When an operator creates another room with slug "standup"
Then the request is rejected as a slug collision
```

- [ ] **FR-3**

```gherkin
@FR-3
Scenario: Paginate room messages
Given a room with more messages than one page holds
When an operator fetches messages with a page cursor
Then only that page is returned with a cursor for the next page
```

- [ ] **NFR-1**

```gherkin
@NFR-1
Scenario: Reject a traversal filename
Given an operator uploads an attachment named "../../secret"
When the upload is processed
Then the request is rejected and nothing is written outside the room directory
```

## Open Questions

- Should chat rooms link to tasks or missions, or stay standalone team spaces?

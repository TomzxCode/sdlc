---
title: "Chat Rooms & Messaging"
status: done
---

# Test Plan: Chat Rooms & Messaging

## Scope

Covers chat room CRUD, membership, message pagination and deletion, attachment validation, and AI reply failure surfacing. Out of scope: PlanningMode task chat (covered by FEAT-p3).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Chat memory focus behavior | Room with mixed message types | Focused messages selected per rule |
| TC-2 | Traversal filename rejected | Filename `../../secret` | Bad-request rejection, no write outside room dir |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-3 | Message tie pagination over PostgreSQL | Messages with identical timestamps | Stable paged order with cursor |
| TC-4 | Room CRUD round trip | Authenticated project context | Create, fetch, update, and delete succeed; duplicate slug rejected |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-5 | Operator chats with an agent in a room | Open ChatView, post a message, wait for reply | Message persists and AI reply renders or a typed error surfaces |

## Coverage Matrix

| Requirement | Test cases |
|---|---|
| FR-1 | TC-4 |
| FR-2 | TC-4 |
| FR-3 | TC-3, TC-4 |
| FR-4 | TC-2 |
| FR-5 | TC-5 |
| NFR-1 | TC-2 |
| NFR-2 | TC-4 (rate-limited routes exercised) |

Test files: `packages/core/src/chat/__tests__/chat-memory-focus.test.ts`, `packages/core/src/chat/__tests__/chat-message-tie-pagination.pg.test.ts`.

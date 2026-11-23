---
title: "Agent Conversations"
status: done
---

# Test Plan: Agent Conversations

## Scope

Tests cover conversation identity and creation, human and agent message paths, idempotency, turn preparation and settlement, reset boundaries, delivery holds and recovery, onboarding chats, read state, and the Chat UI.
Out of scope: external provider connector suites for Slack, Discord, Teams, GitHub, Telegram, iMessage, and email, and Conference Room chat.

Test files found for this feature include `server/src/__tests__/agent-conversations.test.ts`, `server/src/__tests__/agent-chat-messages.test.ts`, `server/src/__tests__/agent-conversation-delivery.test.ts`, `server/src/__tests__/conversation-settlement-transfer.test.ts`, `server/src/__tests__/chat-run-milestone-governed-work.test.ts`, `server/src/__tests__/issue-recovery-conversations.test.ts`, `server/src/__tests__/onboarding-chat-route.test.ts`, `server/src/services/native-runtime/agent-chat-response-recovery.test.ts`, `packages/db/src/agent-chat-migration.test.ts`, `packages/db/src/agent-chat-messages-migration.test.ts`, `ui/src/pages/AgentChat.test.tsx`, `ui/src/pages/AgentChats.test.tsx`, `ui/src/components/AgentConversationsSidebar.test.tsx`, `ui/src/lib/recent-agent-chats.test.ts`, `ui/src/context/LiveUpdatesProvider.read-receipts.test.ts`, `tests/e2e/agent-chat-sessions.spec.ts`, `tests/e2e/agent-chat-messages.spec.ts`, and `tests/e2e/agent-chat-projects.spec.ts`.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Conversation identity and ordinary list exclusion | Company, agent, and user identity rows | One atomic conversation per pair and exclusion from ordinary task lists (`server/src/__tests__/agent-conversations.test.ts:141`) |
| TC-2 | Conversation guidance keeps user-visible naming and link rules | Directive assertions from the conversation service | Prompts use record names, links, and board-only creation boundaries (`server/src/__tests__/agent-conversations.test.ts:990`) |
| TC-3 | Reset processing is explicit | `/new` body and other bodies | Only `/new` is treated as a reset (`server/src/services/agent-conversations.ts:61`) |
| TC-4 | Session boundary generation decides stale runs | Run context generation and issue generation | Older turns and session events are rejected (`server/src/__tests__/agent-conversations.test.ts:784`) |
| TC-5 | Recent chat parsing and ordering | Stored ids, stars, first-created agent, and visits | Deduplicated ids capped at 50 and ordered stars, first agent, then recent (`ui/src/lib/recent-agent-chats.test.ts:14`, `:32`, `:44`) |
| TC-6 | Chat message input shape | Body and idempotency key variants | Trimmed body of 1 to 20000 characters and key of 1 to 240 characters (`packages/shared/src/validators/issue.ts:1200`) |

Files: `server/src/__tests__/agent-conversations.test.ts`, `ui/src/lib/recent-agent-chats.test.ts`, `packages/shared/src/validators/issue.ts`.

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Board routes resolve one chat and keep opens read-only | Seeded company, agent, and user | `getConversation` reads existing rows and `create` is called only on explicit POST (`server/src/__tests__/agent-conversations.test.ts:171`) |
| TC-8 | Committed agent messages replay once | Valid run, standard key, and responsible human | Same key and body returns a replayed receipt, and conflicting content returns conflict (`server/src/__tests__/agent-chat-messages.test.ts:141`) |
| TC-9 | Credential scope and source trust stay confined | Standard, skill test, JWT, API key, external authorizer, and task bridge actors | Only standard run authority publishes and the message keeps source trust (`server/src/__tests__/agent-chat-messages.test.ts:167`, `:175`, `:183`, `:206`) |
| TC-10 | Delivery path does not start a turn or change source status | Active chat reply and native tool delivery | HTTP and native paths publish without generic API tools or extra turns (`server/src/__tests__/agent-chat-messages.test.ts:239`, `:279`) |
| TC-11 | Concurrent first sends and rename races | Concurrent chat creation and proactive sends | One conversation is created and the committed response survives retries (`server/src/__tests__/agent-chat-messages.test.ts:64`, `:93`, `:260`) |
| TC-12 | Owed messages wait and resume | Pause, daily limit, queue error, and accepted run cancellation | Pending comments remain in order and deliver once after the hold clears (`server/src/__tests__/agent-conversation-delivery.test.ts:54`, `:94`, `:127`, `:140`) |
| TC-13 | Recovery respects retired Chat settings | Paused and saved conversations with retired off values | Saved conversations dispatch after resume and parked chats stay parked (`server/src/__tests__/issue-recovery-conversations.test.ts:13`, `:33`, `:53`) |
| TC-14 | Settlement transfers turn ownership correctly | Successful conversation turns with response or interaction artifacts | Only durable responses and interactions park a turn (`server/src/__tests__/conversation-settlement-transfer.test.ts`) |
| TC-15 | Onboarding chat creates no task or project | Onboarding user with no chat | One owner-bound chat with signup context and no early wake (`server/src/__tests__/onboarding-chat-route.test.ts:35`, `:55`, `:124`) |
| TC-16 | Onboarding privacy and greeting suppression | Other user's chat and an existing user reply | Cross-user access is denied and no welcome is queued after a reply (`server/src/__tests__/onboarding-chat-route.test.ts:77`) |
| TC-17 | Milestone work respects governed conversation state | Conversation turns with milestone notifications | Milestone work uses the current conversation identity and does not duplicate actions (`server/src/__tests__/chat-run-milestone-governed-work.test.ts`) |
| TC-18 | Native response recovery handles committed chat replies | Interrupted or retried native runs | Committed responses are recovered without a duplicate message (`server/src/services/native-runtime/agent-chat-response-recovery.test.ts`) |
| TC-19 | Conversation schema migrations enforce identity and retry uniqueness | Fresh and pre-release databases | Constraints accept valid history and reject duplicate or partial identities (`packages/db/src/agent-chat-migration.test.ts:61`, `:72`, `packages/db/src/agent-chat-messages-migration.test.ts:13`) |
| TC-20 | Reset keeps history and ordered queues | Multiple resets with concurrent delivery | History stays visible and queue entries remain separate and ordered (`server/src/__tests__/agent-conversations.test.ts:328`, `:536`) |

Files: `server/src/__tests__/agent-chat-messages.test.ts`, `server/src/__tests__/agent-conversations.test.ts`, `server/src/__tests__/agent-conversation-delivery.test.ts`, `server/src/__tests__/conversation-settlement-transfer.test.ts`, `server/src/__tests__/chat-run-milestone-governed-work.test.ts`, `server/src/__tests__/issue-recovery-conversations.test.ts`, `server/src/__tests__/onboarding-chat-route.test.ts`, `server/src/services/native-runtime/agent-chat-response-recovery.test.ts`, `packages/db/src/agent-chat-migration.test.ts`, `packages/db/src/agent-chat-messages-migration.test.ts`.

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-21 | First chat open is read-only and retries share one task | Open chat, send concurrently, retry, and inspect task state | No chat is created by open and one task serves one conversation (`tests/e2e/agent-chat-sessions.spec.ts:54`) |
| TC-22 | Stop and `/new` resume without losing history | Stop a turn, queue `/new`, and reopen the chat | New turn starts and earlier messages stay visible (`tests/e2e/agent-chat-sessions.spec.ts:164`) |
| TC-23 | Coordinator and secondary navigation keep drafts and unique chats | Switch agents and navigate through secondary chat navigation | Drafts persist, one conversation opens per agent, and layout stays stable (`tests/e2e/agent-chat-sessions.spec.ts:256`, `:293`) |
| TC-24 | Answers and digests update both chat and inbox surfaces | Answer question cards and deliver a routine digest | Both surfaces show the same answer, source link, and unread state (`tests/e2e/agent-chat-messages.spec.ts:7`, `:33`) |
| TC-25 | Project tools and handoffs persist with retry deduplication | Create a project card through the API and tool, then split a handoff | One project is created and retries do not duplicate it (`tests/e2e/agent-chat-projects.spec.ts:53`) |
| TC-26 | AgentChat page handles onboarding, stale routes, and cache scope | Visit onboarding, disabled, error, cross-company, stale, and other-account states | Greeting waits for paint, errors retry, and cached conversations stay account scoped (`ui/src/pages/AgentChat.test.tsx:60`, `:80`, `:100`, `:122`, `:133`, `:147`) |
| TC-27 | AgentChats landing chooses saved and historical chats safely | Visit with primary, unavailable, historical, inaccessible, and failed history states | Most recent valid chat opens, history is scoped, and failures show retry (`ui/src/pages/AgentChats.test.tsx:82`, `:113`, `:122`, `:148`, `:156`, `:171`) |
| TC-28 | Chat sidebar opens contacts without writing and keeps scope | Open contacts, pins, terminated history, unread counts, and 500 agents | No conversation is created before send, pins and counts stay scoped, and rendering stays stable (`ui/src/components/AgentConversationsSidebar.test.tsx:61`, `:169`, `:200`, `:237`) |
| TC-29 | Live updates carry read receipts | Receive conversation read and unread updates | UI state reflects the receipt without a stale count (`ui/src/context/LiveUpdatesProvider.read-receipts.test.ts`) |

Files: `tests/e2e/agent-chat-sessions.spec.ts`, `tests/e2e/agent-chat-messages.spec.ts`, `tests/e2e/agent-chat-projects.spec.ts`, `ui/src/pages/AgentChat.test.tsx`, `ui/src/pages/AgentChats.test.tsx`, `ui/src/components/AgentConversationsSidebar.test.tsx`, `ui/src/context/LiveUpdatesProvider.read-receipts.test.ts`.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-30 | Retry key reused with different content | Conflict instead of a second message |
| TC-31 | Cross-company actor or restricted source task | Denied before conversation or message creation and no restricted content is copied |
| TC-32 | Stale run replies after reset or cancellation | Turn and state updates are ignored |
| TC-33 | Daily limit reached while a message is saved | Message remains owed and delivers after reset |
| TC-34 | Historical agent terminated or missing from roster | Existing chat opens by id and is not offered for new chats |
| TC-35 | Conversation history request fails while active chats are loaded | Healthy chats remain usable and retry history is available |
| TC-36 | Duplicate or partial conversation identity in migration replay | Constraint rejects invalid rows and preserves valid history |
| TC-37 | More than 100 undelivered comments | Sweep processes a bounded batch of 100 per pass |

## Test Infrastructure

- Embedded Postgres test databases for conversation schema and service tests.
- Supertest Express route harness for board chat and agent chat route tests.
- Native runtime fixtures for response recovery and milestone work tests.
- jsdom React harnesses with mocked queries for AgentChat, AgentChats, sidebar, and live update tests.
- Playwright fixtures for company-scoped chat browser journeys.
- Local storage event helpers for recent chats, pins, and cross-tab clearing.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-7, TC-19 |
| FR-2 | TC-7, TC-21, TC-27 |
| FR-3 | TC-21, TC-23, TC-26, TC-30 |
| FR-4 | TC-6, TC-8, TC-9, TC-10, TC-24 |
| FR-5 | TC-2, TC-4, TC-17, TC-18 |
| FR-6 | TC-4, TC-14, TC-24, TC-32 |
| FR-7 | TC-3, TC-4, TC-20, TC-22, TC-32 |
| FR-8 | TC-11, TC-12, TC-13, TC-18, TC-33, TC-37 |
| FR-9 | TC-5, TC-28, TC-29, TC-34, TC-35 |
| FR-10 | TC-15, TC-16, TC-26 |
| FR-11 | TC-9, TC-16, TC-31, TC-36 |
| NFR-1 | TC-9, TC-16, TC-26, TC-27, TC-31 |
| NFR-2 | TC-8, TC-11, TC-19, TC-30 |
| NFR-3 | TC-5, TC-28, TC-37 |

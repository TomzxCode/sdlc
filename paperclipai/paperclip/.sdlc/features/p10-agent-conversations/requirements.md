---
title: "Agent Conversations"
status: done
---

# Requirements: Agent Conversations

## Overview

Board users and agents need a persistent in-app conversation with each agent that keeps history, routes replies back into the conversation, and links proactive task results to their source work.
This feature documents already-implemented functionality grounded in `server/src/services/agent-conversations.ts`, `server/src/services/agent-chat-messages.ts`, `server/src/services/agent-chat-read-state.ts`, `server/src/routes/issues.ts:19281`, `server/src/routes/agent-chat-messages.ts:9`, `server/src/routes/onboarding-chat.ts:30`, `ui/src/pages/AgentChat.tsx`, `ui/src/pages/AgentChats.tsx`, `ui/src/components/AgentConversationsSidebar.tsx`, and `ui/src/hooks/useAgentChatNavigation.ts`.
The conversation is stored as an issue with conversation identity columns, and each message is an issue comment.
The external provider chat connector feature is separate and is not covered here.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board user | Chat with an agent, keep history per agent, see unread replies and proactive results, and start work from a suggestion |
| Agent | Receive conversation turns with bounded history and publish task results into the owner's chat |
| Company operator | Keep all chat data company scoped, visible only to the right people, and tied to normal task permissions |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall store one conversation per company, agent, and board user as an issue with conversation identity columns. |
| FR-2 | Must | The system shall list, read, and resolve conversations by agent reference without creating a conversation on a read. |
| FR-3 | Must | The system shall let a board user send a chat message through the issue comment path with idempotency, attachments, and reopening of finished conversations. |
| FR-4 | Must | The system shall let an authenticated task run publish a proactive chat message to the responsible human with a source task link. |
| FR-5 | Must | The system shall prepare each conversation turn with conversation guidance and replay only comments inside the current session boundary. |
| FR-6 | Must | The system shall keep a conversation active while a reply is pending and park it in waiting state after a durable response or interaction. |
| FR-7 | Must | The system shall process a `/new` reset by advancing the session generation, setting a boundary comment, and keeping earlier history visible. |
| FR-8 | Must | The system shall deliver saved conversation comments in order, deduplicate retries, hold owed messages when required, and recover undelivered comments after interruption. |
| FR-9 | Should | The system shall expose unread counts, recent chats, pins, and historical agent entries in the Chat UI. |
| FR-10 | Should | The system shall provide an onboarding chat with signup context and a greeting that starts only after the chat is visible. |
| FR-11 | Must | The system shall enforce company access, actor authorization, task privacy, and activity logging for conversation reads and writes. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Conversation reads and writes shall enforce company scoping, board or task-run actor checks, issue privacy, and recipient access. |
| NFR-2 | Must | Reliability | Conversation creation, idempotent delivery, and state transitions shall use transactions, row locks, and durable comment records so retries do not duplicate work. |
| NFR-3 | Should | Performance | Conversation replay, delivery sweeps, and recent chat storage shall stay bounded by the limits implemented in the code. |

## Constraints

- Agent Chat is always on, and `enableAgentChat` is a retired compatibility key that always reads true.
- `chat_conversations` and `chat_message_links` support external chat connectors and do not store in-app agent conversations.
- Conversation identity is unique per company, agent, and user through `issues_conversation_identity_idx` in `packages/db/src/schema/issues.ts:105`.
- A board chat read never creates a conversation, and `GET /companies/:companyId/chats/:agentRef` stays read-only.
- A message body is trimmed to between 1 and 20000 characters, and an agent chat idempotency key is between 1 and 240 characters in `packages/shared/src/validators/issue.ts:1200`.
- The undelivered comment sweep is limited to 100 comments in `server/src/services/agent-conversations.ts:551`.
- Recent agent chats are capped at 50 entries in `ui/src/lib/recent-agent-chats.ts:19`.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: One conversation per agent and user
      Given a company with an agent and two board users
      When each user opens or sends to a chat with that agent
      Then each user gets one company-scoped conversation issue and the two conversations remain distinct
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Reading a chat does not create it
      Given a board user with no existing chat for an agent
      When they request that agent's chat by reference
      Then the API returns null without creating an issue or starting a run
    ```

    ```gherkin
    @FR-2
    Scenario: Ambiguous or unknown agent reference
      Given an ambiguous and an unknown agent reference
      When a board user resolves each reference
      Then the API returns conflict for the ambiguous reference and not found for the unknown reference
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Send a chat message with a retry key
      Given an open conversation with a composer draft and an attachment
      When the user sends the same client request twice
      Then the comment is stored once, the attachment is reused, and the conversation stays linked to that agent
    ```

    ```gherkin
    @FR-3
    Scenario: Send to a finished conversation
      Given a conversation with status done, cancelled, or blocked
      When the user sends another message
      Then the conversation is reopened for a new turn and earlier comments remain visible
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Agent publishes a routine result
      Given an active standard task run with a responsible human
      When the run sends a body and idempotency key to the agent chat message endpoint
      Then the agent's conversation receives one comment with a source task link and the caller gets a receipt with chatUrl and replayed
    ```

    ```gherkin
    @FR-4
    Scenario: Agent message retry and conflicting content
      Given a committed agent chat message
      When the same idempotency key is retried with the same body and then with a different body
      Then the first retry returns a replayed receipt and the second retry returns conflict
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Replay stops at the current boundary
      Given a conversation with history before and after a processed reset
      When a new turn is prepared for the current generation
      Then only current-session comments and the wake comment are replayed
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Conversation parks after a reply
      Given a conversation with a pending agent reply
      When the run succeeds with a durable response or interaction
      Then conversationState becomes waiting and the conversation remains available for the next message
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Reset keeps history and fences stale replies
      Given an active conversation with an older reply still running
      When the user sends `/new`
      Then the session generation advances, a boundary comment is recorded, earlier messages stay visible, and the older reply cannot park the reset turn
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Owed messages wait for an active reply or daily limit
      Given a saved comment while the agent is replying or at its daily limit
      When delivery is attempted
      Then the comment stays owed and is sent in order without a duplicate once the hold clears
    ```

    ```gherkin
    @FR-8
    Scenario: Recover an interrupted commit
      Given a committed comment with no matching wakeup request
      When the delivery sweep runs
      Then the undelivered comment is enqueued once with a stable idempotency key
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Sidebar shows account and company scoped state
      Given chats for two companies and unread agent replies for the current company user
      When the Chat sidebar loads
      Then it shows pins first, recent and active chats next, eligible teammates after them, and unread counts only for the current scope
    ```

    ```gherkin
    @FR-9
    Scenario: Historical and recent chats
      Given a terminated agent with an existing chat and a user revisiting several agents
      When the user browses chats
      Then the terminated agent's chat opens by id and recent visits persist up to 50 agents per company and user
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Onboarding chat and greeting
      Given a user finishing onboarding with no chat for their agent
      When the onboarding chat opens and becomes visible
      Then one owner-bound chat is created with signup context, no task, no project, and a greeting that starts only after visibility
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Cross-company and private access denied
      Given a user or agent actor from another company and a restricted source task
      When they read or write a conversation
      Then access is denied before a conversation or message is created and no restricted content is copied into the chat
    ```

    ```gherkin
    @FR-11
    Scenario: Activity logged for conversation writes
      Given an opened conversation and a sent message
      When the write commits
      Then activity entries record conversation opened and comment added with agent, run, and source task details where applicable
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Actor and privacy gates apply to every path
      Given board and task-run actors with different company memberships and issue privacy
      When they use list, resolve, comment, or proactive message endpoints
      Then only authorized and visible rows are returned and every denial includes the normal HTTP error
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Concurrent first sends create one conversation
      Given several concurrent first messages for the same agent and user
      When creation and delivery run
      Then one conversation and one comment per retry key exist and each committed message has one wakeup request
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Bounded replay and delivery work
      Given a conversation with long history and more than 100 undelivered comments
      When a turn and a delivery sweep run
      Then replay uses the current session boundary and the sweep processes at most 100 comments per pass
    ```

## Conflicts

None identified yet.

## Open Questions

1. The retirement date for the `enableAgentChat` compatibility key is not recorded in the code.
2. The product reason for keeping external connector tables named `chat_conversations` is not recorded near the in-app conversation implementation.
3. The code sets the delivery sweep limit to 100 comments, but it does not state whether that number is a product limit or an operational safeguard.

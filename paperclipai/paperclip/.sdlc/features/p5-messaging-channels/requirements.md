---
title: "Messaging channels"
status: done
---

# Requirements: Messaging channels

## Overview

External messaging channels plus board chat give every company conversational task pipelines across chat providers (Discord, Slack, Teams, Telegram, GitHub, Photon iMessage), task-bound email (AgentMail), and the Board Concierge chat relay.
Inbound messages create or continue task-bound conversations without ever granting board authority to external senders.
Outbound publications carry receipts, retries, and attachment hydration, while sender identity linking is the sole basis for authority.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Bind provider channels per company, store credentials, pause or disconnect endpoints, and review conversations and publications |
| Agent | Receive task-bound inbound messages and publish outbound replies through the assigned endpoint |
| External sender | Converse with an agent over a familiar provider without gaining any board authority |
| Board member | Ask the Board Concierge for help through the board chat UI backed by a persisted standing issue |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall bind provider channels per company with vaulted credential storage plus pause and disconnect lifecycle controls. |
| FR-2 | Must | The system shall create or continue task-bound conversations from inbound provider messages. |
| FR-3 | Must | The system shall never grant board authority to external senders. |
| FR-4 | Must | The system shall treat sender identity linking as the sole authority basis for external principals. |
| FR-5 | Must | The system shall publish outbound messages with receipts, retries, and attachment hydration. |
| FR-6 | Must | The system shall persist email send intents durably before any provider contact. |
| FR-7 | Must | The system shall never send email implicitly from internal task activity and shall surface rich status cards for correspondence and delivery outcomes. |
| FR-8 | Must | The system shall relay Board Concierge chat over SSE with action-signal stripping and a turn-tag injection guard. |
| FR-9 | Should | The system shall support automatic and explicit publication modes with board resolution of pending publications and actions. |
| FR-10 | Should | The system shall gate sensitive outbound effects behind consent flows with replayable delivery and publication recovery. |
| FR-11 | Should | The system shall support endpoint setup, resource selection, credential rotation, and health test flows per provider. |
| FR-12 | May | The system shall route agent-to-agent messages across endpoints with bounded hop limits. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | All channel operations must be company-scoped and enforce company access checks. |
| NFR-2 | Must | Security | Provider credentials must be vaulted server-side and never passed to agents. |
| NFR-3 | Should | Reliability | Inbound webhook ingress must be idempotent under provider retries and rate-limited per endpoint. |
| NFR-4 | Should | Observability | Deliveries and publications must expose redacted errors and next-attempt timestamps for diagnosis. |

## Constraints

- Every conversation belongs to exactly one endpoint, one company, and one task.
- External senders never receive board actor permissions regardless of link state.
- AgentMail endpoints are constrained to explicit publication mode with agent execution policy.
- Board chat relay spawns the local `claude` CLI and therefore runs only on local single-operator instances.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Bind a provider channel per company
      Given a company with a connection manager
      When they create a chat endpoint for a provider with credentials
      Then the endpoint is persisted company-scoped with vaulted credentials and draft status
    ```

    ```gherkin
    @FR-1
    Scenario: Pause and disconnect an endpoint
      Given an active chat endpoint
      When the operator pauses then disconnects it
      Then runtime intake stops while historical records remain and independent pause and disconnect states hold
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Inbound message creates a task-bound conversation
      Given an active endpoint with an assigned agent
      When a provider message arrives for an unknown thread
      Then a new conversation is created bound to a new task for that agent
    ```

    ```gherkin
    @FR-2
    Scenario: Inbound message continues the open task
      Given an active conversation bound to an open task
      When another provider message arrives on the same thread
      Then the message is appended to the same task instead of opening a new one
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: External sender gains no board authority
      Given an inbound message from an unlinked external sender
      When the message is processed
      Then no board actor permissions are granted and execution stays under the assigned agent's controls
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Identity linking is the sole authority basis
      Given an external principal with a pending link intent
      When the Paperclip user confirms the link token
      Then the principal is linked and telephone numbers, names, and group membership alone still grant nothing
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Outbound publication with receipt and retry
      Given a board message queued for a conversation
      When provider delivery fails transiently
      Then the publication retries with redacted errors and records the provider message id on success
    ```

    ```gherkin
    @FR-5
    Scenario: Attachment hydration on outbound send
      Given an outbound message referencing task attachments
      When the publication is delivered
      Then attachments are hydrated from task-owned files before provider contact
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Email send intent persisted before provider contact
      Given a board email send request
      When the send is queued
      Then a durable send intent with idempotency key exists before any provider call and reuse with different content conflicts
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: No implicit email sends
      Given internal task activity with no explicit send request
      When the activity completes
      Then no email leaves the instance and the thread shows rich status cards for explicit correspondence only
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Board concierge SSE relay
      Given an enabled Board Concierge on a local single-operator instance
      When the board member sends a chat message
      Then the relay streams the assistant reply over SSE and persists both turns to the standing issue
    ```

    ```gherkin
    @FR-8
    Scenario: Action signals stripped and turns guarded
      Given an assistant reply containing action signals and a user body containing a turn prefix
      When the turn is persisted and prompted
      Then action signals are stripped from storage and the user body stays inside exactly one tagged turn
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Explicit publication resolved by board
      Given a publication awaiting board resolution
      When a board user resolves it
      Then the publication proceeds or is cancelled with an audit record
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Consent-gated file delivery
      Given an outbound Teams file requiring consent
      When the recipient has not consented
      Then the file is held pending consent and replayable after resolution
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Endpoint setup and test
      Given a draft endpoint
      When the operator completes setup and runs a health test
      Then resources are selectable and the test result is reported without leaking secrets
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Bounded agent-to-agent route
      Given an enabled route between two endpoints
      When a message traverses the route
      Then delivery stops once the hop limit is reached
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Company isolation on channel access
      Given an endpoint belonging to company A
      When an actor from company B requests it
      Then access is denied
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Credentials never reach agents
      Given a vaulted provider credential
      When an agent executes a task on a bound conversation
      Then the agent receives no credential material
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Webhook retry deduplication
      Given a delivered provider event
      When the provider retries the same event
      Then the duplicate is deduplicated and no second task is created
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Redacted delivery diagnostics
      Given a failed delivery or publication
      When an operator inspects it
      Then a redacted error and next-attempt timestamp are visible with no secret material
    ```

## Conflicts

None identified yet.

## Open Questions

1. Has the Photon iMessage channel completed live-provider qualification, since the implementation docs still mark it pending and code alone cannot confirm provider-side readiness?

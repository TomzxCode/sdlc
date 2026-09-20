---
title: "Messaging channels"
status: done
---

# Test Plan: Messaging channels

## Scope

Tests cover the durable chat core (endpoints, conversations, deliveries, publications), provider intake and transport (Discord, Slack, Teams, Telegram, GitHub, Photon iMessage), task-bound email intents and threads, identity linking, attachment hydration, and the BoardChat UI.
Out of scope: outbound tool-call gateway behavior and live-provider qualification runs.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Discord bot validation and inventory | Bot tokens, guild and channel payloads | Valid identity with required channel permissions or typed rejection |
| TC-2 | Discord native commands, modals, and question forms | Command and interaction payloads | Registered commands and parsed answers |
| TC-3 | Slack receipt transport bounded | Receipt payloads | Bounded transport without unbounded processing |
| TC-4 | Slack sessions and native modals | Session and modal payloads | Session continuity and modal handling |
| TC-5 | Teams file consent foundation and contract | Consent bindings and tokens | Valid bindings, rejections on tampering, contract conformance |
| TC-6 | Teams file transfers, publication, and inline images | Transfer rows and image payloads | Consent-gated delivery with digests and hydrated images |
| TC-7 | Telegram photo, media, rich intake, ephemeral and stop flows | Photo buffers and message payloads | Bounded validation, media locators, draft-stop handling |
| TC-8 | GitHub attachments, receipts, and webhook config | Comment and attachment payloads | Exact-comment image resolution and receipt reactions |
| TC-9 | Publication pipeline (batches, errors, projection, stream, text parts, ready stream, reconciliation) | Publication rows and payloads | Retry states, redacted errors, streamed text, reconciled outcomes |
| TC-10 | Interaction arbitration and publications | Concurrent interaction payloads | Single-winner arbitration with durable publications |
| TC-11 | Provider links and task URLs | Thread ids and raw payloads | Documented HTTPS provider links or null |
| TC-12 | SDK runtime, state, and admission retry | Runtime events and lease states | Adapter handling with bounded admission retries |
| TC-13 | Chat validators | Endpoint and message schemas | Valid or rejected shared-type payloads |

Files: `server/src/services/chat-discord.test.ts`, `chat-discord-native-*.test.ts`, `chat-discord-modal-wire.test.ts`, `chat-discord-question-forms.test.ts`, `chat-discord-command-registration*.test.ts`, `chat-discord-adapter-patch.test.ts`, `chat-slack-receipts.test.ts`, `chat-slack-sessions.test.ts`, `chat-slack-native-modal.test.ts`, `chat-teams-file-consent.test.ts`, `chat-teams-file-consent.contract.test.ts`, `chat-teams-file-consent-runtime.test.ts`, `chat-teams-file-transfers.test.ts`, `chat-teams-file-publication.test.ts`, `chat-teams-inline-image*.test.ts`, `chat-teams-native-modal.test.ts`, `chat-teams-personal-recipient.test.ts`, `chat-teams-credentials.test.ts`, `chat-telegram-photo.test.ts`, `chat-telegram-media-intake.test.ts`, `chat-telegram-rich-intake.test.ts`, `chat-telegram-ephemeral*.test.ts`, `chat-telegram-draft-stop.test.ts`, `chat-telegram-stop-subscription.test.ts`, `chat-telegram-video-note.test.ts`, `chat-github-attachments.test.ts`, `chat-github-receipt-reactions.test.ts`, `chat-github-webhook-config.test.ts`, `chat-github-provider-stress.test.ts`, `chat-publication-*.test.ts`, `chat-interaction-*.test.ts`, `chat-provider-*.test.ts`, `chat-question-forms.test.ts`, `chat-run-publications.test.ts`, `chat-sdk-*.test.ts`, `chat-task-url.test.ts`, `chat-control-admission-retry.test.ts`, `chat-inbound-wakeup-publications.test.ts`, `chat-outbound-attachment-hydration.test.ts`, `packages/shared/src/validators/chat-channels.test.ts`.

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-20 | Chat channel control-plane integration | Embedded Postgres with seeded company and agent | Endpoint lifecycle, conversations, publications, and Discord registration pass |
| TC-21 | Webhook ingress and diagnostics | Endpoint with public id | Provider webhooks accepted, rate-limited, and diagnosed |
| TC-22 | Identity linking routes | Endpoint with principals | Link intents created, confirmed, previewed, and revoked |
| TC-23 | AgentMail durable email pipeline | Enabled experimental connectors with inbox | Queued intents, threads, deliveries, and uncertain resolution pass |
| TC-24 | Photon channel integration | Photon project fixture | Intake, allocation checks, and task binding pass |
| TC-25 | Heartbeat chat task links | Bound conversation with heartbeat runs | Wakeup publications attach to the bound task |

Files: `server/src/__tests__/chat-channels.integration.test.ts`, `server/src/__tests__/chat-webhook-diagnostics.test.ts`, `server/src/__tests__/chat-webhook-public-url.test.ts`, `server/src/routes/chat-channels.identity.test.ts`, `server/src/routes/chat-channels.webhook.test.ts`, `server/src/__tests__/email-channels.integration.test.ts`, `server/src/__tests__/photon/channel.integration.test.ts`, `server/src/__tests__/photon/photon.test.ts`, `server/src/__tests__/heartbeat-chat-task-link.test.ts`, `server/src/__tests__/heartbeat-reviewed-chat-binding.integration.test.ts`, `server/src/__tests__/durable-chat-wakeup.test.ts`, `server/src/services/native-runtime/external-chat-wait.integration.test.ts`.

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-30 | BoardChat staged typing and concierge flow | Open BoardChat with and without history | Typing dots, welcome reveal, and streamed concierge turns render |
| TC-31 | Runner chat flow | Drive a runner chat scenario | Task-bound chat completes end to end |
| TC-32 | Board chat route gating | Call the stream route with flags and modes | Disabled flags and remote modes return 403 with typed codes |

Files: `ui/src/pages/BoardChat.test.tsx`, `tests/runner-e2e/chat-flow.test.ts`, `server/src/__tests__/board-chat-route-feature-flag.test.ts`.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-40 | Duplicate provider webhook delivery | Second delivery deduplicated, no second task |
| TC-41 | Transient provider send failure | Publication retries with redacted error and next-attempt timestamp |
| TC-42 | Email idempotency key reused with different content | Conflict error, no second provider contact |
| TC-43 | Oversized Discord message | Response moved to a lossless file before truncation |
| TC-44 | Unconsented Teams file | File held in awaiting_consent, replayable after resolution |
| TC-45 | Board chat concurrency saturation | Fourth concurrent stream rejected with busy code |
| TC-46 | Non-local deployment board chat | Request refused as deployment-mode unsupported |

Files: `server/src/services/chat-publication-errors.test.ts`, `chat-publication-reconciliation.test.ts`, `chat-discord.test.ts`, `chat-teams-file-consent.test.ts`, `server/src/__tests__/board-chat-route-feature-flag.test.ts`, `server/src/__tests__/email-channels.integration.test.ts`.

## Test Infrastructure

- Embedded Postgres suites run through `describeEmbeddedPostgres` with graceful skip when unsupported.
- Provider transports are stubbed at the SDK boundary with receipt-transport barriers for determinism.
- Telegram photo and media tests use bounded buffers with no-throw refusal guarantees.
- UI tests use the staged typing and animation guards in `BoardChat.test.tsx`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-20, TC-21 |
| FR-2 | TC-20, TC-25 |
| FR-3 | TC-20, TC-22 |
| FR-4 | TC-22 |
| FR-5 | TC-1 through TC-12, TC-40, TC-41, TC-43 |
| FR-6 | TC-23, TC-42 |
| FR-7 | TC-23 |
| FR-8 | TC-30, TC-32, TC-45, TC-46 |
| FR-9 | TC-10, TC-20 |
| FR-10 | TC-5, TC-6, TC-44 |
| FR-11 | TC-20, TC-21 |
| FR-12 | TC-20 |
| NFR-1 | TC-20 |
| NFR-2 | TC-23 |
| NFR-3 | TC-21, TC-40 |
| NFR-4 | TC-9, TC-41 |

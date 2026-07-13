---
title: "Channel Integration"
status: done
---

# Test Plan: Channel Integration

## Scope

Tests cover the shared channel runtime (inbound event processing, message formatting, session binding) and individual channel plugin implementations. Does not cover gateway or agent runtime behavior.

## Unit Tests

| File | Description |
|---|---|
| `src/channels/plugins/message-actions.test.ts` | Message action handling |
| `src/channels/plugins/session-conversation.test.ts` | Session-to-conversation mapping |
| `src/channels/plugins/registry.test.ts` | Channel plugin registry |
| `src/channels/plugins/approvals.test.ts` | Channel approval workflows |
| `src/channels/plugins/outbound/direct-text-media.test.ts` | Direct text and media outbound delivery |
| `src/channels/plugins/outbound/interactive.test.ts` | Interactive component outbound delivery |

## Integration Tests

| File | Description |
|---|---|
| `extensions/discord/src/channel.test.ts` | Discord channel plugin integration |
| `extensions/telegram/src/channel.message-adapter.test.ts` | Telegram message adapter |
| `extensions/slack/src/channel.message-adapter.test.ts` | Slack message adapter |
| `extensions/mattermost/src/channel.test.ts` | Mattermost channel plugin integration |

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Channel disconnection | Auto-reconnect with exponential backoff |
| Platform rate limit hit | Inbound message debounced, retry queued |
| Unknown message format | Graceful degradation, error logged |
| Attachment too large | Rejected with platform-appropriate error |

## Test Infrastructure

- Vitest unit test runner
- Platform-specific test fixtures and mock servers
- In-memory session store for tests
- Channel plugin test helpers in `@openclaw/plugin-sdk`

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (Send text messages) | `direct-text-media.test.ts`, channel-specific tests |
| FR-2 (Receive messages) | Channel-specific tests |
| FR-3 (Rich formatting) | `markdown.test.ts` (Control UI), channel-specific tests |
| FR-4 (Attachments) | `direct-text-media.test.ts` |
| FR-5 (Typing indicators) | Channel-specific tests |
| FR-6 (Thread binding) | `session-conversation.test.ts` |
| FR-7 (Rate limiting) | Channel-specific tests |

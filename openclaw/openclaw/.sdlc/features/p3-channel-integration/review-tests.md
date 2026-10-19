---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Test plan review: Channel Integration

## Sync drift: 2026-10-19

Six of the ten listed test files still exist.
Three listed files no longer exist, and the FR-1 coverage row points at one of them.
Several large areas of the channel system have no listed coverage.

### Blocking: the FR-1 row points at a deleted test file

- Classification: blocking.
- Artifact says (line 20): "| `src/channels/plugins/outbound/direct-text-media.test.ts` | Direct text and media outbound delivery |"
- Artifact says (line 52): "| FR-1 (Send text messages) | `direct-text-media.test.ts`, channel-specific tests |"
- Code says: `src/channels/plugins/outbound/direct-text-media.test.ts` does not exist. The module `src/channels/plugins/outbound/direct-text-media.ts` does exist.
- Code says: the outbound contract coverage now lives in `src/channels/plugins/contracts/outbound-payload.contract.test.ts` and `src/channels/plugins/contracts/outbound-payload-testkit.ts`.
- Code says: the delivery coverage now lives in `src/channels/plugins/outbound/presentation-delivery.test.ts` and `src/channels/turn/run-channel-turn.delivery.test.ts`.
- Code says: per-channel outbound coverage lives in files such as `extensions/slack/src/outbound-adapter.test.ts`.
- Impact: the artifact points a reader at a path that returns nothing, for the only requirement row that covers outbound sending.

### Blocking: the Telegram message adapter test no longer exists

- Classification: blocking.
- Artifact says (line 28): "| `extensions/telegram/src/channel.message-adapter.test.ts` | Telegram message adapter |"
- Code says: that file does not exist.
- Code says: the Telegram coverage is now split across `extensions/telegram/src/bot-message-context.body.test.ts`, `bot-message-context.media-carriers.test.ts`, `bot-message-context.privacy.test.ts`, `bot-message-context.prompt-context.test.ts`, `bot-message-context.dm-session.test.ts`, `bot-message-context.bot-threads.test.ts`, `bot-message-dispatch-*.test.ts`, and `bot-handlers.inbound-pipeline.test.ts`.
- Impact: the artifact points a reader at a path that returns nothing.

### Blocking: the Slack message adapter test no longer exists

- Classification: blocking.
- Artifact says (line 29): "| `extensions/slack/src/channel.message-adapter.test.ts` | Slack message adapter |"
- Code says: that file does not exist.
- Code says: the Slack coverage is now split across `extensions/slack/src/outbound-adapter.test.ts`, `client-delivery.payload.test.ts`, `message-action-dispatch.test.ts`, `message-tools.test.ts`, `blocks.test.ts`, `actions.read.test.ts`, `action-threading.test.ts`, and `channel.presentation.test.ts`.
- Impact: the artifact points a reader at a path that returns nothing.

### Advisory: the coverage matrix omits four requirements and the durable ingress guarantee

- Classification: advisory.
- Artifact says (lines 50-58): the matrix covers FR-1 through FR-7.
- Artifact says: FR-8, FR-9, FR-10, and NFR-1 have no row.
- Code says: FR-8 and FR-10 are covered in `src/channels/plugins/message-action-dispatch.registry.test.ts` and `src/channels/plugins/message-action-dispatch.write-authority.test.ts`, and `src/channels/plugins/outbound/interactive.test.ts`.
- Code says: NFR-1 is covered in `src/channels/channel-health-monitor.test.ts` and `src/channels/channel-health-policy.test.ts`.
- Code says: the durable ingress guarantee is covered in `src/channels/message/ingress-drain.test.ts`, `ingress-drain-lifecycle.test.ts`, `ingress-drain-supersede.test.ts`, `ingress-drain.watchdog.test.ts`, `ingress-claim-owner.test.ts`, `ingress-retry-policy.test.ts`, and `ingress-monitor.admission.test.ts`.
- Impact: the map is incomplete rather than wrong.

### Advisory: the FR-3 row points at a Control UI test for a channel requirement

- Classification: advisory.
- Artifact says (line 54): "| FR-3 (Rich formatting) | `markdown.test.ts` (Control UI), channel-specific tests |"
- Code says: `ui/src/components/markdown.test.ts` exists and covers the Control UI renderer, not the channel formatting path.
- Code says: the per-channel markdown coverage lives in `extensions/discord/src/markdown.test.ts` and `extensions/feishu/src/markdown.test.ts`.
- Impact: the parenthetical names a file that does not cover the channel side of the requirement.

### Advisory: the Test Infrastructure section does not mention the durable ingress fixtures

- Classification: advisory.
- Artifact says (line 45): "- In-memory session store for tests"
- Artifact says (line 46): "- Channel plugin test helpers in `@openclaw/plugin-sdk`"
- Code says: `src/channels/plugins/contracts/inbound-testkit.ts` and `src/channels/plugins/contracts/outbound-payload-testkit.ts` are the shared channel contract test kits, and `src/channels/message/ingress-drain.test-helpers.ts` and `src/channels/message/ingress-monitor.test-harness.ts` are the ingress harnesses.
- Impact: the infrastructure description omits the harnesses a new channel test would use.

### Advisory: large channel areas have no listed coverage

- Classification: advisory.
- Artifact says (lines 12-30): the plan lists six unit files and four integration files.
- Code says: `src/channels/` holds well over 1,000 test files, and `extensions/` adds one or more per channel.
- Code says: unlisted but notable areas include the sender admission decision in `src/channels/message-access/message-access.test.ts` and `src/channels/message-access/identifier-authentication.test.ts`.
- Code says: unlisted but notable areas include the pairing adapters in `src/channels/plugins/pairing-adapters.test.ts` and the pairing store in `src/pairing/pairing-store.test.ts`.
- Code says: unlisted but notable areas include the channel contract shards in `src/channels/plugins/contracts/plugin.registry-backed-shard-a.contract.test.ts` through `plugin.registry-backed-shard-h.contract.test.ts`.
- Code says: unlisted but notable areas include the per-turn delivery suite in `src/channels/turn/run-channel-turn.*.test.ts` and `src/channels/turn/durable-delivery.test.ts`.
- Impact: the plan under-represents the channel system by a wide margin, which matters for future coverage planning.

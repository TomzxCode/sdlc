---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-16

The test plan was reverse-engineered from the code and was last reviewed on 2026-10-19.
A fresh analysis on 2026-11-16 confirms the deleted test files and coverage gaps recorded then.
It also finds that four paths cited in the 2026-10-19 review no longer exist.
The artifacts were not edited during this sync, so every finding from 2026-10-19 still stands.

### Blocking: the FR-1 row still points at a deleted test file

- Classification: blocking.
- Artifact says (lines 20 and 52): `src/channels/plugins/outbound/direct-text-media.test.ts` is listed as unit coverage and as the FR-1 coverage row.
- Code says: that test file does not exist, while the module `src/channels/plugins/outbound/direct-text-media.ts` does.
- Code says: outbound coverage now lives in `src/channels/plugins/contracts/outbound-payload.contract.test.ts` and `src/channels/plugins/outbound/presentation-delivery.test.ts`.
- Impact: the reader still follows a path that returns nothing.

### Blocking: the Telegram and Slack message adapter tests are still missing

- Classification: blocking.
- Artifact says (lines 28-29): `channel.message-adapter.test.ts` is listed for Telegram and Slack.
- Code says: neither file exists.
- Code says: Telegram coverage is now split across `extensions/telegram/src/bot-message-context.*.test.ts` and `bot-message-dispatch-*.test.ts`, and Slack coverage across `extensions/slack/src/outbound-adapter.test.ts`, `client-delivery.payload.test.ts`, `message-action-dispatch.test.ts`, and `channel.presentation.test.ts`.
- Impact: two listed integration files still resolve to nothing.

### Advisory (new): four coverage paths cited in the 2026-10-19 review no longer exist

- Classification: advisory.
- Prior review says: NFR-1 was covered in `src/channels/channel-health-monitor.test.ts` and `src/channels/channel-health-policy.test.ts`.
- Prior review says: FR-8 and FR-10 were covered in `src/channels/plugins/message-action-dispatch.write-authority.test.ts`, and pairing-store coverage in `src/pairing/pairing-store.test.ts`.
- Code says: none of those four files exists.
- Code says: health and retry coverage now lives in `src/channels/message/ingress-queue-health.test.ts`, `ingress-queue-health.kernel.ts`, and `ingress-retry-policy.test.ts`.
- Code says: the dispatch suite now has only `message-action-dispatch.registry.test.ts`, and pairing coverage is split across `pairing-store-keys.test.ts`, `pairing-store.worker.test.ts`, and `pairing-allowlist.*.test.ts` under `src/pairing/`.
- Impact: four coverage pointers in the prior drift record are now stale and need correction before the next review.

### Advisory: the coverage matrix still omits FR-8 through FR-10 and NFR-1

- Classification: advisory.
- Artifact says (lines 50-58): the matrix covers FR-1 through FR-7 only.
- Code says: the missing requirements are covered in `message-action-dispatch.registry.test.ts`, `outbound/interactive.test.ts`, `ingress-queue-health.test.ts`, and the ingress suites.
- Impact: the map is incomplete rather than wrong.

### Advisory: the FR-3 row still points at a Control UI test

- Classification: advisory.
- Artifact says (line 54): FR-3 is covered in `markdown.test.ts` from the Control UI.
- Code says: `ui/src/components/markdown.test.ts` covers the Control UI renderer, while channel markdown coverage lives in `extensions/discord/src/markdown.test.ts` and `extensions/feishu/src/markdown.test.ts`.
- Impact: the parenthetical still names a file that does not cover the channel side.

### Advisory: the Test Infrastructure section still omits the ingress harnesses

- Classification: advisory.
- Artifact says (lines 43-46): the section lists Vitest, mock servers, an in-memory session store, and SDK test helpers.
- Code says: `src/channels/plugins/contracts/inbound-testkit.ts`, `outbound-payload-testkit.ts`, `src/channels/message/ingress-drain.test-helpers.ts`, and `ingress-monitor.test-harness.ts` are the harnesses a new channel test would use.
- Impact: the description still omits the ingress harnesses.

### Advisory: large channel areas remain unlisted

- Classification: advisory.
- Artifact says (lines 12-30): the plan lists six unit files and four integration files.
- Code says: `src/channels/` holds well over 1,000 test files, and `extensions/` adds more per channel.
- Code says: unlisted areas include `src/channels/message-access/message-access.test.ts`, `identifier-authentication.test.ts`, `src/channels/plugins/pairing-adapters.test.ts`, and the `plugin.registry-backed-shard-*.contract.test.ts` files.
- Impact: the plan still under-represents the channel system by a wide margin.

## Sync drift: 2026-11-23

A fresh analysis against current code confirms the deleted paths and coverage gaps recorded earlier.
The test plan was not edited during this sync, so those findings remain open.

### Blocking: the FR-1 row still points at a deleted test file

- Classification: blocking.
- Artifact says (lines 20 and 52): `src/channels/plugins/outbound/direct-text-media.test.ts` is listed as unit coverage and as the FR-1 coverage row.
- Code says: that test file does not exist, while `src/channels/plugins/outbound/direct-text-media.ts` does.
- Code says: outbound contract coverage now lives in `src/channels/plugins/contracts/outbound-payload.contract.test.ts:1`, and delivery coverage in `src/channels/plugins/outbound/presentation-delivery.test.ts:1` and `src/channels/turn/run-channel-turn.delivery.test.ts:1`.
- Impact: the reader still follows a path that returns nothing.

### Blocking: the Telegram and Slack message adapter tests are still missing

- Classification: blocking.
- Artifact says (lines 28-29): `channel.message-adapter.test.ts` is listed for Telegram and Slack.
- Code says: neither file exists.
- Code says: Telegram coverage is split across `extensions/telegram/src/bot-message-context.*.test.ts` and `extensions/telegram/src/bot-handlers.inbound-pipeline.test.ts:1`, and Slack coverage across `extensions/slack/src/outbound-adapter.test.ts:1`, `extensions/slack/src/outbound-payload.test.ts:1`, `extensions/slack/src/message-action-dispatch.test.ts:1`, and `extensions/slack/src/channel.presentation.test.ts:1`.
- Impact: two listed integration files still resolve to nothing.

### Advisory (new): a replacement pointer from the 2026-10-19 review is now stale

- Classification: advisory.
- Prior review says (lines 40 and 100): Slack payload coverage lives in `extensions/slack/src/client-delivery.payload.test.ts`.
- Code says: that file does not exist, while `extensions/slack/src/outbound-payload.test.ts:1` and `extensions/slack/src/client-delivery.upload.test.ts:17` do.
- Impact: the drift record itself now needs correction before the next review.

### Advisory: the four pointers flagged on 2026-11-16 remain missing

- Classification: advisory.
- Prior review says (lines 106-107): `src/channels/channel-health-monitor.test.ts`, `src/channels/channel-health-policy.test.ts`, `src/channels/plugins/message-action-dispatch.write-authority.test.ts`, and `src/pairing/pairing-store.test.ts` held coverage.
- Code says: none of those four files exists.
- Code says: health and retry coverage now lives in `src/channels/message/ingress-queue-health.test.ts:1` and `src/channels/message/ingress-retry-policy.test.ts:1`, and pairing coverage in `src/pairing/pairing-store-keys.test.ts:1`, `src/pairing/pairing-store.worker.test.ts:1`, and `src/pairing/pairing-allowlist.lifecycle.test.ts:1`.
- Impact: four drift-record pointers are still stale.

### Advisory: the coverage matrix and infrastructure description remain incomplete

- Classification: advisory.
- Artifact says (lines 50-58): the matrix covers FR-1 through FR-7 only, and lines 43-46 list generic infrastructure.
- Code says: `src/channels/plugins/message-action-dispatch.registry.test.ts:1`, `src/channels/plugins/outbound/interactive.test.ts:1`, and the ingress suites cover FR-8 through FR-10 and NFR-1.
- Code says: `src/channels/plugins/contracts/inbound-testkit.ts:1`, `src/channels/plugins/contracts/outbound-payload-testkit.ts:1`, `src/channels/message/ingress-drain.test-helpers.ts:1`, and `src/channels/message/ingress-monitor.test-harness.ts:1` are the harnesses a new channel test would use.
- Code says: `src/channels/` now holds 224 `*.test.ts` files, including `src/channels/message-access/message-access.test.ts:1`, `src/channels/plugins/pairing-adapters.test.ts:1`, and eight `plugin.registry-backed-shard-*.contract.test.ts` files under `src/channels/plugins/contracts/`.
- Impact: the plan still under-represents the channel system by a wide margin.

### Advisory: the FR-3 row still points at a Control UI test

- Classification: advisory.
- Artifact says (line 54): FR-3 is covered in `markdown.test.ts` from the Control UI.
- Code says: `ui/src/components/markdown.test.ts:1` covers the Control UI renderer, while channel markdown coverage lives in `extensions/discord/src/markdown.test.ts:1` and `extensions/feishu/src/markdown.test.ts:1`.
- Impact: the parenthetical still names a file that does not cover the channel side.

---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Specification review: Channel Integration

## Sync drift: 2026-10-19

The specification was reverse-engineered from the code on 2026-10-13.
The code has moved on.
Every finding below is classified as blocking or advisory.

### Blocking: the ChannelMessage data model does not match the durable ingress record

- Classification: blocking.
- Artifact says (lines 31-40): a `ChannelMessage` table with `messageId` as PK, `channelId`, `sessionId` as a NOT NULL foreign key, `text`, `attachments` JSON, and `timestamp`.
- Code says: `src/state/openclaw-state-schema.sql:1273-1294` defines `channel_ingress_events` with a composite primary key of `(queue_name, event_id)` and columns `channel_id`, `account_id`, `status`, `lane_key`, `payload_json`, `metadata_json`, `received_at`, `updated_at`, `claim_token`, `claim_owner`, `claimed_at`, `attempts`, `last_attempt_at`, `last_error`, `failed_reason`, `failed_at`, `completed_at`, and `completed_metadata_json`.
- Code says: `src/channels/message/ingress-queue.types.ts:4-14` scopes every record by `ChannelIngressScope`, which is `{ channelId, accountId, queueName }` per `:267`.
- Code says: the session is bound at turn adoption, not at receive time, and completed rows are tombstoned rather than deleted, per the Durable Ingress rules in `src/channels/AGENTS.md`.
- Code says: there is no `text` column and no `attachments` column, because the whole normalized envelope is carried in `payload_json`.
- Impact: a reader would model a message row that does not exist, would assume the session is known on arrival, and would miss the claim, retry, and tombstone columns that carry the durability contract.

### Blocking: the Message Receive Flow omits the durable ingress lifecycle

- Classification: blocking.
- Artifact says (lines 46-52): "Platform → Channel Plugin: webhook/poll", "Channel Plugin → Channel Runtime: normalized envelope", "Channel Runtime → Gateway: route to agent session", "Agent → Channel Runtime: response with text + attachments", "Channel Runtime → Channel Plugin: formatted response", "Channel Plugin → Platform: send message".
- Code says: `src/channels/message/ingress-drain.ts` drains a durable queue, `src/channels/message/ingress-monitor.ts` monitors it, `src/channels/message/ingress-claim-owner.ts` owns the claim lease, and `src/channels/message/ingress-retry-policy.ts` owns the retry disposition.
- Code says: `src/channels/AGENTS.md` states that completion happens at turn adoption, that deferred holds the claim with the watchdog armed, and that a transient failure releases or fails the row by disposition rather than completing it.
- Code says: `src/channels/turn/run-channel-turn.ts` and `src/channels/turn/durable-delivery.ts` own the outbound side, and `src/channels/turn/pending-delivery-notice.ts` owns the pending-delivery notice.
- Impact: the sequence in the artifact has no durable step between the platform and the agent, so a reader would not know that inbound messages are persisted, leased, and retried before an agent turn adopts them.

### Blocking: the architecture tree omits the contract owner and mislabels the message directory

- Classification: blocking.
- Artifact says (lines 16-23): the tree lists `inbound-event/`, `message/` described as "message formatting and delivery", `status/`, `transport/`, and `turn/`.
- Code says: `src/channels/AGENTS.md` names the public contract as `src/channels/plugins/types.{plugin,core,adapters}.ts`, and `src/channels/plugins/` also holds the plugin registry, the bundled channel catalog, the config write policy, and the gateway auth bypass, none of which the tree shows.
- Code says: the tree omits `src/channels/message-access/`, which owns the inbound admission decision, `src/channels/allowlists/`, which owns allowlist resolution, and `src/channels/join-intro/`, which owns room-join reporting.
- Code says: `src/channels/message/` no longer holds only formatting and delivery. It holds the durable ingress queue, the ingress monitor, the durable receive journal, the outbound bridge, and the outbound echo state, per the file listing of `src/channels/message/`.
- Impact: the tree points an implementer at the wrong directory for the two hardest parts of the channel system, the contract and the ingress guarantee.

### Advisory: the plugin contract owner is stated indirectly

- Classification: advisory.
- Artifact says (line 59): "| Plugin contract | Channel SDK interface in `@openclaw/plugin-sdk` | Consistent integration seam for all channels |"
- Code says: the canonical types live in `src/channels/plugins/types.plugin.ts`, `types.core.ts`, `types.adapters.ts`, `types.config.ts`, `types.public.ts`, and `types.conversation-bindings.ts`, and `@openclaw/plugin-sdk` re-exports them, for example `src/plugin-sdk/channel-contract.ts:28-45` and `src/plugin-sdk/channel-plugin-common.ts:4`.
- Impact: the statement is not false. It names the wrong owner.

### Advisory: the contract is now a set of optional adapter surfaces, not one interface

- Classification: advisory.
- Artifact says (line 10): "Each channel is a self-contained plugin under `extensions/<channel-name>/` that implements the channel contract. The channel system in `src/channels/` provides the shared runtime: inbound event handling, draft streaming, typing indicators, session binding, and message access control."
- Code says: `src/channels/plugins/types.plugin.ts:45-` defines `ChannelPlugin` as roughly twenty optional adapter surfaces, each independently implemented, and `src/channels/plugins/channel-runtime-surface.types.ts` models the runtime surface a plugin actually exposes.
- Impact: granularity. The single-interface phrasing hides which capabilities are mandatory and which are optional.

### Advisory: the Technical Decisions table omits the durable ingress decision

- Classification: advisory.
- Artifact says (lines 57-62): the table lists the plugin contract, streaming, thread binding, and attachment handling.
- Code says: the durable ingress decision, the claim and retry lifecycle, and the closed action vocabulary are absent from the table.
- Impact: the table is incomplete rather than wrong.

### Advisory: the streaming decision still holds

- Classification: advisory.
- Artifact says (line 60): "| Streaming | Chunked draft delivery via draft-stream-loop | Responsive UX; channels display text incrementally |"
- Code says: `src/channels/draft-stream-loop.ts` and `src/channels/draft-stream-controls.ts` still own chunked draft delivery, and `src/channels/plugins/types.core.ts:302-307` still exposes `ChannelStreamingAdapter` for coalescing defaults.
- Impact: no drift. Recorded so the next sync does not re-open it.

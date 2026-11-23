---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-16

The specification was reverse-engineered from the code and was last reviewed on 2026-10-19.
A fresh analysis on 2026-11-16 confirms the recorded drift is unchanged.
The artifacts were not edited during this sync, so every finding from 2026-10-19 still stands.
The schema line numbers recorded in the 2026-10-19 review have since shifted.

### Blocking: the ChannelMessage data model still does not match the durable ingress record

- Classification: blocking.
- Artifact says (lines 31-40): a `ChannelMessage` table with `messageId` as PK, `channelId`, `sessionId` as a NOT NULL foreign key, `text`, `attachments` JSON, and `timestamp`.
- Code says: `src/state/openclaw-state-schema.sql:1254-1276` defines `channel_ingress_events` with a composite key of `(queue_name, event_id)`, claim, attempt, and completion columns, and no `text` or `attachments` column.
- Code says: `src/channels/message/ingress-queue.types.ts:4-14` scopes records by `ChannelIngressScope` as `{ channelId, accountId, queueName }`, and the session is bound at turn adoption.
- Note: the table now sits at lines 1254-1276, up from lines 1273-1294 in the 2026-10-19 review, and the pairing tables moved from lines 777 and 794 to lines 758 and 775.
- Impact: a reader would model a row that does not exist and miss the columns that carry the durability contract.

### Blocking: the Message Receive Flow still omits the durable ingress lifecycle

- Classification: blocking.
- Artifact says (lines 46-52): the sequence moves from a normalized envelope straight to routing at the gateway.
- Code says: `src/channels/message/ingress-drain.ts`, `ingress-monitor.ts`, `ingress-claim-owner.ts`, and `ingress-retry-policy.ts` persist, lease, and retry inbound events before `src/channels/turn/run-channel-turn.ts` adopts them.
- Impact: the sequence still hides the durability step between the platform and the agent.

### Blocking: the architecture tree still omits the contract owner and mislabels the message directory

- Classification: blocking.
- Artifact says (lines 16-23): the tree lists `inbound-event/`, `message/` as formatting and delivery, `status/`, `transport/`, and `turn/`.
- Code says: `src/channels/plugins/` holds the public contract in `types.plugin.ts`, `types.core.ts`, and `types.adapters.ts`, plus the registry, catalog, and config write policy, while `src/channels/message-access/` and `src/channels/allowlists/` own inbound admission.
- Code says: `src/channels/message/` now holds the durable ingress queue and monitor, not only formatting and delivery.
- Impact: the tree still points an implementer at the wrong directories for the contract and the ingress guarantee.

### Advisory: the plugin contract owner is still stated indirectly

- Classification: advisory.
- Artifact says (line 59): the plugin contract is a Channel SDK interface in `@openclaw/plugin-sdk`.
- Code says: the canonical types live in `src/channels/plugins/types.*.ts`, and `@openclaw/plugin-sdk` re-exports them from `src/plugin-sdk/channel-contract.ts` and `channel-plugin-common.ts`.
- Impact: the statement is not false, but it names the re-export rather than the owner.

### Advisory: the contract is still a set of optional adapter surfaces

- Classification: advisory.
- Artifact says (line 10): each channel plugin implements one channel contract.
- Code says: `src/channels/plugins/types.plugin.ts` defines `ChannelPlugin` as roughly twenty optional adapter surfaces, and `src/channels/plugins/channel-runtime-surface.types.ts` models the surface a plugin actually exposes.
- Impact: the single-interface phrasing still hides which capabilities are mandatory.

### Advisory: the Technical Decisions table still omits the durable ingress decision

- Classification: advisory.
- Artifact says (lines 57-62): the table lists the plugin contract, streaming, thread binding, and attachment handling.
- Code says: the durable ingress decision, the claim and retry lifecycle, and the closed action vocabulary are absent from the table.
- Impact: the table is incomplete rather than wrong.

## Sync drift: 2026-11-23

A fresh analysis against current code confirms the recorded drift stands.
The specification was not edited during this sync, so those findings remain open.

### Blocking: the ChannelMessage data model still does not exist in the schema

- Classification: blocking.
- Artifact says (lines 31-40): a `ChannelMessage` table with `messageId` as PK, `channelId`, `sessionId` as a NOT NULL foreign key, `text`, `attachments` JSON, and `timestamp`.
- Code says: `src/state/openclaw-state-schema.sql:1255-1277` defines `channel_ingress_events` with composite key `(queue_name, event_id)`, channel and account ids, status, lane key, payload and metadata JSON, claim columns, attempt columns, and completion columns, and no `text` or `attachments` column.
- Code says: `src/channels/message/ingress-queue.types.ts:4-25` scopes every record by channel id, account id, and queue name and carries the whole envelope in `payload`.
- Code says: `src/channels/AGENTS.md:19-26` requires completion at turn adoption, tombstoning, and a claim refresh heartbeat.
- Impact: a reader would model a row that does not exist and miss the durability contract.

### Blocking: the receive flow still omits durable ingress

- Classification: blocking.
- Artifact says (lines 46-52): the sequence moves from a normalized envelope straight to gateway routing.
- Code says: `src/channels/message/ingress-drain.ts`, `ingress-monitor.ts`, `ingress-claim-owner.ts`, and `ingress-retry-policy.ts` persist, lease, and retry inbound events before `src/channels/turn/run-channel-turn.ts` adopts them.
- Code says: `src/channels/turn/durable-delivery.ts` and `src/channels/turn/pending-delivery-notice.ts` own the outbound side.
- Impact: the sequence still hides the durable step between platform and agent.

### Blocking: the architecture tree still names the wrong owners

- Classification: blocking.
- Artifact says (lines 16-23): the tree lists `inbound-event/`, `message/` as formatting and delivery, `status/`, `transport/`, and `turn/`.
- Code says: `src/channels/AGENTS.md:9-11` names the public contract as `src/channels/plugins/types.{plugin,core,adapters}.ts`.
- Code says: `src/channels/plugins/types.plugin.ts:69-126` holds roughly twenty optional adapter surfaces, and `src/channels/plugins/` also holds the registry, catalog, and config write policy.
- Code says: `src/channels/message-access/` and `src/channels/allowlists/` own inbound admission, while `src/channels/message/` holds the durable ingress queue and monitor.
- Impact: the tree still points an implementer at the wrong directories for the contract and the ingress guarantee.

### Advisory: the plugin contract owner and adapter granularity are still imprecise

- Classification: advisory.
- Artifact says (line 59): the plugin contract is a Channel SDK interface in `@openclaw/plugin-sdk`.
- Code says: `src/plugin-sdk/channel-plugin-common.ts:4` and `src/plugin-sdk/channel-contract.ts:28-45` re-export types owned by `src/channels/plugins/types.*.ts`.
- Code says: `src/channels/plugins/channel-runtime-surface.types.ts:40` models the actual runtime surface because `ChannelPlugin` adapters are optional.
- Impact: the statement is not false, but it names the re-export rather than the owner and hides which capabilities are mandatory.

### Advisory: the Technical Decisions table is still incomplete and one pointer moved

- Classification: advisory.
- Artifact says (lines 57-62): the table lists the plugin contract, streaming, thread binding, and attachment handling, and the prior review at line 69 cites `types.core.ts:302-307` for streaming.
- Code says: `src/channels/plugins/types.core.ts:286` now defines `ChannelStreamingAdapter`, and `src/channels/draft-stream-loop.ts` with `draft-stream-controls.ts` still owns chunked draft delivery.
- Code says: the durable ingress decision, claim and retry lifecycle, and closed action vocabulary remain absent from the table.
- Impact: the streaming decision holds, the line pointer is stale, and the table is incomplete rather than wrong.

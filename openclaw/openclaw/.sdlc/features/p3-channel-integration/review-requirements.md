---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Requirements review: Channel Integration

## Sync drift: 2026-10-19

The requirements were reverse-engineered from the code on 2026-10-13.
The code has moved on.
Every finding below is classified as blocking or advisory.

### Blocking: no requirement covers the durable inbound delivery guarantee

- Classification: blocking.
- Artifact says (lines 22-32): the functional requirement table covers sending, receiving, rich formatting, attachments, typing indicators, thread binding, rate limiting and debouncing, editing and deletion, voice, and reactions and interactive components. None of them states an inbound delivery durability guarantee.
- Artifact says (line 38): "| NFR-1 | Must | Reliability | Channel connection shall auto-recover with exponential backoff on disconnect |"
- Code says: `src/channels/AGENTS.md` names a "Durable Ingress" section owned by `src/channels/message/ingress-drain.ts` and `ingress-monitor.ts` plus `ingress-claim-owner.ts` and `ingress-retry-policy.ts`.
- Code says: `src/channels/message/ingress-queue.types.ts:4-14` defines a queue record with `attempts`, `lastAttemptAt`, `lastError`, and a `claim` holding `token`, `ownerId`, and `claimedAt`.
- Code says: `src/state/openclaw-state-schema.sql:1273-1294` stores the queue in `channel_ingress_events` with `status`, `lane_key`, `claim_token`, `claim_owner`, `claimed_at`, `attempts`, `last_error`, `failed_reason`, `completed_at`, and `completed_metadata_json`.
- Code says: `src/channels/AGENTS.md` requires completion to tombstone rather than delete, completion at turn adoption rather than settle, an attempt floor of 8 and an age gate of 24 hours, a claim refresh heartbeat, and no silent completion on transient failure.
- Impact: the requirements describe inbound delivery as an in-process hand-off. The code ships a durable, leased, retried, tombstoned ingress pipeline, and a reader would not know that inbound messages survive a gateway restart.

### Blocking: no requirement covers sender access control

- Classification: blocking.
- Artifact says (lines 36-39): the non-functional requirements cover only reliability and credential secrecy, with "| NFR-2 | Must | Security | Channel credentials shall be stored securely and never logged |".
- Artifact says (line 45): "- Must handle platform-specific rate limits gracefully"
- Code says: `src/channels/message-access/` owns the admission decision with `allowlist.ts`, `effective-allow-from.ts`, `dm-allow-state.ts`, `identifier-authentication.ts`, `sender-gates.ts`, `runtime-access-groups.ts`, `decision.ts`, and `admission-evidence.ts`.
- Code says: `src/channels/allow-from.ts:18` merges configured DM allowFrom entries with pairing-store sender ids when policy allows it.
- Code says: `src/channels/direct-dm-access.ts:34-58` resolves legacy direct-DM access lists, pairing-store entries, and command authorization, and can return a `pairing` decision.
- Code says: `src/channels/mention-gating.ts` and `src/channels/command-gating.ts` gate mentions and commands independently of the allowlist.
- Code says: `src/pairing/` owns the pairing store, join codes, and challenges, and `src/state/openclaw-state-schema.sql:777` and `:794` define `channel_pairing_requests` and `channel_pairing_allow_entries`.
- Code says: `src/config/types.access-groups.ts` and `docs/channels/access-groups.md` add named sender groups referenced as `accessGroup:<name>` from channel allowlists.
- Code says: `docs/channels/pairing.md` documents DM pairing as the explicit access approval step, including the one-hour code expiry and the three-pending-requests cap per channel account.
- Impact: the requirements never state who may talk to the assistant. A reader would take NFR-2 to be the whole security story and would miss the allowlist, DM policy, pairing, access group, mention, and command gating layers.

### Blocking: FR-1 and FR-2 say "all integrated channels" but no requirement defines the channel set or its capabilities

- Classification: blocking.
- Artifact says (line 23): "| FR-1 | Must | The system shall support sending text messages across all integrated channels |"
- Artifact says (line 24): "| FR-2 | Must | The system shall support receiving messages from all integrated channels |"
- Artifact says (line 62, Open Questions): "2. Should there be a channel capability discovery mechanism?"
- Code says: the bundled channel set is generated into `src/channels/bundled-channel-ids.generated.ts`, which lists 28 channel ids, and `src/channels/ids.ts:7-30` derives the order and aliases from it.
- Code says: `scripts/lib/official-external-channel-catalog.json` lists 29 official external channel plugin packages, five of which are not bundled, so 33 distinct official channel plugins are reachable.
- Code says: `src/channels/plugins/types.plugin.ts:45-` defines the channel plugin contract as roughly twenty optional adapter surfaces, including `ChannelAuthAdapter`, `ChannelConfigAdapter`, `ChannelOutboundAdapter`, `ChannelPairingAdapter`, `ChannelSecurityAdapter`, `ChannelStatusAdapter`, `ChannelAllowlistAdapter`, `ChannelStreamingAdapter`, `ChannelThreadingAdapter`, and `ChannelMessageActionAdapter`.
- Code says: `src/channels/plugins/channel-runtime-surface.types.ts` and `src/agents/tools/manifest-capability-availability.ts` expose which surfaces a given plugin actually implements.
- Code says: `src/channels/plugins/message-action-names.ts:62-` defines a closed core-owned vocabulary of 56 channel message actions with per-action read, send, and write policies.
- Impact: the open question has effectively been answered by the code, and the requirements describe a uniform channel surface that the per-plugin optional surfaces do not provide.

### Advisory: the "30+ messaging platforms" claim is unanchored

- Classification: advisory.
- Artifact says (line 10): "provides a unified abstraction for sending and receiving messages across 30+ messaging platforms."
- Code says: `extensions/` holds 175 extension directories, 171 of which have a package.json, and 28 of those declare `openclaw.channel` in their manifest.
- Code says: `docs/channels/` holds 56 pages covering the bundled channels plus the external-only channels, including `qqbot.md`, `wechat.md`, `wecom.md`, `yuanbao.md`, and `zaloclawbot.md`.
- Impact: the number still holds. The artifact gives no source of truth for the channel set.

### Advisory: FR-7 conflates two separate inbound control mechanisms

- Classification: advisory.
- Artifact says (line 29): "| FR-7 | Must | The system shall support rate limiting and debouncing of inbound messages |"
- Code says: `src/channels/inbound-debounce-policy.ts` owns the inbound debounce policy, and `src/channels/message/ingress-retry-policy.ts` owns the durable ingress retry policy with an attempt floor and an age gate.
- Impact: the requirement is satisfied. Naming both policies would be more precise.

### Advisory: FR-8 through FR-10 are stated without the action vocabulary that now implements them

- Classification: advisory.
- Artifact says (line 30): "| FR-8 | Should | The system shall support message editing and deletion where the platform allows |"
- Artifact says (line 31): "| FR-9 | Should | The system shall support voice message sending |"
- Artifact says (line 32): "| FR-10 | May | The system shall support reactions and interactive components (buttons, select menus) |"
- Code says: `src/channels/plugins/message-action-names.ts:62-` is the closed, core-owned vocabulary of 56 actions, including `edit`, `delete`, `unsend`, `react`, `poll`, `pin`, `sticker`, `thread-create`, and `upload-file`.
- Code says: `src/channels/plugins/message-action-dispatch.ts` dispatches those actions with a write-authority path, and `src/channels/plugins/message-action-discovery.ts` discovers them.
- Impact: the requirements are satisfied. They would be more precise if they named the shared action vocabulary that replaces per-plugin behavior.

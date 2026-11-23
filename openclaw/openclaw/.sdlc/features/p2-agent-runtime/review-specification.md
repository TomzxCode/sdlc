---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Specification review: Agent Runtime

## Sync drift: 2026-10-19

The specification was reverse-engineered from the code on 2026-10-13.
The code has moved on.
Every finding below is classified as blocking or advisory.

### Blocking: the TranscriptTurn data model does not match the transcript store

- Classification: blocking.
- Artifact says (lines 29-38): a `TranscriptTurn` table with `turnId` as PK, `sessionId` as FK, `role`, `content` JSON, `timestamp`, and `tokenCount`.
- Code says: `src/state/openclaw-agent-schema.sql:437-484` defines `transcript_events` with a composite primary key of `(session_id, seq)`.
- Code says: that table stores `event_json` or a zstd-compressed `event_zstd` blob with `event_utf8_bytes`, plus `navigation_json`, `navigation_type`, `navigation_custom_type`, `navigation_display`, `message_role`, `navigation_last_type`, `navigation_last_custom_type`, and `navigation_valid`.
- Code says: there is no `turnId` column and no `tokenCount` column.
- Code says: `src/agents/AGENTS.md:15` states that transcript messages are appended only through awaited `SessionManager.appendMessageAsync`, which assigns `parentId` and persists.
- Code says: `src/state/openclaw-agent-schema.sql:486` adds `session_transcript_archives` and `:511` adds `session_transcript_cold_archives` for reclaimed generations.
- Impact: a reader would model a turn table that does not exist and would miss the navigation, compression, and archive layers that own transcript reads today.

### Blocking: the architecture diagram omits the context engine, the provider plugin layer, and the worker-backed store

- Classification: blocking.
- Artifact says (lines 14-25): "Channel Plugin → Agent Runtime → Model Provider Transport" branching to "Tool Executor", "Stream Handler", "Policy Enforcer", "Response Composer", and "SQLite Store (Transcripts)".
- Code says: `src/context-engine/` is a separate owner that mediates context assembly between the runtime and the model, and `src/agents/harness/context-engine-*.ts` binds it into the turn.
- Code says: `src/plugins/registry-registrars-providers.ts` and `src/plugins/provider-catalog.ts` own the provider layer that the diagram draws as a direct runtime-to-transport hop.
- Code says: `src/agents/sessions/session-manager-metadata.worker.ts` and `src/agents/sessions/session-manager-message-admission.worker.ts` show that transcript and metadata writes go through database workers rather than an in-process SQLite store.
- Code says: `src/agents/embedded-agent-runner/` holds the turn loop, and `src/auto-reply/` holds the inbound reply and dispatch pipeline that feeds it.
- Impact: the diagram is missing three owners, so a reader would not know where to add a new capability.

### Blocking: the "SQLite Store (Transcripts)" box is contradicted by the storage engine selection

- Classification: blocking.
- Artifact says (line 24): "SQLite Store (Transcripts)"
- Code says: `src/infra/database-engine/registry.ts:24-33` marks the `agent` family as `postgres: true`, and `:39-56` resolves a per-family engine override.
- Code says: `package.json:6` sets `openclaw.databaseEngines` to `["sqlite", "postgres"]`.
- Impact: the artifact states as fixed a storage choice that is now operator-selectable.

### Advisory: the provider abstraction decision understates the provider layer

- Classification: advisory.
- Artifact says (line 60): "| Provider abstraction | Transport stream + payload policy | Uniform interface across different model APIs |"
- Code says: transport streams and payload policies are still the mechanism, via `src/plugin-sdk/provider-transport-runtime.ts`, `src/plugin-sdk/provider-stream-shared.ts`, and `packages/ai/src/transports/`.
- Code says: provider implementations themselves are plugin-owned, and `src/llm/providers/` now holds only fast-mode wrappers and stream wrappers.
- Impact: the decision row is still correct. It would be more accurate if it named the plugin registration step.

### Advisory: the compaction decision does not mention engine-owned compaction

- Classification: advisory.
- Artifact says (line 61): "| Compaction strategy | LLM-based summarization | Preserves conversation quality while reducing tokens |"
- Code says: `src/agents/sessions/compaction/` and `src/agents/compaction.ts:1-27` still implement LLM-based summarization with identifier preservation and a reserve-token budget.
- Code says: `src/context-engine/types.ts:9-40` shows that a context engine may own compaction instead, and `src/context-engine/compaction-watchdog.ts:1-5` bounds that path.
- Impact: the decision is still accurate for the default path. It should note the engine-owned alternative.

### Advisory: the subagent spawning decision does not name the Gateway dispatch path

- Classification: advisory.
- Artifact says (line 63): "| Subagent spawning | Managed subagent registry | Isolated state lifecycle for delegated tasks |"
- Code says: `src/agents/subagents/registry/` still owns the managed subagent registry.
- Code says: `src/gateway/server-plugin-subagent-runtime.ts` and `src/gateway/server-plugin-in-process-dispatch.ts` add a second path where a spawned subagent is dispatched in-process through the Gateway router.
- Impact: the decision is still accurate. It would be more complete if it named both paths.

### Advisory: the Out of Scope list omits the new engine seams

- Classification: advisory.
- Artifact says (lines 72-76): "Fine-tuning or training of models", "Custom model hosting", and "Multi-modal model support beyond text, images, and audio".
- Code says: `src/context-engine/` and `src/plugins/registry-contribution-types.ts` add pluggable context-engine and provider seams that were not in scope when the artifact was written.
- Impact: the out-of-scope list is not wrong, but it now omits the seams a reader would most want to extend.

## Sync drift: 2026-11-16

The specification artifact was not changed since the 2026-10-19 review.
The three blocking and four advisory items in the 2026-10-19 section still apply.

### Blocking: compaction ownership has moved partly into the agent-core package

- Classification: blocking.
- The artifact says (line 61): "| Compaction strategy | LLM-based summarization | Preserves conversation quality while reducing tokens |".
- Code says: `src/agents/compaction.ts:1-3` imports `summarization-completion`, `summary-checkpoint-prompt`, and `utils` from `packages/agent-core/src/harness/compaction/`.
- Code says: the core compaction types now live in `packages/agent-core/src/harness/types.ts`, which the runtime imports.
- Code says: `packages/agent-core/` holds 83 files and owns part of the compaction flow that the spec attributes entirely to the runtime.
- Impact: the spec names no package owner for compaction, so a reader would look only under `src/agents/`.

### Blocking: the TranscriptTurn model drift has grown

- Classification: blocking.
- The artifact still describes a `TranscriptTurn` table with `turnId`, `tokenCount`, and a single `content` JSON column.
- Code says: `src/state/openclaw-agent-schema.sql:454` defines `transcript_events` with a composite key and adds navigation report fields such as `navigation_last_type`, `navigation_valid`, and zstd byte accounting that the 2026-10-19 review did not list.
- Impact: the modeled table is further from the real schema than at the last review.

### Advisory: the store box and provider layer omissions remain

- Classification: advisory.
- The architecture diagram still shows a fixed "SQLite Store (Transcripts)" box and a direct runtime-to-provider hop.
- Code says: `package.json:7-13` sets `openclaw.databaseEngines` to `["sqlite", "postgres"]`, so the store is engine-selectable.
- Code says: `src/plugins/registry-registrars-providers.ts` and `src/plugins/provider-catalog.ts` still own the provider layer.
- Impact: unchanged from 2026-10-19, still misleading.

## Sync drift: 2026-11-23

The specification artifact was not changed since the 2026-11-16 review.
The blocking and advisory items recorded in 2026-10-19 and 2026-11-16 still apply.
The evidence below reflects the current checkout.

### Blocking: the TranscriptTurn data model does not match `transcript_events`

- Classification: blocking.
- The artifact says at lines 29-38 that `TranscriptTurn` has `turnId` as PK, `sessionId` as FK, `role`, `content` JSON, `timestamp`, and `tokenCount`.
- Code says: `src/state/openclaw-agent-schema.sql:454-469` defines `transcript_events` with a composite primary key of `(session_id, seq)`.
- Code says: `:457-468` stores `event_json`, `event_zstd`, `event_utf8_bytes`, and navigation fields including `navigation_json`, `navigation_type`, `navigation_display`, `message_role`, `navigation_last_type`, `navigation_last_custom_type`, and `navigation_valid`.
- Code says: there is no `turnId` column and no `tokenCount` column.
- Code says: `src/agents/AGENTS.md:15` requires transcript messages to be appended only through awaited `SessionManager.appendMessageAsync`.
- Impact: a reader would model a table that does not exist and would miss the compression and navigation layers.

### Blocking: the architecture diagram still omits three owners

- Classification: blocking.
- The artifact says at lines 14-25 that the runtime talks directly to a model provider transport and a `SQLite Store (Transcripts)`.
- Code says: `src/context-engine/registry.ts:1` owns context assembly between the runtime and the model.
- Code says: `src/plugins/registry-registrars-providers.ts` and `src/plugins/provider-catalog.ts` own the provider layer.
- Code says: `src/agents/sessions/session-manager-metadata.worker.ts` and `src/agents/sessions/session-manager-message-admission.worker.ts` put transcript and metadata writes behind workers.
- Code says: `src/agents/embedded-agent-runner/` holds the turn loop and `src/auto-reply/` holds inbound dispatch.
- Impact: a reader would not know where to add a new capability.

### Blocking: the store box is contradicted by engine selection

- Classification: blocking.
- The artifact says at line 24 that transcripts live in a `SQLite Store (Transcripts)`.
- Code says: `package.json:8-11` sets `openclaw.databaseEngines` to `["sqlite", "postgres"]`.
- Code says: `src/infra/database-engine/registry.ts:26` marks the `agent` family as `postgres: true`.
- Code says: `:43-52` resolves a per-family engine override.
- Impact: a fixed storage choice is documented where the code provides an operator-selectable one.

### Advisory: the compaction decision misses the package owner and engine-owned path

- Classification: advisory.
- The artifact says at line 61 that compaction is LLM-based summarization owned by the runtime.
- Code says: `src/agents/compaction.ts:1-5` imports summarization and checkpoint helpers from `packages/agent-core/src/harness/compaction/`.
- Code says: `packages/agent-core/src/harness/types.ts` holds the core compaction types.
- Code says: `src/context-engine/types.ts:36-43` allows a context engine to own compaction, and `src/context-engine/compaction-watchdog.ts` bounds that path.
- Impact: the decision is accurate for the default path but names no package owner and no alternative path.

### Advisory: the subagent decision omits the Gateway dispatch path

- Classification: advisory.
- The artifact says at line 63 that a managed subagent registry handles spawning.
- Code says: `src/agents/subagents/registry/` still owns that registry.
- Code says: `src/gateway/server-plugin-subagent-runtime.ts` and `src/gateway/server-plugin-in-process-dispatch.ts` add in-process Gateway dispatch.
- Impact: the decision is accurate but incomplete.

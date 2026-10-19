---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Requirements review: Agent Runtime

## Sync drift: 2026-10-19

The requirements were reverse-engineered from the code on 2026-10-13.
The code has moved on.
Every finding below is classified as blocking or advisory.

### Blocking: the SQLite-only transcript constraint is contradicted

- Classification: blocking.
- Artifact says (line 30): "| FR-7 | Must | The runtime shall persist conversation transcripts to SQLite |"
- Artifact says (line 48): "- Transcript storage is SQLite-only"
- Code says: `package.json:6` sets `openclaw.databaseEngines` to `["sqlite", "postgres"]`.
- Code says: `package.json:11` sets `openclaw.postgresFamilies` to `["state", "agent", "workboard", "logbook", "team-reports"]`.
- Code says: `src/infra/database-engine/registry.ts:24-33` marks the `agent` family as `postgres: true`, and `:39-56` resolves a per-family engine override.
- Code says: `src/state/openclaw-agent-schema.sql:437` stores transcripts in the `transcript_events` table inside the agent family database, so the engine that holds them can be PostgreSQL.
- Code says: `docs/reference/database-engines.md` documents the adapter, and `docs/gateway/postgresql.md` is the operator guide.
- Impact: a reader would build a deployment plan that assumes a local transcript file, and would miss backup, migration, and mixed-engine limits that the code already enforces.

### Blocking: context management is now owned by a pluggable context-engine registry

- Classification: blocking.
- Artifact says (line 25): "| FR-2 | Must | The runtime shall manage conversation context and perform compaction when approaching token limits |"
- Code says: `src/context-engine/registry.ts:1` states that the context-engine registry owns engine registration, resolution, compatibility, and quarantine.
- Code says: `src/context-engine/types.ts:9-40` defines `AssembleResult` with `messages`, `estimatedTokens`, `promptAuthority`, `systemPromptAddition`, and `contextProjection`, so context assembly is delegated rather than owned by the agent runtime.
- Code says: `src/context-engine/registry-selection.ts` and `src/context-engine/registry-quarantine.ts` add engine selection and quarantine behavior that the artifact never mentions.
- Code says: `src/agents/harness/context-engine-assembly-attempt.ts`, `context-engine-lifecycle.ts`, `context-engine-logical-turn.ts`, and `context-engine-turn-begin.ts` bind the engine into the turn loop.
- Code says: `src/context-engine/types.ts` documents that engines that own compaction keep host request admission checks active, so compaction is now conditional on the selected engine.
- Impact: the requirement still reads true, but a reader would assume the agent runtime is the sole context owner and would miss a plugin slot that can replace context assembly, including with a persistent backend thread.

### Blocking: memory search is implemented outside `src/agents/`

- Classification: blocking.
- Artifact says (line 34): "| FR-11 | May | The runtime shall support memory search across past conversations |"
- Code says: `src/agents/memory-search.ts` and `src/agents/memory-search-source-policy.ts` only own the agent-side source policy.
- Code says: the memory subsystem itself lives in `src/memory-host-sdk/`, with `query.ts`, `dreaming.ts`, `event-store.ts`, `event-export.ts`, `engine-storage.ts`, `multimodal.ts`, and `status.ts`.
- Code says: the memory index, chunks, embeddings, and dreaming workers ship as plugin extensions, for example `extensions/memory-core/src/memory/manager-search.worker.ts`, `manager-index.worker.ts`, `manager-publication.worker.ts`, `standing-intents.worker.ts`, and `memory-entry-origins.worker.ts`.
- Code says: `extensions/memory-lancedb/`, `extensions/memory-wiki/`, and `extensions/active-memory/` add more memory backends.
- Code says: `src/state/openclaw-agent-schema.sql:643-721` defines the `memory_index_meta`, `memory_index_sources`, `memory_index_chunks`, `memory_index_chunk_recall_metadata`, `memory_index_chunk_provenance`, `memory_entry_origins`, `memory_session_tombstones`, `memory_embedding_cache`, and `memory_index_state` tables.
- Impact: FR-11 is marked May and is stated as a runtime capability, but the shipped feature is a plugin-owned memory subsystem with its own storage, backends, and lifecycle.

### Blocking: the model provider enumeration is stale and the provider layer is now plugin-registered

- Classification: blocking.
- Artifact says (line 24): "| FR-1 | Must | The runtime shall support multiple AI model providers (OpenAI, Anthropic, Google, open-source) |"
- Code says: providers ship as plugin extensions, including `extensions/anthropic/`, `extensions/anthropic-vertex/`, `extensions/amazon-bedrock/`, `extensions/amazon-bedrock-mantle/`, `extensions/google/`, `extensions/groq/`, `extensions/mistral/`, `extensions/ollama/`, `extensions/openai/`, `extensions/openrouter/`, and `extensions/xai/`.
- Code says: `src/plugins/registry-registrars-providers.ts:1-30` registers provider plugins, and `src/plugins/provider-catalog.ts` owns the provider catalog.
- Code says: `src/agents/agent-model-discovery.ts:1-2` discovers agent models and auth storage through provider and plugin normalization hooks rather than a hardcoded list.
- Code says: `src/llm/providers/` now holds only fast-mode wrappers and stream wrappers, not provider implementations.
- Impact: the parenthetical list names four families where the code ships more than ten, and a reader would look for provider code inside `src/agents/` or `src/llm/` instead of the plugin registry.

### Advisory: the FR-2 acceptance criterion does not cover engine-owned context

- Classification: advisory.
- Artifact says (line 53): "- [ ] **FR-2**: Given a long conversation exceeding the context window, when compaction triggers, then the conversation is summarized and continues within limits"
- Code says: `src/context-engine/types.ts:9-40` allows an engine to return `contextProjection: "thread_bootstrap"`, in which case the assembled context is injected once and the backend thread is reused until the epoch changes.
- Code says: `src/context-engine/compaction-watchdog.ts:1-5` bounds engine-owned compaction with a shared deadline.
- Impact: the criterion describes the in-process summarization path only, so it does not exercise the engine path.

### Advisory: the FR-6 failover requirement does not mention context-overflow classification

- Classification: advisory.
- Artifact says (line 29): "| FR-6 | Must | The runtime shall support auth profiles with API key rotation and failover |"
- Code says: `src/agents/failover/` also classifies context overflow separately, through `context-overflow.ts` and `context-overflow-tables.ts`.
- Code says: `src/agents/failover/classify-core.ts` and `classification-rules.ts` own the classification that decides between retry, provider switch, and compaction.
- Impact: the requirement is satisfied. It would be more precise if it named the failure classes the failover path now distinguishes.

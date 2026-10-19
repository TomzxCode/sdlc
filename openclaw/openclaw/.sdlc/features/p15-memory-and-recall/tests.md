---
title: "Memory and Recall"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Memory and Recall

## Scope

This plan covers the memory storage, search, trust, dreaming, standing intent, and operator surface of the Memory and Recall feature.

Covered:

- The memory index schema, its FTS tables and triggers, and its storage migrations.
- Chunking, embedding providers, and batch upload of remote embedding requests.
- Hybrid search merging, keyword extraction, and query expansion.
- The session transcript corpus and session file reads.
- The write-time trust decision and the core root memory file rules.
- Dreaming configuration, phase reconciliation, and event recording.
- The `openclaw memory` CLI and the Doctor memory health checks.
- The Gateway memory RPC surface, exercised through the CLI and doctor paths that call it.

Out of scope:

- The context engine, compaction, and subagent context lifecycle, which belong to the Context Engine and Compaction feature.
- The LanceDB and wiki backends beyond their role as alternative `memory` slot owners.
- The Control UI memory panels, which render data the Gateway already exposes.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Memory index schema creation, source identity upgrade, and FTS maintenance | `packages/memory-host-sdk/src/host/memory-schema.test.ts` | Canonical tables exist with the expected columns; recall metadata migrates without rewriting chunk rows; path FTS rows stay one per source; source identities survive `VACUUM`; a failed source-identity migration rolls back |
| TC-2 | FTS identity alignment across writes, `VACUUM`, and rollback | `packages/memory-host-sdk/src/host/memory-schema-fts.test.ts` | Chunk FTS and body FTS rowids stay aligned through the write, `VACUUM`, and rollback cycle |
| TC-3 | Storage migration of legacy vectors and embedding cache rows | `packages/memory-host-sdk/src/host/memory-schema-storage-migration.test.ts` | Legacy vectors convert without changing 64-bit identities; malformed vectors retain text and provenance and record regeneration debt; an admitted migration rolls back its physical changes when authority is lost |
| TC-4 | Chunk provenance backfill and collation | `packages/memory-host-sdk/src/host/memory-schema-provenance.test.ts` | Missing provenance is backfilled; `NULL` source matching and chunk-side path collation are preserved |
| TC-5 | Bounded and safe reads of workspace and extra memory paths | `packages/memory-host-sdk/src/host/read-file.test.ts` | Reads are truncated at the character limit; extra path reads through symlinked directory components are rejected; transient read errors are retried; an allowed hardlinked file larger than the root byte limit is still read |
| TC-6 | Session file and transcript corpus enumeration | `packages/memory-host-sdk/src/host/session-files.test.ts` | Live SQLite rows and archived JSONL artifacts are both surfaced; symlinked archive artifacts are omitted; `.bak` and checkpoint artifacts are skipped; malformed archive line ordinals are preserved |
| TC-7 | Session transcript corpus discovery | `packages/memory-host-sdk/src/host/session-transcript-corpus.test.ts` | The caller's configured store is discovered without a global runtime snapshot; worker content revisions are read without claiming an agent database lease |
| TC-8 | Remote embedding provider request grouping | `packages/memory-host-sdk/src/host/embeddings-remote-provider.test.ts` | Query batches run as one request per input by default; document singleton calls use the batch-shaped request path; the per-request input cap is exposed on the provider |
| TC-9 | Batch upload request framing and error handling | `packages/memory-host-sdk/src/host/batch-upload.test.ts` | Malformed file-upload JSON is wrapped with the request error prefix; a leading-zero content length is accepted on a successful upload |
| TC-10 | Keyword extraction for multilingual queries | `packages/memory-host-sdk/src/host/query-expansion.test.ts` | English, Chinese, Korean, Japanese, Spanish, and Portuguese queries extract keywords; stop words are filtered; Korean particles are stripped without producing single-character stems |
| TC-11 | Memory artifact provenance and the write-time trust decision | `src/memory/memory-artifact-provenance.test.ts` | A workspace is listed in order; a symlinked alias resolves to the same workspace identity; the least-trusted origin stays sticky across later writes; an older rollback does not erase a later reservation; only host-owned memory artifact paths are accepted |
| TC-12 | Canonical root memory file resolution | `src/memory/root-memory-files.test.ts` | Exact workspace entries are distinguished from missing entries and missing path components |
| TC-13 | Dreaming configuration resolution | `src/memory-host-sdk/dreaming.test.ts` | String settings normalize; hex and exponent phase counts are rejected; execution defaults and phase execution override the top-level model; dreaming defaults to enabled with separate storage and the config timezone; canonical roster identities are used when agent aliases share a workspace |
| TC-14 | Recall metadata storage and project eligibility | `packages/memory-host-sdk/src/host/memory-recall-metadata.test.ts` | Exact project eligibility is preserved through selective candidate reads, and recall metadata is stored in a rollback-safe additive table that leaves the chunk table columns unchanged |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-15 | `openclaw memory` CLI against a real index | `extensions/memory-core/src/cli.test.ts` | `reset` and `index` rebuild the real index without changing canonical session bytes or other owners; `reset` requires confirmation and does not create a missing agent database; repeated `forget` selectors are forwarded and reported in both output formats; one `session-backfill --apply` drains the admitted backfill before a preview; vector status prints when available; disabled dreaming phases are reported by `status` |
| TC-16 | Dreaming service reconciliation | `extensions/memory-core/src/dreaming.test.ts` | The managed dreaming job is created for the system agent and reconciled without an ambient owner; a replaced service updates the job and stops the old reconciliation timer; scheduler maintenance stays out of user, heartbeat, and cron reply hooks; managed dreaming fires only while the queued cron event is still pending |
| TC-17 | Doctor memory and embedding health | `extensions/memory-core/src/doctor-health.test.ts` | The local embedding setup check refreshes host state and re-registers after a registry reset; a configured local setup passes and non-local providers are ignored; only local agents are snapshotted; a structured blocker is reported when the local provider plugin is unavailable; a stale built-in index is ignored when another plugin owns the memory slot; an active WAL index is read without changing committed bytes |
| TC-18 | Gateway memory RPC surface | `src/gateway/server-methods/memory-search.test.ts`, `src/gateway/server-methods/memory-provider.test.ts`, `src/gateway/server-methods/memory-provider.authority.test.ts`, `src/gateway/server-methods/doctor.memory-provider.test.ts` | `memory.search` validates the query, the agent id, and the search options; the `version: 2` request is rejected for a provider-runtime backend; `memory.search.owner` refuses when the owner changed; the provider runtime validates the `memory.search`, `memory.get`, and `memory.status` payloads and enforces the caller authority for a read; the doctor memory handlers report the embedding runtime state |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-19 | Active Memory trigger lookup stall under a stalled index generation lock | `test/e2e/qa-lab/runtime/active-memory-trigger-stall.product-proof.e2e.test.ts` | With the memory index generation lock stalled, the Active Memory trigger lookup does not block the turn, and the model recall still runs. The suite is gated on `OPENCLAW_ACTIVE_MEMORY_TRIGGER_STALL_PROOF=1` and runs against a built `dist/index.js` Gateway with a mock OpenAI provider |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-20 | The memory index revision is bumped by a concurrent writer | The read path observes a consistent revision, and a stale index reports staleness rather than silently serving incomplete results |
| TC-21 | A chunk's embedding model differs from the currently configured model | The stored vector is invalidated for regeneration while the chunk text and provenance are preserved |
| TC-22 | An embedding provider returns a malformed vector | The chunk is retained with its text and provenance, and the regeneration debt is recorded rather than dropping the chunk |
| TC-23 | The FTS tokenizer is `trigram` instead of `unicode61` | The FTS table is rebuilt under the new tokenizer, and the search mode falls back to `fts-only` when the vector provider is disabled |
| TC-24 | A memory artifact write does not match the previously recorded content hash | The stored origin class becomes `untrusted`, and the entry is excluded from automatic injection |
| TC-25 | A recall result set exceeds the persisted event payload bounds | The stored event is marked truncated while the aggregate result count stays exact |
| TC-26 | A dreaming phase fails mid-run | The phase outcome is recorded as `failed` with the error detail, and no candidate is promoted |
| TC-27 | A standing intent is past its expiry or already cancelled | It is never matched, and its fire count is not incremented |
| TC-28 | A session backfill owner changes while the operation runs | The operation aborts with an explicit owner-changed error rather than writing under the new owner |
| TC-29 | A memory read is requested for a session owned by another agent, in `extensions/memory-core/src/session-search-visibility.cross-agent.test.ts` | Cross-agent session hits are dropped from the result, including owner-qualified hits that collide with a scoped stem, and the refusal does not widen the search to the foreign session |

## Test Infrastructure

- SQLite fixtures for the memory index, with WAL mode exercised in the doctor health tests.
- A mock OpenAI provider and a built `dist/index.js` Gateway child process for the end-to-end Active Memory proof.
- Temporary workspaces with symlink and hardlink variants for the provenance and read tests.
- Isolated agent databases and plugin-state stores so a test never writes into another owner's store.
- The end-to-end proof is opt-in through `OPENCLAW_ACTIVE_MEMORY_TRIGGER_STALL_PROOF=1` because it needs a built `dist/index.js` and a mock provider.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-12, TC-11 |
| FR-2 | TC-1, TC-2, TC-4, TC-14 |
| FR-3 | TC-1, TC-2, TC-10, TC-18 |
| FR-4 | TC-4, TC-11, TC-24 |
| FR-5 | TC-15, TC-18, TC-19 |
| FR-6 | TC-13, TC-16, TC-25 |
| FR-7 | TC-13, TC-16, TC-26 |
| FR-8 | TC-15 |
| FR-9 | TC-18 |
| FR-10 | TC-27 |
| FR-11 | TC-19 |
| FR-12 | TC-8, TC-9, TC-17 |
| FR-13 | TC-15 |
| FR-14 | TC-17 |
| NFR-1 | TC-20, TC-21 |
| NFR-2 | TC-19, TC-26 |
| NFR-3 | TC-11, TC-24 |
| NFR-4 | TC-1, TC-3, TC-20 |
| NFR-5 | TC-29 |
| NFR-6 | TC-17, TC-18 |

---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.
The memory subsystem changed substantially in v0.98.0, so several requirements now describe behavior the code no longer has.

## Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-5 | "The system shall inject relevant memories into the agent prompt on session turns." | Automatic recall is globally disabled. `get_relevant_parallel` clears pending memory and returns an empty result (`crates/jcode-base/src/memory.rs:1116-1127`); the retained pipeline is dead code (`:1129-1131`); the injection site never fires (`crates/jcode-app-core/src/agent/turn_streaming_mpsc.rs:180-205`). Changelog v0.98.0: "Disable automatic memory recall while retaining explicit memory search". | "The system shall not inject memories into the agent prompt automatically; recall is available only through explicit requests (the `memory` tool and `jcode memory search`)." |
| FR-2 | "The system shall compute local text embeddings for memories using a bundled ONNX MiniLM model so no external embedding API is required." | The `embeddings` cargo feature is opt-in and off by default (`Cargo.toml:218-235`; `crates/jcode-base/Cargo.toml:52,143`). Memories are stored without embedding inference (`crates/jcode-base/src/memory.rs:385-388`). `backfill_embeddings` has no callers. | "The system shall compute local text embeddings for memories using a bundled ONNX MiniLM model when built with the optional `embeddings` cargo feature; the default build performs no local inference and uses no external embedding API." |
| FR-4 | "The system shall support both keyword and semantic search over memories." | Semantic search is now a remote call, not local. `jcode memory search --semantic` routes to `memory_jev::recall` (`src/cli/commands.rs:1675-1678`), and the module contract states "No embeddings, lexical prefilter, sidecar, cached answers, or recent-memory cap are used" (`crates/jcode-base/src/memory_jev.rs:1-8`). | "The system shall support both local keyword search and semantic search over memories; semantic search uses remote Jev relevance decisions and requires Jev access." |
| FR-6 | "The system shall rerank candidate memories (configurable cadence and votes) to keep recall precise." | All three knobs are marked "Legacy setting, retained for config compatibility. Jev recall ignores it." (`crates/jcode-config-types/src/lib.rs:612-620`). `memory_rerank.rs` is imported only by the offline benchmark `src/bin/memory_recall_bench.rs:742`. | "The system shall keep a listwise LLM reranker available for recall benchmarking (configurable cadence and votes); it is not part of the shipped recall path." |
| FR-7 | "The system shall consolidate and merge related memories over time, including overnight consolidation." | There is no memory consolidation pipeline and no overnight memory job. Write-time dedup reinforces an exact duplicate (`crates/jcode-base/src/memory.rs:406-421`). Maintenance is agent-driven under ambient mode (`crates/jcode-app-core/src/ambient/prompt.rs:483`). | "The system shall merge duplicate memories on write (reinforcing the existing entry) and support agent-driven memory-graph maintenance (consolidating duplicates, resolving contradictions, pruning) through ambient mode." |
| FR-8 | "The system shall expose a memory sidecar agent for autonomous memory maintenance." | The sidecar's `check_relevance` and `check_contradiction` methods have no callers (`crates/jcode-base/src/sidecar.rs:716,758`). The background actor (`crates/jcode-base/src/memory_agent.rs`) now performs extraction only, every 12 turns and at session end. | "The system shall run a background memory agent that extracts memories from the session (periodically and at session end) through a sidecar LLM call." |

## Non-functional requirements

NFR-2 reads "Memory embeddings and extraction shall run locally without sending session content to third parties."
Extend it: explicit semantic recall sends only memory content, category, and tags to the configured Jev provider (`crates/jcode-base/src/memory_jev.rs:116-124`).

## Constraints

Two constraints are stale:

- "Embeddings must work out of the box in default builds (the `embeddings` feature is on by default)." is false. Replace with: "The `embeddings` cargo feature is opt-in and off by default; it is retained for benchmarks and debugging only."
- "A `local` embedding backend is required; an `openai` backend is optional." should read: "A `local` embedding backend is the default when the feature is enabled; an `openai` backend is optional."

## Overview

The overview says memories are "re-injected into prompts on later turns".
That is no longer true.
Reword to state that memories are extracted from sessions, stored locally, and recalled only on explicit request.

## Completeness

Missing functional requirements for shipped capabilities:

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-9 | The system shall select relevant memories through remote Jev Decisions, with a configurable provider, model, and relevance threshold, and shall fail closed when Jev access is unavailable. | `crates/jcode-base/src/memory_jev.rs`, `crates/jcode-base/src/jev.rs:20` (`DEFAULT_MEMORY_JEV_MODEL`), `crates/jcode-config-types/src/lib.rs:592-604` (`memory_jev_provider`, `memory_jev_model`, `memory_jev_threshold` default 0.8). |
| FR-10 | The system shall expose memory operations to the agent through the `memory` tool (remember, recall, search, list, forget, tag, link, related) with a per-call scope and limit. | `crates/jcode-app-core/src/tool/memory.rs:107-126,184`. |
| FR-11 | The system shall prefilter candidates with a local BM25 ranker before the remote relevance call. | `crates/jcode-base/src/memory/ranking.rs` (`bm25_rank`, `prefilter_for_jev`). |
| FR-12 | The system shall store memories per project and globally, and shall support graph edges, tags, clusters, cascade retrieval, supersede, and contradiction marking. | `crates/jcode-base/src/memory.rs:179,354` (store paths), `crates/jcode-memory-types/src/graph.rs:92-147,366-546`. |

## Open questions

Open Question 1 asks for the per-turn recall budget.
Nothing is injected, so there is no per-turn budget.
Replace it with: "What relevance threshold and candidate budget should explicit recall use? The live knobs are `[agents] memory_jev_threshold` (default 0.8), `[agents] memory_jev_provider`, and per-call limits (10 for the memory tool, 20 for the CLI)."

## Conflicts

| Requirements | Type | Description | Suggested Resolution |
|---|---|---|---|
| FR-2, FR-4, NFR-2 | Functional vs non-functional tension | FR-2 promises a local embedding path that is off by default, FR-4 promises semantic search that now discloses memory content to a remote provider, and NFR-2 promises no session content leaves the machine. | Reword all three so the local path, the remote relevance path, and the privacy boundary are each stated accurately. |

## Testability

The acceptance criteria list covers every FR and NFR, but the coverage matrix in `tests.md` has no row for FR-5, FR-6, FR-7, FR-8, NFR-1, or NFR-4.
Each added FR needs at least one Gherkin acceptance criterion, and the FR-5 criterion must be inverted to assert that nothing is injected.

## Feasibility

No issues found.

---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Overview | "Local embeddings come from the `jcode-embedding` crate (tract ONNX inference of all-MiniLM-L6-v2). Recall and injection happen in the agent turn loop; consolidation runs as a background/overnight job." | The recall path is `crates/jcode-base/src/memory_jev.rs` (remote Jev Decisions). Injection is disabled. There is no overnight consolidation job. Local embeddings are opt-in and off by default. | Reword the overview to describe the extraction agent, the local store, the BM25 prefilter, the remote Jev relevance call, and the disabled automatic recall. |
| Architecture map | node `embedding (ONNX MiniLM)`, `memory_rerank.rs`, `memory store ──► recall ──► prompt injection on later turns`, `(overnight consolidation merges memories)` | The map never mentions `memory_jev.rs` or `memory/ranking.rs`, and three of the four nodes describe behavior that no longer exists. | Replace the diagram with: session turns feed the memory agent, which extracts through a sidecar call into the project and global JSON stores; an explicit recall request is prefiltered locally with BM25 and then ranked by remote Jev relevance decisions; keyword search stays local. |
| Architecture map | "Memory as graph + store \| `memory_graph.rs` plus durable store" | `crates/jcode-base/src/memory_graph.rs` is a 5-line compatibility re-export of `crates/jcode-memory-types`. | Point at `crates/jcode-memory-types/src/graph.rs`. |
| Architecture map | the `crates/jcode-base/src/memory/` listing names only activity, cache, and pending | `crates/jcode-base/src/memory/` also contains `ranking.rs` (the BM25 prefilter). The map also omits `memory_jev.rs`, `memory_log.rs`, `memory_prompt.rs`, `memory_judge_metrics.rs`, and the agent-facing `crates/jcode-app-core/src/tool/memory.rs`. | Add the missing modules. |
| Data Models | the "Memory Entry" table with `id`, `text`, `embedding`, `extracted_at`, `score` | `MemoryEntry` (`crates/jcode-memory-types/src/lib.rs:233-274`) has `id`, `category`, `content` (not `text`), `tags`, `search_text`, `created_at` and `updated_at` (not `extracted_at`), `access_count`, `source`, `trust`, `strength`, `active`, `superseded_by`, `reinforcements`, `embedding` (optional), `embedding_model`, `confidence`. There is no `score` field. | Replace the table with the real field list. |
| Sequences | "Turn start → query memory store → keyword + semantic candidates → rerank (if due) → select injection set → inject into prompt → run turn" | There is no turn-time query, no rerank, and no injection. | Replace with two sequences: explicit recall on request (load, BM25 prefilter, Jev relevance decisions, ranked results returned) and automatic recall (disabled: pending memory cleared, nothing injected). |
| Technical Decisions | "Local ONNX embeddings \| jcode-embedding with all-MiniLM-L6-v2 \| feature-gated but enabled by default." | The feature is off by default. | Reword: "Local ONNX embeddings (optional build): keeps the embedding stack local when enabled; the crate is feature-gated and off by default, and the shipped recall path uses Jev Decisions rather than local inference." |
| Technical Decisions | the opt-level-3 pin rationale for the embedding stack | The pins are present (`Cargo.toml:556-615`), but the repo comment gives a different rationale (letting the idle unloader release the model). | Reword the rationale to match the repo comment. |
| Out of Scope | "Embedding backends beyond local ONNX and the optional OpenAI backend." | The OpenAI backend is now reachable only through the `memory_embedding_backend` key, which is labelled "Legacy benchmark/debug embedding backend. Jev recall never uses it." (`crates/jcode-config-types/src/lib.rs:618-621`). | Reword: "Embedding backends beyond local ONNX and the optional OpenAI backend; both are benchmark and debug only and off in default builds." |

## Missing Information

- The on-disk storage layout is not stated: `~/.jcode/memory/projects/<project-hash>.json`, `~/.jcode/memory/global.json`, and `~/.jcode/memory/test/*` for `clear-test` (`crates/jcode-base/src/memory.rs:179,354`).
- The extraction toggles are not documented: `[agents] memory_sidecar_enabled` and `[features] memory` (`crates/jcode-config-types/src/lib.rs:605-610,1202-1203`).
- The memory activity and widget state surface is not described (`crates/jcode-base/src/memory/activity.rs`, `memory_log.rs`, `memory_judge_metrics.rs`, surfaced through `crates/jcode-tui/src/tui/info_widget.rs:2221`).
- The Jev provider resolution rules are not described (auto, openrouter, typesafe, laya, aimlapi, jcode; model override; threshold; capability check) in `crates/jcode-base/src/jev.rs`.

## Implementability

No issues found beyond the corrections above.

## Reversibility

No issues found.

## Forward Compatibility

No issues found.

## Ambiguities

No issues found.

## Incoherences

No issues found.

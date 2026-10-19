---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.

## Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-2 | "The system shall support multiple compaction strategies: reactive (on threshold), proactive (before it is needed), and semantic." | The semantic strategy depends on local embeddings (`crates/jcode-base/src/compaction.rs:595-690`), and `crate::embedding` is a stub unless the optional `embeddings` feature is on (`crates/jcode-base/src/lib.rs:39-43,113-114`; `Cargo.toml:221`). The stub's `embed` bails (`embedding_stub.rs:121-127`), so topic-shift detection cannot run and `semantic_cutoff` falls back to the standard recency cutoff (`compaction.rs:645-649`). | "The system shall support multiple compaction strategies: reactive (on threshold), proactive (before it is needed), and semantic. The semantic strategy requires the optional `embeddings` cargo feature; without it, semantic compaction falls back to the standard recency cutoff." |
| FR-6 | "The system shall allow strategy configuration per the [compaction] section (reactive/proactive/semantic)." | `[compaction]` has a single `mode` key, not three (`crates/jcode-config-types/src/lib.rs:363-403`, `CompactionMode` at `:20-47`), plus ten per-mode tuning keys. | "The system shall allow compaction strategy configuration under the [compaction] config section via the mode key (reactive, proactive, or semantic) and the per-mode tuning keys." |

## Completeness

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-8 | The system shall report context usage before and after a compaction (token counts and percentage of the context window) in the completion notice. | v0.98.0 shipped this. `CompactionEvent.pre_tokens`, `post_tokens`, `tokens_saved` (`crates/jcode-compaction-core/src/lib.rs:98-108`), populated at `crates/jcode-base/src/compaction.rs:1204-1240`, rendered at `crates/jcode-tui/src/tui/app/conversation_state.rs:88-112`. |
| FR-9 | The system shall support provider-native compaction, with a configurable mode (auto, explicit, off) and threshold, and shall fall back to a text summary when the native payload is oversized. | `crates/jcode-config-types/src/lib.rs:1263-1266`, `crates/jcode-app-core/src/agent.rs:911-980`, `crates/jcode-app-core/src/agent/compaction.rs:308-350`, `crates/jcode-base/src/compaction.rs:418-455`. |
| FR-10 | The system shall recover from a context-limit error, an HTTP 413 payload-too-large error, and a provider image rejection by compacting and retrying the turn. | `crates/jcode-app-core/src/agent/compaction.rs:130-230` (context limit), `:232-280` (413), `:282-306` (image rejection). |
| FR-11 | The system shall cap the compaction trigger budget with a configurable maximum context size. | `[compaction] max_context_tokens` (`crates/jcode-config-types/src/lib.rs:394-402`), applied at `crates/jcode-base/src/compaction.rs:261`. |

## Overview

The overview paragraph does not mention the before-and-after usage reporting or the provider-native path.
Add: "Compaction reports the context usage before and after the fold, and supports OpenAI provider-native compaction alongside the text-summary path."

## Testability

The acceptance criteria cover FR-1 through FR-7, but the coverage matrix in `tests.md` has no row for FR-2, FR-3, FR-6, or NFR-2.
Each added FR needs at least one Gherkin acceptance criterion.

## Feasibility

No issues found.

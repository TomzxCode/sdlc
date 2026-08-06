---
title: "Agent Memory System"
status: done
---

# Specification: Agent Memory System

## Overview

The memory system lives in `crates/jcode-base/src/memory/` (activity, cache, pending) with the extraction agent and graph logic in `memory.rs`, `memory_agent.rs`, `memory_graph.rs`, and `memory_rerank.rs`. Local embeddings come from the `jcode-embedding` crate (tract ONNX inference of all-MiniLM-L6-v2). Recall and injection happen in the agent turn loop; consolidation runs as a background/overnight job. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
session turns ──► memory.rs / memory_agent.rs ──► memory graph (persistent)
                       │                                 │
                       ▼                                 ▼
                embedding (ONNX MiniLM)          memory_rerank.rs
                       │                                 │
                       ▼                                 ▼
              memory store ──► recall ──► prompt injection on later turns
                                  ▲
                                  │ (overnight consolidation merges memories)
```

## Data Models

### Memory Entry

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Stable identifier of the memory. |
| text | string | not null | The memory content. |
| embedding | vector<f32> | backend dependent | Local embedding for semantic recall. |
| extracted_at | timestamp | not null | When the memory was created. |
| score | float | rerank output | Rerank score used for ranking. |

### Session Search

Search over multi-megabyte session files uses memchr-based case-insensitive matching (pinned to `opt-level = 3`).

## API Contracts

### CLI: `jcode memory list | search | export | import | stats`

- `list` — enumerate stored memories.
- `search <query>` — keyword and/or semantic search.
- `export` / `import` — serialize/deserialize the memory store.
- `stats` — counts and store health.
- `clear-test` — test-only clearing helper.

## Sequences

### Recall on a turn

```
Turn start → query memory store → keyword + semantic candidates
→ rerank (if due) → select injection set → inject into prompt → run turn
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Local ONNX embeddings | `jcode-embedding` with all-MiniLM-L6-v2 | Privacy (NFR-2) and no external API dependency; feature-gated but enabled by default. |
| `opt-level = 3` pin for embedding stack | tract/ndarray/tokenizers pinned | Unoptimized inference measured ~666 ms per embed; optimized keeps the agent loop responsive. |
| Memory as graph + store | `memory_graph.rs` plus durable store | Supports consolidation and relationship-aware recall. |
| Rerank with cadence/votes | `memory_rerank.rs` | Keeps recall precise at a tunable cost. |

## Risks and Unknowns

1. The exact default recall budget and rerank cadence are not documented; behavior was inferred from config and code.
2. Memory extraction quality depends on the extraction agent's prompt, which may drift with model updates.

## Out of Scope

- Cloud-hosted memory sync (a Jade cloud integration exists elsewhere but is not part of this subsystem).
- Embedding backends beyond local ONNX and the optional OpenAI backend.

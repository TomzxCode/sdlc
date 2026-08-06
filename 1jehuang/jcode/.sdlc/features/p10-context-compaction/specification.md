---
title: "Context Compaction"
status: done
---

# Specification: Context Compaction

## Overview

Compaction is implemented in `crates/jcode-base/src/compaction.rs` (policy and state), `crates/jcode-compaction-core` (compaction engine), and `crates/jcode-app-core/src/agent/compaction.rs` (turn-loop integration). The message model supports `OpenAICompaction` content blocks and cache-relevant message hashes (`stable_message_hash`, `cache_relevant_message_hashes`) so KV-cache prefix changes are detected after compaction. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
agent turn loop (app-core/agent/compaction.rs)
   │ checks budget + strategy
   ▼
jcode-base/src/compaction.rs (reactive/proactive/semantic policy, session compaction state)
   │
   ▼
jcode-compaction-core (engine)
   │
   ├── summary preserved in message stream
   ├── session compaction state recorded (StoredCompactionState)
   └── cache-relevant hashes updated for KV-cache correctness
```

## Data Models

### Compaction config (`[compaction]`)

| Key | Description |
|---|---|
| reactive | Compact when approaching the limit. |
| proactive | Compact before it is needed. |
| semantic | Compaction informed by semantic importance. |

### Compaction-related message model

| Field | Type | Description |
|---|---|---|
| OpenAICompaction | ContentBlock | Compacted-context marker in the message stream. |
| stable_message_hash | string | Stable hash for unchanged prefixes. |
| cache_relevant_message_hashes | list | Hashes that affect KV-cache prefix validity. |

## Sequences

### Reactive compaction on a turn

```
Turn start → context usage checked → limit approached
→ run compaction strategy → compress context → append summary
→ record compaction state on session → update cache-relevant hashes
→ turn continues with compacted context
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Multiple strategies | reactive/proactive/semantic | Users tune cost vs. context quality. |
| Hash-based KV-cache detection | `stable_message_hash` / `cache_relevant_message_hashes` | Prevents stale KV-cache prefixes after compaction. |
| Compaction core crate | `jcode-compaction-core` | Isolates engine from policy and turn-loop. |
| Compaction state persisted | `StoredCompactionState` | Resume reflects compacted context. |

## Risks and Unknowns

1. Compaction thresholds and retention are not formally documented; inferred from code.
2. Semantic compaction quality depends on model behavior and embedding importance scoring.

## Out of Scope

- Lossless long-term context storage beyond the preserved summary.
- Provider-specific compaction APIs that are not already integrated.

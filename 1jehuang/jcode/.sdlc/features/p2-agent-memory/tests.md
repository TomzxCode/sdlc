---
title: "Agent Memory System"
status: done
---

# Test Plan: Agent Memory System

## Scope

Covers memory extraction, embedding, storage, search, reranking, and injection. Out of scope: live provider round-trips and real-model quality evaluation (guarded behind dedicated cohorts and scripts).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Memory store operations | `crates/jcode-base/src/memory_tests.rs` | Store persists and recalls memories correctly |
| TC-2 | Memory extraction agent behavior | `crates/jcode-base/src/memory_agent_tests.rs` | Agent produces valid memory candidates |
| TC-3 | Session search scoring | `crates/jcode-session-types/src/session_search_tests.rs` | Results ranked correctly |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Embedding numeric stability across inference engines | CI `minilm_embedding_is_numerically_stable_across_inference_engines` cohort | Embeddings stable across engines |
| TC-5 | Memory e2e flows | `scripts/test_memory.py` | Extract/search/recall works end to end |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Empty memory store | Search returns no results without error |
| TC-7 | Very large session files | Search still responsive (SIMD path) |

## Test Infrastructure

- Python script suite (`scripts/test_memory.py`).
- CI numeric-stability cohort for embeddings.
- `jcode memory clear-test` helper for sandboxed runs.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-2 |
| FR-2 | TC-4 |
| FR-3 | TC-1 |
| FR-4 | TC-3, TC-5 |
| NFR-2 | TC-4 |
| NFR-3 | TC-7 |

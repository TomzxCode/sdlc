---
title: "Semantic Search"
status: done
---

# Test Plan: Semantic Search

## Scope

Tests cover embedding index building, generation management (activation/retirement), pure semantic search, hybrid RRF search, configurable embedding endpoints, incremental index updates, and background scheduler.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Build embedding index from session messages | Message content | Vector index created |
| TC-2 | Activate/retire embedding generations | Generation IDs | Correct generation state |
| TC-3 | Pure semantic search returns similarity-ranked results | Query text | Results ordered by cosine similarity |
| TC-4 | Hybrid search merges FTS5 and semantic results | Query text | RRF-merged ranked results |
| TC-5 | Embedding encoder batches requests | Multiple messages | Batched API calls |
| TC-6 | Index staleness detection | Build version vs current data | Correct staleness verdict |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Full embedding build pipeline | Messages synced | Vectors stored and searchable |
| TC-8 | Index repair on corruption | Corrupted vector index | Index rebuilt |

## Test Files

- `internal/vector/build_test.go` - Embedding index build tests
- `internal/vector/search_test.go` - Semantic/hybrid search tests
- `internal/vector/index_test.go` - Index management tests
- `internal/vector/encoder_test.go` - Embedding encoder tests
- `internal/vector/manager_test.go` - Generation management tests
- `internal/vector/repair_test.go` - Index repair tests
- `internal/vector/chunk_test.go` - Chunking for embedding tests
- `internal/server/huma_routes_embeddings_test.go` - Embedding API tests

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9 | Embedding API endpoint unreachable | Build fails gracefully with error |
| TC-10 | Zero messages to index | No-op, no index created |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-7 |
| FR-2 | TC-2 |
| FR-3 | TC-2 |
| FR-4 | TC-3 |
| FR-5 | TC-4 |
| FR-6 | TC-5 |

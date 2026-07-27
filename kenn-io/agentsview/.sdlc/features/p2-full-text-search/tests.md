---
title: "Full-Text Search"
status: done
---

# Test Plan: Full-Text Search

## Scope

Tests cover FTS5 index creation, query modes (AND, exact phrase, prefix), snippet generation, filtering by agent/project/date/machine/branch, cursor-based pagination, and regex search.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | AND-mode search returns only messages matching all terms | Multi-term query | Filtered results |
| TC-2 | Exact phrase search matches quoted terms | Quoted phrase query | Results matching exact phrase |
| TC-3 | Prefix search matches trailing wildcard | Prefix query | Results with matching prefix |
| TC-4 | Snippet generation includes hit context | Search query + message body | Snippet with highlighted terms |
| TC-5 | Filter by agent returns only that agent's sessions | Agent filter param | Filtered results |
| TC-6 | Filter by project returns only that project's sessions | Project filter param | Filtered results |
| TC-7 | Date range filter scopes results correctly | Since/until params | Results only in date range |
| TC-8 | Cursor pagination returns next page of results | Cursor from first page | Next page results |
| TC-9 | Hybrid search merges FTS5 and semantic results | RRF mode query | Merged ranked results |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-10 | Search across indexed messages | Messages synced to DB | Results returned with snippets |

## Test Files

- `internal/db/search_test.go` - Core search query tests
- `internal/db/search_content_test.go` - Content search tests
- `internal/db/search_content_scope_test.go` - Scope filtering tests
- `internal/db/search_content_chunk_test.go` - Chunk-level search tests
- `internal/db/search_content_bench_test.go` - Search performance benchmarks
- `internal/server/search_test.go` - HTTP search handler tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-10 |
| FR-2 | TC-1 |
| FR-3 | TC-2 |
| FR-4 | TC-3 |
| FR-5 | TC-4 |
| FR-6 | TC-5, TC-6, TC-7 |
| FR-7 | TC-8 |

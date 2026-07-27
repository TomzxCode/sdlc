---
title: "DuckDB Mirror"
status: done
---

# Test Plan: DuckDB Mirror

## Scope

Tests cover push from SQLite to DuckDB, incremental push with fingerprinting, full rebuild, read-only serve, Quack remote protocol, dual driver support (CGO and pure Go), and project filtering.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Push syncs session data from SQLite to DuckDB | SQLite session data | DuckDB has matching rows |
| TC-2 | Incremental push detects changed sessions | Modified session fingerprints | Only changed data pushed |
| TC-3 | Full rebuild creates complete DuckDB mirror | All SQLite data | Complete DuckDB mirror |
| TC-4 | Read-only serve returns query results | DuckDB mirror | Query results returned |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Quack protocol remote query | Quack server running | Remote query returns results |
| TC-6 | Mirror watch detects file changes | Watch daemon running | Auto-push on change |
| TC-7 | Store contract parity | SQLite + DuckDB with same data | Identical query results |

## Test Files

- `internal/duckdb/push_bounded_test.go` - Bounded push tests
- `internal/duckdb/sync_test.go` - Sync lifecycle tests
- `internal/duckdb/sync_fastpath_test.go` - Fast path sync tests
- `internal/duckdb/rebuild_test.go` - Full rebuild tests
- `internal/duckdb/probe_test.go` - Mirror probe tests
- `internal/duckdb/smoke_test.go` - Smoke tests
- `internal/duckdb/store_test.go` - Store query tests
- `internal/duckdb/store_contract_test.go` - Store contract tests
- `internal/duckdb/connect_test.go` - Connection tests
- `internal/duckdb/quack_smoke_duckdbtest_test.go` - Quack protocol tests
- `internal/duckdb/quack_sql_test.go` - Quack SQL tests
- `internal/duckdb/quack_url_form_duckdbtest_test.go` - Quack URL tests
- `internal/duckdb/mirror_watch_test.go` - Mirror watch tests

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | DuckDB file locked | Push waits or reports error |
| TC-9 | Incompatible DuckDB driver version | Error reported |
| TC-10 | Quack connection without token | Connection rejected |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-3 |
| FR-2 | TC-2 |
| FR-3 | TC-4 |
| FR-4 | TC-5 |
| FR-5 | TC-6 |

---
title: "PostgreSQL Sync"
status: done
---

# Test Plan: PostgreSQL Sync

## Scope

Tests cover incremental push from SQLite to PostgreSQL, project filtering, fingerprint-based change detection, named targets, read-only serve, conflict detection, watch mode, OS service management, and pricing sync.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Push syncs session data from SQLite to PostgreSQL | SQLite session data | PostgreSQL has matching rows |
| TC-2 | Fingerprint change detection identifies new/modified | Session fingerprint state | Correct incremental set |
| TC-3 | Project filtering includes/excludes correctly | Include/exclude lists | Filtered push set |
| TC-4 | Named target resolution correct | Config with named targets | Correct target selected |
| TC-5 | Conflict detection by owning machine | Same session from different machines | Conflict flagged |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Full push lifecycle | Real PostgreSQL instance | Data replicated correctly |
| TC-7 | Watch mode pushes on file change | Running watch daemon | Auto-push on new session |
| TC-8 | Read-only serve from PostgreSQL | PostgreSQL with data | Web UI served from PG |

## Test Files

- `internal/postgres/push_test.go` - Push lifecycle tests
- `internal/postgres/push_pgtest_test.go` - Push integration tests (PG)
- `internal/postgres/push_fingerprint_test.go` - Fingerprint tests
- `internal/postgres/push_window_test.go` - Push window tests
- `internal/postgres/sync_test.go` - Sync lifecycle tests
- `internal/postgres/schema_test.go` - Schema management tests
- `internal/postgres/store_test.go` - Store query tests
- `internal/postgres/sessions_test.go` - Session query tests
- `internal/postgres/messages_test.go` - Message query tests
- `internal/postgres/connect_test.go` - Connection tests
- `internal/postgres/analytics_pgtest_test.go` - Analytics PG tests
- `internal/postgres/activityreport_pgtest_test.go` - Activity report PG tests
- `internal/postgres/curation_pgtest_test.go` - Curation PG tests
- `internal/postgres/pricing_pgtest_test.go` - Pricing PG tests

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9 | PostgreSQL unreachable | Push fails with connect error |
| TC-10 | Schema version mismatch | Migration applied or error reported |
| TC-11 | Duplicate push (idempotency) | Same state, no duplicates |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-6 |
| FR-2 | TC-3 |
| FR-3 | TC-2 |
| FR-4 | TC-4 |
| FR-5 | TC-8 |
| FR-6 | TC-5 |
| FR-7 | TC-7 |

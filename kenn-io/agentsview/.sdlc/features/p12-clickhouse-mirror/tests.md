---
title: "ClickHouse Mirror"
status: done
---

# Test Plan: ClickHouse Mirror

## Scope

Tests cover incremental push from SQLite to ClickHouse, fingerprint-based change detection, project filtering, named targets, read-only serve parity, analytics and activity-report queries, usage and pricing sync, watch mode, transport-security guards, and schema management.
Live-server tests use the `chtest` harness and file suffix `_chtest_test.go`.
Out of scope are recall queries and semantic search, which the ClickHouse reader reports as unavailable.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Push syncs session data from SQLite to ClickHouse | SQLite session data | ClickHouse has matching rows |
| TC-2 | Fingerprint change detection identifies new/modified | Session fingerprint state | Correct incremental set |
| TC-3 | Project filtering includes/excludes correctly | Include/exclude lists | Filtered push set |
| TC-4 | Named target resolution correct | Config with named targets | Correct target selected |
| TC-5 | Transport-security guard rejects plain-text URLs | `http://` URL without allowance | Security error returned |
| TC-6 | Schema creation produces ReplacingMergeTree tables | Empty mirror database | Expected tables exist |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Full push lifecycle | Live ClickHouse via chtest | Data replicated correctly |
| TC-8 | Watch mode pushes on file change | Running watch loop | Auto-push on new session |
| TC-9 | Read-only serve from ClickHouse | ClickHouse with data | Web UI served from ClickHouse |
| TC-10 | Store parity with SQLite | Same data in both stores | Identical query results |
| TC-11 | Analytics and activity reports query correctly | ClickHouse with usage data | Correct summaries and buckets |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-12 | CLI push and status round-trip | Run `clickhouse push` then `clickhouse status` | Status shows clean watermark |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | ClickHouse unreachable | Push fails with connect error |
| TC-14 | Duplicate push (idempotency) | Same state, no duplicates |
| TC-15 | Scope change triggers full push | All in-scope sessions re-pushed |
| TC-16 | Stale mirror sessions removed | Sessions missing locally are deleted |

## Test Infrastructure

- `internal/clickhouse/chtest/` harness provisions live ClickHouse instances for `_chtest_test.go` files.
- `internal/clickhouse/testing.go` provides fixture builders for mirror tests.
- `internal/config/config_clickhouse_test.go` covers target resolution and precedence.

## Test Files

- `internal/clickhouse/push_chtest_test.go` - Push lifecycle tests (live server).
- `internal/clickhouse/store_chtest_test.go` - Store query tests (live server).
- `internal/clickhouse/serve_chtest_test.go` - Read-only serve tests (live server).
- `internal/clickhouse/analytics_chtest_test.go` - Analytics query tests (live server).
- `internal/clickhouse/activityreport_chtest_test.go` - Activity report tests (live server).
- `internal/clickhouse/usage_chtest_test.go` - Usage sync tests (live server).
- `internal/clickhouse/project_identity_chtest_test.go` - Project identity tests (live server).
- `internal/clickhouse/fixture_chtest_test.go` - Shared fixtures for live tests.
- `internal/clickhouse/connect_test.go` - Connection and target tests.
- `internal/clickhouse/schema_test.go` - Schema management tests.
- `cmd/agentsview/clickhouse_test.go` - CLI push/status/serve tests.
- `internal/config/config_clickhouse_test.go` - Named target config tests.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-7 |
| FR-2 | TC-3 |
| FR-3 | TC-2 |
| FR-4 | TC-4 |
| FR-5 | TC-9, TC-10 |
| FR-6 | TC-8 |
| FR-8 | TC-11 |
| FR-9 | TC-12 |
| NFR-1 | TC-14 |
| NFR-2 | TC-5 |

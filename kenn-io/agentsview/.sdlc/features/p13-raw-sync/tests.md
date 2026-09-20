---
title: "Raw Sync Mesh"
status: done
---

# Test Plan: Raw Sync Mesh

## Scope

Tests cover laptop capture into the durable outbox, checkpoint persistence and acknowledgement, missing-object negotiation, resumable upload, manifest acceptance with parent fencing, device authentication with scoped tokens and revocation, the watch worker with bounded audits, server-side derivation jobs, CLI watch and status commands, HTTP routes, and PostgreSQL-backed custody stores.
Out of scope are public enrollment, hosted browsing and embeddings, retention and garbage collection, and `pg push` migration, which are not implemented.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Capture stores provider files in the outbox without parsing | Provider source files on disk | Unpublished generation with content-addressed objects |
| TC-2 | Unchanged sources report unchanged and write nothing new | Unmodified source files | Unchanged status with no new outbox rows |
| TC-3 | Checkpoint advances source heads only on durable receipts | Server commit result | Head updated, spool reclaimed on acknowledgement |
| TC-4 | Outbox enforces capacity and reservation accounting | Oversized capture plan | Outbox-full error without partial writes |
| TC-5 | Manifest canonicalization binds tenant and device identity | Manifest envelope | Stable digest used as manifest ID |
| TC-6 | Custody verifies SHA-256 and length before registering | Object bytes | Matching content registers, conflicts rejected |
| TC-7 | Stale parent receipts and reused capture identities fail closed | Conflicting commit | Rejection with head unchanged |
| TC-8 | Device tokens carry fixed scopes and short TTLs | Credential exchange | Scoped token issued, wrong scope rejected |
| TC-9 | Revocation blocks issuance and invalidates tokens | Revoked device | No new tokens, outstanding tokens unusable |
| TC-10 | Upload offset tracking supports resume | Partial upload state | Retry continues from accepted offset |
| TC-11 | Derivation worker claims jobs and records allowlisted error codes | Ready parse job | Complete state or stage-qualified code, no raw content persisted |
| TC-12 | Watch config validation rejects bad URLs and missing credentials | Flag and env combinations | Precise refusal for each invalid combination |
| TC-13 | Path validation accepts canonical relative paths only | Candidate logical paths | Invalid paths rejected across platforms |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-14 | Client drains a generation end to end against a live server | Laptop outbox plus raw-sync server | Receipt bound and checkpoint acknowledged |
| TC-15 | Interrupted upload resumes after client restart | Partial upload with persisted offset | Completed object without re-sending held bytes |
| TC-16 | Watch worker serializes capture, audit, and upload | Changed provider files | Single bounded work stream converges to clean status |
| TC-17 | Bounded audit defers excess sources to later passes | More changes than the audit limit | Remaining sources reconcile on subsequent audits |
| TC-18 | PostgreSQL custody stores accept generations transactionally | Live PostgreSQL with raw schema | Manifest, entries, head, and parse job in one transaction |
| TC-19 | `pg serve` gates raw routes on role privileges | Read-only or under-granted role | Routes omitted with exact missing-privilege log |
| TC-20 | Derivation pipeline materializes and parses retained sources | Accepted generation with objects | Parsed sessions or retryable failure recorded |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-21 | CLI watch uploads and status reports clean checkpoint | Run `raw-sync watch`, change a session file, run `raw-sync status` | Generation acknowledged, status shows no pending work |
| TC-22 | HTTP custody round-trip through tokens, negotiation, upload, and commit | Authenticate device, negotiate, upload, commit manifest | Durable receipt with monotonic generation |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-23 | Server unreachable mid-drain | Transient failure class with retry on the next tick |
| TC-24 | Permanent server rejection | Permanent failure class, generation blocked without retry storm |
| TC-25 | Duplicate byte-identical commit | Existing receipt returned as a no-op |
| TC-26 | Tombstone generation for a deleted source | Deletion propagates as a custody fact |
| TC-27 | SQLite snapshot of a locked provider database | Safe snapshot captured without locking the provider out |
| TC-28 | Non-loopback HTTP server URL | Watch refuses without the insecure allowance |

## Test Infrastructure

- `internal/rawsync` unit tests exercise custody and device auth without a database.
- `internal/postgres` `*_pgtest_test.go` files run PostgreSQL-backed custody, upload, device-auth, derivation, schema, and status suites.
- `internal/rawclient/e2e_test.go` drives the HTTP transport against a test server.
- `cmd/agentsview/raw_sync_test.go` covers watch-config validation and status output.
- `cmd/agentsview/pg_raw_sync_test.go` covers `pg serve` route gating.
- `internal/server/huma_routes_raw_upload_test.go` and `huma_routes_raw_sync_test.go` cover the HTTP routes.

## Test Files

- `internal/rawcapture/capturer_test.go` - Capture planning and unchanged detection.
- `internal/rawcapture/sqlite_snapshot_test.go` - Safe SQLite snapshot behavior.
- `internal/rawcapture/sqlite_snapshot_unix_test.go` - Unix snapshot behavior.
- `internal/rawcapture/sqlite_snapshot_windows_test.go` - Windows snapshot behavior.
- `internal/rawcapture/identity_windows_test.go` - Windows file identity.
- `internal/rawcapture/capacity_linux_test.go` - Linux capacity accounting.
- `internal/rawcheckpoint/store_test.go` - Checkpoint persistence and heads.
- `internal/rawcheckpoint/outbox_test.go` - Outbox spooling and reservations.
- `internal/rawcheckpoint/ack_test.go` - Receipt acknowledgement and failure classes.
- `internal/rawcheckpoint/recovery_test.go` - Restart recovery.
- `internal/rawcheckpoint/status_test.go` - Path-free client status.
- `internal/rawcheckpoint/rows_error_test.go` - Row error mapping.
- `internal/rawsync/manifest_test.go` - Manifest canonicalization and limits.
- `internal/rawsync/device_auth_test.go` - Credential, token, scope, and revocation logic.
- `internal/rawsync/service_test.go` - Custody acceptance and fencing.
- `internal/rawsync/upload_test.go` - Upload offset and finalization.
- `internal/rawsync/object_store_artifact_test.go` - Object repository behavior.
- `internal/rawupload/uploader_test.go` - Outbox draining and retry classes.
- `internal/rawclient/client_test.go` - Client construction and error decoding.
- `internal/rawclient/tokens_test.go` - Token exchange.
- `internal/rawclient/upload_test.go` - Chunked resumable upload.
- `internal/rawclient/commit_test.go` - Manifest commit.
- `internal/rawclient/e2e_test.go` - Client transport against a test server.
- `internal/rawderive/manifest_test.go` - Job manifest handling.
- `internal/rawderive/materializer_test.go` - Source reconstruction.
- `internal/rawderive/parser_test.go` - Derived parsing.
- `internal/rawderive/worker_test.go` - Job claiming and retry codes.
- `internal/rawwatch/auditor_test.go` - Bounded audit behavior.
- `internal/rawwatch/auditor_windows_test.go` - Windows audit behavior.
- `internal/rawwatch/worker_test.go` - Serialized capture, audit, and upload.
- `internal/postgres/raw_ingest_schema_pgtest_test.go` - Raw schema migrations.
- `internal/postgres/raw_ingest_store_pgtest_test.go` - Ingest metadata store.
- `internal/postgres/raw_upload_store_pgtest_test.go` - Upload custody store.
- `internal/postgres/raw_device_auth_store_pgtest_test.go` - Device auth store.
- `internal/postgres/raw_parse_jobs_pgtest_test.go` - Parse-job lifecycle.
- `internal/postgres/raw_sync_status_pgtest_test.go` - Tenant status aggregation.
- `internal/postgres/raw_ingest_custody_pgtest_test.go` - Custody acceptance transactions.
- `internal/postgres/raw_upload_custody_pgtest_test.go` - Upload custody transactions.
- `internal/postgres/raw_client_e2e_pgtest_test.go` - Client against live PostgreSQL.
- `internal/postgres/raw_derive_pipeline_pgtest_test.go` - Derivation pipeline.
- `internal/server/huma_routes_raw_upload_test.go` - Upload HTTP routes.
- `internal/server/huma_routes_raw_sync_test.go` - Token, manifest, and status routes.
- `cmd/agentsview/raw_sync_test.go` - Watch validation and status CLI.
- `cmd/agentsview/pg_raw_sync_test.go` - `pg serve` route gating.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-27 |
| FR-2 | TC-3 |
| FR-3 | TC-14 |
| FR-4 | TC-10, TC-15 |
| FR-5 | TC-5, TC-6, TC-7, TC-18, TC-25 |
| FR-6 | TC-8, TC-9 |
| FR-7 | TC-12, TC-16, TC-17 |
| FR-8 | TC-21 |
| FR-9 | TC-11, TC-20 |
| FR-10 | TC-19 |
| FR-11 | TC-6 |
| FR-12 | TC-22 |
| NFR-1 | TC-12 |
| NFR-2 | TC-28 |
| NFR-3 | TC-8 |
| NFR-4 | TC-10, TC-15 |
| NFR-5 | TC-7, TC-24, TC-25 |
| NFR-6 | TC-4, TC-17 |

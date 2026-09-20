---
title: "Raw Sync Mesh"
status: done
---

# Specification: Raw Sync Mesh

## Overview

The laptop side (`internal/rawcapture`, `internal/rawcheckpoint`, `internal/rawclient`, `internal/rawupload`, `internal/rawwatch`, `internal/rawpath`) captures provider files into a SQLite-backed outbox and drains generations through a token-scoped HTTP transport.
The server side (`internal/rawsync` custody and device-auth services over `internal/postgres` raw tables) accepts objects and manifests transactionally, tracks source heads and parse jobs, and exposes tenant-scoped status.
Server derivation (`internal/rawderive`) is an internal worker library that claims parse jobs and reconstructs sources, but `pg serve` does not start it yet.

## Architecture

```
Provider roots → rawwatch worker → rawcapture → rawcheckpoint outbox (SQLite + spool)
                                              ↓
rawupload → rawclient → HTTP transport → rawsync service → postgres metadata + object store
                                              ↓
                                    source heads, receipts, parse jobs → rawderive worker (library only)
```

## Data Models

### Raw manifest

| Field | Type | Constraints | Description |
|---|---|---|---|
| manifest_id | string | PK, canonical JSON digest | Identity of the accepted generation |
| provider | string | not null | Provider that owns the source files |
| source_key | string | not null | Logical source within the provider |
| configured_root_id | string | not null | Configured source-root identity |
| capture_id | string | not null, unique per content | Capture identity, single-use per content |
| capture_time | timestamp | not null | Time the generation was captured |
| snapshot | object | snapshot or tombstone | Ordered file-object references or deletion marker |
| parent_receipt | string | not null | Expected receipt of the preceding accepted generation |

### Object reference

| Field | Type | Constraints | Description |
|---|---|---|---|
| sha256 | bytes | not null, exact | Content address of the raw object |
| length | int64 | not null, exact | Byte length the content must match |
| logical_path | string | validated via rawpath | Cross-platform relative path of the source file |

### Source head

| Field | Type | Constraints | Description |
|---|---|---|---|
| device_id | string | not null | Immutable device that owns the source |
| source_key | string | not null | Logical source identity |
| generation | int64 | monotonic | Accepted generation counter |
| manifest_id | string | not null | Currently accepted manifest |
| receipt | string | not null | Durable receipt for the accepted generation |
| parse_pending | bool | not null | A parse job awaits claiming |
| parse_leased | bool | not null | A parse job is leased to a worker |
| parse_failed | bool | not null | The latest parse attempt failed |

### Device and token

| Field | Type | Constraints | Description |
|---|---|---|---|
| device_id | string | PK, `dev_` prefixed | Immutable device identity |
| credential_digest | bytes | SHA-256, not null | Digest of the once-returned clear credential |
| device_name | string | display only | Human-readable name, never authorization identity |
| revoked | bool | not null | Revocation blocks issuance and invalidates tokens |
| token_digest | bytes | SHA-256, not null | Digest of the opaque short-lived token |
| token_scopes | int | fixed allowlist | One or more of negotiate, upload, commit, status |
| token_expiry | timestamp | max 24h, default 15m | Short-lived token validity window |

### Parse job

| Field | Type | Constraints | Description |
|---|---|---|---|
| job_id | string | PK | Parse job for one accepted generation |
| manifest_id | string | FK | Generation to reconstruct and parse |
| state | enum | not null | Ready, leased, retrying, complete, failed, or superseded |
| attempts | int | not null | Claimed attempt counter for retries |
| error_code | string | allowlisted | Persisted stage-qualified code, never raw content or paths |

### Laptop checkpoint

| Field | Type | Constraints | Description |
|---|---|---|---|
| device_id | string | not null | Locally pinned device identity |
| source_heads | rows | one per source | Last server-acknowledged receipt and generation |
| outbox_objects | rows | content-addressed spool | Captured objects awaiting upload, capped at 1 GiB |
| generations | rows | durable | Unacknowledged generations with failure classes |
| coverage | rows | one per root | Complete or degraded state with gap intervals |

## API Contracts

### `agentsview raw-sync watch`

**Request**

| Flag | Type | Required | Description |
|---|---|---|---|
| --server | string | yes, or AGENTSVIEW_RAW_SYNC_URL | Raw-sync server URL, HTTPS except loopback with flag |
| --device-id | string | yes, or AGENTSVIEW_RAW_SYNC_DEVICE_ID | Provisioned device ID |
| --allow-insecure-http | bool | no | Allow HTTP only for loopback servers |
| --debounce | duration | no, default 2s | Coalesce window for filesystem changes |
| --interval | duration | no, default 15m | Bounded full-source audit interval |
| --audit-limit | int | no, default 128 | Maximum source work per provider audit |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| daemon | process | Runs until SIGINT or SIGTERM, retrying uploads every minute |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 2 | MISSING_CONFIG | Server URL, device ID, or credential is absent |
| 2 | INVALID_INPUT | Server URL invalid, contains credentials, or non-loopback HTTP without allowance |
| 2 | INVALID_INPUT | No configured provider supports raw capture |

### `agentsview raw-sync status`

Prints path-free JSON with the local checkpoint, pending work, retry time, failures, and coverage.
Reads the laptop checkpoint database only and never contacts the server.

### `POST /api/v1/raw-sync/tokens`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| device_id | string | yes | Provisioned device identity |
| credential | string | yes | Once-issued clear device credential |
| scopes | string[] | yes | Fixed names: negotiate, upload, commit, status |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| token | string | Opaque short-lived access token, default 15-minute TTL |

### `POST /api/v1/raw-sync/objects/missing`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| provider | string | yes | Declared upload source for custody gating |
| objects | ObjectRef[] | yes, batches of 2048 | Canonical object references to check |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| missing | ObjectRef[] | References not yet in custody |

### `POST /api/v1/raw-sync/uploads`

Starts or resumes an object upload for the `upload` scope.

### `HEAD /api/v1/raw-sync/uploads/{id}`

Reads the accepted upload offset for the `upload` scope.

### `PATCH /api/v1/raw-sync/uploads/{id}`

Appends and finalizes object bytes for the `upload` scope.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 401 | unauthorized | Missing, expired, revoked, or wrong-scoped token |
| 404 | not_found | Unknown upload or custody object |
| 409 | conflict | Conflicting content for an existing object |
| 409 | upload_offset_conflict | Resumed offset does not match the accepted offset |
| 422 | checksum_mismatch | Finalized bytes fail SHA-256 or length verification |

### `POST /api/v1/raw-sync/manifests`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| manifest | object | yes | Canonical generation envelope for the `commit` scope |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| manifest_id | string | Canonical digest of the accepted manifest |
| receipt | string | Durable receipt for this generation |
| generation | int64 | Monotonically assigned generation number |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 409 | head_conflict | Expected parent receipt does not match the current source head |
| 422 | missing_object | A referenced object is absent or fails verification |

### `GET /api/v1/raw-sync/status`

Returns source heads, parse-job counts, devices with last-seen times, and open-upload metadata for the authenticated tenant.
Uses one read-only PostgreSQL transaction and changes no raw-sync state.

## Sequences

### Capture and upload

```
Watcher event → rawwatch worker → rawcapture plans source → outbox spool + reservation
→ periodic drain → missing-object negotiation → resumable chunk uploads
→ manifest commit → server receipt → checkpoint acknowledgement → spool garbage collection
```

### Device authentication

```
Operator provisions device → laptop stores credential in env
→ POST /tokens with credential → server checks digest, revocation, expiry
→ scoped token → per-route scope check → revocation invalidates outstanding tokens
```

### Manifest acceptance

```
Commit arrives → verify every referenced object exists and checksums match
→ compare expected parent receipt with source head → record manifest, entries, references
→ assign generation and receipt → create parse job → advance head, retire prior pending job
```

### Bounded audit and retry

```
Startup audit (limit 128 sources) → filesystem watch with 2s debounce
→ 15m full audit tick → 1m upload retry and root re-registration tick
→ degraded coverage rows persist gap intervals until recovery
```

### Server derivation (library only)

```
Worker claims ready parse job → materializes source files to scratch
→ parses into sessions → marks complete or records allowlisted error code
→ pg serve does not start this worker yet
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Transport unit | Whole logical generations with canonical manifests | Atomic custody handoff keeps multi-file sources consistent |
| Content identity | Exact SHA-256 plus byte length | Identical retries become no-ops while conflicts fail closed |
| Manifest identity | Canonical JSON digest | Stable IDs make replay detection and receipt binding exact |
| Auth model | Operator-provisioned credentials with short-lived scoped tokens | Limits blast radius per operation without public enrollment |
| Digest-only storage | SHA-256 of credentials and tokens in PostgreSQL | A database leak never yields usable secrets |
| Manifest-last commits | Objects before manifests | A manifest can only reference verified custody |
| Laptop state | Dedicated SQLite checkpoint database | Restart-safe retries without touching the session archive |
| Outbox cap | 1 GiB default with backpressure errors | Bounded laptop disk use under large or stuck generations |
| Path validation | Canonical relative paths via rawpath | Manifests stay portable across Windows, mac­OS, and Linux |
| Tombstones | First-class manifest variant | Source deletions propagate as custody facts rather than silence |

## Risks and Unknowns

1. Server derivation is unconnected to `pg serve` startup, so retained generations are not yet browsable sessions.
2. Retention, garbage collection, disaster rebuilds, and migration from `pg push` are undefined.
3. PostgreSQL row-level security is a planned defense-in-depth layer and is not configured.
4. The HTTP surface is an internal laptop-to-server protocol with no compatibility policy for external integrators.

## Out of Scope

- Parsed-session remote sync via SSH and S3, which belongs to `p1-session-sync`.
- Public device enrollment and revocation endpoints.
- End-to-end encryption of retained provider files.
- Hosted embedding generation and browsable hosted sessions.
- Retention, garbage collection, disaster rebuilds, and `pg push` migration tooling.

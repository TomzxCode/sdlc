---
title: "Cloud Upstreams"
status: draft
---

# Specification: Cloud Upstreams

## Overview

Cloud Upstreams provide OAuth-based cross-instance company synchronization. The system connects a local Paperclip instance to a remote (cloud) instance, allowing export and sync of company data. Connection secrets are encrypted at rest, transfers are idempotent and tracked as runs with progress, warnings, and conflict reporting. The feature is gated behind an experimental flag.

## Architecture

The cloud upstream system consists of:
- `server/src/routes/cloud-upstreams.ts` — REST API routes for connection and run management
- `server/src/services/cloud-upstreams.ts` — Service layer handling OAuth flow, transfer execution, encryption, and reconciliation
- `ui/src/pages/CloudUpstream.tsx` — UI for managing connections and viewing runs
- `packages/db/src/schema/cloud_upstreams.ts` — DB schema for connections and run storage

## Data Models

### cloud_upstream_connections

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Connection identifier |
| company_id | uuid | FK to companies, not null | Owning company |
| remote_url | text | not null | Remote instance URL |
| source_instance_id | text | not null | Local instance identifier |
| token_status | text | not null | Current token lifecycle status |
| scopes | text[] | not null, default [] | OAuth scopes |
| private_key_pem | text | not null (encrypted) | Instance private key |
| access_token | text | nullable (encrypted) | OAuth access token |
| target_stack_id | text | not null | Remote stack identifier |
| target_company_id | text | not null | Remote company identifier |
| target_origin | text | not null | Remote origin URL |
| target_schema_major | integer | not null | Remote schema version |

### cloud_upstream_runs

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, defaultRandom | Run identifier |
| connection_id | uuid | FK to connections, not null | Parent connection |
| company_id | uuid | FK to companies, not null | Owning company |
| status | text | not null | Run status (queued, running, succeeded, failed, etc.) |
| active_step | text | not null | Current transfer step |
| progress_percent | integer | not null, default 0 | Progress indicator |
| dry_run | boolean | not null, default false | Whether this is a dry run |
| summary | jsonb | not null, default [] | Transfer summary counts |
| warnings | jsonb | not null, default [] | Non-blocking warnings |
| conflicts | jsonb | not null, default [] | Transfer conflicts |
| events | jsonb | not null, default [] | Event log |
| report | jsonb | not null, default {} | Detailed run report |
| idempotency_key | text | not null | Idempotency key for safe retry |

## API Contracts

### GET /api/cloud-upstreams

List upstream connections for a company.

### POST /api/cloud-upstreams/connect/start

Initiate OAuth connection flow. Returns a redirect URI for the authorization step.

### POST /api/cloud-upstreams/connect/finish

Complete the OAuth flow with the authorization code.

### POST /api/cloud-upstreams/:id/sync

Trigger a transfer/sync run, optionally in dry-run mode.

### GET /api/cloud-upstreams/runs

List transfer runs with pagination.

## Sequences

### Connection Flow

```
Operator → POST connect/start → Service creates pending connection → Returns redirect URI
Operator completes OAuth in browser → Service receives callback → POST connect/finish
Service exchanges code for tokens → Encrypts and stores credentials → Connection is active
```

### Transfer Flow

```
Operator → POST sync → Service builds export manifest → Exports entity chunks
Service sends chunks to remote → Remote applies/validates → Run completes with summary
On interruption → Server reconciler marks run as failed on next startup
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Credential encryption | Instance-scoped seal/unseal keys | Prevents plaintext credential storage in the database |
| Transfer idempotency | Idempotency key per run | Safe retry without duplicate application |
| Feature gating | Experimental flag | Feature is still maturing; disabled by default |
| Chunked export | Max chunk bytes per connection target | Handles large companies without memory issues |

## Risks and Unknowns

1. Schema version mismatch between local and remote instances may cause transfer failures.
2. Conflict resolution strategy for modified-on-both-sides data is not fully implemented.
3. Large companies may have slow initial syncs due to chunked transfer overhead.
4. The feature is experimental and behind a flag; API stability is not guaranteed.

## Out of Scope

- Bidirectional sync (local ← cloud) — currently export-only from local
- Realtime/continuous sync — only manual or triggered runs
- Conflict resolution UI — conflicts are reported but not resolvable in the current UI

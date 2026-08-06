---
title: "Artifact Sync & Generative Dashboard"
status: done
---

# Specification: Artifact Sync & Generative Dashboard

## Overview

`ArtifactSync` (`gateway/sync.ts`) is the byte-ingress cluster: `sync()` reconciles a full manifest against the server's `artifact_files` state, and `putBlob()` stores content-addressed bytes in the shared `BlobStore` (R2 or in-memory). The daemon's `watcher.ts` builds manifests incrementally with a stat cache. Dashboard rendering parses front-matter at ingress (`server/frontmatter.ts`) and renders typed panels (`components/LoopView.tsx` registry) with DOMPurify sanitization.

## Architecture

```
daemon watcher (chokidar)
  └─ buildManifest (stat cache, incremental sha256, capManifest ceilings)
      └─ POST /api/machine/sync → server replies needHashes
          └─ PUT /api/machine/blob/:hash (4-concurrent, hash verified)
              └─ BlobStore (R2 | in-memory) ← blobs row (+ parsed front-matter meta)
                                                     └─ artifact_files (loopId, path, hash, deleted, oversize)

web: /api/artifact/:loopId/* (session-authed, loopInScope)
  └─ image inline route (allowlist imageMime, nosniff + CSP sandbox)
  └─ LoopView renders ui markup → DOMPurify → loop-embed / loop-calendar / loop-kanban
  └─ runSnapshots at report → getRunDiff (jsdiff) for the run page
retention: maintainStorage → prune snapshots (keep 20) → blob GC (grace, re-check, bytes-before-metadata)
```

## Data Models

### blobs

| Field | Type | Constraints | Description |
|---|---|---|---|
| hash | text | PK | sha256 hex; the R2 object key |
| size | integer | not null | Byte length |
| binary | boolean | default false | NUL heuristic (download-only) |
| meta | jsonb | nullable | Parsed front-matter `{type?, title?, date?}` |
| createdAt | text | not null | Ingress time |

### artifact_files

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Row id |
| loopId | text | not null | Owning loop |
| path | text | not null | Normalized, loop-relative |
| hash | text | → blobs.hash; null if deleted/oversize | Current bytes |
| size | integer | nullable | Byte length |
| oversize / deleted | boolean | default false | Cap / tombstone flags |
| lastRunId | text | nullable | Run in flight when the change synced |

### run_snapshots

| Field | Type | Constraints | Description |
|---|---|---|---|
| runId | text | PK | Run boundary |
| loopId | text | not null | Owning loop |
| manifest | jsonb | `SnapshotManifest` | Full path → {hash,size,binary,oversize} |

## API Contracts

### POST /api/machine/sync

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| token | string | yes | `dk_` device token |
| manifest | object | yes | Full sha256 manifest per loop |
| inline | blob[] | no | Small inline blobs (≤64KB, ≤1MB aggregate) |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| needHashes | string[] | Hashes the server wants uploaded |

### PUT /api/machine/blob/:hash

**Response (200 OK)**

Stores the body (verified hash) and returns the accepted blob metadata. Only hashes the sync handshake asked for are accepted.

## Sequences

### Sync reconcile

```
daemon flush → POST sync (full manifest, incremental inline)
server: compare manifest vs artifact_files → reply needHashes
daemon: PUT missing blobs (4-concurrent) → server verifies sha256 + caps
server: upsert artifact_files rows (deletions = absence), parse front-matter once
```

### Run diff

```
report() → capture manifest → run_snapshots row (no diff computed on write)
run page → getRunDiff(runN) → diff vs prior snapshot manifest (jsdiff) → "Changes" tab
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Content addressing | sha256 keyed bytes in R2 | Dedup across loops/runs; business DB holds only metadata |
| Sync handshake | Server asks for `needHashes` only | A device token is never an uncapped write channel |
| Incremental hashing | Stat cache (size+mtime+ctime, racy-write guard) | Unchanged files never re-read; digest-match skips the network |
| Manifest ceilings | `capManifest` (5000 files / 256MB) | A burst can't 413/timeout into a retry storm; content home survives |
| Front matter | Parsed once at ingress, pure and bounded | Authoritative product date; soft convention, never a storage gate |
| XSS containment | HTML in a `sandbox="allow-scripts"` opaque-origin iframe; SVG never inlined | Stored XSS containment is load-bearing |
| GC bias | Keep in doubt; bytes before metadata; re-check per candidate | A wrong delete is data loss; a leaked blob is a cost bug |
| Grid | `auto-fit minmax(min(100%, max(28rem, (100% - gap)/2)), 1fr)` | Hard two-column cap; content blocks span full width |

## Risks and Unknowns

1. The shared blob store is load-bearing: boot constructs ONE instance for gateway + sync, or retention could delete bytes sync never wrote.
2. The never-syncable dir list and caps must be kept in sync between `watcher.ts` and `gateway/artifacts.ts`.
3. In-memory blob store is the test/dev default and loses bytes on restart (documented).

## Out of Scope

- Executing or interpreting artifact content (beyond the front-matter parse).
- Full-text search or preview beyond the files panel and dashboard panels.

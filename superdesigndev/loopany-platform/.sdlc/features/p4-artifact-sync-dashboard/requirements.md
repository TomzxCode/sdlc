---
title: "Artifact Sync & Generative Dashboard"
status: done
---

# Requirements: Artifact Sync & Generative Dashboard

## Overview

This feature turns a loop's folder into durable server-side content and renders it as a generative dashboard. The daemon watcher builds a full sha256 manifest of each loop folder and syncs changes to the server; bytes live in a content-addressed blob store (R2 or in-memory) with metadata in `blobs`/`artifact_files`. Front-matter-typed markdown products render as generative-UI panels (`loop-embed`, `loop-calendar`, `loop-kanban`, charts), a run's snapshot enables a per-run diff, and retention/GC keeps storage bounded. The server only stores and reads bytes; it never interprets or executes them.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Loop owner | A dashboard that renders the loop's real products (reports, kanban cards, calendars, charts) without manual setup. |
| Loop operator | Loop folders sync live; heavy work stays out of the loop folder so sync stays bounded. |
| Server operator | Retention/GC keeps storage within the per-loop cap; inline images are served sandboxed. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The daemon shall watch each loop folder and build a full sha256 manifest with incremental hashing (stat-cache, racy-write guard). |
| FR-2 | Must | The daemon shall POST the manifest to `/api/machine/sync`, upload only the hashes the server requests via `PUT /api/machine/blob/:hash`, and verify the hash server-side. |
| FR-3 | Must | The server shall store blob bytes in a content-addressed store (R2 when configured, in-memory otherwise) keyed by sha256, with metadata rows in `blobs` and current file state in `artifact_files`. |
| FR-4 | Must | The server shall enforce per-file (10MB) and per-loop (500MB) byte caps, marking oversized files metadata-only, and honor the never-syncable dir list. |
| FR-5 | Must | The daemon shall bound every sync to per-loop file-count and byte ceilings, keeping the top-level content home and dropping overflow with one loud warning. |
| FR-6 | Must | Markdown products with front-matter `type`/`title`/`date` shall be indexed once at byte ingress and rendered as generative dashboard panels. |
| FR-7 | Must | The dashboard shall render custom panels (`loop-embed`/`loop-calendar`/`loop-kanban`) plus charts from numeric run state, sanitized against stored XSS. |
| FR-8 | Must | Run snapshots shall capture the manifest at report, and the run page shall diff run N against the prior snapshot. |
| FR-9 | Must | Retention/GC shall prune snapshots (keep 20), unpin old blobs, honor a grace window, re-check referencedness, and delete bytes before metadata. |
| FR-10 | Should | HTML artifacts shall render in a strict sandboxed iframe (never same-origin); images (incl. SVG) render via a hardened inline route. |
| FR-11 | Should | The task file shall appear exactly once in the files panel and render from the loop record's content, not a blob fetch. |
| FR-12 | Should | The dashboard grid shall cap at two columns, with only custom panels tiling and content blocks spanning full width. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The never-syncable dir list and caps must be enforced identically on daemon and server to keep the two in sync. |
| NFR-2 | Must | Security | Inline image serving must set `X-Content-Type-Options: nosniff` and `Content-Security-Policy: sandbox`. |
| NFR-3 | Must | Performance | Unchanged files must never be re-read (incremental hashing); a digest match skips the network entirely. |
| NFR-4 | Must | Availability | A sync burst must never 413 the server's body cap (inline blob budget + overflow to the PUT path). |
| NFR-5 | Should | Performance | Blob PUTs shall run bounded-concurrent (4); inline blobs budgeted 1MB aggregate per POST. |
| NFR-6 | Should | Reliability | Blob GC must bias to keep: a leaked blob is a cost bug, a wrong delete is data loss. |

## Constraints

- The server never executes or interprets artifact bytes beyond parsing front-matter (pure, bounded, never throws).
- SVG is scriptable and must never be inlined into the app DOM.
- The dev (vite) server 404s asset-extension routes; image rendering verifies against a nitro prod build.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**
    - **Given** a loop folder with an unchanged file
    - **When** the watcher rebuilds the manifest
    - **Then** the file is not re-read (stat-cache hit)
- [ ] **FR-2**
    - **Given** a sync with a changed file
    - **When** the server responds `needHashes`
    - **Then** only those blobs are PUT and each PUT's hash is verified server-side
- [ ] **FR-3**
    - **Given** a blob PUT
    - **When** stored
    - **Then** bytes land in the blob store keyed by sha256 and metadata rows record it
- [ ] **FR-4**
    - **Given** a file over 10MB or a loop over 500MB
    - **When** synced
    - **Then** it is metadata-only (oversize) and the byte cap is enforced authoritatively at `putBlob`
- [ ] **FR-5**
    - **Given** a loop folder over the manifest ceilings
    - **When** the watcher caps it
    - **Then** the top-level content home survives and overflow drops with one loud warning
- [ ] **FR-6**
    - **Given** a markdown product with `type: report`, `title`, `date` front matter
    - **When** its bytes arrive
    - **Then** `{type?, title?, date?}` is parsed once and stored on the blob row
- [ ] **FR-7**
    - **Given** dashboard markup with `loop-kanban` and columns
    - **When** rendered
    - **Then** artifacts group into columns (unmatched types collect in "Other"; task file excluded)
- [ ] **FR-8**
    - **Given** a run finalizing
    - **When** report persists
    - **Then** a snapshot is captured and the run page can diff it against the prior snapshot
- [ ] **FR-9**
    - **Given** unreferenced blobs past the grace window
    - **When** GC runs
    - **Then** bytes delete before metadata, with a live keep-set re-check per candidate
- [ ] **NFR-1**
    - **Given** a `.env` file or `node_modules` dir in a loop folder
    - **When** synced
    - **Then** it is excluded on both daemon and server
- [ ] **NFR-2**
    - **Given** an inline image request
    - **When** served
    - **Then** `nosniff` + `CSP: sandbox` are set
- [ ] **NFR-3**
    - **Given** an unchanged manifest digest
    - **When** the daemon syncs
    - **Then** the network round-trip is skipped entirely
- [ ] **NFR-4**
    - **Given** a burst of inline blobs over the aggregate budget
    - **When** synced
    - **Then** overflow takes the PUT path and the POST never 413s

## Conflicts

None identified yet.

## Open Questions

1. None: behavior is fully determined by the code and its tests.

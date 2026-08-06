---
title: "Artifact Sync & Generative Dashboard"
status: done
---

# Test Plan: Artifact Sync & Generative Dashboard

## Scope

Testing the watcher manifest/hash logic, the sync reconcile handshake, blob storage and caps, front-matter indexing, retention/GC, artifact byte serving, and the generative dashboard panels. Out of scope: daemon poll/run lifecycle (covered by the machine gateway and daemon features).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Manifest build is incremental (stat cache) | Unchanged file across rebuilds | File not re-read; digest matches, network skipped |
| TC-2 | Manifest drops never-syncable dirs and key files | `.git`, `node_modules`, `.env` in a loop folder | Excluded from the manifest on both daemon and server |
| TC-3 | `capManifest` keeps the shallowest-then-smallest | Loop folder over the file-count/byte ceilings | Content home survives; overflow dropped with one warning |
| TC-4 | Sync reconcile replies with `needHashes` | Manifest with one new file | Only the missing hash is requested |
| TC-5 | Blob PUT verifies the hash | Mismatched body | Put rejected; only handshake-asked hashes accepted |
| TC-6 | Per-file and per-loop caps enforced | File > 10MB, loop > 500MB | Oversize metadata-only; authoritative cap at `putBlob` |
| TC-7 | Front-matter parsed once at ingress | Markdown product with `type`/`title`/`date` | Indexed subset stored on the blob row; dedup reuses it |
| TC-8 | Front-matter parse is bounded and never throws | Junk front matter / huge file | Parse skipped, meta null, no throw |
| TC-9 | Snapshot captured at report; run diff computed lazily | Run N vs prior snapshot | "Changes" diff via jsdiff; runs without snapshots degrade gracefully |
| TC-10 | Snapshot pruning keeps 20 | 25 snapshots | 20 retained, old blobs unpinned |
| TC-11 | Blob GC honors grace and re-checks referencedness | Candidate referenced / recent / old-unreferenced | Bytes deleted before metadata only for safe candidates |
| TC-12 | Inline image serving is hardened | Known image mime via `?view=inline` | `nosniff` + `CSP: sandbox`, real content-type |
| TC-13 | Unknown/oversize artifact renders metadata-only | Oversize file request | Note, no bytes served |
| TC-14 | Kanban groups typed artifacts into columns | `type:`-tagged markdown cards | Columns per `columns` attr; unmatched → "Other"; task file excluded |
| TC-15 | Dashboard grid caps at two columns | Wide container + custom panels | Panels tile 2-up; content blocks span full width |
| TC-16 | File entries dedup the task file | Task file + synced copy | Appears exactly once; task row renders from the loop record |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-17 | Full watcher→sync→blob lifecycle against pglite + in-memory store | Seeded loop folder with changes | Files sync, bytes stored, artifact_files consistent |
| TC-18 | Blob PUT body cap (32MB `SYNC_BODY_CAP`) | Oversized POST | 413, no partial write |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-19 | Inline burst over the 1MB aggregate budget | Overflow takes the PUT path; no 413 |
| TC-20 | First flush after watcher start | Inlines nothing (server already has almost everything) |
| TC-21 | SVG artifact | Never inlined into the app DOM; served via hardened inline route |
| TC-22 | HTML artifact with a script | Runs in a strict sandboxed opaque-origin iframe; can't reach parent/cookies |

## Test Infrastructure

- vitest; server tests use the shared in-memory blob store; integration tests use real pglite.
- `gatewayWithStore` mirrors the production shared-store wiring for retention tests.
- jsdom + DOMPurify for dashboard panel rendering; Recharts mounted under `act` with a ResizeObserver stub.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-4, TC-5 |
| FR-3 | TC-17 |
| FR-4 | TC-2, TC-6 |
| FR-5 | TC-3 |
| FR-6 | TC-7, TC-8 |
| FR-7 | TC-14 |
| FR-8 | TC-9 |
| FR-9 | TC-10, TC-11 |
| FR-10 | TC-12, TC-21, TC-22 |
| FR-11 | TC-16 |
| FR-12 | TC-15 |
| NFR-1 | TC-2 |
| NFR-2 | TC-12 |
| NFR-3 | TC-1 |
| NFR-4 | TC-19 |
| NFR-5 | TC-19 |
| NFR-6 | TC-11 |

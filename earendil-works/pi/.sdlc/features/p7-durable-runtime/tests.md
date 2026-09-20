---
title: "Durable runtime"
status: done
---

# Test Plan: Durable runtime

## Scope

This plan covers the Pico record contracts and `MemoryStorage` behavior in `packages/durable`.
It is derived from `test/memory-storage.test.ts` (twelve behavior cases) and `test/types.test.ts` (one compile-time discriminator case).
Out of scope are the Session mutation line, persistent backends, and Chord delta mechanics.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Root conversation reserves ID 1 and rejects duplicates | Mint ID, commit root, recommit root | First mint is 2, duplicate commit throws `already belongs to conversation`. |
| TC-2 | Mixed-table batch commits atomically and rolls back on failure | Entry, task, and input writes followed by a batch with a duplicate conversation ID | First batch visible with its sequence, failed batch throws, none of its writes visible, next commit gets `initialSeq + 1`. |
| TC-3 | Retained writes and returned records are detached | Mutated caller objects and mutated read results | Stored entry data, task checkpoint, and input detail keep original values. |
| TC-4 | Prototype-like JSON keys clone without changing prototypes | Entry data with `__proto__`, `constructor`, and `toString` keys | Reads keep `Object.prototype`, keep own `__proto__` data, and global prototype stays clean. |
| TC-5 | Out-of-order entry IDs index in sorted order | Entries 30, 10, and marker 20 committed together | Newest-first scan returns 30, 20, 10 and latest head marker is 20. |
| TC-6 | Entry cursor continues below its last item after a newer commit | Two-page newest-first scan with an append between pages | Second page returns only the oldest entry with no further cursor. |
| TC-7 | Conversations paginate ascending by opaque cursor | Root plus two conversations committed out of order | First page returns root and second with `{ after }` cursor, second page returns third. |
| TC-8 | Deep fork history scans newest-first through every ancestor cap | Three-level fork with caps, exclusions, and head markers | Pages return grandchild, child-cap, and root entries in order with correct markers and commit sequences. |
| TC-9 | Task records replace fully and page through filtered scans | Three tasks with memo, background, and abort flags advanced to terminal | Latest record returned, pending pages split 1 plus 1, terminal and background filters match. |
| TC-10 | Request IDs index per conversation and input records replace fully | Same key in two conversations plus placed transition | Per-conversation lookup resolves, replacement visible by ID and by key. |
| TC-11 | Global ID namespace rejects cross-table reuse and exhausted minting | Explicit ID 100, cross-table task write, `MAX_SAFE_INTEGER` entry | Cross-table write throws `already belongs to entry`, minting past the safe integer throws. |
| TC-12 | Closed storage rejects every operation | Commit and reads after `close` | Commit, lookup, and mint all throw `closed`. |
| TC-13 | Type discriminators accept valid shapes and reject invalid ones | Omit, replace, pending, terminal, document, outcome, and input shapes | Valid shapes compile, thirteen invalid shapes each raise `@ts-expect-error`. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-14 | Entry commit sequence ties reads to their commit | Root conversation exists | Each entry read carries the sequence of its creating commit. |
| TC-15 | Head-marker search resolves through fork ancestry | Three-level fork with markers at each level | Current and historical markers resolve, pre-history cutoff returns undefined. |
| TC-16 | Unknown conversations fail fast on history reads | No conversation with the queried ID | Entry scan and head-marker search throw `Unknown conversation`. |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-17 | Package check passes for sources and tests | Run the root check | No erasable-TypeScript or import-hygiene violations for the package. |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-18 | Same input written twice in one batch | Commit rejects the batch and persists nothing. |
| TC-19 | Task write reuses an entry ID | Commit throws `already belongs to entry`. |
| TC-20 | Cursor continuation after interleaved newer commit | Older page resumes strictly below the first page cursor. |

## Test Infrastructure

- Vitest suite in `packages/durable/test/` using `BACKGROUND_CONTEXT` as the storage context.
- Small local factories for pending tasks and entries keep each case isolated with a fresh `MemoryStorage`.
- Type-level assertions use `expectTypeOf` plus `@ts-expect-error` for the thirteen invalid shapes.
- Targeted runs avoid the full suite: `node ../../node_modules/vitest/dist/cli.js --run test/memory-storage.test.ts`.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-8, TC-15, TC-16 |
| FR-2 | TC-5, TC-6, TC-8, TC-14 |
| FR-3 | TC-10, TC-18 |
| FR-4 | TC-9 |
| FR-5 | TC-13 |
| FR-6 | TC-2, TC-7, TC-9, TC-10, TC-14, TC-15, TC-16 |
| FR-7 | TC-1, TC-2, TC-3, TC-4, TC-5, TC-6, TC-7, TC-8, TC-11, TC-12, TC-20 |
| FR-8 | TC-1, TC-11 |
| FR-9 | TC-13 |
| FR-10 | TC-6, TC-7, TC-9 |
| NFR-1 | TC-2 |
| NFR-2 | TC-3, TC-4 |
| NFR-3 | TC-13, TC-17 |
| NFR-4 | TC-5, TC-8 |

---
title: "Knowledge Graph & Memory"
status: done
---

# Test Plan: Knowledge Graph & Memory

## Scope

This plan covers deterministic extraction, incremental rebuild, query behavior, artifact recovery, inferred-edge provenance, and the memory backend tests observed in the tree.
Dashboard rendering and whole-graph canvas behavior are out of scope.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Module derivation from file set | derive-modules.test.ts fixture files | Stable module nodes derived every build. |
| TC-2 | Dispatcher composition across languages | extract-file-composition.test.ts mixed fixtures | Exactly one file node per discovered file. |
| TC-3 | FNXC rationale extraction | extract-fnxc.test.ts comment fixtures | One rationale node per stamped header. |
| TC-4 | Markdown extraction outside fenced code | extract-markdown.test.ts markdown fixtures | Concepts and rationale only outside code spans. |
| TC-5 | TypeScript symbol extraction | extract-typescript.test.ts TS fixtures | Exported declarations become collapsed symbol nodes. |
| TC-6 | File discovery surface | file-discovery.test.ts repo layout | Package sources, scripts, plugins, docs, and dashboard app are included. |
| TC-7 | Graph node and edge identity | graph-identity.test.ts colliding fixtures | Deterministic path-derived identifiers with escaped separators. |
| TC-8 | Query API behavior | graph-query.test.ts built graph | queryNodes, neighbors, and shortestPath retain full provenance. |
| TC-9 | Artifact serialization stability | graph-serialization.test.ts graph fixtures | Sorted LF JSON with content-derived values only. |
| TC-10 | Inferred-edge writer provenance | inferred-edge-writer.test.ts semantic inputs | Every written edge is stamped inferred unconditionally. |
| TC-11 | Import reference resolution | resolve-imports.test.ts relative imports | Lexical ts, tsx, and index candidates resolve without aliases. |
| TC-12 | Memory stash backend persistence | memory-backend-stash.test.ts session fixtures | Session capture persists and reloads through the stash backend. |
| TC-13 | Memory topic search | memory-search-topic.test.ts indexed records | Topic queries return the expected stored records. |
| TC-14 | Stash settings handling | stash-settings.test.ts settings fixtures | Stash configuration round-trips without loss. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-15 | Builder equivalence between full and incremental runs | graph-builder-equivalence.test.ts with prior artifact | Incremental output matches a forced full rebuild byte for byte. |
| TC-16 | Incremental rebuild and deletion pruning | graph-builder-incremental.test.ts with changed tree | Only changed files re-extract and deleted ownership is pruned. |
| TC-17 | Store recovery on invalid artifacts | graph-store-recovery.test.ts with corrupt payloads | Shape violations and contradictions trigger complete rebuild. |
| TC-18 | Artifact gitignore policy | graph-artifact-not-gitignored.test.ts with git check | Runtime graph directory stays ignored and rebuild is documented. |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-19 | CLI rebuild from scratch | Run `fn knowledge-graph build --force` on a checkout | Nodes, edges, and manifest regenerate and queries succeed. |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-20 | Malformed TypeScript source with syntax errors | Extraction completes best-effort without blocking the build. |
| TC-21 | Interrupted build leaves nodes without a manifest | The next build discards the partial set and runs a full rebuild. |

## Test Infrastructure

- Fixture trees for TypeScript, markdown, FNXC comments, imports, and corrupt artifacts.
- Prior-artifact harness comparing incremental output against forced full rebuilds.
- Git ignore assertions proving the runtime artifact stays untracked.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-2, TC-4, TC-5, TC-6 |
| FR-2 | TC-15, TC-16, TC-1, TC-11 |
| FR-3 | TC-8, TC-7 |
| FR-4 | TC-10 |
| FR-5 | TC-3, TC-4 |
| FR-6 | TC-18, TC-19 |
| NFR-1 | TC-9, TC-15 |
| NFR-2 | TC-18 |
| NFR-3 | TC-5, TC-20 |
| NFR-4 | TC-9, TC-17, TC-21 |

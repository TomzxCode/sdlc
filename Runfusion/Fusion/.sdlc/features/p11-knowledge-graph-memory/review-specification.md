---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Data Models

- The Manifest model does not match the code. specification.md:43-46 describes a `fingerprints` map and an `importRefs` map. The code defines `packages/core/src/knowledge-graph/graph-types.ts:25-26` as `GraphManifest { schemaVersion, extractorVersion, files: Record<string, GraphManifestEntry> }` and `GraphManifestEntry { hash, importRefs? }`. There is no top-level fingerprints map, and import references live inside each file entry.

- The Node model omits three persisted fields. specification.md:23-28 lists id, kind, source and attributes, but `packages/core/src/knowledge-graph/graph-types.ts:21` also persists `name`, `owner` and `ownerPath`.

- The Edge model omits three persisted fields and mis-types a fourth. specification.md:34-39 lists kind, source, owner and provenance and calls `source` a string foreign key. `packages/core/src/knowledge-graph/graph-types.ts:22` defines `GraphEdge` with `id`, `kind`, `from`, `to`, `provenance`, `owner`, `ownerPath`, `source` and `attributes`, where `source` is a `SourceLocation` object of path, line and column (`packages/core/src/knowledge-graph/graph-types.ts:20`).

- The recall record has no model. `packages/core/src/memory/recall/recall-types.ts:11-17` defines `RecallRecord` with kind, content, contentHash, source, tags, graphNodeIds and timestamps, and `packages/core/src/postgres/schema/project.ts:713-718` defines the backing `memory_recall_records` table.

- The `knowledgeGraphDir` project setting has no model. `packages/core/src/knowledge-graph/graph-store.ts:12-15` defines the default and the containment check, `packages/dashboard/src/knowledge-graph-access.ts:50-53` reads the setting, and `packages/cli/src/commands/knowledge-graph.ts:48-51` reads it too.

### Architecture

- Persistence is attributed to the wrong module. specification.md:15 says "graph-manifest.ts persists fingerprints and import references". `packages/core/src/knowledge-graph/graph-manifest.ts` holds only the `fingerprintContent` helper. Persistence lives in `packages/core/src/knowledge-graph/graph-store.ts:124` (`loadArtifacts`) and `packages/core/src/knowledge-graph/graph-store.ts:127` (`writeArtifacts`), with encoding in `packages/core/src/knowledge-graph/graph-serialization.ts:42` (`serializeManifest`) and `packages/core/src/knowledge-graph/graph-serialization.ts:121` (`deserializeArtifacts`).

- The Memory Keeper data flow is absent. `packages/engine/src/memory/memory-consolidation.ts:35-56` runs the graph refresh, recall capture, cross-reference and semantics steps, and `packages/engine/src/memory/memory-consolidation-adapters.ts:29-30` wires them to the graph build and the inferred-edge writer. The Architecture section describes none of it.

### API Contracts

- None of the three documented error codes exist in the code. specification.md:64-68 lists 404 `GRAPH_NOT_BUILT`, 404 `NODE_NOT_FOUND` and 400 `INVALID_ARTIFACT`. The code returns `packages/dashboard/src/routes/register-knowledge-routes.ts:78` as `ApiError(404, loaded.recoveryReason)`, where the values come from `packages/core/src/knowledge-graph/graph-store.ts:13` and are `missing-artifact`, `invalid-artifact`, `version-mismatch`, `inconsistent-artifact` and `forced`. `packages/dashboard/src/routes/register-knowledge-routes.ts:161` and `packages/dashboard/src/routes/register-knowledge-routes.ts:170` return `ApiError(404, "Unknown graph node")`. There is no 400 `INVALID_ARTIFACT` response.

- The endpoint table omits two live endpoints. specification.md:52-60 omits `GET /api/knowledge/query` at `packages/dashboard/src/routes/register-knowledge-routes.ts:107-124` and `POST /api/knowledge/refresh` at `packages/dashboard/src/routes/register-knowledge-routes.ts:198-214`.

- The endpoint table omits the memory commands. specification.md:52-60 lists only `fn knowledge-graph build`. The tree also ships `fn mcp serve-memory` at `packages/cli/src/bin.ts:1797` and `fn memory-backup` at `packages/cli/src/bin.ts:2028-2047`.

### Out of Scope

- The out-of-scope list contradicts shipped code. specification.md:126 excludes "LLM calls, embeddings, vector recall, and MCP tools". The tree ships a model-driven semantics pass at `packages/engine/src/memory/memory-semantics.ts:43-50`, an MCP memory server under `packages/core/src/memory/mcp/` with the CLI entry at `packages/cli/src/commands/mcp-memory-server.ts`, and durable recall records with graph cross-references at `packages/core/src/postgres/schema/project.ts:713-718`. The exclusion holds only for the deterministic extraction layer.

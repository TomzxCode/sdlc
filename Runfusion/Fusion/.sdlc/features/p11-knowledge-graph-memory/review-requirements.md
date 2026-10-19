---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Missing requirements

- The memory subsystem has no functional requirement. The Overview at requirements.md:11 names "a memory backend in packages/core/src/memory/", and the feature source list includes `packages/core/src/memory/`, `packages/engine/src/memory/`, `packages/cli/src/commands/memory-backup.ts`, and `packages/cli/src/commands/mcp-memory-server.ts`, but FR-1 to FR-6 and NFR-1 to NFR-4 only describe graph extraction, query, provenance, and the CLI build. Evidence: `packages/core/src/memory/index.ts:6-16` exports the memory barrel (memory-backend, memory-backup, memory-compaction, memory-dreams, memory-insights, project-memory, recall, recall-capture, mcp, memory-pre-steering).

- The Memory Keeper consolidation tick has no requirement. `packages/engine/src/memory/memory-consolidation.ts:35-56` (`runConsolidationTick`) refreshes the graph, appends recall material, cross-references graph node ids, and runs the semantics pass, and `packages/engine/src/memory/memory-consolidation-adapters.ts:29-30` wires the graph build and the inferred-edge write. FR-4 covers only the inferred edge write, not the tick that produces it.

- Durable recall records and their graph cross-reference have no requirement. `packages/core/src/postgres/schema/project.ts:713-718` defines the `memory_recall_records` table with a `content_hash` column, a unique key on project, kind and hash, a `graph_node_ids` jsonb column, and two indexes. `packages/core/src/memory/recall/recall-store.ts:37-45` (`appendRecall`) takes a per-project and per-kind advisory lock before inserting. `packages/core/src/memory/recall/recall-types.ts:6-17` defines the decision, preference and solution record kinds. `docs/knowledge-graph.md` documents this behavior under "Automatic recall capture", but no FR or NFR covers it.

- The recall material derived from rationale nodes has no requirement. `packages/engine/src/memory/memory-consolidation-material.ts:11-21` (`deriveRecallMaterial`) turns each rationale node into a decision record tagged with the node id and the owning file node id.

- The MCP memory server has no requirement, and the specification declares MCP tools out of scope. `packages/core/src/memory/mcp/memory-mcp-tools.ts`, `packages/core/src/memory/mcp/memory-mcp-handler.ts`, and `packages/core/src/memory/mcp/memory-mcp-serialization.ts` implement the tool surface, `packages/cli/src/commands/mcp-memory-server.ts` serves it, and `packages/cli/src/bin.ts:1797` registers `fn mcp serve-memory`.

- The memory backup and restore command has no requirement. `packages/core/src/memory/memory-backup.ts:15-25` defines the project, agents and all scopes plus retention, and `packages/cli/src/bin.ts:2028-2047` registers `fn memory-backup --create`, `--list` and `--restore`.

- The dashboard read surface for the graph has no requirement. `packages/dashboard/src/routes/register-knowledge-routes.ts:132-190` implements the status, nodes, node, neighbors, path and build endpoints, but FR-6 covers only the CLI command. The `POST /api/knowledge/refresh` endpoint at `packages/dashboard/src/routes/register-knowledge-routes.ts:198-214` and the `GET /api/knowledge/query` endpoint at `packages/dashboard/src/routes/register-knowledge-routes.ts:107-124` are also uncovered.

- The `knowledgeGraphDir` project setting is uncovered. `packages/core/src/knowledge-graph/graph-store.ts:12-15` defines `DEFAULT_KNOWLEDGE_GRAPH_DIR` and `resolveKnowledgeGraphDir`, `packages/dashboard/src/knowledge-graph-access.ts:50-53` reads `settings.knowledgeGraphDir`, and `packages/cli/src/commands/knowledge-graph.ts:48-51` reads the same setting.

- The rule that an incremental rebuild keeps inferred edges is not in FR-2. `packages/core/src/knowledge-graph/graph-builder.ts:53-55` retains every edge whose provenance is `inferred` across a structural rebuild, and `packages/core/src/knowledge-graph/graph-builder.ts:118-133` re-anchors each retained inferred edge to the current `from` node. FR-2 mentions only fingerprint reuse and deletion pruning.

- The inferred-edge writer's family restriction and its outcome counts are not in FR-4. `packages/core/src/knowledge-graph/inferred-edge-writer.ts:24-27` allows only concept to concept `relates-to` and rationale to symbol `rationale-supports`, and `packages/core/src/knowledge-graph/inferred-edge-writer.ts:12-17` reports `added`, `deduped` and `droppedUnresolved` separately.

- The rule that the semantics pass calls a model only when graph material changed is not in FR-4. `packages/engine/src/memory/memory-semantics.ts:50-52` returns `skipped: "unchanged"` when `graphChanged` is false, and `packages/engine/src/memory/memory-semantics.ts:54-57` returns `skipped: "no-candidates"` when there are no candidate nodes.

### Stale requirements

- Open question 1 at requirements.md:164 is answered by the code. It asks whether the dashboard Memory tab should trigger an automatic rebuild on a missing artifact. The code ships an explicit operator rebuild instead: `packages/dashboard/src/routes/register-knowledge-routes.ts:187-190` registers `POST /api/knowledge/graph/build`, `packages/dashboard/src/knowledge-graph-access.ts:85-96` implements `rebuildProjectKnowledgeGraph`, and `packages/dashboard/app/components/KnowledgeGraphPanel.tsx` exposes the control. Reads still report a missing artifact as a 404 with a recovery reason at `packages/dashboard/src/routes/register-knowledge-routes.ts:78`.

- FR-5 at requirements.md:32 understates the markdown rule. It says "markdown HTML comments outside fenced code", but `packages/core/src/knowledge-graph/extract-fnxc.ts:101-107` also refuses to open a comment inside narrowly defined indented code, which is four spaces or a tab after a blank line or another indented line. `docs/knowledge-graph.md` describes both fences and indented code.

- NFR-2 at requirements.md:42 and the code disagree about whether the artifact can be committed. NFR-2 says the artifact stays untracked and `.gitignore:134` ignores `.fusion-knowledge/`, but `packages/core/src/knowledge-graph/graph-store.ts:8-10` still says "The graph is review-visible and committable, while .fusion is ignored, so artifacts live under .fusion-knowledge/graph". The requirement matches the gitignore and `docs/knowledge-graph.md`, so the code comment is the stale part.

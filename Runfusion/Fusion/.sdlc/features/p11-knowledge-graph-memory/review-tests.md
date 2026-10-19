---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

- Three test cases have no requirement anchor. The Coverage Matrix at tests.md:62-73 maps FR-1 to NFR-4 only. TC-12 (`memory-backend-stash.test.ts`), TC-13 (`memory-search-topic.test.ts`) and TC-14 (`stash-settings.test.ts`) appear in no row, which follows from the requirements gap.

- TC-12 names an ambiguous file. `memory-backend-stash.test.ts` exists twice: `packages/core/src/memory/__tests__/memory-backend-stash.test.ts` covers session-folder assignment and event metadata, and `packages/core/src/__tests__/memory-backend-stash.test.ts` covers the Stash REST client against local http and https servers. The plan should name the path.

- TC-19 has no automated test. It is listed as an end-to-end case that runs `fn knowledge-graph build --force` on a checkout, but the only CLI-level test, `packages/cli/src/__tests__/knowledge-graph-command.test.ts:28-32`, mocks `@fusion/core` and asserts on the mocked build. No test spawns the command or builds a checkout through the CLI. The nearest coverage is `packages/core/src/knowledge-graph/__tests__/graph-builder-equivalence.test.ts:25-27`, which builds a fixture tree through the core builder.

- The two CLI test files for the graph are not in the plan. `packages/cli/src/__tests__/knowledge-graph-command.test.ts` and `packages/cli/src/__tests__/knowledge-graph-bundle-shape.test.ts` are absent from the Unit, Integration and End-to-End tables. The bundle-shape file at `packages/cli/src/__tests__/knowledge-graph-bundle-shape.test.ts:4` asserts the `typescript` runtime dependency that NFR-3 depends on.

- The dashboard HTTP contract has no test case. `packages/dashboard/src/routes/__tests__/register-knowledge-graph-routes.test.ts` covers the endpoints listed in the specification API table, and `packages/dashboard/src/__tests__/knowledge-graph-access.test.ts` covers the cache and the bounded path search. The plan stops at the CLI.

- The MCP memory server has no test case. `packages/core/src/memory/mcp/__tests__/memory-mcp-handler.test.ts`, `packages/core/src/memory/mcp/__tests__/memory-mcp-serialization.test.ts`, `packages/cli/src/commands/__tests__/mcp-memory-server.test.ts`, `packages/cli/src/commands/__tests__/mcp-memory-server-spawn.test.ts` and `packages/engine/src/__tests__/mcp-memory-handshake.test.ts` are all absent from the plan.

- The memory backend surface is only partly covered. Beyond the three listed files, the tree holds `packages/core/src/__tests__/memory-backend.test.ts`, `packages/core/src/__tests__/memory-compaction.test.ts`, `packages/core/src/__tests__/memory-dreams.test.ts`, `packages/core/src/__tests__/memory-insights.test.ts`, `packages/core/src/__tests__/project-memory.test.ts`, `packages/core/src/__tests__/memory-pre-steering.test.ts`, `packages/core/src/__tests__/agent-memory-mode.test.ts` and `packages/core/src/__tests__/available-memory.test.ts`. None is in the plan.

- The recall layer has no test case. `packages/core/src/__tests__/memory/recall-capture.test.ts`, `packages/core/src/__tests__/memory-recall-dedup-search.test.ts`, `packages/core/src/__tests__/memory-recall-instructions.test.ts`, `packages/core/src/__tests__/postgres/memory-recall-store.pg.test.ts` and `packages/core/src/__tests__/postgres/memory-recall-graph-cross-reference.pg.test.ts` are absent from the plan.

- The Memory Keeper engine pass has no test case. `packages/engine/src/__tests__/memory-semantics-pass.test.ts`, `packages/engine/src/__tests__/memory-consolidation-tick.test.ts`, `packages/engine/src/__tests__/memory-consolidation-ports.test.ts`, `packages/engine/src/__tests__/memory-consolidation-heartbeat-hook.test.ts`, `packages/engine/src/__tests__/memory-consolidation-run-audit-metadata.test.ts` and `packages/engine/src/__tests__/executor-memory-capture.test.ts` are absent from the plan.

- The memory backup command has no test case. `packages/cli/src/commands/__tests__/memory-backup.test.ts` and `packages/cli/src/commands/__tests__/memory-backup-lock-retry.test.ts` are absent from the plan.

- The declared scope is narrower than the test tree. tests.md:11 puts "Dashboard rendering and whole-graph canvas behavior" out of scope, but `packages/dashboard/app/components/__tests__/KnowledgeGraphPanel.test.tsx` and `packages/dashboard/app/hooks/__tests__/useKnowledgeGraph.test.ts` exist and cover the graph tab.

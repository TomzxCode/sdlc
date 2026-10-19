---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Missing test cases

- The coverage matrix has no row for FR-6 (foreach and loop). The code ships dedicated suites for both. Evidence: `packages/core/src/__tests__/workflow-ir-foreach.test.ts` (validation of foreach templates, modes, isolation, concurrency, and the rework-cycle clamp), `packages/core/src/__tests__/workflow-ir-loop.test.ts`, `packages/engine/src/__tests__/workflow-graph-foreach.test.ts`, `packages/engine/src/__tests__/workflow-graph-loop.test.ts`.
- The coverage matrix has no row for FR-7 (dashboard API routes and validation). The route suite lives at `packages/dashboard/src/routes/__tests__/workflow-validate-route.test.ts` and `packages/dashboard/src/routes/__tests__/workflow-setting-attribution.test.ts`.
- The coverage matrix has no row for NFR-3 (custom workflow reliability acceptance map). The map itself is a shipped artifact. Evidence: `docs/custom-workflow-reliability-acceptance-map.md`.
- No test case covers the workflow definition kinds (workflow versus fragment) or the fragment exclusion from pickers. Evidence: `packages/core/src/workflows/workflow-definition-types.ts:15`, `packages/core/src/task-store/workflow-definitions.ts:838`.
- No test case covers built-in workflow enablement, plugin gating, or deprecation. Evidence: `packages/core/src/workflows/builtin-workflows.ts:66` (`isBuiltinWorkflowToggleEligible`), `packages/core/src/workflows/builtin-workflows.ts:116` (`resolveEffectiveDefaultWorkflowId`), `packages/core/src/types.ts:75` (`DEPRECATED_BUILTIN_WORKFLOW_IDS`).
- No test case covers the save-time reconciliation rules (occupied column refusal, rehome target, incompatible field coercion). Evidence: `packages/core/src/__tests__/workflow-switch-reconciliation-report.test.ts`, `packages/core/src/__tests__/workflow-delete-rehome-default-entry.test.ts`.
- No test case covers the plugin workflow extension registry. Evidence: `packages/core/src/__tests__/workflow-extension-registry.test.ts`, `packages/core/src/workflows/workflow-extension-types.ts:8-15`.
- No test case covers the AI design route. Evidence: `packages/dashboard/src/routes/register-workflow-routes.ts:1036` (`POST /workflows/design`); no test file references `workflows/design`.
- No test case covers the board multi-lane payload. Evidence: `packages/dashboard/src/__tests__/board-workflows.test.ts`.
- No test case covers the agent and CLI workflow tools. Evidence: `packages/cli/src/__tests__/extension-workflow-tools.test.ts`, `packages/engine/src/agent-tools.ts:3189-4213`.
- No test case covers the optional-group (optional step) resolution, the trait registry, or the workflow lifecycle traits. Evidence: `packages/core/src/__tests__/workflow-optional-steps.test.ts`, `packages/core/src/__tests__/trait-registry.test.ts`, `packages/core/src/__tests__/workflow-lifecycle-traits.test.ts`.

### Stale test cases

- TC-3 names a test file that no longer exists. The custom v1 dispatch cases were absorbed into the no-selection default suite, and the absorbing file documents the move. Evidence: `packages/core/src/__tests__/no-selection-default-workflow-move.test.ts:78` (the note recording the merge), and the file `packages/core/src/__tests__/custom-v1-workflow-dispatch.test.ts` does not exist.
- TC-5 names a test file that no longer exists. The allowlist suite was renamed. Evidence: `packages/core/src/__tests__/sync-workflow-ir-callsite-allowlist.test.ts` is the current file, and `packages/core/src/__tests__/legacy-workflow-ir-callsite-allowlist.test.ts` does not exist.
- TC-8 states the invalid-definition case returns 400 with validation errors. The route returns 200 with a `valid: false` body and a typed error list, and reserves 400 for a missing body and 404 for an unknown workflow id. Evidence: `packages/dashboard/src/routes/__tests__/workflow-validate-route.test.ts:73-95`, `packages/dashboard/src/routes/register-workflow-routes.ts:331`.
- TC-2 lists four built-in IR suites, but the catalog now holds 13 built-ins and one suite asserts it covers every catalog id. Evidence: `packages/engine/src/__tests__/builtin-workflows-lifecycle.test.ts:523` ("covers every built-in workflow in the catalog"), `packages/core/src/workflows/builtin-workflows.ts:517-1004`.

### Stale key test files

- `packages/core/src/__tests__/custom-v1-workflow-dispatch.test.ts` does not exist. Evidence: `packages/core/src/__tests__/no-selection-default-workflow-move.test.ts:78`.
- `packages/core/src/__tests__/legacy-workflow-ir-callsite-allowlist.test.ts` does not exist. Evidence: `packages/core/src/__tests__/sync-workflow-ir-callsite-allowlist.test.ts`.
- `packages/core/src/__tests__/legacy-tombstones.test.ts` does not exist. The cutover ratchet lives in the engine package. Evidence: `packages/engine/src/__tests__/legacy-tombstones.test.ts`.
- The board-workflows test path is wrong. The suite lives in the dashboard package root test directory, not in the routes test directory. Evidence: `packages/dashboard/src/__tests__/board-workflows.test.ts` exists and `packages/dashboard/src/routes/__tests__/board-workflows.test.ts` does not.

### Test infrastructure

- The stated test infrastructure omits the PostgreSQL harness that the workflow suites depend on. Evidence: `packages/dashboard/src/routes/__tests__/workflow-validate-route.test.ts:6` (imports `createTaskStoreForTest` and `pgDescribe` from the shared harness), `packages/core/src/__test-utils__/pg-test-harness.ts`.

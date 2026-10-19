---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

### Architecture

- The core module list omits the trait, extension, reconciliation, and lifecycle modules that now own workflow semantics. Evidence: `packages/core/src/workflows/trait-registry.ts` (trait registry), `packages/core/src/workflows/workflow-extension-registry.ts` (plugin extension registry), `packages/core/src/workflows/workflow-reconciliation.ts` (save-time rehome and field-coercion rules), `packages/core/src/workflows/workflow-lifecycle-traits.ts` (column role resolution), `packages/core/src/workflows/workflow-lifecycle-direction.ts` (forbidden backward paths), `packages/core/src/workflows/workflow-ir-resolver.ts` (per-task IR resolution and drift pins), `packages/core/src/workflows/workflow-optional-steps.ts` (optional group resolution).
- The engine module list omits the durable work-item scheduler and the graph branch and column-boundary modules. Evidence: `packages/engine/src/workflows/workflow-work-scheduler.ts`, `packages/engine/src/workflows/workflow-work-processor.ts`, `packages/engine/src/workflows/workflow-graph-branches.ts`, `packages/engine/src/workflows/workflow-column-boundary.ts`, `packages/engine/src/workflows/workflow-graph-task-runner.ts`, `packages/engine/src/workflows/workflow-merge-nodes.ts`.
- The per-node runner list names a review runner that does not exist and omits the runners that do. Evidence: `packages/engine/src/workflow-node-runners/` contains `code-runner.ts`, `exit-gate-runner.ts`, `gate-runner.ts`, `merge-runner.ts`, `notify-runner.ts`, `parse-steps-runner.ts`, `verification-gate.ts` and no review runner. Review is a node handler at `packages/engine/src/workflows/workflow-node-handlers.ts:541` and `:593` plus a service at `packages/engine/src/workflows/workflow-review-service.ts:20`.
- The dashboard component list omits the panels and mobile surfaces that carry the editor. Evidence: `packages/dashboard/app/components/WorkflowColumnPanel.tsx`, `packages/dashboard/app/components/WorkflowAddStepModal.tsx`, `packages/dashboard/app/components/WorkflowOptionalStepsDropdown.tsx`, `packages/dashboard/app/components/WorkflowResultsTab.tsx`, `packages/dashboard/app/components/MobileWorkflowGraphView.tsx`, `packages/dashboard/app/components/WorkflowSwitcher.tsx`, `packages/dashboard/app/components/WorkflowIcon.tsx`.
- The diagram does not show the durable execution tables that back restart survival. Evidence: `packages/core/src/postgres/schema/project.ts:1134` (`workflow_work_items`), `:1191` (`workflow_run_branches`), `:1205` (`workflow_run_step_instances`).

### Data models

- The workflow definition model lists `kind` as an enum of `builtin / custom / v1`. The persisted kind is `workflow | fragment` and builtin-ness comes from the id prefix, not the kind. Evidence: `packages/core/src/workflows/workflow-definition-types.ts:15` (`WorkflowDefinitionKind = "workflow" | "fragment"`), `packages/core/src/workflows/workflow-definition-types.ts:53`, `packages/core/src/workflows/builtin-workflows.ts:30` (`isBuiltinWorkflowId` checks the `builtin:` prefix), `packages/core/src/postgres/schema/project.ts:840` (`kind: text("kind").notNull().default("workflow")`).
- The model lists `nodes` and `settings` as top-level definition fields. The definition stores the graph under `ir` and holds editor geometry under `layout`, and workflow settings live in a separate per-project table. Evidence: `packages/core/src/workflows/workflow-definition-types.ts:55` (`ir: WorkflowIr`), `:57` (`layout: Record<string, WorkflowNodeLayout>`), `packages/core/src/postgres/schema/project.ts:832-846` (workflows table columns), `packages/core/src/postgres/schema/project.ts:1226` (`workflow_settings` table).
- The model omits the fields the definition actually carries. Evidence: `packages/core/src/workflows/workflow-definition-types.ts:43-64` (`name`, `description`, `icon`, `lifecycleWarnings`, `createdAt`, `updatedAt`).
- No model covers the IR itself, whose version 2 shape adds columns, fields, artifacts, and settings declarations. Evidence: `packages/core/src/workflows/workflow-ir-types.ts:493-504` (`WorkflowIrV2`), `packages/core/src/workflows/workflow-ir-types.ts:478-483` (`WorkflowIrV1`).
- No model covers the task workflow selection row. Evidence: `packages/core/src/postgres/schema/project.ts:848` (`task_workflow_selection` with `workflowId` and `stepIds`).

### API contracts

- The documented request field is `definition`. The route accepts `ir` or `workflowId`. Evidence: `packages/dashboard/src/routes/register-workflow-routes.ts:141-147` (`requireIr` reads `body.ir`), `:321-329` (the `workflowId` branch).
- The documented response always carries `valid` and `errors`. A successful validation returns only `{ valid: true }`, and request errors return 400 or 404. Evidence: `packages/dashboard/src/routes/register-workflow-routes.ts:331` (`res.status(200).json(result.valid ? { valid: true } : { valid: false, errors: result.errors })`), `packages/dashboard/src/routes/__tests__/workflow-validate-route.test.ts:92-95` (400 for a missing body, 404 for an unknown id).
- The contract section documents one route. The workflow registrar mounts 23 routes, and the task workflow registrar mounts 89 more. Evidence: `packages/dashboard/src/routes/register-workflow-routes.ts` (23 route handlers including traits, step parsers, definition CRUD, setting values, prompt overrides, task selection, project default, board selection, export, import, and design), `packages/dashboard/src/routes/register-task-workflow-routes.ts` (89 route handlers).
- The import and export contracts are undocumented even though they are the portability boundary. Evidence: `packages/dashboard/src/routes/register-workflow-routes.ts:832` (`GET /workflows/:id/export`), `:868` (`POST /workflows/import`), `:860-867` (the documented validation order including the 409 forward-compatibility gate and the approval-flag stripping trust boundary).
- The design contract is undocumented. Evidence: `packages/dashboard/src/routes/register-workflow-routes.ts:1026-1036` (`POST /workflows/design` with 400, 429, 404, and 422 outcomes).

### Sequences

- The graph advance sequence routes the review node through `workflow-review-service`. The graph executor's step-review handler calls the review primitive directly, and the service is wired only in the legacy seam path. Evidence: `packages/engine/src/workflows/workflow-node-handlers.ts:609` (`primitives.runReview`), `packages/engine/src/executor/create-authoritative-workflow-seams.ts:467` (`new WorkflowReviewService()`).
- The sequence attributes the transition decision to a transition policy inside the graph. The transition policy is evaluated by the task store on moves, and the graph executor does not call it. Evidence: `packages/core/src/task-store/moves.ts:743` (`evaluateTransitionInvariants`), and no import of `workflow-transition-policy` in `packages/engine/src/workflows/workflow-graph-executor.ts`.
- The sequence omits the durable work-item and branch state that carries a run across a restart. Evidence: `packages/engine/src/workflows/workflow-work-scheduler.ts`, `packages/core/src/postgres/schema/project.ts:1134` (`workflow_work_items`), `:1191` (`workflow_run_branches`), `:1205` (`workflow_run_step_instances`).

### Technical decisions

- The decision to keep the IR in a single core module is stale. The IR is split across a type module, a parser module, a resolver module, and a settings module. Evidence: `packages/core/src/workflows/workflow-ir-types.ts`, `packages/core/src/workflows/workflow-ir.ts`, `packages/core/src/workflows/workflow-ir-resolver.ts`, `packages/core/src/workflows/workflow-settings.ts`.
- The decision to keep the graph executor in one engine module is stale. The executor, the task runner, the task runtime, the work scheduler, and the work processor are separate modules. Evidence: `packages/engine/src/workflows/workflow-graph-executor.ts:635`, `packages/engine/src/workflows/workflow-graph-task-runner.ts:389`, `packages/engine/src/workflows/workflow-task-runtime.ts:112`, `packages/engine/src/workflows/workflow-work-scheduler.ts`, `packages/engine/src/workflows/workflow-work-processor.ts`.
- The single-review-authority decision no longer matches the code, which supports two review paths, a legacy seam and a runtime primitive. Evidence: `packages/engine/src/workflows/workflow-node-handlers.ts:541` (`createStepReviewHandler`), `packages/engine/src/workflows/workflow-node-handlers.ts:593` (`createPrimitiveStepReviewHandler`), `packages/engine/src/workflows/workflow-node-handlers.ts:738-739` (the choice between them).
- The decision to own the visual editor in dashboard components is stale, because the editor also runs as a headless agent lane. Evidence: `packages/dashboard/src/routes/register-workflow-routes.ts:1026-1036` (`POST /workflows/design` with a rate limit and an agent session).

### Risks and unknowns

- The tracked reliability map exists and is current, so that risk is not stale. Evidence: `docs/custom-workflow-reliability-acceptance-map.md`.

### Out of scope

- The out-of-scope list is accurate. Evidence: `packages/engine/src/__tests__/legacy-tombstones.test.ts:60-108` ratchets the deleted legacy execution path.

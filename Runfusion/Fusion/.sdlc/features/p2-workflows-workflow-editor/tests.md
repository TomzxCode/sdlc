---
title: "Selectable Workflows & Visual Workflow Editor"
status: done
---

# Test Plan: Selectable Workflows & Visual Workflow Editor

## Scope

Covers built-in workflow IRs and catalog, workflow selection/resolution, graph execution and node runners, gates and transitions, the editor surface, and workflow validation routes. Lifecycle-board and merge tests belong to FEAT-p1/FEAT-p5.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Built-in workflow catalog resolves | no selection | Default built-in workflow applied |
| TC-2 | Built-in IR parses (coding, brainstorming, coding-ideas, lead-generation) | IR definition | Valid IR, correct node set |
| TC-3 | Custom v1 workflow dispatch | v1 definition | Dispatches to the intended node |
| TC-4 | Workflow settings resolver / no-selection default | settings + task | Resolved workflow |
| TC-5 | Legacy workflow IR call sites still allowlisted | legacy IR usage | Only allowlisted call sites exist |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Workflow lifecycle through built-in workflow | task in progress | Graph advances to done |
| TC-7 | Executor fast-mode workflows | fast-mode enabled | Executes via graph boundary |
| TC-8 | Workflow validate route | invalid definition | 400 / validation errors |
| TC-9 | Graph boundary (no legacy fallback) | store without workflow selection | Fail-closed park, not fallback |
| TC-10 | Workflow editor render + authoring | dashboard | Editor renders, nodes editable |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | Gate fails mid-graph | Graph halts or routes per transition policy |
| TC-12 | Graph interrupted by restart | Execution state preserved |

## Test Infrastructure

- Vitest across `@fusion/core`, `@fusion/engine`, `@fusion/dashboard`
- Workflow editor component tests under `packages/dashboard/app/components/__tests__/WorkflowNodeEditor*`

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-6, TC-9 |
| FR-3 | TC-1, TC-4 |
| FR-4 | TC-8, TC-10 |
| FR-5 | TC-11 |
| NFR-1 | TC-12 |
| NFR-2 | TC-9 |

## Key Test Files

- `packages/core/src/__tests__/builtin-workflows.test.ts`, `builtin-*-workflow-ir.test.ts`, `custom-v1-workflow-dispatch.test.ts`, `legacy-workflow-ir-callsite-allowlist.test.ts`
- `packages/engine/src/__tests__/builtin-workflows-lifecycle.test.ts`, `executor-graph-boundary.test.ts`, `executor-fast-mode-workflows.test.ts`, `benchmark-six-column-workflow.test.ts`, `workflow-*.test.ts`
- `packages/dashboard/src/routes/__tests__/workflow-validate-route.test.ts`, `board-workflows`
- `packages/dashboard/app/components/__tests__/WorkflowNodeEditor*`
- `packages/core/src/__tests__/legacy-tombstones.test.ts` (workflow cutover ratchet)
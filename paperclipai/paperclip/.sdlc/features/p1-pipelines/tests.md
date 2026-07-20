---
title: "Pipelines"
status: done
---

# Test Plan: Pipelines

## Scope

Tests cover pipeline and case CRUD, schema validation, pipeline health calculations, CLI parity, and end-to-end tutorial flow.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Pipeline health calculation returns correct status | Pipeline with cases in various stages | Health status enum |
| TC-2 | Pipeline schema validates correctly | Pipeline schema | Valid schema |

Files: `packages/shared/src/pipeline-health.test.ts`, `packages/db/src/pipelines-schema.test.ts`

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-3 | CLI pipeline commands work | Authenticated CLI | Pipeline CRUD operations succeed |
| TC-4 | Pipelines tutorial e2e flow | Fresh deployment | Complete tutorial flow passes |

Files: `cli/src/__tests__/pipelines.test.ts`, `tests/e2e/pipelines-tutorial-flow.spec.ts`

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-5 | UI case pages render correctly | Company has pipeline cases | List and detail pages display case data |

Files: `ui/src/pages/Cases.test.tsx`, `ui/src/pages/CaseDetail.test.tsx`

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-01 through FR-12 | TC-1, TC-2, TC-3 (unit + integration) |
| UI case management | TC-5 |
| E2E tutorial flow | TC-4 |

---
title: "Evals"
status: done
---

# Test Plan: Evals

## Scope

Tests cover the `src/harness.ts` adapter (model selection, environment isolation, documentation variants), the comparison runner (`src/plan.ts` task planning, `src/report.ts` observation pairing and lift summary), and the harness contract.
Model-backed eval runs themselves (smoke, documentation-audit, `*.docs.eval.ts`) are on-demand and excluded from the default unit suite.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | `src/harness.ts` adapts an `AgentSession` to the harness interface | Harness options | A valid harness instance |
| TC-2 | Task planning expands cases into `(case, variant, model, run)` arms | Discovered cases | Correct planned cohort |
| TC-3 | Observation reading attaches session artifacts and aggregates lift | Completed run | Artifacts recorded, paired summary |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | `vitest-evals` summary aggregates results across evals | Multiple eval results | Aggregated summary with pass/fail |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-5 | No provider/model configured | Eval run fails with a clear error |
| TC-6 | Harness without a model selection and no default | Run reports a configuration error |

## Test Infrastructure

- Ran with Vitest (`packages/evals/test/`):
  - `harness.test.ts`, `plan.test.ts`, `report.test.ts`, `comparison.test.ts`, `configured-runtime.test.ts`, `acme-server.test.ts`.
- Host evals live in `evals/` (`smoke.eval.ts`, `documentation-audit.eval.ts`) and documentation-lift evals in `evals/*.docs.eval.ts`; run via `npm run eval` (host) / `npm run eval:docs` (comparison) with a provider/model.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-07 | TC-2 |
| NFR-03 | TC-3, TC-4 |
| FR-04 | TC-5 |

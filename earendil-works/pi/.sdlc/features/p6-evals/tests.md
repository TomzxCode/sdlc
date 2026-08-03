---
title: "Evals"
status: done
---

# Test Plan: Evals

## Scope

Tests cover the `pi-harness` adapter, the `vitest-evals` harness primitives (harness-table, artifacts, summary), and the harness contract.
Model-backed eval runs themselves (smoke, extensions) are on-demand and excluded from the default unit suite.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | `pi-harness` adapts an `AgentSession` to the harness interface | Harness options | A valid harness instance |
| TC-2 | Harness table summarizes multiple harness configurations | Table of harnesses | Correct summary output |
| TC-3 | Artifact collection attaches session artifacts | Completed run | Artifacts recorded |

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
  - `pi-harness.test.ts`, `vitest-evals/artifacts.test.ts`, `vitest-evals/harness-table.test.ts`, `vitest-evals/summary.test.ts`.
- Core evals live in `src/` (`smoke.eval.ts`, `extensions.eval.ts`) and run via `npm run eval` with a provider/model.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-07 | TC-2 |
| NFR-03 | TC-3, TC-4 |
| FR-04 | TC-5 |

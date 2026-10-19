---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf8354fffesr0VHEmF0qeXtg
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### TC-1 is not implemented as described
- **Evidence:** `packages/evals/test/harness.test.ts` contains no test that creates a harness instance or an `AgentSession`. The file covers `resolveModelSelection` (`packages/evals/test/harness.test.ts:15-38`), `applyIsolatedEnvironment` (`packages/evals/test/harness.test.ts:40-61`), `resolveDocumentationVariant` (`packages/evals/test/harness.test.ts:63-70`), `excludePiDocumentation` (`packages/evals/test/harness.test.ts:72-91`), `verifySystemPrompt` (`packages/evals/test/harness.test.ts:93-104`), the missing-marker failures (`packages/evals/test/harness.test.ts:106-111`), and the container-sandbox guard (`packages/evals/test/harness.test.ts:113-115`). The session-creation path lives in `packages/evals/src/harness.ts:283-355` and is exercised only by model-backed eval runs, which the plan excludes.
- **Artifact says:** "| TC-1 | `src/harness.ts` adapts an `AgentSession` to the harness interface | Harness options | A valid harness instance |", and the coverage matrix maps FR-01 to TC-1.
- **Required change:** Either mark TC-1 as covering the model-backed path only (excluded from the default suite), or replace it with the cases that are actually unit tested: model selection precedence and rejection, environment isolation, variant resolution, system-prompt documentation stripping, prompt verification, and the container-sandbox guard. FR-01 has no automated coverage of the session creation itself.
- **Severity:** blocking

### TC-4 has no implementation
- **Evidence:** `packages/evals/test/comparison.test.ts:61-125` is a unit test of `summarizeEvalObservations` and `formatEvalComparisonReport` with hand-built `EvalObservation` values. `packages/evals/vitest.test.config.ts:8` includes only `test/**/*.test.ts`, and no test file starts a vitest-evals suite or aggregates real eval results. `packages/evals/src/report.ts:359-413` is the only aggregation code, and it is exercised only through those unit tests.
- **Artifact says:** The Integration Tests table lists "| TC-4 | `vitest-evals` summary aggregates results across evals | Multiple eval results | Aggregated summary with pass/fail |".
- **Required change:** Remove TC-4 or restate it as the unit-level pairing test it actually is (`packages/evals/test/comparison.test.ts`: paired lift, blocked pairs on errored or missing arms, duplicate observations, missing metrics kept distinct from zero, report formatting). No integration test exists.
- **Severity:** blocking

### `src/docker.ts` and `src/cli.ts` have no test coverage and are not in the plan scope
- **Evidence:** No file under `packages/evals/test/` imports `../src/docker.ts` or `../src/cli.ts`. The untested functions are `buildImages` (`packages/evals/src/docker.ts:38-61`), `requireEvalAuthFile` (`packages/evals/src/docker.ts:67-89`), `createDockerContext` (`packages/evals/src/docker.ts:126-135`), `discoverCases` (`packages/evals/src/docker.ts:137-154`), `runTask` (`packages/evals/src/docker.ts:161-175`), and the whole argument parser `parseEvalCli` (`packages/evals/src/cli.ts:27-86`), which defines the accepted flags, the file-selection rule, and the `PI_PROVIDER`/`PI_MODEL`/`PI_EVAL_RUNS_PER_VARIANT` fallbacks.
- **Artifact says:** The Scope section covers "`src/harness.ts` adapter (model selection, environment isolation, documentation variants), the comparison runner (`src/plan.ts` task planning, `src/report.ts` observation pairing and lift summary), and the harness contract."
- **Required change:** Add `src/docker.ts` and `src/cli.ts` to the plan scope and add test cases for the pure, testable parts: `parseEvalCli` flag and file parsing, the `requireEvalAuthFile` contract (missing file, invalid JSON, missing provider entry), and the cohort comparison that rejects mismatched variant discovery (`packages/evals/src/cli.ts:106-112`).
- **Severity:** blocking

### The coverage matrix omits requirements that the suite does exercise
- **Evidence:** FR-02 and NFR-01 are covered by `packages/evals/test/harness.test.ts:40-61` (the isolated home, agent directory, and `PI_EVAL_*` stripping with restore), and FR-03 is covered by `packages/evals/test/report.test.ts:158-182` (the session artifact is persisted to a per-variant `sessions/` JSONL file).
- **Artifact says:** The Coverage Matrix lists only FR-01, FR-07, NFR-03, and FR-04.
- **Required change:** Add FR-02, FR-03, FR-05, FR-06, and NFR-01 to the matrix, and mark FR-05 and NFR-02 as uncovered, since no test covers the argument filters or the auth-file contract.
- **Severity:** advisory

### TC-5 and TC-6 describe the same case
- **Evidence:** Both map to `packages/evals/test/harness.test.ts:32-37`, which asserts that an incomplete model selection throws "Select a harness model explicitly".
- **Artifact says:** "TC-5 | No provider/model configured | Eval run fails with a clear error" and "TC-6 | Harness without a model selection and no default | Run reports a configuration error".
- **Required change:** Merge TC-5 and TC-6 into one case and point it at `packages/evals/test/harness.test.ts:32-37`.
- **Severity:** advisory

## Open questions
- The plan does not state whether the comparison runner is expected to have a non-Docker test seam. `packages/evals/src/docker.ts:23-31` shells out to `docker` and `packages/evals/src/docker.ts:23` is not injectable, so a unit test of the runner currently needs either an injectable seam or a fake `docker` binary on `PATH`. The code does not make that choice.

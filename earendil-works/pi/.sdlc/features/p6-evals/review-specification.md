---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf8354fffesr0VHEmF0qeXtg
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The comparison runner CLI contract is incomplete and misroutes the model flags
- **Evidence:** `packages/evals/src/cli.ts:24-25` (`RUNNER_OPTIONS` is `--provider`, `--model`, `--runs-per-variant`; `FILTER_OPTIONS` is `-t`, `--testNamePattern`), `packages/evals/src/cli.ts:48-52` (the inline `--testNamePattern` form), `packages/evals/src/cli.ts:37-40` (file arguments), `packages/evals/src/cli.ts:71-83` (CLI selection wins over `PI_PROVIDER`/`PI_MODEL`; `PI_EVAL_RUNS_PER_VARIANT` is the fallback for the repetition count), `packages/evals/src/harness.ts:70-80` (the host harness reads the environment only).
- **Artifact says:** The API Contracts section documents a single command, `npm run eval`, with optional `--provider` and `--model` flags, `provider` described as "Default provider (`*` unless every harness sets its own model)", `model` as "Default model", and a response of "exit code | number | Vitest exit code for the eval run".
- **Required change:** Document the comparison runner contract: `--provider`, `--model`, `--runs-per-variant`, positional `*.docs.eval.ts` file arguments, `-t`/`--testNamePattern` filters applied during discovery, the environment fallbacks `PI_PROVIDER`, `PI_MODEL`, `PI_EVAL_RUNS_PER_VARIANT`, and the rule that CLI selection requires both `--provider` and `--model` while environment selection requires both variables (`src/cli.ts:72-77`). State that these flags reach the comparison runner only, that the host runner resolves its model from the environment only, and that the comparison runner exits nonzero when any pair is blocked (`src/cli.ts:192`) rather than returning a Vitest exit code.
- **Severity:** blocking

### The data model omits the comparison report and the on-disk artifacts
- **Evidence:** `packages/evals/src/report.ts:75-83` (`EvalComparisonReport` with `schemaVersion: 3`, `protocolDigest`, `control`, `treatment`, `comparisons`, `blockedPairs`, `operationalTotals`), `packages/evals/src/report.ts:43-73` (`EvalSetComparison`, `PairedMetricSummary`, `VariantTotals`, `BlockedPair`), `packages/evals/src/report.ts:32-34` (`EvalObservation` outcomes `scored`, `unscored`, `skipped`, `pending`, `errored`), `packages/evals/src/report.ts:11-19` (`EvalRunIdentity`, `ExpectedEvalRun`), `packages/evals/src/plan.ts:4-15` (`DiscoveredEvalCase`, `EvalTask`), `packages/evals/src/cli.ts:153-189` (`protocol.json`, `expected-runs.json`, `observations.jsonl`, `tasks/` Vitest JSON, per-variant `sessions/` JSONL, `report.json`, `report.txt`).
- **Artifact says:** The Data Models section has a single table, "Eval artifact", with two rows: `session` and `result`.
- **Required change:** Add the comparison report model and the artifact layout, including the `.eval/` run directory whose name is a timestamp plus a UUID, the protocol digest, the control/treatment assignment (`without_docs` is the control, `with_docs` the treatment, `src/report.ts:191-192`), the pairing key `(evalSet, caseId, model, runNumber)` (`src/report.ts:209-211`), and the rule that a pair contributes to lift only when both arms produce exactly one score (`src/report.ts:249-281`).
- **Severity:** blocking

### The comparison sequence flow is missing
- **Evidence:** `packages/evals/src/cli.ts:114-192` (build images, discover in both variants, require identical cohorts, plan every arm, run each arm, read native Vitest JSON through `@vitest-evals/core/node` at `src/report.ts:6`, pair, write the report), `packages/evals/src/docker.ts:137-154` (`discoverCases` runs `vitest list --json`), `packages/evals/src/docker.ts:161-175` (`runTask` runs one exact test name per container), `packages/evals/src/plan.ts:52-56` (variant order alternates by run number to reduce order bias).
- **Artifact says:** The Sequences section has one flow, "Run an eval", which covers only the host path: `npm run eval` to `vitest-evals` to `src/harness.ts` to a temp project plus agent dir, an adapted `AgentSession`, an attached session artifact, and a recorded result.
- **Required change:** Add the comparison sequence: build the `without_docs` and `with_docs` images from the staged runtime, discover cases in both images and require identical cohorts, plan every `(case, variant, model, runNumber)` arm before execution, run each arm in a fresh container, read the native Vitest JSON, pair exact arms, and write the comparison report.
- **Severity:** blocking

### The auth decision is wrong
- **Evidence:** `packages/evals/src/docker.ts:67-89` (`requireEvalAuthFile` requires a provider-keyed `auth.json` file), `packages/evals/src/docker.ts:121` (bind mount at `/run/pi-eval-secrets/auth.json`), `packages/evals/docker/Dockerfile:34-35` (mount point created with mode 0700), `packages/evals/docker/entrypoint.ts:109-110` (copied into the run agent directory), `packages/evals/src/harness.ts:312-315` (the host path uses `readStoredCredential`, which tolerates a missing file).
- **Artifact says:** "| Auth | normal `ModelRuntime` | Subscription + env API keys, no new secret handling |".
- **Required change:** Record that the comparison runner introduces its own secret handling: it locates the Pi `auth.json`, requires a credential entry for the selected provider, and mounts that file into the container as `/run/pi-eval-secrets/auth.json` with mode 0700. Environment API keys alone do not satisfy the comparison runner.
- **Severity:** blocking

### The isolation decision omits the container sandbox
- **Evidence:** `packages/evals/src/docker.ts:98-114` (read-only container, tmpfs mounts), `packages/evals/src/harness.ts:104-120` (`PI_EVAL_SANDBOX_UID` and `PI_EVAL_SANDBOX_GID` must both be set), `packages/evals/src/harness.ts:154-188` (permanent drop to the unprivileged identity, Vite transform cache made unreadable), `packages/evals/src/harness.ts:526-528` (the documentation harness refuses to run outside the container sandbox), `packages/evals/docker/entrypoint.ts:90-101` (evaluator sources are root-only and probed for sandbox readability).
- **Artifact says:** "| Isolation | temp project + agent dirs per eval | No side effects on the real workspace |".
- **Required change:** Add the second isolation layer used by the comparison path: Docker with a read-only root filesystem, a per-run container, a permanent drop to UID 65532 before the model is prompted, and root-only evaluator sources. Keep temp-dir isolation as the host-path decision.
- **Severity:** blocking

### The specification does not state that the package is private and has no public API
- **Evidence:** `packages/evals/package.json:4` (`"private": true`), `packages/evals/package.json` (no `exports` map), `packages/evals/` (no `src/index.ts`), `packages/evals/package.json:6-12` (the scripts are the only entry points).
- **Artifact says:** The Overview presents `pi-evals` as turning real Pi agent runs into behavioral evals, and the API Contracts section presents the CLI as the only contract, without stating the package's distribution status.
- **Required change:** State that `pi-evals` is a private, unpublished workspace package with no `src/index.ts` and no `exports` map, consumed only through its npm scripts.
- **Severity:** advisory

## Open questions
- The specification's "Out of Scope" list does not mention the model provider, and the code treats the provider as configuration rather than a feature. The code cannot answer whether a specific provider set is intended, so the scope boundary stays unstated.

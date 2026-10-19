---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf8354fffesr0VHEmF0qeXtg
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The documentation-lift comparison feature is missing from the requirements
- **Evidence:** `packages/evals/src/plan.ts:1` (`DOCUMENTATION_VARIANTS = ["without_docs", "with_docs"]`), `packages/evals/src/cli.ts:114-192` (orchestration), `packages/evals/src/docker.ts:38-61` (image build), `packages/evals/src/docker.ts:137-175` (case discovery and arm execution), `packages/evals/src/report.ts:359-413` (pairing and lift), `packages/evals/src/report.ts:379` (headline withheld when a pair is blocked), `packages/evals/src/cli.ts:192` (`process.exitCode = 1` on blocked pairs).
- **Artifact says:** The requirements cover only single-eval harness behaviour (adapt an `AgentSession`, isolate the run, attach session artifacts, run from the repo root, filter, ship core evals, per-eval model override). No requirement mentions two variants, paired arms, Docker, discovery, planning, or a comparison report.
- **Required change:** Add requirements for the documentation-lift experiment: the two variants `without_docs` and `with_docs` (`src/plan.ts:1`), the paired `(case, variant, model, runNumber)` arm plan (`src/plan.ts:39-59`), the requirement that both variants discover an identical case cohort (`src/cli.ts:106-112`), the requirement that each arm runs in a fresh container (`src/docker.ts:161-175`), the paired comparison report with blocked-pair handling, and the nonzero exit code when any pair is blocked (`src/cli.ts:192`).
- **Severity:** blocking

### FR-04 acceptance criterion is wrong about which runner receives `--provider` and `--model`
- **Evidence:** `packages/evals/src/cli.ts:24` (`RUNNER_OPTIONS` is parsed only by the comparison runner), `packages/evals/src/cli.ts:114` (the comparison runner is the only consumer of the parsed flags), `packages/evals/src/harness.ts:70-80` (`resolveModelSelection` reads only `options.model`, `PI_PROVIDER`, and `PI_MODEL`), `packages/evals/package.json:8` (`eval` runs `eval:host` first, which receives no flags).
- **Artifact says:** "**When** `npm run eval -- --provider openai --model gpt-5.6-sol` runs, **Then** evals execute with that default." The overview also says the system is runnable "from the repo root via `npm run eval` with a provider/model default".
- **Required change:** State that `--provider` and `--model` are consumed by the comparison runner only. The host evals resolve their model from `PI_PROVIDER` and `PI_MODEL` alone, so `npm run eval -- --provider X --model Y` leaves the host half running with the environment default, or failing with "Select a harness model explicitly or set both PI_PROVIDER and PI_MODEL as defaults." (`src/harness.ts:77`). There is no built-in default provider or model: `src/cli.ts:115` throws "Set PI_PROVIDER and PI_MODEL, or pass --provider and --model."
- **Severity:** blocking

### The auth constraint is wrong for the comparison runner
- **Evidence:** `packages/evals/src/docker.ts:67-89` (`requireEvalAuthFile` requires a readable `auth.json` file, valid JSON, with a property named for the selected provider), `packages/evals/src/docker.ts:121` (the file is bind-mounted at `/run/pi-eval-secrets/auth.json`), `packages/evals/docker/Dockerfile:34-35` (the mount point is created with mode 0700), `packages/evals/docker/entrypoint.ts:109-110` (the file is copied into the run agent directory), `packages/evals/src/harness.ts:312-315` (the host path reads the stored credential with `readStoredCredential`, which returns undefined when absent).
- **Artifact says:** "Requires the normal Pi `ModelRuntime` auth (subscription credentials or API-key env vars)." NFR-02 says "Evals shall not require real provider keys beyond the user's normal Pi auth."
- **Required change:** State that the comparison runner additionally requires a physical `auth.json` file at `$PI_CODING_AGENT_DIR/auth.json` (or `~/.pi/agent/auth.json`) that contains an entry keyed by the selected provider. A provider configured only through an environment API key is not enough: `requireEvalAuthFile` throws "Eval authentication file has no credential for provider ${provider}." (`src/docker.ts:86`).
- **Severity:** blocking

### The package is a private, script-only workspace package and the requirements do not say so
- **Evidence:** `packages/evals/package.json:4` (`"private": true`), `packages/evals/package.json` (no `exports` map, no `main`, no `bin`), `packages/evals/` (no `src/index.ts`), `packages/evals/package.json:6-12` (the only entry points are the `clean`, `eval`, `eval:host`, `eval:docs`, and `test` scripts).
- **Artifact says:** The overview presents `@earendil-works/pi-evals` as a package that "provides behavioral, model-backed evals for Pi workflows", with no statement that it is unpublished or has no importable surface.
- **Required change:** State that `pi-evals` is a private workspace package with no `src/index.ts` and no `exports` map, consumed only through its npm scripts, and therefore has no public API and is not published.
- **Severity:** blocking

### Isolation is described as temp directories only
- **Evidence:** `packages/evals/src/docker.ts:98-114` (containers run with `--read-only`, tmpfs for `/tmp` and the Vite temp dir, and a bind-mounted artifacts directory), `packages/evals/src/harness.ts:154-188` (the harness permanently drops to an unprivileged UID and GID), `packages/evals/src/harness.ts:526-528` (`createPiDocumentationEvalHarness` throws "Documentation evals must run in the isolated container sandbox." unless `PI_EVAL_CONTAINER=1` and a sandbox identity are set), `packages/evals/docker/entrypoint.ts:90-101` (evaluator sources must be root-only and unreadable by the sandbox user).
- **Artifact says:** NFR-01 says "Evals shall be isolated (temp dirs) so runs do not touch the real workspace." The technical approach in the specification describes only "temp project + agent dirs per eval".
- **Required change:** Record the stronger, second isolation layer: the comparison path requires Docker, a read-only container filesystem, and a permanent drop to UID 65532 with root-only evaluator sources. The host path keeps temp-dir isolation only.
- **Severity:** advisory

### FR-05 does not state which files the comparison runner accepts
- **Evidence:** `packages/evals/src/cli.ts:37-40` (only arguments ending in `.docs.eval.ts` are treated as file selections), `packages/evals/src/cli.ts:124-126` ("Documentation runner cannot execute non-doc eval").
- **Artifact says:** "The system shall support filtering evals by file or by test name (Vitest forwarding)."
- **Required change:** State that the comparison runner accepts only `*.docs.eval.ts` files and rejects other file arguments, and that the host runner forwards any Vitest filter unchanged.
- **Severity:** advisory

## Open questions
- The requirements leave open whether evals belong in CI. The code has no CI workflow that runs `packages/evals`; the only mention of evals in the repository workflows is the smoke eval file, so the question stays open and is not answerable from the code.

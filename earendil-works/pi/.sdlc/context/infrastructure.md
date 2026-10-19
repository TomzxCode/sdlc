<!-- session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8 -->
# Infrastructure

<!--
This file captures the project's technology stack, development tooling, CI/CD pipelines,
environments, and deployment procedures.
It gives implementation, testing, and deployment skills the commands and configuration they need without grepping the codebase each time.
Update this file when tooling, environments, or deployment procedures change.
-->

## Technology stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript, erasable syntax only in code checked by the root config | 7.0.2 |
| Runtime | Node.js, ESM only (`"type": "module"`) | >=22.19.0 |
| Monorepo | npm workspaces (`packages/*`, `apps/*`, five coding-agent extension examples) | root `pi-monorepo` 0.0.3, private |
| Published packages | ten workspace packages released in lockstep, plus the private `pi-evals` | 1.3.0 |
| Lint and format | Biome, tabs, indent width 3, line width 120, `recommended` rules | 2.3.5 |
| Test runner | Vitest | 4.1.11 |
| Bundler | esbuild | 0.28.2 |
| Remote execution daemon | Rust crate `pi-env` in `packages/env/daemon/`, edition 2024 | toolchain 1.96.0, crate 0.1.0 |
| Sandboxing | `pi-codemode`, QuickJS compiled to WebAssembly (`quickjs-wasi`) | 3.6.2 |
| SQL storage | SQLite through `node:sqlite`, used only by `pi-durable` | Node built-in |
| Other persistence | JSONL files (durable storage backend, coding-agent sessions) or memory (`MemoryStorage`) | n/a |

The Rust daemon is the only non-TypeScript source in the repository.
Its dependencies are pinned with `=` in `packages/env/daemon/Cargo.toml` and the build uses `cargo build --locked`.

| Directory | npm name | Published |
|---|---|---|
| `packages/ai` | `@earendil-works/pi-ai` | yes |
| `packages/agent` | `@earendil-works/pi-agent-core` | yes |
| `packages/tui` | `@earendil-works/pi-tui` | yes |
| `packages/coding-agent` | `@earendil-works/pi-coding-agent` | yes |
| `packages/codemode` | `@earendil-works/pi-codemode` | yes |
| `packages/mcp` | `@earendil-works/pi-mcp` | yes |
| `packages/env` | `@earendil-works/pi-env` | yes |
| `packages/durable` | `@earendil-works/pi-durable` | yes |
| `packages/chord` | `@earendil-works/chord` | yes |
| `packages/telemetry` | `@earendil-works/pi-telemetry` | yes |
| `packages/evals` | `@earendil-works/pi-evals` | no, private |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| npm | Install dependencies | `npm install --ignore-scripts` to hydrate, `npm ci --ignore-scripts` for a clean or CI install |
| Biome | Lint and format | `node scripts/biome-check.mjs --write`, run by `npm run check` |
| tsc | Type check | `tsc --noEmit`, run by `npm run check` |
| Repo checks | Dependency and import hygiene | `npm run check:pinned-deps`, `check:runtime-deps`, `check:ts-imports`, `check:entry-graphs`, `check:install-lock:coding-agent`, `check:browser-smoke` |
| Vitest | Package tests | `./test.sh` from the repo root |
| node --test | `packages/tui` tests and `scripts/*.test.mjs` | `node --test test/specific.test.ts`; `npm run test:scripts` for the scripts |
| MCP conformance | pi's MCP client against the pinned official suite | `npm run test:mcp-conformance` |
| Model data | Generate or verify provider model data | `npm run generate:models`, `npm run hydrate:model-data`, `npm run check:model-data` |
| Build | Build every package in dependency order | `npm run build`, `npm run build:offline` |
| cargo | Build the pi-env Rust daemon | `npm run build:daemon --workspace packages/env` |
| husky | Pre-commit hook, blocks lockfile commits | `PI_ALLOW_LOCKFILE_CHANGE=1` to allow a lockfile commit |
| Install lock | Regenerate the coding-agent install lock | `npm run install-lock:coding-agent`, verify with `npm run check:install-lock:coding-agent` |
| Release | Cut a release | `npm run release:patch`, `npm run release:minor`, `npm run release:major` |
| Publish | Publish to npm | `npm run publish`, dry run with `npm run publish:dry` |
| Local release | Pack, install, and smoke test without publishing | `npm run release:local` |
| Pack | Produce the tarball artifact set | `npm run pack:packages` |

`npm run check` runs, in order: `node scripts/biome-check.mjs --write`, `npm run check:pinned-deps`, `npm run check:runtime-deps`, `npm run check:ts-imports`, `npm run check:entry-graphs`, `npm run check:install-lock:coding-agent`, `tsc --noEmit`, `npm run check:browser-smoke`.
It does not run tests.

Never run the full Vitest suite directly, because the e2e tests activate when endpoint or auth environment variables are present.
Use `./test.sh` from the repo root, or one file from the package root: `node "$(git rev-parse --show-toplevel)/node_modules/vitest/dist/cli.js" --run test/specific.test.ts`.
`packages/tui` uses `node --test test/specific.test.ts` instead.

Build order is telemetry, then chord, then tui, then codemode, then mcp, then ai, then durable, then env, then agent, then coding-agent.

Never hand-edit `packages/ai/src/models.generated.ts`.
Change `packages/ai/scripts/generate-models.ts` and run `npm run generate:models` instead.

### Supply-chain hardening

- Every direct external dependency in every workspace `package.json` is pinned to an exact `x.y.z` version.
  `npm run check:pinned-deps` fails the build otherwise.
- `.npmrc` sets `save-exact=true` and `min-release-age=2`, so a dependency published less than two days ago cannot be installed.
- `package-lock.json` is the ground truth for the resolved tree.
  Refresh it with `npm install --package-lock-only --ignore-scripts` when dependency metadata changes.
- The pre-commit hook runs `scripts/check-lockfile-commit.mjs`, which blocks a `package-lock.json` change unless `PI_ALLOW_LOCKFILE_CHANGE=1` is set.
- `packages/coding-agent/install-lock/` is a generated two-file npm project that pins the CLI runtime tree for the pi.dev installer.
  `npm run check:install-lock:coding-agent` compares it byte for byte.
  A dependency with an install script is rejected unless it is on the `allowedInstallScriptPackages` allowlist in `scripts/generate-coding-agent-install-lock.mjs`, which currently holds `@google/genai@2.21.0` and `protobufjs@7.6.6`.
- CI installs with `npm ci --ignore-scripts`, so no lifecycle script runs during a build.
- The `npm-audit` workflow runs daily at 07:37 UTC: `node scripts/npm-audit.mjs` over `npm ci --ignore-scripts --no-audit --no-fund`, followed by `npm audit signatures --omit=dev`.
- Every GitHub Action in every workflow file is pinned to a commit SHA with a version comment.

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Local developer machine | topic branch (`feature/...`, `fix/...`, or a bare slug) | development and verification | n/a, the CLI runs from source |
| Integration | `main` | integration branch, releases are cut from here | n/a |
| npm registry | release tag `vX.Y.Z` | the ten published packages | https://registry.npmjs.org |
| pi.dev | n/a | installer, documentation, version check, model catalog, install telemetry | https://pi.dev |
| Model catalog store | n/a | published model catalogs, one per minimum pi version | https://pi.dev/api/models/revisions/<rev> |
| Nix stable | `stable` | fast-forwards to the latest release tag | n/a |

There is no staging environment, no preview environment, and no hosted pi service.

`main` is the integration branch, and a release tags `vX.Y.Z` on `main`.
The `stable` branch fast-forwards to the release tag in the `nix.yml` `update-stable` job.
That push has no `--force`, so `stable` never moves back to an older release.
`durable-env-*` branches also trigger the `env.yml` workflow.

pi.dev endpoints used by the CLI and the release pipeline:

| Endpoint | Used by |
|---|---|
| `https://pi.dev/api/latest-version` | the CLI version check |
| `https://pi.dev/api/report-install` | the install telemetry ping |
| `https://pi.dev/api/models`, `https://pi.dev/api/models/revisions/<rev>` | the model catalog |
| `https://pi.dev/api/installer/releases` | the managed installer and self-update |
| `https://pi.dev/install.sh`, `https://pi.dev/install.ps1` | the installer scripts |
| `https://pi.dev/docs/latest` | the documentation |

The version check is skipped by `PI_SKIP_VERSION_CHECK=1`, by `--offline`, and by `PI_OFFLINE`.
Install telemetry is opt-out through `PI_TELEMETRY=0` or the `enableInstallTelemetry` setting, and `PI_OFFLINE` suppresses it.

Remote pi-env SSH targets require explicit host-key trust.
Run `scanHostKey`, compare the fingerprint out of band, then call `acceptHostKey`, which writes the key to the target known-hosts file (`packages/env/src/ssh.ts`).

## CI/CD pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| `ci.yml` | push to `main`, pull request to `main` | `npm ci --ignore-scripts`, `npm run build`, `npm run check`, `npm run build:daemon --workspace packages/env`, `npm test`; a second job runs `npm run test:mcp-conformance` |
| `env.yml` | push to `main` or `durable-env-*`, pull request to `main` (filtered on `packages/durable/src/env/**`, `packages/durable/src/tools/**`, `packages/durable/test/env-*`, `packages/env/**`, and the two env workflow files), manual dispatch | calls `env-daemons.yml`; builds and checks the repo; asserts the `packages/env` tarball contains the expected `dist/`, `docs/`, and `bin/pi-env-<platform>/` entries and no `src/`, `daemon/`, or `test/`; runs the pi-env tests against the release daemon on six platforms; runs `cargo fmt --check`, `cargo clippy --locked --all-targets -- -D warnings`, `cargo test --locked`, and the durable env tests on five operating systems |
| `env-daemons.yml` | `workflow_call` with a `ref` input, manual dispatch | builds the Rust daemon for eight targets on native runners (linux x64 and arm64 musl, android arm64 and x64, darwin arm64 and x64, windows x64 and arm64) and uploads `pi-env-<platform>-<arch>` artifacts |
| `build-binaries.yml` | push of a `v*` tag, manual dispatch with `tag` and `source_ref` | builds the release binaries, smoke-tests them, stages a draft GitHub release, calls `env-daemons.yml`, publishes to npm, announces the release on pi.dev, publishes the GitHub release, and deletes the draft release when a step fails |
| `nix.yml` | push of a `v*.*.*` tag, pull request to `main` (filtered on the flake, `nix/**`, `package-lock.json`, `packages/*/package.json`, `packages/coding-agent/install-lock/**`), `workflow_run` after Publish Model Catalog, daily schedule, manual dispatch | refreshes the `nix/model-catalog.json` pin, runs `nix flake check --all-systems --no-build` and `nix build -L .`, and fast-forwards `stable` to the tag |
| `publish-model-catalog.yml` | `workflow_run` after CI completes, pull request on catalog paths, weekday schedule (`17 8-13 * * 1-5`, publishing at 10:17, 12:17, and 14:17 Europe/Vienna), manual dispatch | generates the catalog, runs `npm run check:model-catalog` and `check:model-catalog-compat`, uploads it to the catalog store |
| `npm-audit.yml` | daily schedule (`37 7 * * *`), manual dispatch | `npm ci --ignore-scripts --no-audit --no-fund`, `node scripts/npm-audit.mjs`, `npm audit signatures --omit=dev` |
| `approve-contributor.yml` | issue comment created | adds or removes an entry in `.github/APPROVED_CONTRIBUTORS` with capability `issue` for `lgtmi` or `pr` for `lgtm` |
| `issue-gate.yml` | issue opened | auto-closes issues from unapproved contributors, and skips `dependabot[bot]`, `sentry[bot]`, and `claude[bot]` |
| `pr-gate.yml` | pull request opened (`pull_request_target`) | closes pull requests from contributors without `lgtm` approval |
| `issue-triage-labels.yml` | issue reopened or labeled | manages the `untriaged`, `no-action`, `last-read`, `to-discuss`, and `inprogress` labels and their assignees |
| `remove-inprogress-on-close.yml` | issue closed | removes the `inprogress` label |
| `issue-analysis.yml` | issue labeled `pi-analyze`, or a comment asking for analysis | runs the repository `/is` prompt against the issue in a pi conversation, uploads a session gist, and can write back refreshed `PI_AUTH_JSON` |

All actions are pinned to commit SHAs.

## Deployment

There is no server-side deployment.
pi is a CLI, so a release publishes artifacts and packages rather than pushing code to a running service.

1. `npm run release:patch`, `npm run release:minor`, or `npm run release:major` runs `scripts/release.mjs`.
   It checks for a clean tree, verifies that every public workspace package is registered on npm, pins the newest published model catalog for Nix, bumps every package in lockstep, updates the per-package `CHANGELOG.md` files, regenerates the release artifacts, runs the checks and tests, commits and tags `vX.Y.Z`, adds fresh `[Unreleased]` sections, then pushes `main` and the tag.
2. The `vX.Y.Z` tag push triggers `build-binaries.yml`.
   The `build` job compiles the release binaries and `scripts/build-binaries.sh` mirrors it locally.
   The `smoke-test-binaries` job runs `scripts/smoke-test-codemode-binary.mjs` against the built binary.
   The `stage-github-release` job creates a draft GitHub release holding the source archive, the six platform archives, the install-lock files, `SHA256SUMS`, and the release notes, and verifies the checksums.
3. `env-daemons.yml` builds the pi-env daemon for every supported platform.
4. The `publish-npm` job runs in the `npm-publish` GitHub environment with OIDC trusted publishing: build, check, `npm run build:daemon`, `npm test`, `npm run check:package-install`, `node scripts/publish.mjs --dry-run`, then `node scripts/publish.mjs`.
5. The `announce-pi-dev-release` job verifies that every public package resolves at the exact release version and writes the release marker that `pi.dev/api/latest-version` reads.
6. The `publish-github-release` job turns the draft release into a published release.
   If any step fails, `cleanup-draft-github-release` deletes the draft.
7. `nix.yml` builds the flake and fast-forwards `stable` to the tag.
   `publish-model-catalog.yml` publishes the model catalog on its own schedule.

Supporting scripts: `scripts/release.mjs`, `scripts/publish.mjs`, `scripts/local-release.mjs`, `scripts/build-binaries.sh`, `scripts/create-source-archive.sh`, `scripts/pack-packages.mjs`.
`npm run release:local` (`scripts/local-release.mjs`) runs the pack, install, and smoke-test path without publishing.

### Rollback

- npm versions are immutable, so a published version cannot be replaced or removed.
  A bad release is fixed by publishing a new patch version.
- A draft GitHub release can be deleted, and `build-binaries.yml` deletes it automatically when a step fails.
  Once the release is published, the workflow refuses to mutate it.
- The publish helper is idempotent and skips package versions already on npm, so the failed `publish-npm` job can be rerun after fixing CI or a transient npm problem.
- The announcement job rechecks availability before updating the R2 marker, so the `announce-pi-dev-release` job can also be rerun.
- The Nix `stable` branch stays on the previous release if the Nix build fails, because the tag cannot be fixed.
  Fix `main` and ship the fix in the next release.
  The `stable` branch can be force-moved to an earlier tag by hand, but the workflow never does this.
- `pi update --self` updates or reinstalls the CLI from npm, so a user on a bad version can pull a fixed one.
- The repository documents no single formal rollback command beyond these paths, in `.pi/skills/release.md`.

## Health checks

There are no `/health`, `/healthz`, or `/ready` HTTP endpoints anywhere in this repository.
The readiness equivalents are:

| Check | What it reports | Where |
|---|---|---|
| `pi auth check` | provider and model credential readiness, with status `ready`, `not_ready`, or `invalid` | `packages/coding-agent/src/cli/auth-check.ts` |
| `host.ready()` | in-process object and host startup readiness; rejects with `unavailable/ready_timeout` after `readyTimeout`, which defaults to 60 s | `packages/chord/src/host.ts` |
| pi-env daemon `hello` handshake | protocol version, daemon version, remote platform, and features; a ping every 5 s and a 30 s silence limit enforce liveness | `packages/env/daemon/src/main.rs`, `packages/env/docs/protocol.md` |

`packages/coding-agent/docs/llama-cpp.md` documents the `/health` endpoint of a third-party llama.cpp server, which pi does not serve.

## Smoke tests

| Suite | Command | Covers |
|---|---|---|
| Browser smoke | `npm run check:browser-smoke` (`scripts/check-browser-smoke.mjs`) | esbuild-bundles `scripts/browser-smoke-entry.ts`, `scripts/durable-browser-smoke-entry.ts`, and `scripts/agent-treeshake-smoke-entry.ts` to catch Node-only imports in browser-facing exports; also run by `npm run check` |
| Coding-agent policy smoke | `scripts/coding-agent-smoke.mjs` (`smokeTestCodingAgent`) | policy smoke tests for the installed coding agent |
| npm consumer smoke | `scripts/local-package-install.mjs` (`smokeTestNpmConsumer`) | installs a tarball into a temp npm project and runs the generated `artifact-smoke.mjs` |
| Package install check | `npm run check:package-install` (`scripts/check-package-install.mjs`) | runs both smoke tests for every published package |
| Codemode binary smoke | `scripts/smoke-test-codemode-binary.mjs` | starts a fake OpenAI-compatible server, runs the built `pi` binary against it, and asserts that the `codemode` tool executes |
| Model-backed eval | `packages/evals/evals/smoke.eval.ts` | the smallest model-backed eval |
| MCP conformance | `npm run test:mcp-conformance` (`packages/coding-agent/test/mcp-conformance/run.ts`) | pi's MCP client against the pinned official conformance suite, with a regression baseline |
| pi-env conformance | `packages/env/test/*` | daemon, SSH, and terminal conformance and differential tests |

## Hosting

Hosting is local-first.
The CLI runs on the developer's own machine, and the files it writes stay there.
Remote execution goes through the pi-env SSH daemon, which is deployed to the target host and verified by SHA-256 before every start.
Persistence is JSONL files plus the durable SQLite store, both local.
The only hosted services are pi.dev, which serves the installer, documentation, model catalog, version check, and install telemetry, and the npm registry.
Nix packaging is provided by `flake.nix` and `nix/package.nix`, which build a `pi` package offline from a pinned model-catalog revision for `aarch64-darwin`, `aarch64-linux`, `x86_64-darwin`, and `x86_64-linux`.

## Secrets management

| Item | Where it lives | How it is used |
|---|---|---|
| Provider credentials in the environment | environment variables; the canonical list is `packages/ai/src/env-api-keys.ts` | read at runtime by the model registry, with OAuth PKCE for subscription providers |
| Stored credentials | `~/.pi/agent/auth.json` | the credential store used by `pi auth check` and the model runtime |
| npm publishing | npm trusted publishing over OIDC in the `npm-publish` environment | no long-lived npm token is stored in the repository |
| Issue analysis | the `pi-analyze` GitHub environment holds `PI_AUTH_JSON`, `PI_GIST_TOKEN`, and `PI_AUTH_UPDATE_TOKEN`; the `EARENDIL_ORG_READ_TOKEN` repository secret authorizes the actor | `issue-analysis.yml` |
| Catalog and release artifacts | AWS credentials for the R2 catalog store and the release marker | `publish-model-catalog.yml`, `build-binaries.yml` |
| pi-env daemon | the deployed binary is verified by SHA-256 before every start, and SSH host keys must be accepted out of band | `packages/env/src/ssh.ts` |
| Local test runs | `pi-test.sh` and `pi-test.ps1` unset 35 credential variables, and `./test.sh` runs `npm test` under `env -i` with an isolated HOME | no credential reaches the tests |
| Evals harness | the auth file is bind-mounted into the container at `/run/pi-eval-secrets` with mode 0700 | `packages/evals/docker/Dockerfile`, `packages/evals/src/docker.ts` |

Local `.env` files are gitignored and never committed.
The install telemetry ping to `https://pi.dev/api/report-install` is opt-out through `PI_TELEMETRY=0` or the `enableInstallTelemetry` setting, and `PI_OFFLINE` suppresses it.

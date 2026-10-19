# Infrastructure

This file captures the project's technology stack, development tooling, CI/CD pipelines, environments, and deployment procedures.

## Technology Stack

| Component | Technology | Version |
|---|---|---|
| Workspace | pnpm monorepo, root package `fusion-workspace`, published CLI `@runfusion/fusion` | 0.78.0-beta.7 |
| Language | TypeScript | ^5.7.0 (the CLI package pins 5.9.3) |
| Runtime | Node.js | `engines.node` >=22.19.0, CI composite defaults to Node 24, Dockerfile uses `node:22-slim` |
| Executable runtime | Bun (`bun build` for the single-file CLI binary) | via `pnpm build:exe` and `pnpm build:exe:all` |
| Package manager | pnpm | 10.33.0 (`packageManager` field, corepack in the Dockerfile) |
| Monorepo layout | pnpm workspace: `packages/*`, `plugins/examples/*`, and each named `plugins/fusion-plugin-*` package | `pnpm-workspace.yaml` |
| Framework (web) | React SPA plus Express 5 API server | React ^19.0.0, Express ^5.1.0, via `@fusion/dashboard` |
| Database | PostgreSQL (embedded `embedded-postgres` for local runs, Drizzle ORM over the `postgres` driver) | PostgreSQL 15, embedded-postgres 15.18.0-beta.17, drizzle-orm, postgres 3.4.9 |
| Desktop shell | Electron | ^35.0.0, via `@fusion/desktop` |
| Mobile shell | Capacitor | `@capacitor/core` ^8.5.1, via `@fusion/mobile` |
| Localization | i18next with `i18next-cli` | i18next ^26.3.6, via `@fusion/i18n` |
| Test runner | Vitest | ^4.1.10 |
| License | MIT | |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| pnpm | Package management and workspace scripts | `pnpm` |
| ESLint | Linting | `pnpm lint` |
| TypeScript | Type checking | `pnpm typecheck` (recursive, excludes `@fusion/desktop` and `@fusion/mobile`) |
| Vitest | Testing | `pnpm test` (changed-only, bounded), `pnpm test:gate` (merge gate), `pnpm test:full` (full suite, opt-in) |
| changesets | Published-package versioning | `pnpm changeset`, `pnpm version` (runs `changeset version`) |
| esbuild and bun | Build | `pnpm build` (`scripts/build-workspace.mjs`) |
| tsx | TypeScript execution for scripts | `tsx` |
| i18next-cli | i18n catalog extract, sync, and typegen | `pnpm i18n:extract`, `pnpm i18n:sync`, `pnpm i18n:types` |
| check scripts | Static guardrail scripts run in `pretest` and `test:gate:static` | `node scripts/check-*.mjs` |

Command reference:

- `pnpm test` runs the gate suite plus changed-only affected tests. It is bounded and never runs the full suite.
- `pnpm test:gate` is the merge gate. It runs the static gate checks, the curated `engine-core` suite, the core PostgreSQL gate suite, the core unit gate suite, and the CLI workflow test (`packages/cli/src/__tests__/ci-workflow.test.ts`).
- `pnpm smoke:boot` is the boot smoke. It checks CLI help, project init, and `/api/health` on a served dashboard.
- `pnpm verify:fast` is the test-free verification path. It bootstraps artifacts, typechecks and builds the changed packages, builds the CLI, and runs the boot smoke.
- `pnpm test:full` is the full workspace suite and needs an explicit opt-in.
- `pnpm verify:workspace` is the deep opt-in verification. It runs lint, the full test suite, and the full build.
- `pnpm check:changesets` validates the changeset body format.
- `pnpm check:routes-modular` validates dashboard route registrar modularity and mount order.

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Development | `main` | Default branch for ongoing work, and the source of the beta release channel | local `fn dashboard` on port 4040 |
| Beta npm channel | `main` | Pre-release `X.Y.Z-beta.N` published to the npm `beta` dist-tag, plus a GitHub prerelease | npm dist-tag `beta` |
| Stable release | `release` | Long-lived stable channel. `pnpm release --channel stable` publishes `latest`, marks the GitHub Release latest, and bumps the Homebrew tap | npm dist-tag `latest`, plus `https://runfusion.ai/install.sh` |
| Ad-hoc smoke | any | `pnpm smoke:boot` verifies CLI help, project init, and `/api/health` locally | `http://127.0.0.1:<ephemeral port>/api/health` |

## CI/CD Pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| `pr-checks.yml` | PR to `main` | The thin merge gate with four blocking jobs: Lint, Typecheck, Build, Gate. The Lint job also runs the changeset-format, pre.json anchor, route-modularity, lifecycle-column, SQL-column, move-target, inert-seam, FNXC-date, lane-wiring, plugin-interop, and quarantine-ledger ratchets. The Gate job runs the boot smoke and `pnpm test:gate`. The required checks are exactly Lint, Typecheck, Build, Gate |
| `full-suite.yml` | push to `main` | Non-blocking post-merge signal: four test shards, the dashboard curated-gate guard, the lifecycle-column ratchet drift check, the line-count audit, the engine slow tier, the pipeline smoke tier, the post-merge evidence gate, and the warm gate build cache |
| `desktop-packaging.yml` | PR to `main`, skipped unless the diff touches the dependency or desktop closure | Advisory `electron-builder --dir` dependency-closure walk. It is not in the required set |
| `desktop-windows.yml` | workflow_dispatch | Windows desktop build and signing, with an optional embedded-PostgreSQL smoke |
| `mobile.yml` | workflow_dispatch | Builds the dashboard web bundle, then an iOS artifact from it |
| `agent-browser-install.yml` | PR to `main`, path-gated to the agent-browser pack surface | Packs the CLI and the `agent-browser` tarball, then installs them on each supported desktop OS |
| `verify-elevated-restricted.yml` | workflow_dispatch, or push to `feature/win-elevated-no-user` or `fix/embedded-pg-encoding-auto-reinit` | Windows verification of the restricted-token PostgreSQL launch |
| `release.yml` | tag `v*` or workflow_dispatch | Builds the CLI binaries (Linux x64 and arm64, macOS arm64, Windows x64), the desktop installers for Windows, macOS, and Linux, and the Android APK and AAB, then creates the GitHub Release |
| `version.yml` | workflow_dispatch | npm publishing through changesets with npm OIDC trusted publishing. Stable channel only |
| `test-release.yml` | workflow_dispatch | Builds and tests the same binaries and installers as `release.yml` without creating a GitHub Release |
| `threatcrush-scan.yml` | pull_request | Security scan for credentials and vulnerable patterns. It produces SARIF, uploads it to the Security tab, and comments the report on same-repository pull requests |

## Deployment

- `@runfusion/fusion` is published to npm. `scripts/release.mjs` is the source of truth, and `pnpm release` is an operator-only human action.
- Never run a release from inside a Fusion task.
- `pnpm release --channel beta` runs on `main`. It enters changesets pre-mode, versions `X.Y.Z-beta.N`, publishes the npm `beta` dist-tag, tags `vX.Y.Z-beta.N`, and creates a GitHub prerelease. It does not bump the Homebrew tap.
- `pnpm release --channel stable` runs on the long-lived `release` branch. It exits pre-mode, publishes the npm `latest` dist-tag, marks the GitHub Release latest, and bumps the Homebrew tap.
- Without `--channel` the script prompts for a channel and defaults to the beta channel.
- `pnpm release --channel beta --resume` recovers a release that was interrupted before the tag was pushed.
- `release.yml` builds the platform binaries on `v*` tags.
- Desktop and mobile are packaged with signed installers (macOS and Windows signing scripts).
- The Docker image is built from `Dockerfile` (`node:22-slim`) with `docker build -t fusion .`. No registry publishes it.
- `version.yml` is the CI publish path. It publishes with npm OIDC trusted publishing, while the local `pnpm release` path uses the operator's npm token.

### Rollback

- Rollback is an npm and GitHub Release revert. Re-run the previous release, or run `changeset version` in the opposite direction and republish the prior tag.
- For betas, exit changesets pre-mode (`changeset pre exit`) before restoring.
- No automated canary or instant-rollback tooling exists.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `GET /api/health` | 200 with the health payload, including PostgreSQL connectivity, task-ID integrity, and migration status | `pnpm smoke:boot`, the merge-gate Gate job, dashboard boot |
| `GET /api/health/reliability` | 200 with reliability metrics JSON, scoped to the request project | dashboard Command Center reliability tab |
| `POST /api/health/reliability/reset` | 200 with the new `resetAt` timestamp | operator reset |
| `POST /api/health/refresh` | 200 with a recomputed health payload | operator or diagnostic refresh |
| `POST /api/health/compact` | 200 with per-table `VACUUM` and `ANALYZE` stats, or 503 when the PostgreSQL layer is unavailable | operator compact |
| `GET /metrics` | 200 with Prometheus text holding numeric gauges only. It is mounted at the app level, not under `/api` | Prometheus or an operator scrape |

`/api/health` and every path under `/api/health/` are exempt from bearer-token auth, and `/metrics` is public.
Other `/api/*` routes require a token when auth is configured (`packages/dashboard/src/auth-middleware.ts`).

## Smoke Tests

`pnpm smoke:boot` (`scripts/boot-smoke.mjs`) runs four assertions against the built workspace:

- `fn --help` exits 0 and mentions `serve`.
- `fn init` writes `.fusion/project.json` into a throwaway project.
- `fn serve` on an ephemeral port answers `GET /api/health` with 200 within a generous timeout.
- The server shuts down cleanly on SIGTERM.

The smoke runs with an isolated `HOME` and a throwaway project directory, and it never binds or kills the reserved port 4040.
It is deterministic and flake-free, and it is the recommended non-test verification path through `pnpm verify:fast`.

## Hosting

- Self-hosted model. There is no hosted SaaS deployment.
- Users install `@runfusion/fusion` from npm (or with the `https://runfusion.ai/install.sh` one-line installer), build the Docker image locally, or install a signed desktop or mobile build, then run the dashboard and CLI locally.
- The dashboard listens on port 4040 by default.
- Durable project state lives in PostgreSQL. Embedded mode uses a per-machine embedded PostgreSQL data directory. Multi-node fleets share state through an external `DATABASE_URL` and coordinate with the shared-cluster protocol (`docs/shared-mesh-protocol.md`).
- CI runs on GitHub Actions. Most jobs use `ubuntu-latest` runners. The shared `setup-node-pnpm` action defaults to Node 24, and `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` opts the JavaScript actions into Node 24.

## Secrets Management

- Project and global secrets are encrypted at rest with AES-256-GCM and stored in the `project.secrets` and `central.secrets_global` tables.
- The master key comes from the OS keychain when `keytar` is available, otherwise from a `master.key` file with 0600 permissions in the global Fusion directory.
- Each secret has an access policy (`auto`, `prompt`, or `deny`), resolved from the row, then the global `secretsAccessPolicy` setting, then a fallback of `prompt`.
- Secrets can be marked env-exportable with an export key, and each read is attributed with a timestamp and a reader identity.
- The local environment files `.env` and `.env.local` are gitignored.
- Node auth and MCP configs hold API keys. Plugin MCP servers and `.mcp.json` are gitignored.
- Credential material is never persisted in run-audit rows or logs.
- See `docs/secrets.md`.

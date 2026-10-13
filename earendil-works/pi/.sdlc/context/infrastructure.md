<!-- session_link: reconciled 2026-10-13 from codebase facts -->
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
| Language | TypeScript (erasable syntax only in checked code) | 7.0.2 |
| Runtime | Node.js (ESM, `type: module`) | >=22.19.0 |
| Monorepo | npm workspaces (`packages/*`, `apps/*`, coding-agent extension examples) | private root 0.0.3, per-package 1.2.0 lockstep |
| Storage | SQLite via `pi-durable` storage subpaths (`./storage/sqlite`) | workspace |
| Build | `tsc -p tsconfig.build.json` per package plus esbuild for bundles | esbuild 0.28.2, pinned in root devDependencies |
| Sandboxing | `pi-codemode` sandboxed JS on QuickJS WASM (`quickjs-wasi`) with worker-thread runtime (`src/runtime/worker.ts`, `vm.ts`, `wasm.ts`) | quickjs-wasi 3.6.2 |
| Remote env | `pi-env` Rust daemon (`packages/env/daemon`, Cargo package `pi-env` 0.1.0) plus TypeScript `RemoteExecutionEnv` client | workspace plus Cargo locked deps |
| Protocol client | `pi-mcp` standalone Model Context Protocol client (`src/client.ts`, `protocol/`, `transports/`) | workspace |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| Biome | Lint and format (tabs, width 3, line width 120) | `npm run check` (runs `node scripts/biome-check.mjs --write`) |
| tsc | Typecheck (TypeScript 7.0.2) | `tsc --noEmit` (part of `npm run check`) |
| Vitest | Unit tests for agent, ai, chord, codemode, coding-agent, durable, env, mcp, telemetry, evals | `./test.sh` for non-e2e, or per-file Vitest from package root |
| node --test | Unit tests for tui plus `scripts/*.test.mjs` via `test:scripts` | `npm run test` (workspaces) or `node --test test/specific.test.ts` |
| esbuild | Bundling and builds | via package build scripts in dependency order |
| cargo | Build the pi-env Rust daemon | `npm run build:daemon --workspace packages/env` (`cargo build --manifest-path daemon/Cargo.toml --locked`) |
| husky | Pre-commit hooks (blocks lockfile commits unless allowed) | `PI_ALLOW_LOCKFILE_CHANGE=1` to permit lockfile commit |
| release.mjs | Lockstep version bump, changelogs, commit plus tag | `node scripts/release.mjs patch\|minor\|major` for real, `npm run release:local` for smoke |
| install-lock scripts | Reproducible coding-agent install graph | `node scripts/generate-coding-agent-install-lock.mjs` (`--check` in CI as `check:install-lock:coding-agent`) |

Build order is chord, then tui, then telemetry, then codemode, then mcp, then ai, then durable, then env, then agent, then coding-agent.
Never run the full Vitest suite directly because e2e tests activate on endpoint or auth env vars.
Custom checks in `npm run check` are `check:pinned-deps`, `check:runtime-deps`, `check:ts-imports`, `check:entry-graphs`, `check:install-lock:coding-agent`, `tsc --noEmit`, and `check:browser-smoke`.

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| local | feature, fix, or short slug branches | Development and verification | n/a (CLI run from source) |
| integration | main | Integration branch and release source | n/a (tags cut from main) |
| distribution | vX.Y.Z tags | Public release via npm and binaries | https://pi.dev/api/latest-version (version check) |

There is no staging or production service deployment because the product is a CLI distributed via npm.
Install telemetry reports to `https://pi.dev/api/report-install`.
Version check is disabled with `PI_SKIP_VERSION_CHECK=1` or `--offline`.
Telemetry is disabled with `PI_TELEMETRY=0`.
Remote `pi-env` SSH targets require explicit host-key trust via `scanHostKey` then `acceptHostKey` into the target known-hosts file (`packages/env/src/ssh.ts`).

## CI/CD pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| ci.yml | push to main and PR to main | build, check, pi-env daemon build (`build:daemon`), tests, plus mcp-conformance job |
| env.yml | push or PR touching durable env, tools, or env package | execution-environment parity (Durable NodeExecutionEnv versus pi-env daemon plus RemoteExecutionEnv) on every OS |
| env-daemons.yml | called by env.yml and build-binaries.yml, or manual dispatch | builds pi-env daemon release artifacts (`pi-env-<platform>-<arch>`) on native runners (linux, macos, windows, android) |
| build-binaries.yml | tag push (`v*`) or manual dispatch | builds binaries and publishes via npm trusted publishing (OIDC) |
| nix.yml | tag push and PR to main | keeps the Nix flake model-catalog pin usable and builds release tags as tagged |
| npm-audit.yml | scheduled | dependency audit |
| publish-model-catalog.yml | scheduled or manual | publishes model catalog |
| pr-gate.yml | PR | PR quality gate |
| issue-gate.yml | issues | issue quality gate |
| issue-triage-labels.yml | issues | automatic issue labeling |
| approve-contributor.yml | PR comments | contributor approval flow |
| remove-inprogress-on-close.yml | issue close | project board cleanup |
| issue-analysis.yml | issues | issue analysis via `pi-analyze` label or staff comment trigger |

CI publishes releases with npm trusted publishing using OIDC (job env `npm-publish`).
No manual approval step is defined in the release workflow beyond pushing the tag.

## Deployment

Releases are cut with `scripts/release.mjs patch|minor|major`, which verifies npm registration, bumps all packages in lockstep, updates per-package `CHANGELOG.md` files, regenerates artifacts, runs checks and tests, then commits and tags `vX.Y.Z` and pushes.
Pushing the tag triggers `build-binaries.yml`, which calls `env-daemons.yml` for daemon artifacts before building and publishing via npm trusted publishing.
Use `npm run release:local` (`scripts/local-release.mjs`) for a local release smoke test without publishing.

### Rollback

There is no service rollback because distribution is versioned npm packages plus binaries under `packages/coding-agent/binaries/`.
Revert by publishing a new patch release with the fix (or revert commit) following the same release procedure.
Tags are immutable, so never move or reuse a published `vX.Y.Z` tag.

## Health checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| none | n/a (CLI product, no service endpoint) | n/a |

Grep for `/health`, `/ready`, and `healthz` in `packages/*/src` returns no matches.
State remains explicitly none unless a service component is added.

## Smoke tests

Browser smoke coverage runs with `npm run check:browser-smoke` (`scripts/check-browser-smoke.mjs`).
Release smoke coverage runs with `npm run release:local` (`scripts/local-release.mjs`).
Non-e2e regression coverage runs with `./test.sh` from the repo root.
MCP conformance coverage runs with `npm run test:mcp-conformance` (`packages/coding-agent/test/mcp-conformance/run.ts`).
Codemode binary coverage runs with `scripts/smoke-test-codemode-binary.mjs`.

## Hosting

Packages are hosted on the npm registry via trusted publishing.
Binaries ship under `packages/coding-agent/binaries/` (populated by the release binary build, otherwise gitignored).
Model catalog is published via `publish-model-catalog.yml`.
There is no application server, region, scaling policy, or infrastructure-as-code because there is no deployed service.

## Secrets management

Npm publishing uses OIDC trusted publishing with no long-lived local credentials.
Provider API keys are ambient environment credentials resolved at runtime via `ModelRegistry` (including OAuth PKCE for subscriptions).
Local `.env` files are gitignored and never committed.
Issue analysis automation uses `PI_AUTH_JSON` and `PI_GIST_TOKEN` environment secrets plus an org-read token for staff authorization.

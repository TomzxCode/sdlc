<!-- session_link: reconciled 2026-09-20 from codebase facts -->
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
| Language | TypeScript (erasable syntax only in checked code) | 5.9.3 |
| Runtime | Node.js (ESM, `type: module`) | >=22.19.0 |
| Monorepo | npm workspaces (`packages/*`, `packages/session-backends/*`, coding-agent examples) | private root 0.0.3, per-package 0.86.0 lockstep |
| Database | SQLite via `pi-storage-sqlite-node` (tested through agent harness) | bundled |
| Build | esbuild plus `tsx` for script execution | pinned in root devDependencies |
| Protocol | Custom CBOR protocol (`pi-protocol`) between client and server | workspace |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| Biome | Lint and format (tabs, width 3, line width 120) | `npm run check` (includes `biome check --write --error-on-warnings`) |
| tsgo | Typecheck | `tsgo --noEmit` (part of `npm run check`) |
| Vitest | Unit tests for ai, agent, coding-agent, protocol, client, server, evals | `./test.sh` for non-e2e, or per-file Vitest from package root |
| node --test | Unit tests for tui plus `scripts/*.test.mjs` via `test:scripts` | `npm run test` (workspaces) or `node --test test/specific.test.ts` |
| esbuild | Bundling and builds | via package build scripts in dependency order |
| tsx | Run TypeScript scripts directly | `tsx scripts/<name>.mjs` |
| husky | Pre-commit hooks (blocks lockfile commits unless allowed) | `PI_ALLOW_LOCKFILE_CHANGE=1` to permit lockfile commit |
| release.mjs | Lockstep version bump, changelogs, commit plus tag | `npm run release:local` for smoke, `scripts/release.mjs patch\|minor` for real |
| shrinkwrap scripts | Reproducible coding-agent install graph | `node scripts/generate-coding-agent-shrinkwrap.mjs` (`--check` in CI) |

Build order is chord, then tui, then telemetry, then ai, then durable, then agent, then sqlite-node, then protocol, then client, then server, then coding-agent.
Never run the full Vitest suite directly because e2e tests activate on endpoint or auth env vars.
Custom checks in `npm run check` are `check:pinned-deps`, `check:runtime-deps`, `check:ts-imports`, `check:entry-graphs`, `check:shrinkwrap`, `check:install-lock`, and `check:browser-smoke`.

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

## CI/CD pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| ci.yml | push and PR | lint, typecheck, and tests |
| build-binaries.yml | tag push | builds binaries and publishes via npm trusted publishing (OIDC) |
| npm-audit.yml | scheduled | dependency audit |
| publish-model-catalog.yml | scheduled or manual | publishes model catalog |
| pr-gate.yml | PR | PR quality gate |
| issue-gate.yml | issues | issue quality gate |
| issue-triage-labels.yml | issues | automatic issue labeling |
| approve-contributor.yml | PR comments | contributor approval flow |
| remove-inprogress-on-close.yml | issue close | project board cleanup |
| issue-analysis.yml | issues | issue analysis |

CI publishes releases with npm trusted publishing using OIDC (job env `npm-publish`).
No manual approval step is defined in the release workflow beyond pushing the tag.

## Deployment

Releases are cut with `scripts/release.mjs patch|minor`, which bumps all packages in lockstep, updates per-package `CHANGELOG.md` files, runs checks, then commits and tags `vX.Y.Z` and pushes.
Pushing the tag triggers `build-binaries.yml`, which builds and publishes via npm trusted publishing.
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

## Hosting

Packages are hosted on the npm registry via trusted publishing.
Binaries ship under `packages/coding-agent/binaries/`.
Model catalog is published via `publish-model-catalog.yml`.
There is no application server, region, scaling policy, or infrastructure-as-code because there is no deployed service.

## Secrets management

Npm publishing uses OIDC trusted publishing with no long-lived local credentials.
Provider API keys are ambient environment credentials resolved at runtime via `ModelRegistry` (including OAuth PKCE for subscriptions).
Local `.env` files are gitignored and never committed.

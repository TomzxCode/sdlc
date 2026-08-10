# Infrastructure

This file captures the project's technology stack, development tooling, CI/CD pipelines, environments, and deployment procedures.

## Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript | ^5.7.0 |
| Runtime | Node.js | 22 (CI actions images; Dockerfile `node:22-slim`) |
| Executable runtime | Bun (`bun build` for the CLI single-file binary) | via `build:exe` / `build:exe:all` |
| Package manager | pnpm (workspace) | 10.33.0 |
| Monorepo | pnpm-workspace (`packages/*`, `plugins/*`) | — |
| Framework (web) | React 19 SPA + Express API server | via `@fusion/dashboard` |
| Database | PostgreSQL (embedded `embedded-postgres` binaries for local/dev; Drizzle ORM `drizzle-orm` + `postgres` driver) | PG 15 |
| Desktop shell | Electron | via `@fusion/desktop` |
| Mobile shell | Capacitor | via `@fusion/mobile` |
| Localization | i18next (`i18next-cli`) | via `@fusion/i18n` |
| License | MIT | — |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| pnpm | Package management and workspace scripts | `pnpm` |
| ESLint | Linting | `pnpm lint` |
| TypeScript | Type checking | `pnpm typecheck` (scoped, excludes desktop/mobile) |
| Vitest | Testing | `pnpm test` (changed-only, gate + affected), `pnpm test:gate` (merge gate), `pnpm test:full` (full suite, opt-in) |
| changesets | Published-package versioning | `pnpm changeset`, `pnpm changeset version` |
| esbuild / bun | Build | `pnpm build` (`scripts/build-workspace.mjs`) |
| tsx | TypeScript execution for scripts | via `tsx` |
| i18next-cli | i18n catalog extract/sync/typegen | `pnpm i18n:*` |
| check scripts | Static guardrail scripts run in `pretest` (no-nohup, no-4040, no-getdatabase, changeset format, route modularity, etc.) | `node scripts/check-*.mjs` |

Testing commands (from AGENTS.md and `package.json`):
- `pnpm test` — gate suite + changed-only affected tests (bounded)
- `pnpm test:gate` — the merge gate (`test:gate:static` + engine-core curated suite + CI-shape test)
- `pnpm smoke:boot` — boot smoke: CLI `--help` + real `serve` `/api/health`
- `pnpm verify:fast` — test-free verification (artifact bootstrap + scoped typecheck/build + CLI build + boot smoke)
- `pnpm test:full` — full workspace suite (explicit opt-in only)

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Beta npm channel | `main` | Pre-release `X.Y.Z-beta.N` published to npm `beta` dist-tag; GitHub prerelease | npm dist-tag `beta` |
| Stable release | `release` | Long-lived stable channel; `pnpm release --channel stable` publishes `latest`, marks GitHub Release latest, bumps Homebrew tap | npm dist-tag `latest`; runfusion.ai installer |
| Ad-hoc smoke | any | `pnpm smoke:boot` verifies CLI help + `serve` health locally | `http://127.0.0.1:<free port>/api/health` |

## CI/CD Pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| `pr-checks.yml` | PR to `main` | Thin merge gate: Lint, Typecheck, Build, Gate (boot smoke + `pnpm test:gate`). Blocking; required checks are exactly those four jobs |
| `full-suite.yml` | push to `main` | Full sharded suite, engine slow tier, dashboard inventory guard. Non-blocking post-merge signal |
| `desktop-packaging.yml` | PR to `main` (path-gated) | Advisory `electron-builder --dir` dependency-closure walk; not in required set |
| `desktop-windows.yml` | workflow_dispatch | Windows desktop build/signing |
| `mobile.yml` | workflow_dispatch | Mobile web bundle build |
| `agent-browser-install.yml` | (manual/triggered) | Agent browser install |
| `verify-elevated-restricted.yml` | (manual) | Elevated/restricted verification |
| `release.yml` | tag `v*`, dispatch | Builds platform binaries and creates GitHub Release |
| `version.yml` | workflow_dispatch | npm publishing via changesets + npm OIDC trusted publishing (stable-channel only) |
| `test-release.yml` | workflow_dispatch | Test binary builds without creating a real release |

## Deployment

`@runfusion/fusion` is published to npm (`pnpm release`, operator-only human action). `scripts/release.mjs` is the source of truth: `--channel beta` runs on `main` via changesets pre-mode, publishes npm tag `beta`, tags `vX.Y.Z-beta.N`, creates a GitHub prerelease; `--channel stable` runs on the long-lived `release` branch, publishes `latest`, marks the GitHub Release latest, and bumps the Homebrew tap. Platform binaries are built by `release.yml` on `v*` tags. Desktop/mobile are packaged with signed installers (macOS/Windows signing scripts). Docker images build from `Dockerfile` (`node:22-slim`). Never run a release from inside a Fusion task.

### Rollback

Rollback is an npm/GitHub Release revert: re-run the previous release or `changeset version` in the opposite direction and republish the prior tag. For betas, exit changesets pre-mode (`changeset pre exit`) before restoring. No automated canary/instant-rollback tooling exists.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `GET /api/health` | 200 with health JSON (includes PostgreSQL health check) | `pnpm smoke:boot`, dashboard boot |
| `GET /api/health/reliability` | 200 with reliability metrics JSON | dashboard Command Center / reliability surface |
| `POST /api/health/refresh` | 200 | operator/diagnostic refresh |
| `POST /api/health/compact` | 200 | operator compact |
| `POST /api/health/reliability/reset` | 200 | operator reset |

All `/api/health` endpoints are exempt from bearer-token auth; other `/api/*` routes require a token when auth is configured (`packages/dashboard/src/server.ts`).

## Smoke Tests

`pnpm smoke:boot` (`scripts/boot-smoke.mjs`) boots the sourced-build CLI, asserts `fn --help` exits 0 and mentions `serve`, then serves the real dashboard and asserts `GET /api/health` returns 200 within a generous timeout. It is deterministic and flake-free, recommended as a non-test verification path (`pnpm verify:fast`).

## Hosting

Self-hosted model: there is no hosted SaaS deployment. Users install `@runfusion/fusion` from npm (or the runfusion.ai one-line installer), the Docker image, or signed desktop/mobile installers, and run the dashboard/cli locally. Multi-node fleets coordinate over a shared PostgreSQL backend via the mesh protocol (`docs/shared-mesh-protocol.md`). CI runs on GitHub Actions (ubuntu-latest runner images, Node 22/24; `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` opts actions into Node 24).

## Secrets Management

Project and global secrets are stored encrypted at rest (AES-256-GCM) in `project.secrets` / `central.secrets_global` under scopes with access policies (`auto`/`prompt`/`deny`), with per-key env-export controls and last-read attribution. Local environment: `.env`, `.env.local` (gitignored). Node auth and MCP configs hold API keys; plugin MCP servers and `.mcp.json` are gitignored. See `docs/secrets.md`. Credential material is never persisted in run-audit rows or logs.
# Infrastructure

<!--
This file captures the project's technology stack, development tooling, CI/CD pipelines,
environments, and deployment procedures.
It gives implementation, testing, and deployment skills the commands and configuration they need without grepping the codebase each time.
Update this file when tooling, environments, or deployment procedures change.
-->

## Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript (strict ESM, no `any`) | 6.0.3 |
| Runtime | Node.js (`>=24.16.0 <25 \|\| >=26.1.0`, Node 26 recommended) | See `node-version.mjs` floors |
| Package manager | pnpm (isolated linker, `verifyDepsBeforeRun: false`) | 12.4.0 |
| Bundler | tsdown via `scripts/tsdown-build.mts` | Pinned in `pnpm-lock.yaml` |
| Type checker | tsgo native compiler (`pnpm tsgo:core`, shards for extensions/scripts/tests) | Pinned in `pnpm-lock.yaml` |
| Gateway server | Custom `node:http` server in `src/gateway` (probe routing in `gateway-http-route-contracts.ts`) | n/a |
| Control UI | Lit web components built with Vite | Lit 3.3.3, Vite 8.3.0 |
| Database | SQLite via `node:sqlite` with Kysely query builder | Kysely 0.29.5 |
| Test runner | Vitest with per-area configs in `test/vitest/` | 5.0.0 |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| pnpm | Package management and workspace scripts | `pnpm install --frozen-lockfile` |
| oxfmt | Formatting (config: `.oxfmtrc.jsonc`) | `pnpm format` / `pnpm format:check` |
| oxlint | Linting (config: `.oxlintrc.json`, plus boundary guards in `config/oxlint/`) | `node scripts/run-oxlint.mjs` |
| tsgo | Type checking | `pnpm tsgo:core` (full: `pnpm tsgo:all`) |
| tsdown | Production build (`scripts/build-all.mts`, Docker variant `pnpm build:docker`) | `pnpm build` |
| Vitest | Unit tests (fast lane) and gateway/e2e suites | `pnpm test:fast` / `pnpm test` / `node --import ./scripts/tsx.mjs scripts/test-projects.mts` |
| tsx | Running TypeScript scripts without a build step | `node --import ./scripts/tsx.mjs scripts/<name>.mts` |
| Control UI dev server | Local UI development | `pnpm ui:dev` (build: `pnpm ui:build`) |

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Local dev | Any working branch | Day-to-day development, Gateway on loopback port 18789 by default | `http://127.0.0.1:18789` |
| CI ephemeral | PR or `main` push | Automated lint, typecheck, test, and build lanes | Varies per run |
| Docker Compose local | Any | Containerized Gateway plus CLI sidecar for isolation testing | Host port from `${OPENCLAW_GATEWAY_PORT:-18789}` |
| Operator production | Release tag or channel | User-operated Gateway (self-hosted, Fly.io, Render, or VPS); there is no centrally hosted OpenClaw fleet | Operator-defined |

## CI/CD Pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| `ci.yml` | Push to `main`, PR events, manual dispatch | Preflight routing manifest, then lint, tsgo typecheck, format check, Vitest suites, builds, UI tests, and platform lanes |
| `install-smoke.yml` / `install-smoke-reusable.yml` | Daily schedule (`17 3 * * *`) and manual dispatch | Installer and update smoke tests against the `latest` baseline |
| `openclaw-npm-release.yml` | Manual dispatch with release tag or SHA | Validation preflight, package build, and gated npm publish |
| `openclaw-release-publish.yml` | Manual dispatch with tag and preflight/validation evidence | Full release publication after Full Release Validation evidence checks |
| `openclaw-release-prepare.yml` | Manual dispatch with frozen publication inputs | Non-publishing npm and ClawHub preparation and recovery |
| `docker-release.yml` | `workflow_call` from the release flow | Multi-arch image build and push to GHCR and Docker Hub |
| `docker-image-refresh.yml` | Weekly schedule (Mondays) and manual dispatch | Dated rebuild of the stable and extended-stable image channels |
| `package-acceptance.yml` | Manual dispatch with package source | End-to-end acceptance of an npm, ref, URL, or artifact package candidate |

## Deployment

- Operator upgrades run through `openclaw update` with channel selection (`--channel`), dry-run preview, and recorded update history.
- Releases publish the `openclaw` npm package under version tags and channel dist-tags (`latest`, `beta`, `extended-stable`).
- The same release publishes Docker images to GHCR (`ghcr.io/openclaw/openclaw`, primary) and a Docker Hub mirror (`openclaw/openclaw`) with version, channel, and `-browser` variant tags.
- Fly.io deploys with `fly deploy` from the repo-root `fly.toml`, and Render deploys from the repo-root `render.yaml` blueprint.
- Release publication is maintainer-dispatched and gated on preflight plus Full Release Validation evidence, so routine operator updates need no manual approval but releases do.

### Rollback

- Roll back an operator install by running `openclaw update` against the previous version or channel, which restores the prior package and replays config reads from the restored code.
- Downgrades require explicit confirmation, and cleanup of staged originals permanently gives up rollback to those originals (see `docs/install/updating.md`).
- The serving Gateway stays in place while preflight checks run, so a failed update attempt does not take down the running instance.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `/healthz` (alias `/health`) | `200 OK` with `{ok: true, status: "live"}` | Docker `HEALTHCHECK` via `node dist/docker-healthcheck.js`, Compose healthcheck |
| `/readyz` (alias `/ready`) | `200 OK` with readiness payload when ready, `503` otherwise (details only for local or authenticated callers) | Gateway startup sequencing, orchestrators, `scripts/e2e` readiness waits |
| `/startupz` (alias `/startup`) | `200 OK` with `{ok: true, status: "started"}` once startup completes, `503` while starting | Fly.io `http_service.checks`, Render `healthCheckPath` |

## Smoke Tests

- Installer and update smoke coverage lives in `scripts/test-install-sh-docker.sh`, `scripts/test-install-sh-e2e-docker.sh`, and `scripts/e2e/cli-installer-distribution-docker.sh`, orchestrated by the `install-smoke` workflows.
- Release beta smoke checks run via `pnpm release:beta-smoke` (`scripts/release-beta-smoke.ts`).
- Container liveness smoke is the Docker healthcheck probe in `src/docker-healthcheck.ts`, which resolves the active Gateway port from the lock file and GETs `/healthz`.
- CI runs QA smoke lanes (`run_qa_smoke_ci` in the `ci.yml` preflight manifest) plus channel and contract suites for release qualification.

## Hosting

- OpenClaw is a self-hosted product with no operator-run production fleet, so each user hosts their own single-tenant Gateway.
- Supported targets are npm global install, Docker (GHCR primary, Docker Hub mirror), Fly.io (`primary_region = "iad"`, `shared-cpu-2x` with 2048 MB RAM and a persistent `/data` volume), Render (starter plan with a 1 GB `/data` disk), and documented VPS and bare-metal guides under `docs/install/`.
- Scaling follows a one-cell-per-tenant model where multi-user hosting means one Gateway container per tenant, not a shared server.
- Infrastructure as code lives at the repo root (`Dockerfile`, `docker-compose.yml`, `fly.toml`, `render.yaml`) with deployment guides in `docs/install/`.

## Secrets Management

- Local secret conventions live in `.env.example`, and env precedence is process env, then `./.env`, then `~/.openclaw/.env`, then the `openclaw.json` `env` block.
- Real secrets are never committed, and the Gateway refuses to start when `OPENCLAW_GATEWAY_TOKEN` still holds the documented example placeholder.
- Opt-in SecretRefs keep credentials out of plaintext config via `env`, `file`, `exec` (1Password, Bitwarden, Vault, `pass`, sops), and `store` providers backed by the shared SQLite secret store with egress-time sentinel injection.
- The lifecycle workflow is `openclaw secrets audit --check` to find plaintext residue, then `secrets configure` and `secrets apply` to migrate, as documented in `docs/gateway/secrets.md` and its subpages.

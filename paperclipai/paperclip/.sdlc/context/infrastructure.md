# Infrastructure

## Technology stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript (strict, ES2023 target) | `^7.0.2` |
| Runtime | Node.js | `>=24.11.0` |
| Package manager | pnpm (workspace monorepo) | `9.15.4` |
| API framework | Express | `^5.1.0` |
| UI framework | React + React Router + Vite | React `^19.2.8`, Vite `^8.2.2` |
| ORM / migrations | Drizzle ORM + drizzle-kit | ORM `^0.45.2`, kit `^0.31.10` |
| Database driver | postgres (plus embedded-postgres for dev packaging) | `^3.4.9` |
| Database dialect | PostgreSQL (`postgresql` in `packages/db/drizzle.config.ts`) | Postgres 17 in compose |
| Dev database | Embedded PGlite when `DATABASE_URL` is unset | n/a (local data in `data/pglite`) |
| Native runner | Rust crate in `packages/paperclip-runner` with pinned toolchain | see `packages/paperclip-runner/rust-toolchain.toml` |
| Auth | Better Auth sessions in `authenticated` mode | `1.7.2` |

- Language and runtime versions are pinned in `package.json:99-102` (`engines`, `packageManager`) and repeated in `server/package.json:165-167`, `ui/package.json:92-94`, and `cli/package.json:66-68`.
- The pnpm workspace layout is declared in `pnpm-workspace.yaml:1-14` (packages, adapters, plugins, server, ui, cli).
- TypeScript strictness and `ES2023` target live in `tsconfig.base.json:1-20`.
- The UI stack (React, Vite, Tailwind, TanStack Query, Lexical/MDX editor) is declared in `ui/package.json:31-75`.
- The server dependency surface (Express, Drizzle, `embedded-postgres`, `@aws-sdk/client-s3`, OpenTelemetry peers, Sentry peer) is declared in `server/package.json:46-138`.
- The CLI (`paperclipai` bin) bundles workspace code with esbuild and is declared in `cli/package.json:1-68`.

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| pnpm | Install, run, and orchestrate workspace scripts | `pnpm install` |
| tsx | Dev server and script runner | `pnpm dev` (via `scripts/dev-runner.ts`) |
| TypeScript | Type checking across all packages | `pnpm -r typecheck` |
| Vitest | Unit/integration tests (cheap default) | `pnpm test` / `pnpm test:run` |
| Playwright | Browser E2E suite (opt-in) | `pnpm test:e2e` |
| Playwright | Release smoke suite (opt-in) | `pnpm test:release-smoke` |
| esbuild / tsc / vite | Production builds | `pnpm build` |
| Token gates | UI design-token enforcement | `pnpm check:token-gates` |
| drizzle-kit | Generate SQL migrations from compiled schema | `pnpm db:generate` |
| drizzle migrate | Apply migrations | `pnpm db:migrate` |

- The cheap default test path is Vitest only, and browser suites stay opt-in (`AGENTS.md:153-168`).
- The full pre-handoff check is `pnpm -r typecheck`, `pnpm test:run`, `pnpm build` (`AGENTS.md:172-178`).
- UI changes must pass `pnpm check:token-gates` (`scripts/check-token-gates.mjs`) before committing (`AGENTS.md:226`).
- The database change workflow is edit `packages/db/src/schema/*.ts`, export from the schema index, run `pnpm db:generate`, then `pnpm -r typecheck` (`AGENTS.md:131-151`).
- `packages/db/drizzle.config.ts:1-10` reads the compiled schema from `./dist/schema/*.js` with dialect `postgresql`, so `pnpm db:generate` compiles first.

## Environments

| Environment | Source | Purpose | URL |
|---|---|---|---|
| Local dev | Any branch, `DATABASE_URL` unset | Embedded PGlite, API serves UI in middleware mode | `http://localhost:3100` |
| Local dev with Postgres | Any branch, `DATABASE_URL` set | Dev against external Postgres via compose | `http://localhost:3100` |
| Docker compose | `docker/docker-compose.yml` | Local Postgres 17 plus server container | Service-dependent ports |
| Production / self-hosted | `master` releases, Docker image or npm `paperclipai` | Operator-run instance | Operator-configured |

- Dev uses embedded PGlite by leaving `DATABASE_URL` unset, serving API and UI on `:3100`, with reset via `rm -rf data/pglite` (`AGENTS.md:44-70`).
- Compose ships Postgres 17 (`postgres:17-alpine`) with `pg_isready` health checks (`docker/docker-compose.yml:1-20`).
- The Docker image builds from `node:24-trixie-slim` with multi-stage deps/build targets (`Dockerfile:1-40`).
- Runtime auth has two modes, `local_trusted` and `authenticated`, where `authenticated` splits into `private` and `public` exposure (`doc/DEPLOYMENT-MODES.md:8-18`).
- Reachability (`server.bind`) is a separate concern with `loopback | lan | tailnet | custom` values (`doc/DEPLOYMENT-MODES.md:20-40`).
- `local_trusted` is loopback-only with no human login, while `authenticated + private` needs login on a trusted network and `authenticated + public` needs an explicit public URL plus stricter doctor checks (`doc/DEPLOYMENT-MODES.md:44-66`).
- Onboarding defaults are interactive and flagless via `pnpm paperclipai onboard`, with quickstart defaulting to loopback (`doc/DEPLOYMENT-MODES.md:86-110`).

## CI/CD pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| `pr.yml` | `pull_request` | Thin caller into `pr-trusted.yml@master` |
| `pr-trusted.yml` | `workflow_call` from `pr.yml` | Gate/policy, typecheck plus release registry, general and serialized tests, Docker context integrity, Runner verify, build, canary dry run |
| `commitperclip-review.yml` | `pull_request_target` (opened, synchronize, reopened) | Dependency review and quality gates from base-branch context, never PR code |
| `release.yml` | Push to `master`, nightly cron `0 9 * * *`, `workflow_dispatch` | Channel releases (`stable`, `beta`, `nightly`, `preview`, `cloud-migrator`) |
| `release-verify.yml` | `workflow_call` with a ref | Runner chaos evals, typecheck, and related verification for a candidate ref |
| `release-smoke.yml` | `workflow_dispatch` / `workflow_call` with a dist-tag | Installs the published artifact (systemd service leg plus Docker leg) and runs release smoke specs |
| `docker.yml` | Push to `master`, `v*` / `nightly/v*` / `beta/v*` tags, `workflow_dispatch` | Multi-arch self-hosted image build and GHCR push with monotonic canary retag |
| `docker-cloud.yml` | `workflow_dispatch` / `workflow_call` | Cloud image build for canonical master SHAs |
| `cloud-readiness.yml` | Push to `master`, `workflow_dispatch` | Cloud image, release verification, and exact-source artifact wait |
| `cloud-migrator-artifacts.yml` | Push to `master`, `workflow_dispatch` | Exact-source `db`/`shared` bundle plus lockfile with install verification |
| `e2e.yml` | `workflow_dispatch` | Paid allowlisted-actor E2E campaign behind the `runner-e2e-paid` environment |
| `runner-full-stack-e2e.yml` | Weekly cron, `workflow_dispatch` | Full-stack Runner E2E matrix with paid-campaign authorization |
| `runner-live-evals.yml` | Weekly cron, `workflow_dispatch` | Paid live Runner evals from the default branch only |
| `runner-protocol-live-evals.yml` | Weekly cron, `workflow_dispatch` | Direct protocol live evals against a pinned evals SHA |
| `runner-chaos-evals.yml` | Weekly cron, `workflow_dispatch`, `workflow_call` | Restart, replay, trace, and recovery fault suites, also used pre-release |
| `docker-runner-check.yml` | PRs touching the Dockerfile or native Runner sources | Native Runner compile plus dependency-cache reuse check |
| `agent-runtime-images.yml` | Push to `master` touching `docker/agent-runtime/**`, `workflow_dispatch` | Agent harness image bake and cosign signing to GHCR |
| `storybook-visual.yml` | PRs labeled `storybook-visual`, `workflow_dispatch` | Storybook visual regression against baselines |
| `storybook-deploy.yml` | `workflow_dispatch` / `workflow_call` | CODEOWNER-authorized Storybook publish to S3/CloudFront |
| `refresh-lockfile.yml` | Push to `master`, `workflow_dispatch` | Resolution-only `pnpm-lock.yaml` refresh with auto-PR |

- Trusted CI runs on a reusable workflow pinned to master so untrusted PR code cannot redefine CI (`pr.yml:1-20`).
- Node setup across workflows uses Node 24 with pnpm `9.15.4` (for example `release-verify.yml` setup steps).
- Release promotion order is canary, then nightly, then beta, then stable, enforced by tag requirements in `scripts/release.sh:20-50`.

## Deployment

- Releases are cut with `./scripts/release.sh <canary|nightly|beta|stable>` plus `--date`, `--dry-run`, `--skip-verify`, `--print-version`, and `--notes-file` flags (`scripts/release.sh:13-50`).
- Stable versions use `YYYY.MDD.P` date versioning, and canary/nightly/beta suffixed variants publish under matching npm dist-tags (`scripts/release.sh:30-50`).
- The npm `paperclipai` bundle is built by `./scripts/build-npm.sh` via esbuild with a forbidden-token check and typecheck gate (`scripts/build-npm.sh:1-40`).
- Stable tags get a GitHub Release via `./scripts/create-github-release.sh <version>` after pushing the tag (`scripts/create-github-release.sh:13-30`).
- Per-release notes live in `releases/` (for example `releases/v0.3.1.md`).
- Docker self-hosted images publish from `Dockerfile`, with compose entry points in `docker/` (`docker/docker-compose.yml`, `docker/docker-compose.quickstart.yml`, `docker/quadlet`, `docker/ecs-task-definition.json`).
- The npm channel aliases are `pnpm release`, `pnpm release:canary`, `pnpm release:stable`, `pnpm release:github`, and `pnpm release:rollback` (`package.json:36-42`).

### Rollback

- Rollback repoints the npm `latest` dist-tag with `./scripts/rollback-latest.sh <stable-version> [--dry-run]` (`scripts/rollback-latest.sh:1-30`).
- Rollback does not unpublish anything, it only moves the dist-tag pointer (`scripts/rollback-latest.sh:20-30`).
- No automated database down-migration path was found in the release scripts, so data rollback is a manual operator procedure.

## Health checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `GET /api/health` | `200` with `{ status: "ok" }` when ready, `"starting"` during startup, `503 { status: "unhealthy", error: "database_unreachable" }` on DB failure | Load balancers, compose health checks, workspace runtime probes, gateway mapping |
| `GET /api/companies/:companyId/secret-providers/health` | Provider health payload | Secrets settings UI |
| `POST /api/secret-provider-configs/:id/health` | Single provider config health payload | Secrets settings UI |
| `GET /api/plugins/:pluginId/health` | Plugin diagnostics payload | Plugin runtime and settings UI |
| `GET /api/pipelines/:pipelineId/health` | Pipeline health payload | Pipeline UI and API consumers |
| `POST /api/tool-connections/:connectionId/health-check` | Tool connection check result | Connections UI |

- The canonical health router is `healthRoutes` in `server/src/routes/health.ts:120-136`, mounted so it serves `/health` under `/api` (`server/src/app.ts:40`, `server/src/app.ts:635`).
- Anonymous callers on `authenticated` instances get a redacted payload (liveness, deployment mode, commit, bootstrap status), while board and agent actors get full details including server info and recovery state (`server/src/routes/health.ts:45-51`, `server/src/routes/health.ts:388-435`).
- The build commit SHA is intentionally public on every response so deploy tooling can identify the running build without authenticating (`server/src/routes/health.ts:254-258`).
- Health logging is exempted from verbose HTTP logs (`server/src/middleware/http-log-policy.ts:4`).
- Workspace runtimes probe `/api/health` on guests before publishing them as running (`server/src/services/workspace-runtime.ts:5380`, `server/src/services/workspace-runtime.ts:8364`).
- No separate `/ready` or `/healthz` endpoint was found, readiness is folded into the `status` field of `/api/health`.

## Smoke tests

- The release smoke suite lives in `tests/release-smoke/` and runs with `pnpm test:release-smoke` (`package.json:84`).
- Its Playwright config targets `PAPERCLIP_RELEASE_SMOKE_BASE_URL` (default `http://127.0.0.1:3232`) with Chromium, one CI retry, and screenshot plus trace on failure (`tests/release-smoke/playwright.config.ts:1-30`).
- Current specs cover Docker auth plus onboarding (`tests/release-smoke/docker-auth-onboarding.spec.ts`).
- The general browser E2E suite lives in `tests/e2e/` and runs with `pnpm test:e2e` (`package.json:66`).
- Runner-specific suites live in `tests/runner-e2e/` and `tests/runner-acceptance/` with dedicated vitest configs and launch scripts (`package.json:67-78`).
- Prompt-based evals live in `evals/promptfoo` and run with `pnpm evals:smoke` (`package.json:83`).
- Storybook visual baselines run with `pnpm test:storybook-visual` (`package.json:64`).

## Hosting

- Paperclip is self-hosted and local-first, with no default managed region found in the repo.
- The primary production artifact is the Docker image built from `Dockerfile` (base `node:24-trixie-slim`).
- Local orchestration uses `docker/docker-compose.yml` (Postgres 17 plus server with a `pids_limit` backstop), plus quickstart and untrusted-review variants in `docker/`.
- Alternative targets include systemd quadlet units (`docker/quadlet`) and an ECS task definition (`docker/ecs-task-definition.json`).
- File storage is pluggable with two providers, `local_disk` and `s3` (`packages/shared/src/constants.ts:823`).
- The S3 path uses `@aws-sdk/client-s3` (`server/package.json:47`) behind the storage interface in `server/src/storage/s3-provider.ts` and `server/src/storage/types.ts:1-40`.
- No infrastructure-as-code module (Terraform, Pulumi, CloudFormation) was found beyond compose, quadlet, and the ECS task JSON.

## Secrets management

- Secret vaults are pluggable with four provider ids: `local_encrypted`, `aws_secrets_manager`, `gcp_secret_manager`, and `vault` (`packages/shared/src/constants.ts:706-712`).
- The default is the local encrypted provider (`server/src/secrets/local-encrypted-provider.ts`).
- AWS Secrets Manager has a real provider (`server/src/secrets/aws-secrets-manager-provider.ts`), while GCP and Vault are unavailable stubs that store external references only (`server/src/secrets/external-stub-providers.ts:1-30`).
- Provider resolution and health aggregation go through `server/src/secrets/provider-registry.ts`.
- Full credential handling, rotation, and proposal flows live in the secrets feature, this section is only the hosting-relevant summary.

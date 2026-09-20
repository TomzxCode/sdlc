# Infrastructure

## Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript (strict, both packages) | ^6.0.3 |
| Runtime | Node.js | >=22 |
| Framework | TanStack Start (React 19, TanStack Router, nitro node-server preset) | React ^19.2.7, nitro 3.0.260610-beta |
| Database | PostgreSQL via Supabase (hosted tier) or embedded PGlite WASM Postgres (local tier) | postgres ^3.4.9, @electric-sql/pglite ^0.5.4 |
| ORM / migrations | Drizzle ORM + drizzle-kit (postgresql dialect, `packages/server/drizzle/`) | drizzle-orm ^0.45.2, drizzle-kit ^0.31.10 |
| Auth | Better Auth with GitHub OAuth | better-auth ^1.6.19 |
| Scheduler | In-process cron engine via croner (single owner, never scaled past one machine) | croner ^10.0.1 |
| Daemon | Node CLI binary `@crewlet/loopany` (poll loop, runner, watcher, MCP bridge via mcporter) | 0.17.0, mcporter 0.12.3 |
| Artifact bytes | Cloudflare R2 over S3 API (hosted) or in-memory store (local/test default) | @aws-sdk/client-s3 ^3.1075.0 |
| Build | Vite 8 + nitro (`vite build` then `node scripts/copy-pglite-assets.mjs`) | vite ^8.0.16 |
| Container | node:22-slim image with pnpm via corepack | Node 22 |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| pnpm | Package management (sole version source is root `packageManager`) | `pnpm install --frozen-lockfile` / `pnpm add ...` |
| tsc + tsr | Type checking (server regenerates routes first, so fresh checkouts typecheck) | `pnpm -r typecheck` |
| vitest | Unit and integration testing, both packages | `pnpm --filter @loopany/server test` / `pnpm --filter @crewlet/loopany test` |
| drizzle-kit | Generate SQL migrations from schema (needs no live DB) | `pnpm --filter @loopany/server db:generate` |
| drizzle-kit | Apply migrations to a real Postgres over `DIRECT_DATABASE_URL` | `pnpm --filter @loopany/server db:migrate` |
| vite dev | Local server on port 3000 (binds IPv4 `127.0.0.1`, `LOOPANY_PORT` overrides) | `pnpm dev` |
| vite build + nitro | Production bundle to `.output/server/index.mjs` | `pnpm build` |
| prestart + node | Boot gate (migrations/config check) then serve the nitro bundle | `pnpm start` |
| demo script | End-to-end cookie loop against the unified server | `bash scripts/demo-cookie-unified.sh` |

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| local | any worktree | Day-to-day development with embedded pglite at `LOOPANY_DATA_DIR/pgdata` (default `~/.loopany`), open auth unless GitHub gate env is set | http://127.0.0.1:3000 |
| staging | main | Auto-deployed pre-release testing on Fly app `loopany-testing` (region nrt, pglite on a 1GB volume via `LOOPANY_DB=pglite`) | https://loopany-testing.fly.dev |
| prod | main (via staging gate) | Live user-facing environment on Fly app `loopany-prod` (region sjc, stateless, Supabase Postgres plus R2) | https://loopany.ai |

## CI/CD Pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| deploy.yml (`Deploy (Fly)`) | push to `main` (ignores daemon-only and doc-only paths), or manual `workflow_dispatch` | `flyctl deploy --remote-only` to loopany-testing, then smoke-checks `/api/health` serves the pushed SHA |
| deploy-prod.yml (`Deploy Prod (Fly)`) | `workflow_run` completion of `Deploy (Fly)` gated on `conclusion == 'success'`, or manual `workflow_dispatch` | Preflights `FLY_API_TOKEN_PROD`, checks out the exact staged SHA, `flyctl deploy --ha=false -c fly.prod.toml -a loopany-prod`, then smoke-checks `/api/health` on loopany.ai |
| publish-daemon.yml (`Publish daemon (npm)`) | push of a `v*` tag (must match `packages/daemon/package.json` version), or manual `workflow_dispatch` | Frozen install, daemon build, `npm publish --access public` for `@crewlet/loopany` only via npm OIDC trusted publishing |

## Deployment

Staging deploys automatically on every push to `main` via `flyctl deploy --remote-only` with `GIT_SHA` and `BUILT_AT` baked in as image build args.
Prod is never deployed straight off a push or a `v*` tag, it auto-promotes only after the staging workflow for the same commit succeeds (pinned via the triggering run's `head_sha`), with `--ha=false` so exactly one machine runs the scheduler.
Prod promotions can also run out-of-band via manual `workflow_dispatch`, optionally behind required reviewers on the `production` GitHub environment.
Migrations are forward-only and apply at boot: `packages/server/scripts/prestart.mjs` runs the postgres-js migrator over `DIRECT_DATABASE_URL` on the hosted tier, while the embedded pglite tier migrates in-process via `runMigrations()`.
A missing `DATABASE_URL` without the explicit `LOOPANY_DB=pglite` opt-in fails the boot loudly (exit 1), so a lost DB secret can never silently boot an empty database.

### Rollback

Roll back by redeploying a previous image or re-running the deploy workflow at an older SHA, since each deploy bakes its commit into `/api/health`.
Migrations are forward-only, so rolling back the image does not roll back schema and a rollback must be checked against migrations applied since.
Check the fleet's `machines.daemon_version` before removing legacy daemon endpoints, since old daemons keep polling across a server rollback.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `/api/health` | 200 with `{ok: true, sha, builtAt}` (`"unknown"` in local dev) | Post-deploy smoke steps in both deploy workflows (assert served `sha` equals the pushed commit) |
| `/api/health/db` | 200 with `{ok: true, db: "up"}`, or fast 503 with `{ok: false, db: "down"}` on pool failure | Fly `[[http_service.checks]]` every 15s (10s timeout, 30s grace) on both apps, de-routes an unhealthy machine |

## Smoke Tests

Run `bash scripts/demo-cookie-unified.sh` for the end-to-end smoke test.
It boots the unified server on `LOOPANY_PORT` (default 3877), self-registers a demo device token via `POST /api/machine/poll`, creates a loop via `POST /api/machine/loop`, and reads the result back via `GET /api/machine/log`.
Both deploy workflows additionally run a post-deploy smoke loop that polls `/api/health` up to five times and fails the run if the served SHA does not match the deployed commit.

## Hosting

Both apps run on Fly.io as a single always-on machine (`auto_stop_machines = false`, `min_machines_running = 1`), because the in-process scheduler must never double-fire.
Staging (`loopany-testing`, region nrt) uses `shared-cpu-1x` with 512MB RAM and a persistent volume mounted at `/data` for pglite.
Prod (`loopany-prod`, region sjc, colocated with Supabase us-west-1) uses `performance-1x` dedicated CPU with 2048MB RAM and no volume, since all state lives in Supabase and R2.
Prod keeps a DB watchdog (`server/dbWatchdog.ts`, armed via `LOOPANY_DB_WATCHDOG`) that exits the process on a sustained pool wedge so Fly's restart policy brings up a fresh pool.
No infrastructure-as-code beyond `fly.toml`, `fly.prod.toml`, and `Dockerfile` at the repo root.

## Secrets Management

All server secrets live in Fly secrets, set once per app and never committed (see the setup comments at the top of `fly.toml` and `fly.prod.toml`).
`LOOPANY_AUTH_SECRET` is required at boot whenever the GitHub login gate (`GITHUB_CLIENT_ID`/`GITHUB_CLIENT_SECRET`) is enabled, and the app throws rather than falling back to a dev secret.
Database and storage credentials are `DATABASE_URL` (pooler `:6543`), `DIRECT_DATABASE_URL` (direct `:5432` for DDL), and the `LOOPANY_R2_*` keys (`ACCOUNT_ID`, `BUCKET`, `ACCESS_KEY_ID`, `SECRET_ACCESS_KEY`, optional `ENDPOINT`/`REGION`).
Machine identity uses opaque device tokens (`dk_` prefix, owner-visible only) and run leases (`rk_` prefix, keyed in `run_leases` by sha256 hash so a DB leak never yields live credentials).
Deploy tokens are split per environment (`FLY_API_TOKEN` for staging, `FLY_API_TOKEN_PROD` for prod, with a loud preflight when the prod token is empty), and daemon npm publishing uses OIDC trusted publishing with no long-lived `NPM_TOKEN`.
Push notification destinations (Slack, Telegram, Feishu webhook URLs) are per-team dashboard channels, not server secrets, with the Feishu URL guarded by an SSRF allowlist plus DNS and IP checks.

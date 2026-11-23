<!-- session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA -->
# Infrastructure

<!--
This file captures the project's technology stack, development tooling, CI/CD pipelines,
environments, and deployment procedures. It gives implementation, testing, and deployment
skills the commands and configuration they need without grepping the codebase each time.
Update this file when tooling, environments, or deployment procedures change.
-->

## Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript throughout | `npm:@typescript/typescript6@6.0.2` catalog, `@typescript/native` uses `npm:typescript@7.1.0-beta` |
| Runtime | Bun | `1.4.4` in root `packageManager`, CI also uses Node 24 and Node 26.4.0 for build checks |
| Core runtime | Effect | `4.1.0` catalog |
| HTTP API server | Effect HttpApi | Effect platform |
| Terminal UI | SolidJS with OpenTUI | `solid-js@1.9.17`, `@opentui/core@0.9.4` catalog |
| Web app | SolidJS with SolidStart, Vite, and Tailwind | SolidStart `2.1.0`, Vite `7.3.7` catalog, Tailwind `4.1.11` catalog |
| Desktop | Electron with electron-builder and electron-vite | Electron `44.9.1`, electron-builder `26.15.7`, electron-vite `6.0.0-beta.1` |
| Website and docs | SolidStart site in `services/site` | Site pins Vite `8.2.4` |
| Storage | SQLite with Drizzle and `@effect/sql-sqlite-bun` or `@effect/sql-sqlite-node` | Drizzle `1.0.0-rc.5-169397b`, Effect SQL `4.1.0` |
| Deployed services | Cloudflare Workers built with `cf` or Wrangler | Pinned CLIs under `.github/release/` |
| Infrastructure definitions | Nix flake, pinned Cloudflare configs, and a CLI Dockerfile | No SST config and no `infra/` directory |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| Bun | Package management and script running | `bun install`, `bun run --cwd <package> <script>` |
| Turbo | Monorepo task orchestration | `bun turbo test --concurrency=3`, `bun turbo typecheck --concurrency=3` |
| oxlint and ast-grep | Linting and structural rules | `bun run lint` |
| TypeScript | Local type check | `bun run typecheck` from root |
| TypeScript native | CI type check used by publish and checks | `bun run typecheck:tsc` from root |
| Combined check | Canonical full lint and type check | `bun run check` from root |
| Bun test | Unit tests | `bun turbo test` from root or `bun test` from a package directory |
| Playwright | Browser e2e and component tests | `bun --cwd packages/app test:e2e:built`, `bun --cwd packages/app test:components` |
| Husky | Git hooks | Installed by the root `prepare` script |
| Nix | Reproducible dev shell and packages | `nix develop`, `nix build .#opencode`, `nix build .#opencode-desktop` |
| Docker | CLI container image | `packages/cli/Dockerfile` uses prebuilt baseline musl binaries |

- Root workspaces are `packages/*`, `packages/plugins/*`, `services/*`, and `packages/data/*`.
- Root dev entry points are `dev`, `dev:live`, `dev:vite`, `dev:vite:live`, `dev:desktop`, `dev:web`, and `dev:site`.
- For live local UI work, run the backend with `bun dev serve --port 4096` and the app with `bun --cwd packages/app dev -- --port 4444`.
- Tests must run from package directories or through Turbo from root.
- The root `test` script exits 1 with `do not run tests from root`.

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| production | `production` | Live user-facing services and stable releases | `https://opencode.ai`, `https://docs.opencode.ai`, `https://opencode.ai/data`, `https://opencode.ai/update`, `https://opencode.ai/files/*` |
| dev | `dev` | Default branch, integration target, and dev service stage | `https://dev.opencode.ai` and stage dev Workers |
| beta | `beta` | Beta release channel, not a separate web deployment | No hosted beta site URL is configured |
| local | none | Local CLI, service, app, desktop, and site development | `http://localhost:4096` backend, `http://localhost:4444` app |

- The default branch is `dev` and pull requests target `dev`.
- `deploy.yml`, `deploy-site.yml`, `deploy-files.yml`, and `deploy-update.yml` select the stage from the branch name.
- `deploy.yml`, `deploy-site.yml`, and `deploy-files.yml` deploy both `dev` and `production`.
- `deploy-update.yml` deploys only `production`.
- The release schedule plans the `dev` channel, while pushes to `beta` plan the `beta` channel.
- No staging or pull request preview deployment is configured.
- No explicit manual approval step is encoded in the repository beyond GitHub environment protection.

## CI/CD Pipelines

The repository has 19 workflow files in `.github/workflows/`.

| Workflow | Trigger | What it runs |
|---|---|---|
| `check.yml` | Push to `dev`, PR into `dev` or `beta`, dispatch | `bun run lint`, `bun run typecheck:tsc`, and `bun run lint:changed HEAD^1` on PRs |
| `check-test.yml` | Push to `dev` or `beta`, PRs, dispatch, reusable call | Fast affected Linux unit tests on PRs. Full unit tests on Linux and Windows, compiled CLI builds, service smoke, library builds, Node build smoke, generated client and OpenAPI checks, and Playwright suites on pushes and manual runs |
| `check-docs.yml` | PR paths for docs, OpenAPI, CLI config, itself, dispatch | Site generation and docs build in `services/site` |
| `check-nix.yml` | Push to `dev`, PR into `dev`, dispatch | Flake evaluation for `x86_64-linux`, `aarch64-linux`, and `aarch64-darwin` |
| `check-process-daemon.yml` | Path-filtered PR or push to `dev`, dispatch | Rust, Zig, and Ghostty checks, Miri, fmt, clippy, tests, builds, and executable version smoke |
| `check-bot-scope.yml` | PR or dispatch | Requires `bot/nix-hashes` changes to be only a valid `nix/hashes.json` |
| `bot-nix-hashes.yml` | Push to `dev` on lock and package changes, dispatch | Builds Nix node modules and opens a PR that updates `nix/hashes.json` |
| `deploy.yml` | Push to `dev` or `production`, dispatch | Legacy Worker, data site, OG Worker, and data sync Workflow |
| `deploy-site.yml` | Push to `dev` or `production`, dispatch | opencode.ai site and V2 docs Worker |
| `deploy-files.yml` | Push to `dev` or `production`, dispatch | Public file distribution Worker |
| `deploy-update.yml` | Push to `production`, dispatch | Update Worker |
| `release.yml` | Push to `beta`, schedule every 6 hours, dispatch | Plans channel and version, runs the full test gate for stable releases, builds, signs, and publishes CLI, npm, desktop, Docker, Homebrew, AUR, Winget, GitHub release, and Discord artifacts |
| `release-process-daemon.yml` | Tag `process-daemon-v*`, path-filtered PR, dispatch | Builds, packs, signs, and publishes PTY binaries and npm packages |
| `nightly-beta.yml` | Daily schedule at 09:17 UTC, dispatch | Runs full beta tests and quarantine browser tests |
| `triage-contributor.yml` | PR opened | Adds the `contributor` label |
| `triage-close-issues.yml` | Daily schedule, dispatch | Closes stale issues with `script/github/close-issues.ts` |
| `triage-close-prs.yml` | Daily schedule, dispatch | Closes old PRs without enough positive reactions |
| `triage-pr-standards.yml` | PR opened, edited, or synchronized | Checks PR standards and posts findings |
| `triage-compliance-close.yml` | Every 30 minutes, dispatch | Closes items with `needs:compliance` after 72 hours |

## Deployment

- Deploy workflows split build and deploy.
- Build jobs run repository code with no stage secrets and no OIDC token.
- Build jobs upload an artifact with `SHA256SUMS` and report the manifest digest.
- Deploy jobs run in the `dev`, `production`, or `release` GitHub environment.
- Deploy jobs assume an AWS role through GitHub OIDC in `us-east-1`, then mint a short-lived Cloudflare token from the token issuer.
- Deploy jobs check out only `.github/release/`, verify the artifact digest, install pinned `cf` or Wrangler CLIs, and run one `deploy-*.sh` script.
- Deploy scripts treat artifacts as data and accept only the configs pinned in `.github/release/targets/`.
- Worker names, routes, custom domains, crons, Workflow names, exports, and bindings are pinned in those target files.
- Website builds run `bun script/build.ts --mode <stage>` from `services/site`.
- Data builds run `bun script/build.ts --mode <stage>` from `services/data`.
- Legacy builds run `cf build --mode <stage>` from `services/legacy`.
- Files and update builds run Wrangler dry-run deployment before the separate deploy job.
- Stable releases are cut by dispatching `release.yml` on `dev` with a bump or version and reviewed release notes. Only listed releasers can start them.
- Dev releases run from the `release.yml` schedule on `dev` and from dispatch without a bump or version.
- Beta releases run from pushes to `beta`.
- Process daemon releases run from `process-daemon-v*` tags.
- Nix packages are built from `flake.nix` and hashes are refreshed by `bot-nix-hashes.yml`.

### Rollback

- No dedicated rollback workflow is documented in the repository.
- Revert the source change on `dev` or `production` and push to re-run the matching deploy workflow.
- Re-run a deploy workflow by dispatch from a known good branch ref.
- For a published release, cut a new release with a fixed version.
- Changing a pinned deploy target is a separate review because CODEOWNERS reviews `.github/`.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `GET /api/info` | `ServerInfo` with 200 when ready, 500 when failed, and 503 while starting or stopping | Local service clients and the compiled service smoke test |
| `GET /openapi.json` | 200 with the generated API document when authenticated | Generated artifact checks and the compiled service smoke test |
| `GET /api/health` in the data app | `{ "ok": true, "app": "stats" }` | Data app route only |

- No dedicated `/health`, `/healthz`, `/ready`, `/live`, or `/ping` route was found in `packages/server/src` or `packages/protocol/src`.
- No deploy workflow performs a post-deploy health check.

## Smoke Tests

| Test | Command | Covers |
|---|---|---|
| Compiled service lifecycle | `bun run script/build.ts --single --skip-install` then `bun run script/service-smoke.ts` from `packages/cli` | Service election, registration, readiness, auth, web UI assets, MCP socket, plugin watcher, stop, and cleanup |
| Node build lifecycle | `bun run script/build-node.ts --single --skip-install --outdir=dist/node` then `bun run script/service-smoke.ts --node` from `packages/cli` | Same service contract for the Node build |
| App e2e | `bun --cwd packages/app test:e2e:built --shard=1/2` and `--shard=2/2` | Built web app against the production build |
| Service worker | `bunx playwright test --config e2e/service-worker/playwright.config.ts` from `packages/app` | Precache and upgrade behavior |
| Components | `bun --cwd packages/session-ui test:components` and `bun --cwd packages/app test:components` | Component behavior on mounted stories |
| Generated contracts | `bun run check:generated` in `packages/client` and `packages/protocol` | Generated client and OpenAPI document freshness |

## Hosting

- Web services run on Cloudflare Workers.
- The site uses `cf` Build Output and pinned configs in `.github/release/targets/site/<stage>/`.
- The legacy Worker serves `opncd.ai` and `api.opencode.ai`.
- The data service deploys three Workers from `services/data`: the site, an OG image Worker, and a sync Workflow.
- The data database is the `opencode-stats` PlanetScale database, with `dev` and `production` branches.
- The update Worker uses Cloudflare D1 and receives events through a Cloudflare Pipeline.
- The files Worker serves `opencode.ai/files/*` from R2.
- CLI, desktop, and Docker artifacts publish through `release.yml`, with CLI and desktop uploads sent to R2.
- The CLI Dockerfile uses Alpine with prebuilt `linux-x64-baseline-musl` or `linux-arm64-musl` binaries.
- Deploy and release jobs use AWS roles in `us-east-1` for secret access and token minting.
- CI uses Blacksmith Ubuntu 24.04 and Windows 2025 runners. Release signing uses macOS 26 and Windows 2025 runners.
- The Nix flake supports `x86_64-linux`, `aarch64-linux`, and `aarch64-darwin`, with `opencode` and `opencode-desktop` packages.
- Scaling is managed by Cloudflare. No capacity or autoscaling rules are kept in this repository.

## Secrets Management

- Build jobs do not receive stage secrets or an OIDC token.
- Deploy jobs read stage secrets from AWS Secrets Manager at deploy time and pass them to `cf` through temporary files.
- Stage roles are `arn:aws:iam::604439173067:role/github/opencode-dev` and `arn:aws:iam::604439173067:role/github/opencode-production`.
- Release jobs use `arn:aws:iam::604439173067:role/github/opencode-release` in the `release` environment.
- Deploy jobs mint 15-minute Cloudflare tokens through `vars.CLOUDFLARE_TOKEN_URL`.
- Release CLI and desktop uploads use 30-minute Cloudflare tokens minted by `.github/release/cloudflare-token.sh`.
- Legacy production reads `opencode/production/GITHUB_APP_ID` and `opencode/production/GITHUB_APP_PRIVATE_KEY`.
- Data services read `opencode/<stage>/DATA_DATABASE_HOST`, `DATA_DATABASE_USERNAME`, `DATA_DATABASE_PASSWORD`, `R2_SQL_AUTH_TOKEN`, and `DATA_HIDDEN_MODELS`.
- Release signing and publisher credentials live in AWS Secrets Manager paths such as `shared/APPLE_SIGNING_CERTIFICATE`, `shared/APPLE_NOTARY_KEY`, `shared/HOMEBREW_TAP_DEPLOY_KEY`, `shared/AUR_SSH_KEY`, `opencode/release/RELEASE_TAG_KEY`, and `opencode/release/DISCORD_WEBHOOK`.
- Azure trusted signing IDs are repository variables.
- The deployed site Worker holds no GitHub token. The build writes a GitHub snapshot, and runtime GitHub API reads are unauthenticated and cached.
- No `.env.example` file exists. Local development uses environment variables documented in service READMEs.

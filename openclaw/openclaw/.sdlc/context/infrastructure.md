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
| Language | TypeScript (strict ESM, no `any`) | `7.1.0-dev.20261011.1` (devDependency in `package.json`) |
| Runtime | Node.js (`>=24.16.0 <25 \|\| >=26.1.0`, Node 26 recommended); Bun is an explicit opt-in runtime with a `1.4.3` floor, and the desktop apps use a pinned OpenClaw Bun fork | Floors in `node-version.mjs` (`NODE_RELEASE_FLOORS`, `MINIMUM_BUN_VERSION`) |
| Package manager | pnpm (isolated linker, `verifyDepsBeforeRun: false`, `packageImportMethod: clone-or-copy`) | `12.12.1` (`packageManager` in `package.json`) |
| Bundler | tsdown via `scripts/tsdown-build.mts` | `0.23.1` |
| Type checker | Native TypeScript 7 compiler driven by `scripts/run-tsgo.mts`: `tsrs` where a platform binary exists (`darwin-arm64`, `linux-arm64`, `linux-x64`), otherwise `tsgo`; `OPENCLAW_TYPECHECKER=tsgo\|tsrs` forces one | `tsrs` `0.16.0-ts7.1.0-dev.20260929`; `oxlint-tsgolint` `7.0.2004` |
| Gateway server | Custom `node:http` server in `src/gateway` (probe routing in `gateway-http-route-contracts.ts`, handlers in `server-http-probes.ts`) | n/a |
| Control UI | Solid 2 web components built with Vite; embeds a web terminal (`@openclaw/libterminal`, `ghostty-web`, `@novnc/novnc`) and a CodeMirror editor (`@codemirror/*`) | `solid-js` `2.0.0-rc.14`, `@solidjs/signals` `2.0.0-rc.14`, `@solidjs/web` `2.0.0-rc.14`, Vite `8.3.4` |
| Database | SQLite via `node:sqlite` with the Kysely query builder (default), plus an experimental PostgreSQL engine via `pg` | Kysely `0.29.6`, `pg` `8.23.1` |
| Lint and format | oxlint (config `.oxlintrc.json`, boundary guards in `config/oxlint/`) and oxfmt (config `.oxfmtrc.jsonc`) | oxlint `1.87.0`, oxfmt `0.72.0` |
| Test runner | Vitest with per-area configs in `test/vitest/` (124 `vitest.*.config.ts` files) | `5.0.3` |

### Database engines and schema versions

- `package.json` `openclaw.databaseEngines` lists `["sqlite", "postgres"]`; SQLite is the default and PostgreSQL is experimental (`docs/reference/database-engines.md`).
- `package.json` `openclaw.postgresFamilies` lists the PostgreSQL-backed families: `state`, `agent`, `workboard`, `logbook`, `team-reports`.
- `package.json` `openclaw.schemaVersions` pins `state` at `28` and `agent` at `31`; the same constants live in `src/state/openclaw-schema-versions.ts` (`OPENCLAW_STATE_SCHEMA_VERSION`, `OPENCLAW_AGENT_SCHEMA_VERSION`).
- Canonical SQLite schemas are `src/state/openclaw-state-schema.sql` and `src/state/openclaw-agent-schema.sql`; the generated PostgreSQL tree is `src/state/postgres-schema.generated/`.
- PostgreSQL shared-state generation requires PostgreSQL 16 or newer; see `docs/reference/database-schemas.md` and `docs/reference/database-schemas/` for migration, worker access, and recovery rules.

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| pnpm | Package management and workspace scripts | `pnpm install --frozen-lockfile` |
| oxfmt | Formatting (config `.oxfmtrc.jsonc`) | `pnpm format` / `pnpm format:check` |
| oxlint | Linting (config `.oxlintrc.json`, boundary guards in `config/oxlint/`) | `pnpm lint` (sharded) / `node scripts/run-oxlint.mjs` (`pnpm lint:all`) |
| tsgo/tsrs | Type checking | `pnpm tsgo:core` (full: `pnpm tsgo:all`; production set: `pnpm tsgo:prod`) |
| tsdown | Production build (`scripts/build-all.mts`, Docker variant `pnpm build:docker`) | `pnpm build` |
| Vitest | Unit tests (fast lane), gateway, channel, contract, and e2e suites | `pnpm test:fast` / `pnpm test` / `pnpm test:e2e` / `pnpm test:live` |
| tsx | Running TypeScript scripts without a build step | `node --import ./scripts/tsx.mjs scripts/<name>.mts` |
| Control UI dev server | Local UI development | `pnpm ui:dev` (build: `pnpm ui:build`) |
| Local check graph | Guard preflights, typecheck, lint, and policy guards | `pnpm check` (`scripts/check.mts`), scoped: `pnpm check:changed`, lane mapping: `pnpm changed:lanes` |

### Architecture and policy checks

- `pnpm check:architecture` runs `check:import-cycles`, `check:madge-import-cycles`, `check:deprecated-api-usage`, `check:wrapper-shadowing`, `check:deprecated-jsdoc`, `db:kysely:check`, `db:postgres:check`, `lint:kysely`, and `check:database-first-legacy-stores`.
- `pnpm audit:seams` audits import seams across the repository (`scripts/audit-seams.mts`).
- Ratchets: `pnpm check:line-cap-ratchet`, `pnpm check:max-lines-ratchet`, `pnpm check:database-dialect-ratchet`, `pnpm check:database-worker-ratchet`, `pnpm check:agents-md-size`, `pnpm check:env-var-count`.
- Docs and generated artifacts: `pnpm docs:list`, `pnpm docs:check-links`, `pnpm docs:check-links:anchors`, `pnpm plugins:inventory:gen`, `pnpm maturity:render`, `pnpm maturity:check`.
- Observability smoke: `pnpm qa:otel:smoke`, `pnpm qa:observability:smoke` (adds `pnpm qa:prometheus:smoke`).

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Local dev | Any working branch | Day-to-day development, Gateway on loopback port 18789 by default | `http://127.0.0.1:18789` |
| CI ephemeral | PR, `main` push, hourly schedule, or manual dispatch | Automated lint, typecheck, test, and build lanes | Varies per run |
| Docker Compose local | Any | Containerized Gateway plus a CLI sidecar sharing the Gateway network namespace for isolation testing | Host port from `${OPENCLAW_GATEWAY_PORT:-18789}` |
| Operator production | Release tag or channel | User-operated Gateway (self-hosted, Fly.io, Render, or a VPS); there is no centrally hosted OpenClaw fleet | Operator-defined |

- There is no preview or staging environment and no per-branch deploy path; every release lane publishes from a maintainer-dispatched workflow.
- The GitHub Environments used by the release workflows (`docker-release`, `android-release`, `android-store-release`, `android-internal`, `ios-store-release`, `ios-testflight`, `release-signing`, `qa-live-shared`) are approval and secret gates, not deployed preview hosts.

## CI/CD pipelines

`.github/workflows/` holds 118 workflow files.
`docs/ci.md` and `docs/ci/` document the job graph, scope gates, and release umbrellas.

| Lane | Workflows | Trigger | What it runs |
|---|---|---|---|
| Core CI | `ci.yml` | Hourly at minute 23, `main` push, PR events, manual dispatch | Preflight routing manifest, then lint, tsgo typecheck, format check, Vitest suites, builds, UI tests, and platform lanes; publishes the `openclaw/ci-gate` aggregate |
| Core CI support | `ci-test-timings-refit.yml` (daily at 09:43), `vitest-cache-warm.yml` (hourly at minute 17), `release-npm-cache-warm.yml` (daily at 08:17), `workflow-sanity.yml` (PR and `main` push), `sandbox-common-smoke.yml` (daily at 05:23, plus PR and `main` push) | Scheduled, PR, or manual | Test-timing refit, dependency cache warming, workflow schema validation, and the sandbox container smoke |
| Testbox and platform lanes | `ci-check-testbox.yml`, `ci-check-focused-testbox.yml`, `ci-check-routine-testbox.yml`, `ci-check-arm-testbox.yml`, `ci-check-high-memory-testbox.yml`, `ci-build-artifacts-testbox.yml`, `ci-android-focused-testbox.yml`, `windows-blacksmith-testbox.yml`, `windows-testbox-probe.yml`, `linux-app.yml` | PR or manual dispatch | Blacksmith testbox runs for focused, routine, ARM, high-memory, artifact-build, Android, and Windows lanes |
| Release and validation | `full-release-validation.yml`, `full-release-candidate.yml`, `full-release-validation-nightly.yml`, `full-release-artifacts.yml`, `full-release-child-evidence.yml`, `openclaw-release-checks.yml`, `release-validation-skill-runner.yml`, `authorized-beta-focused-validation.yml` | Manual dispatch, `workflow_call` from the release flow, or nightly at `7 */3 * * *` | Full Release Validation over an exact SHA, candidate preparation, artifact assembly, child evidence, and the nightly pinned-main run |
| Release publication | `openclaw-release-prepare.yml`, `openclaw-release-publish.yml`, `openclaw-release-promote.yml`, `openclaw-npm-release.yml`, `openclaw-npm-preflight.yml`, `package-acceptance.yml`, `openclaw-stable-main-closeout.yml` | Manual dispatch or `workflow_call` | Non-publishing preparation and recovery, the maintainer release button that dispatches a prepared release artifact once, gated npm publication, package acceptance for npm, ref, URL, and artifact candidates, and the stable-main closeout after a version and changelog push |
| Install and update lanes | `install-smoke.yml`, `install-smoke-reusable.yml`, `update-migration.yml`, `ci-published-driver-update.yml` | Daily at `17 3 * * *`, Sunday at `17 3 * * 0`, or `workflow_call` | Installer and update smoke against the `latest` baseline, update-survivor migration scenarios, and the published-driver × candidate update cell |
| Docker distribution | `docker-release.yml`, `docker-release-prepare.yml`, `docker-image-refresh.yml`, `docker-channel-promote.yml`, `vercel-container-registry-publish.yml` | `workflow_call` from the release flow, weekly on Mondays, or manual dispatch | Multi-arch image build and push to GHCR and Docker Hub, dated stable and extended-stable refreshes, channel promotion, and the Vercel registry mirror |
| Code quality and security | `codeql.yml`, `codeql-critical-quality.yml`, `codeql-android-critical-security.yml`, `codeql-macos-critical-security.yml`, `opengrep-precise.yml`, `opengrep-precise-full.yml`, `security-review.yml`, `dependency-audit.yml`, `browser-mcp-contract.yml`, `real-behavior-proof.yml` | PR, `main` push, scheduled reconciliation, or manual dispatch | CodeQL security and quality profiles, precise OpenGrep rules (`security/opengrep/`), the security-review reconciler, dependency scanning, the browser MCP contract, and PR context and evidence |
| Docs | `docs.yml`, `docs-agent.yml`, `docs-external-links.yml`, `docs-mirror-freshness.yml`, `docs-sync-publish.yml`, `docs-translate-trigger-release.yml`, `website-installer-sync.yml`, `control-ui-locale-refresh.yml`, `native-app-locale-refresh.yml` | `main` push, release, scheduled, or manual dispatch | Docs lint and link checks, the main-only docs repair agent, external link audits, docs mirror freshness, publish-repo sync, translation triggers, and locale refresh for the Control UI and native apps |
| Plugin and channel distribution | `plugin-npm-release.yml`, `plugin-prerelease.yml` (hourly at minute 37), `plugin-clawhub-new.yml`, `plugin-clawhub-release.yml`, `plugin-clawhub-postpublish.yml`, `plugin-clawhub-recovery.yml`, `plugin-init-scaffold-validation.yml`, `npm-telegram-beta-e2e.yml`, `npm-placeholder-bootstrap.yml` | Hourly, `main` push, or manual dispatch | Official plugin npm and ClawHub publication and recovery, the complete extension runtime inventory, plugin scaffold validation, and Telegram beta distribution proof |
| Mobile and desktop releases | `android-release.yml`, `android-release-e2e.yml`, `android-store-release.yml`, `android-emulator-diagnostic.yml`, `ios-release-e2e.yml`, `ios-store-release.yml`, `macos-release.yml`, `windows-node-release.yml`, `linux-app-release.yml`, `linux-app-mirror.yml`, `linux-app-release-request.yml`, `mobile-store-release-notify.yml` | Weekly store schedules, `workflow_call` from release flows, or manual dispatch | Android APK and Play Store releases, iOS TestFlight and App Store releases, macOS and Windows node releases, and the Linux app release and mirror |
| Dead-code and native analysis | `ios-periphery.yml`, `ios-periphery-comment.yml`, `macos-periphery.yml`, `shared-openclawkit-periphery.yml` | PR, `workflow_call`, or `workflow_run` | Periphery dead-code scans for the iOS app, macOS app, and the shared OpenClawKit library, with a PR comment lane |
| QA and live proof | `qa-live-transports-convex.yml`, `qa-profile-evidence.yml`, `mantis-scenario.yml`, `mantis-discord-smoke.yml`, `mantis-discord-status-reactions.yml`, `mantis-discord-thread-attachment.yml`, `mantis-slack-desktop-smoke.yml`, `mantis-telegram-bot-e2e-proof.yml`, `mantis-web-ui-chat-proof.yml`, `mantis-clear-reaction.yml`, `mantis-resolve-request.yml`, `openclaw-scheduled-live-checks.yml`, `openclaw-release-telegram-qa.yml`, `live-media-runner-image.yml`, `crabbox-hydrate.yml`, `pr-crabbox-gate-publisher.yml` | Scheduled, `workflow_call`, or manual dispatch | QA Lab transport lanes, Mantis scenario and channel proof, scheduled live and e2e checks, Telegram release QA, and the Crabbox gate publisher |
| Performance and maturity | `openclaw-performance.yml`, `maturity-scorecard.yml` | Daily at `11 5 * * *` or manual dispatch | Kova diagnostic, deep-profile, and live-OpenAI performance lanes plus a Vitest paired benchmark, and the maturity scorecard render from QA evidence |
| Node runtime channels | `node-runtime-compat.yml`, `node-runtime-conformance.yml` | Weekly on Mondays, hourly, `main` push, and PR | Minimum-Node 26 compatibility and the hourly node runtime conformance suite |
| FRV proof | `frv-proof-broker.yml`, `frv-proof-fixture.yml` | Manual dispatch | Targeted job rerun boundary proof for merged recovery-controller changes |
| Repository maintenance | `stale.yml`, `labeler.yml`, `duplicate-after-merge.yml`, `dated-todo-sweep.yml`, `pr-ci-sweeper.yml`, `sticky-disk-cleanup.yml`, `auto-response.yml`, `clawsweeper-dispatch.yml`, `maintainer-command-reactions.yml` | Scheduled, issue or PR events, or manual dispatch | Stale PR handling, path labeling, duplicate detection, dated TODO sweeps, PR CI sweeping, runner disk cleanup, and maintainer automation |

## Deployment

- Operator upgrades run through `openclaw update` with channel selection (`--channel`), dry-run preview (`--dry-run`), and recorded update history.
- The supported update channels are `stable`, `beta`, `extended-stable`, and `dev` (`src/infra/update-channels.ts`).
- Releases publish the `openclaw` npm package under version tags and channel dist-tags: `latest` for stable, `beta`, and `extended-stable` (`docs/reference/RELEASING.md`).
- The same release publishes Docker images to GHCR (`ghcr.io/openclaw/openclaw`, primary) and a Docker Hub mirror (`openclaw/openclaw`) with version, channel, and `-browser` variant tags.
- Fly.io deploys with `fly deploy` from the repo-root `fly.toml`, and Render deploys from the repo-root `render.yaml` blueprint.
- Release publication is maintainer-dispatched and gated on preflight plus Full Release Validation evidence, so routine operator updates need no manual approval but releases do.

### Rollback

- Roll back an operator install by running `openclaw update` against the previous version or channel, which restores the prior package and replays config reads from the restored code.
- Downgrades require explicit confirmation, and cleanup of staged originals permanently gives up rollback to those originals (see `docs/install/updating.md`).
- The serving Gateway stays in place while preflight checks run, so a failed update attempt does not take down the running instance.

## Health checks

The Gateway serves three probe routes (`src/gateway/gateway-http-route-contracts.ts`, handled in `src/gateway/server-http-probes.ts`).
All three accept `GET` and `HEAD` only and return `405` for other methods.

| Endpoint | Expected response | Checked by |
|---|---|---|
| `/healthz` (alias `/health`) | `200 OK` with `{"ok": true, "status": "live"}` | Docker `HEALTHCHECK` via `node dist/docker-healthcheck.js`, Compose healthcheck, `scripts/e2e/compose-setup.sh` |
| `/readyz` (alias `/ready`) | `200 OK` with `{"ready": true, ...}` when ready, `503` with `{"ready": false, "failing": [...]}` otherwise; subsystem details only for local-direct or authenticated callers | Gateway startup sequencing, orchestrators, `scripts/e2e/compose-setup.sh`, `scripts/e2e/gateway-network-docker.sh` |
| `/startupz` (alias `/startup`) | `200 OK` with `{"ok": true, "status": "started"}` once startup completes, `503` with `{"ok": false, "status": "starting"\|"draining"}` while starting or draining | Fly.io `http_service.checks`, Render `healthCheckPath` |

## Smoke tests

- Installer and update smoke coverage lives in `scripts/test-install-sh-docker.sh`, `scripts/test-install-sh-e2e-docker.sh`, and `scripts/e2e/cli-installer-distribution-docker.sh`, orchestrated by the `install-smoke` workflows.
- Release beta smoke checks run via `pnpm release:beta-smoke` (`scripts/release-beta-smoke.ts`).
- Container liveness smoke is the Docker healthcheck probe in `src/docker-healthcheck.ts`, which resolves the active Gateway port from the lock file and GETs `/healthz`.
- CI runs QA smoke lanes (`run_qa_smoke_ci` in the `ci.yml` preflight manifest) plus channel and contract suites for release qualification.
- Sandbox isolation smoke runs daily in `sandbox-common-smoke.yml` against `scripts/docker/sandbox/Dockerfile`.

## Hosting

- OpenClaw is a self-hosted product with no operator-run production fleet, so each user hosts their own single-tenant Gateway.
- Supported targets are npm global install, Docker (GHCR primary, Docker Hub mirror), Fly.io (`primary_region = "iad"`, `shared-cpu-2x` with 2048 MB RAM and a persistent `/data` volume), and Render (starter plan with a 1 GB `/data` disk).
- `docs/install/` documents additional targets: DigitalOcean, Hetzner, Hostinger, GCP, Azure, Railway, Northflank, Oracle Cloud, Raspberry Pi, Kubernetes, Cloudflare Containers, Upstash Box, Podman, Nix, and Ansible.
- Scaling follows a one-cell-per-tenant model where multi-user hosting means one Gateway container per tenant, not a shared server.
- Infrastructure as code lives at the repo root (`Dockerfile`, `docker-compose.yml`, `fly.toml`, `render.yaml`) with deployment guides in `docs/install/`.
- The Docker image builds on `node:24-trixie` and ships Bun `1.4.3`; `docker-compose.yml` runs the Gateway plus a CLI sidecar that shares the Gateway network namespace.

## Secrets management

- Local secret conventions live in `.env.example`, and env precedence is process env, then `./.env`, then `~/.openclaw/.env`, then the `openclaw.json` `env` block (documented in `docs/help/environment.md`).
- Real secrets are never committed, and the Gateway refuses to start when `OPENCLAW_GATEWAY_TOKEN` still holds the documented example placeholder.
- Opt-in SecretRefs keep credentials out of plaintext config via the `env`, `file`, `exec` (1Password, Bitwarden, Vault, `pass`, sops), and `store` sources.
- The `store` source is backed by the shared secret store in the shared state SQLite database (`state/openclaw.sqlite`); store values are unencrypted at rest and rely on the database's `0600` file and `0700` directory permissions.
- Model-provider credentials backed by SecretRefs resolve to an opaque process-local sentinel (`oc-sent-v2.<authenticated-ciphertext>.end`) and are substituted immediately before egress; unknown sentinel-shaped values block the request.
- The secret egress proxy is default off and runs in a dedicated Gateway Worker; each protected secret must name the exact HTTPS hosts where substitution is allowed.
- The CLI lifecycle is `openclaw secrets audit --check` to find plaintext residue, then `openclaw secrets configure` and `openclaw secrets apply` to migrate, plus `openclaw secrets reload` to re-resolve refs and swap the runtime snapshot.
- `openclaw secrets store list|set|get|rm|import` manages the team-scoped store, with `secret` entries write-only and `env` entries agent-readable.
- The workflow is documented in `docs/gateway/secrets.md` and its subpages (`runtime-model`, `secretref-contract`, `secret-store-and-egress`, `integration-examples`, `operations`).

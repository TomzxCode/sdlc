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
| Language | Python | `requires-python = ">=3.11,<3.15"` (type-check target 3.13 via `[tool.ty.environment]`, 3.14 wheels verified) |
| Runtime | CPython (venv per install) | 3.14 runtime (3.11–3.13 allowed only as an update bridge; `uv.lock` resolves 3.14 only) |
| Web framework | FastAPI | `>=0.104.0,<1` in core, `==0.133.1` in `[web]` extra |
| ASGI server | Uvicorn (standard) | `>=0.31.0,<1` in core, `==0.54.0` in `[web]` extra |
| LLM SDK | OpenAI SDK | `==2.54.0` (gated `python_version >= '3.14'`) |
| Data validation | Pydantic | `==2.14.1` |
| HTTP clients | httpx (+ httpx2 for MCP), aiohttp, requests | httpx `==0.28.1`, aiohttp `==3.14.5`, requests `==2.34.2` |
| CLI framework | Fire + prompt_toolkit + Rich | fire `==0.7.1`, prompt_toolkit `==3.0.53`, rich `==14.3.4` |
| Scheduler | croniter | `==6.2.4` |
| Lockfile | uv.lock (exact-pinned core deps) | Present at repo root |
| JS runtime | Node.js | `>=26` (root and desktop `engines`, `engineStrict: true`) |
| JS package manager | pnpm workspaces (`apps/*`, `ui-tui`, `ui-tui/packages/*`, `web`, `tests-js`) | pnpm `^12` (exact pin in `pm/lock.json`), `pnpm-lock.yaml` at repo root, npm refused in every workspace `engines` |
| Desktop shell | Electron | `==44.10.2` with electron-builder `==27.0.0-alpha.6` |
| Desktop bundler | Vite | `==8.3.4` |
| UI libraries | React + React DOM | `==19.3.0` (TUI, desktop, and web) |
| TUI renderer | Ink via local `@hermes/ink` fork | `workspace:*` (`ui-tui/packages/hermes-ink`) |
| JS language | TypeScript | `==6.0.3` |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| uv / pm | Python package management and locking | After editing `pyproject.toml`, run `hermes pm lock` and commit `uv.lock`; never mutate a Hermes environment with raw pip/uv |
| pnpm | JS workspace installs and scripts | `pnpm install --frozen-lockfile` at repo root (pnpm pin in `pm/lock.json`); every workspace script runs via `pnpm run ...` |
| ruff | Python linting and formatting | `ruff check .` / `ruff format .` via the pinned ci-tools env; `python scripts/check` runs every blocking check (config `ruff.toml`, rules include `PLW1514`, `ASYNC210/220/221/251`) |
| ty | Python type checking | Pinned `ty==0.0.89` in `[dependency-groups] dev`, run advisory via `lint.yml` |
| pytest | Python testing (canonical runner required) | `scripts/run_tests.sh` (per-file subprocess isolation, `TZ=UTC`, hermetic env) |
| vitest | JS testing (TUI, desktop, web, tests-js) | `pnpm run test` per workspace (`vitest run`, version `4.1.12`) |
| tsc | JS type checking | `pnpm run typecheck` per workspace |
| eslint | JS linting | `pnpm run lint` per workspace |
| prettier | JS formatting | `pnpm run fmt` per workspace |
| vite | Desktop/web build | `pnpm run build` in `apps/desktop` (or `web`) |
| electron-builder | Desktop packaging (dmg/zip, msix, AppImage/deb/rpm) | `pnpm run dist` in `apps/desktop` |
| Docker | Container build and publish | `Dockerfile` + `docker-compose.yml` at repo root |
| Nix | Reproducible dev shell (`HERMES_PYTHON`) | `nix flake check` |

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| local dev | feature branches | Developer workstation with local venv plus Node workspaces | Not applicable (localhost) |
| production (self-hosted) | `main` | User-operated installs updated via `hermes update`, Docker image, or managed installer | Not applicable (each user hosts their own gateway, dashboard, and desktop backend) |
| staging | Not documented | Not documented | Not documented |
| preview | Not documented | No ephemeral PR preview environments are documented | Not documented |

## CI/CD Pipelines

`ci.yaml` is the required-check orchestrator. It fans out via `workflow_call`; Docker, site deployment, releases, and scheduled audits own their own triggers.

Workflow | Trigger | What it runs
--- | --- | ---
`ci.yaml` | `workflow_dispatch`, `workflow_call`, `pull_request`, `push` to `main` | Orchestrator; calls the reusable workflows below |
`tests.yml` | `workflow_call` from CI | Full pytest suite via `scripts/run_tests.sh` with per-file parallel subprocesses; optional `tests/e2e/` and upgrade shards |
`tests-os.yml` | `workflow_call` from CI | OS-specific pytest lanes on macOS and Windows runners |
`lint.yml` | `workflow_call` from CI | Footgun/guard checks, blocking `ruff check .`, code-health ratchet, advisory ruff + ty diff versus target branch |
`js-tests.yml` | `workflow_call` from CI | One 32-core job running per-workspace `check` scripts (vitest, tsc, eslint) across root, TUI, desktop, web, and tests-js |
`rust-tests.yml` | `workflow_call` from CI | Cargo tests for the Rust bootstrap installer |
`catalog-tests.yml` | `workflow_call` from CI | Plugin catalog tests |
`remote-backends.yml` | `workflow_call` from CI | E2E for SSH/Modal/Daytona terminal backends |
`bootstrap-installer.yml` | `workflow_call` from CI | Bootstrap installer build and tests |
`e2e-desktop.yml`, `e2e-desktop-core.yml`, `e2e-desktop-update.yml` | `workflow_call` from CI | Desktop E2E, core flows, and update flows |
`docs-site-checks.yml` | `workflow_call` from CI | Docusaurus site checks |
`repo-guards.yml` | `workflow_call` from CI | Repo guards; the `uv_lock` lane verifies `uv.lock` is in sync with `pyproject.toml`, `npm_lock` diffs `pnpm-lock.yaml` |
`docker.yml` | `pull_request`, `push` to `main`, `workflow_call` (the `release` trigger was removed deliberately) | Docker build, pytest against the built image via `HERMES_TEST_IMAGE`, and publish to `nousresearch/hermes-agent` |
`nix.yml` | `pull_request`, `push` to `main`, `workflow_call` | Nix flake check for the reproducible dev shell |
`osv-scanner.yml` | `schedule`, `workflow_dispatch` | OSV dependency scanning; the former `supply-chain-audit.yml` is no longer present |
`install-e2e.yml` | `workflow_dispatch`, `workflow_call` | Installer and `hermes update` E2E; legs `install-e2e-run.yml`, `install-e2e-macos-run.yml`, `install-e2e-windows-run.yml`, tracker `install-e2e-red.yml` |
`deploy-site.yml` | `release: published`, `push` to `main` (paths), `workflow_dispatch` | Builds and deploys the Docusaurus website |
`windows-venv-e2e.yml` | Pushes to `wine2e/**`, `workflow_call` | Live Windows venv holder process-topology tests on a real runner |
`live-providers.yml` | `push`, `workflow_dispatch` | Secrets-gated live provider canaries |
`termux-verify.yml` | `push` to `main` (paths), `pull_request` (paths), `workflow_dispatch`, `workflow_call` | Termux contract and TUI verification |
`canary-release.yml` | `schedule`, `workflow_dispatch` | Canary tag/release creation and pruning |
`stable-release.yml`, `stable-release-publication.yml` | `workflow_dispatch` (+ `workflow_run` for publication) | Stable release admission and receipt-bound publication |
`desktop-bundled-release.yml`, `desktop-bundle-smoke.yml` | `workflow_call`, `workflow_dispatch` | Bundled desktop release builds and bundle smoke tests |
`bootstrap-installer-build.yml` | `workflow_dispatch` | Standalone bootstrap installer build |
`pm-bundle.yml` | `workflow_dispatch`, `workflow_call`, `pull_request` (paths) | PM bundle build |
`sandbox-image.yml` | `pull_request` (paths), `workflow_run`, `schedule`, `workflow_dispatch` | Sandbox desktop image build and publish |
`windows-bundle-sdk.yml` | `pull_request` (paths), `workflow_dispatch` | Windows bundle SDK checks |
`windows-desktop-attach-e2e.yml`, `windows-install-update-e2e.yml` | `workflow_dispatch`, `push` to `wine2e-desktop/**` / `wine2e-install/**`, `workflow_call` | Windows desktop attach and install/update E2E |
`js-autofix.yml` | `push` to `main` (paths), `workflow_dispatch` | JS lint/format autofix commits |
`catalog-dead-repos.yml` | `schedule`, `workflow_dispatch` | Delist dead repos from the plugin catalog |
`ci-review-comment.yml` | `workflow_run` (`in_progress`) | Unified CI review comment |
`docs-search-monitor.yml` | `schedule`, `workflow_run`, `workflow_dispatch` | Docs search monitoring |
`skills-index.yml`, `skills-index-freshness.yml` | `schedule`, `workflow_dispatch`, `push` to `main` (paths) | Skills index build and freshness checks |
`plugin-catalog-ci.yml` | `pull_request` (paths) | Plugin catalog structural checks |
`label-rerun.yml` | `pull_request` (`labeled`) | Rerun CI when a rerun label is applied |
`archive-inputs.yml` | `push` to `main` (paths), `workflow_call`, `workflow_dispatch` | Archive pinned PM inputs |

## Deployment

Production deployment is a self-hosted update, not a push to a central fleet.
The primary path is `hermes update`, which pulls the target branch, re-syncs the venv, refreshes Node dependencies with pnpm, and finishes in a post-swap child interpreter via `hermes_cli/update_handoff.py`.
Docker users deploy by pulling the published `nousresearch/hermes-agent` image instead of running `hermes update` inside the container.
Managed installs record an install method so `hermes update` can refuse or redirect when an external manager owns the install.
Desktop releases are packaged with electron-builder from `apps/desktop` (`dmg`/`zip` on macOS, `msix` on Windows, `AppImage`/`deb`/`rpm` on Linux).
No manual approval gate is documented for self-hosted updates.

### Rollback

`hermes update` takes pre-update snapshots and backups of state and config via `hermes_cli/backup.py` before mutating anything.
An interrupted update leaves a marker that the next launch detects and repairs through the early-recovery path.
Docker rollback is redeploying a prior image tag.
A scripted single-command application rollback beyond the backup snapshots is not documented.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `GET /health` (API-server adapter, webhook adapters) | `200 OK` with `{"status": "ok", "platform", "version"}` | Operators, tunnels, and dashboard probes |
| `GET /v1/health` (API-server adapter) | `200 OK` with `{"status": "ok"}` | OpenAI-compatible clients expecting the `/v1/` prefix |
| `GET /health/detailed` (API-server adapter, Bearer auth) | `200 OK` with gateway state, platform list, and PID | Dashboard and authenticated operators |
| `GET /api/health`, `GET /api/health/idle`, `POST /api/health/retirement` (dashboard router) | `200 OK` liveness (version, commit, auth flag), token-gated idle proof, and retirement fence | Desktop app gated readiness probe |
| OTLP gateway health export (`agent/monitoring/gateway_health_export.py`) | Shared-metrics projection with no network exporter by default | Optional `monitoring.gateway_health_export` consumer |
| `POST /healthz` (Photon platform sidecar only) | `200 OK` sidecar readiness | Photon adapter lifecycle watchdog, not the core gateway |

## Smoke Tests

Docker smoke tests live in `tests/docker/test_smoke.py` and cover the image entrypoint and subcommands.
Installer end-to-end smoke coverage lives in `tests/install/installer-script-e2e.sh`, including the `hermes desktop --build-only` phase that proves an installed CLI can build the desktop app.
Secrets-gated live provider canaries live in `tests/e2e/core/live` under the `live` pytest marker and run via `live-providers.yml`; other `*_live.py` tests are gated behind the same marker.
Run the Python smoke subset with `scripts/run_tests.sh tests/docker/test_smoke.py`.
Run the JS suites with `pnpm run test` inside the relevant workspace.

## Hosting

Hermes is self-hosted on the user's own machine, VPS, or container host.
Supported runtimes include a local venv install, Docker (`Dockerfile`, `docker-compose.yml`), and remote terminal backends (SSH, Modal, Daytona) for sandboxed execution.
Regions, autoscaling policy, and infrastructure-as-code are not documented because there is no centrally operated production fleet.
The website docs deploy from `main`, a published release, or a manual dispatch via `deploy-site.yml`.

## Secrets Management

Secrets live in `.env`, which holds credentials only, while behavioral settings live in `config.yaml`.
Code bridges a behavioral setting to an internal environment variable when the mechanism needs one, rather than adding a new `HERMES_*` user-facing variable.
Each profile has its own secret scope resolved at call time via `agent/secret_scope.py`, so a secondary profile's keys never leak through `os.environ` or module globals under multiplex.
OAuth and shared-auth state uses profile-scoped directories rather than a global store.

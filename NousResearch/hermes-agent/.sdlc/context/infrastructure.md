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
| Language | Python | `requires-python = ">=3.11,<3.14"` (type-check target 3.13 via `[tool.ty.environment]`) |
| Runtime | CPython (venv per install) | 3.11–3.13 |
| Web framework | FastAPI | `>=0.104.0,<1` in core, `==0.133.1` in `[web]` extra |
| ASGI server | Uvicorn (standard) | `>=0.31.0,<1` in core, `==0.41.0` in `[web]` extra |
| LLM SDK | OpenAI SDK | `==2.24.0` |
| Data validation | Pydantic | `==2.13.4` |
| HTTP clients | httpx (+ httpx2 for MCP), aiohttp, requests | httpx `==0.28.1`, aiohttp `==3.14.3`, requests `==2.33.0` |
| CLI framework | Fire + prompt_toolkit + Rich | fire `==0.7.1`, prompt_toolkit `==3.0.52`, rich `==14.3.3` |
| Scheduler | croniter | `==6.0.0` |
| Lockfile | uv.lock (exact-pinned core deps) | Present at repo root |
| JS runtime | Node.js | `^22.22.0 \|\| ^24.11.0 \|\| >=26.0.0` (root and desktop `engines`) |
| JS package manager | npm workspaces (`apps/*`, `ui-tui`, `web`, `tests-js`) | npm `<11.10.0 \|\| >=11.17.0`, `package-lock.json` present |
| Desktop shell | Electron | `==40.10.2` with electron-builder `==26.15.3` |
| Desktop bundler | Vite | `==8.2.0` |
| UI libraries | React + React DOM | `==19.2.7` (TUI and desktop) |
| TUI renderer | Ink via local `@hermes/ink` fork | `file:./packages/hermes-ink` |
| JS language | TypeScript | `==6.0.3` |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| uv | Python package management and locking | `uv add <package>` then `uv lock` |
| ruff | Python linting and formatting | `uv run ruff check .` / `uv run ruff format .` (enforced rules: `PLW1514`, `ASYNC210/220/221/251`) |
| ty | Python type checking | Declared as `ty==0.0.21` in `[dev]` extra, run via lint workflow |
| pytest | Python testing (canonical runner required) | `scripts/run_tests.sh` (per-file subprocess isolation, `TZ=UTC`, hermetic env) |
| vitest | JS testing (TUI, desktop, tests-js) | `npm run test` per workspace (`vitest run`, version `4.1.10`) |
| tsc | JS type checking | `npm run typecheck` per workspace |
| eslint | JS linting | `npm run lint` per workspace |
| prettier | JS formatting | `npm run fmt` per workspace |
| vite | Desktop/TUI build | `npm run build` in `apps/desktop` |
| electron-builder | Desktop packaging (dmg/zip, nsis/msi, AppImage/deb/rpm) | `npm run dist` in `apps/desktop` |
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

| Workflow | Trigger | What it runs |
|---|---|---|
| `ci.yaml` | `pull_request` and `push` to `main` | Orchestrator that fans out to lint, tests, JS, Docker, and supply-chain jobs |
| `lint.yml` | `workflow_call` from CI | Advisory ruff plus ty diff versus target branch and blocking `ruff check .` |
| `tests.yml` | `workflow_call` from CI | Full pytest suite via `scripts/run_tests.sh` with per-file parallel subprocesses plus `tests/e2e/` |
| `tests-os.yml` | `workflow_call` from CI | OS-specific pytest lanes on macOS and Windows runners |
| `js-tests.yml` | `workflow_call` from CI | Per-workspace `check` scripts (vitest, tsc, eslint) across root, TUI, desktop, web, and tests-js |
| `docker.yml` | `pull_request`, `push`, `release` | Docker build, pytest against the built image via `HERMES_TEST_IMAGE`, and publish to `nousresearch/hermes-agent` |
| `install-e2e.yml` | `workflow_dispatch` (plus `install-e2e-{macos,windows}-run.yml` legs) | Installer and `hermes update` end-to-end runs including the desktop `--build-only` smoke |
| `uv-lockfile-check.yml` | `workflow_call` from CI | Verifies `uv.lock` is consistent with `pyproject.toml` |
| `supply-chain-audit.yml` | `workflow_call` from CI | OSV scanning and supply-chain review of dependency changes |
| `nix.yml` | `pull_request` and `push` | Nix flake check for the reproducible dev shell |
| `rust-tests.yml` | `workflow_call` from CI | Cargo tests for the Rust bootstrap installer |
| `deploy-site.yml` | `push` to `main` | Builds and deploys the Docusaurus website |
| `windows-venv-e2e.yml` | Pushes to `wine2e/**` branches | Live Windows venv holder process-topology tests on a real runner |

## Deployment

Production deployment is a self-hosted update, not a push to a central fleet.
The primary path is `hermes update`, which pulls the target branch, re-syncs the venv, refreshes Node dependencies, and finishes in a post-swap child interpreter via `hermes_cli/update_handoff.py`.
Docker users deploy by pulling the published `nousresearch/hermes-agent` image instead of running `hermes update` inside the container.
Managed installs record an install method so `hermes update` can refuse or redirect when an external manager owns the install.
Desktop releases are packaged with electron-builder from `apps/desktop` (`dmg`/`zip` on macOS, `nsis`/`msi` on Windows, `AppImage`/`deb`/`rpm` on Linux).
No manual approval gate is documented for self-hosted updates.

### Rollback

`hermes update` takes pre-update snapshots and backups of state and config via `hermes_cli/backup.py` before mutating anything.
An interrupted update leaves a marker that the next launch detects and repairs through the early-recovery path.
Docker rollback is redeploying a prior image tag.
A scripted single-command application rollback beyond the backup snapshots is not documented.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `GET /health` (API-server adapter, webhook adapters) | `200 OK` with `{"status": "ok"}` | Operators, tunnels, and dashboard probes |
| `GET /v1/health` (API-server adapter) | `200 OK` with `{"status": "ok"}` | OpenAI-compatible clients expecting the `/v1/` prefix |
| `GET /health/detailed` (API-server adapter, Bearer auth) | `200 OK` with gateway state, platform list, and PID | Dashboard and authenticated operators |
| `GET /api/health`, `GET /api/health/idle` (dashboard router) | `200 OK` readiness and idleness state | Desktop app gated readiness probe |
| OTLP gateway health export (`agent/monitoring/gateway_health_export.py`) | Shared-metrics projection with no network exporter by default | Optional `monitoring.gateway_health_export` consumer |
| `GET /healthz` (Photon platform sidecar only) | `200 OK` sidecar readiness | Photon adapter lifecycle watchdog, not the core gateway |

## Smoke Tests

Docker smoke tests live in `tests/docker/test_smoke.py` and cover the image entrypoint and subcommands.
Installer end-to-end smoke coverage lives in `tests/install/installer-script-e2e.sh`, including the `hermes desktop --build-only` phase that proves an installed CLI can build the desktop app.
Ad-hoc live provider smoke tests exist under `tests/agent/test_*_live.py` and neighboring smoke-named tests.
Run the Python smoke subset with `scripts/run_tests.sh tests/docker/test_smoke.py`.
Run the JS suites with `npm run test` inside the relevant workspace.

## Hosting

Hermes is self-hosted on the user's own machine, VPS, or container host.
Supported runtimes include a local venv install, Docker (`Dockerfile`, `docker-compose.yml`), and remote terminal backends (SSH, Modal, Daytona) for sandboxed execution.
Regions, autoscaling policy, and infrastructure-as-code are not documented because there is no centrally operated production fleet.
The website docs deploy from `main` via `deploy-site.yml`.

## Secrets Management

Secrets live in `.env`, which holds credentials only, while behavioral settings live in `config.yaml`.
Code bridges a behavioral setting to an internal environment variable when the mechanism needs one, rather than adding a new `HERMES_*` user-facing variable.
Each profile has its own secret scope resolved at call time via `agent/secret_scope.py`, so a secondary profile's keys never leak through `os.environ` or module globals under multiplex.
OAuth and shared-auth state uses profile-scoped directories rather than a global store.

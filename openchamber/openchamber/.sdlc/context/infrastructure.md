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
| Language | TypeScript (strict mode) | ~5.9.0 |
| Runtime | Node.js (>= 22), Bun for builds/scripts | node >=22, bun 1.4.2 |
| Framework (frontend) | React 19, Vite 7, Zustand, Tailwind CSS v4, Base UI, CodeMirror | React ^19.1.1, Vite ^7.1.2 |
| Framework (backend) | Express 5 | ^5.1.0 |
| Desktop shell | Electron (boots the web server in-process) | Electron 41 |
| Mobile | Capacitor (iOS Swift, Android) | Capacitor |
| VS Code extension | VS Code Extension API, esbuild | — |
| Database | None (no persistent relational DB; state stored in files/JSON and OpenCode's own storage) | — |

## Development Tooling

| Tool | Purpose | Command |
|---|---|---|
| bun | Package manager and script runner | `bun install`, `bun run <script>` |
| tsc | Type checking (each package) | `bun run type-check` (workspace) / `bun run type-check:ui` etc. |
| eslint + oxlint | Linting (incl. `anti-slop` plugin via oxlint) | `bun run lint`, `bunx oxlint <paths>` |
| vitest | Web package test runner | `bun run --cwd packages/web test` |
| run-isolated-tests.mjs | Isolated test runner for ui/vscode/electron/scripts | `bun run --cwd packages/ui test` etc. |
| vite | Frontend build (web, vscode webview) | `bun run build:web` |
| esbuild | VS Code extension build | `bun run --cwd packages/vscode build` |
| electron-builder | Electron packaging | `bun run build:electron` |
| knip | Dead-code analysis (non-blocking) | `bun run dead-code` |

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| local/dev | any | `bun run dev` HMR web, `bun run electron:dev`, mobile sim | http://localhost:5173 / http://localhost:3001 |
| production (self-hosted) | main (tagged `vX.Y.Z`) | Users run locally or on their own servers; npm package, Docker, or desktop app | varies |

There is no hosted staging or preview environment; deployments are self-hosted and user-driven.

## CI/CD Pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| release.yml | tag `v*` push or manual dispatch | Builds Electron DMG/zip (macOS arm64), VS Code VSIX; publishes releases |
| build-macos-arm64-dmg.yml | manual dispatch | macOS Electron DMG build |
| vscode-extension.yml | tag push or manual dispatch | VS Code extension build and publish |
| docs-source.yml | push to main | Documentation site build |
| mobile-ci.yml | manual dispatch | Mobile smoke build |
| mobile-release.yml | manual dispatch | Mobile release |
| oc-integration.yml | PR/comment driven | Integration checks via `opencode` bot |
| oc-review.yml | pull_request | PR checks (lint/type-check/tests per repo guidance) |
| opencode.yml | issue/PR comments | Runs `/oc`, `/opencode` commands via bot |
| sdk-preview.yml | manual dispatch | SDK preview build |
| issue-intake.yml | issues | Issue intake automation |
| label-merge-conflict.yml | pull requests | Merge-conflict labeling |
| pr-review.yml, reproduce-issue.yml, triage.yml, stale.yml, bot-help.yml, bot-summarize.yml | various | Issue triage, review automation, bot helpers |
| release-desktop-smoke.yml, opencode-smoke.yml | manual dispatch | Release build smoke tests |

The repository's own guidance (per-repo `AGENTS.md`) notes that `bun run lint` and `bun run type-check` are time-consuming; prefer `bun build:web` after implementation.

## Deployment

Deployment is self-hosted and user-driven. Supported paths:
- **Desktop**: Electron installers produced by the release workflow (DMG/zip on macOS, other platforms via electron-builder).
- **Server**: run `openchamber` CLI (`packages/web/bin/cli.js`) or `bun start:web`; or Docker via `Dockerfile` + `docker-compose.yml`.
- **npm package**: published CLI consumed via `npm i -g openchamber` (or the `openchamber` binary).
- **VS Code extension**: published from `vscode-extension.yml`.

### Rollback

- Desktop/app releases: reinstall a prior release artifact (release workflow keeps per-tag assets).
- Self-hosted server: redeploy a previous image/tag or previous `openchamber` npm version.
- No automated rollback mechanism exists; rollback is manual.

## Health Checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `/health` | 200 OK | Monitoring |

## Smoke Tests

- **Desktop release smoke**: `.github/workflows/release-desktop-smoke.yml` + `scripts/test-release-build.sh` (`bun run release:test`).
- **OpenCode smoke**: `.github/workflows/opencode-smoke.yml`.
- **Mobile smoke build**: `mobile-ci.yml` (manual dispatch).
- **Package tests**: `bun run test` (runs isolated tests across scripts, ui, vscode, electron, web).

## Hosting

Self-hosted by the user: local machine, own server, or Docker. No OpenChamber-run hosting for instances.
The private relay is the only OpenChamber-hosted infrastructure, used for E2EE remote access transport only (not for hosting instances).

## Secrets Management

Secrets live in user-controlled locations:
- Provider API keys are stored by OpenCode (OpenCode's auth/config, e.g. `~/.local/share/opencode/` and provider auth files).
- OpenChamber-managed credentials (quota provider credentials) are written to `~/.config/openchamber/quota/*.json` with `0o600` permissions (see `packages/web/server/lib/quota/credentials/store.js`).
- Remote-access pairing secrets and signing keys are generated at runtime and stored locally; relay identity/signing key under the OpenChamber config dir.
- No secrets are logged; code and tooling enforce not committing `.env` or credential files.
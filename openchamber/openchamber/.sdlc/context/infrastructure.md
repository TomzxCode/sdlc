# Infrastructure

<!--
This file captures the project's technology stack, development tooling, CI/CD pipelines,
environments, and deployment procedures. It gives implementation, testing, and deployment
skills the commands and configuration they need without grepping the codebase each time.
Update this file when tooling, environments, or deployment procedures change.
-->

## Technology stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript (strict mode) | ~7.0.2 |
| Runtime | Node.js (>=24.14.0; `.nvmrc` is `lts/krypton`), Bun for builds/scripts | node >=24.14.0, Bun 1.4.5 |
| Framework (frontend) | React 19, Vite 7, Zustand, Tailwind CSS v4, Base UI, CodeMirror | React ^19.1.1, Vite ^7.3.2, tailwindcss ^4.0.0 |
| Framework (backend) | Express 5 | ^5.1.0 |
| Desktop shell | Electron (boots the web server in-process), electron-builder | Electron ^45.0.0, electron-builder ^26.0.0 |
| Mobile | Capacitor (iOS Swift, Android) | Capacitor |
| VS Code extension | VS Code Extension API, esbuild | — |
| SDK | `@openchamber/sdk` guest contract | v2.8.0 |
| OpenCode packages | `@opencode/client`, `@opencode/schema`, `@opencode/server`, `@opencode/util`, `@opencode/plugin` | 2.3.2 |
| OpenCode CLI | `opencode` declared by the web package | >=2.2.4 |
| Validation | `zod` | ^4.6.7 (root) |
| Testing | `vitest` | ^4.1.4 |
| Linting | `oxlint` with custom plugins | 1.94.0 |
| Database | None (no persistent relational DB; state stored in files/JSON and OpenCode's own storage) | — |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| bun | Package manager and script runner (v1.4.5) | `bun install`, `bun run <script>` |
| oxlint | Linting with custom OpenChamber plugins | `bun run lint`, `bun run lint:anti-slop`, `bun run deslop`, `bun run check:changed` |
| tsc | Type checking (each package) | `bun run type-check`, `bun run type-check:web`, `bun run type-check:ui`, `bun run type-check:electron`, `bun run vscode:type-check` |
| vite | Frontend build (web, vscode webview) | `bun run build`, `bun run build:web`, `bun run build:web:diag`, `bun run build:ui` |
| esbuild | Server, VS Code extension, and script builds | `bun run build:server`, `bun run extensions:build`, `bun run vscode:build`, `bun run vscode:package` |
| electron-builder | Electron packaging | `bun run build:electron` |
| bun (mobile) | Mobile web bundle | `bun run build:mobile` |
| vitest | Web package test runner | `bun run --cwd packages/web test` |
| run-isolated-tests.mjs | Isolated test runner for ui/vscode/electron/scripts | `bun run --cwd packages/ui test` etc. |
| test scripts | Full test and verification suite | `bun run test`, `bun run verify` |
| knip | Dead-code analysis via `bunx knip@5.80.0` (non-blocking) | `bun run dead-code` |
| profiling scripts | CPU and heap profiling | `bun run profile:*` |

`bunfig.toml` preloads `packages/ui/src/test/preload.ts` for tests.

The repository's own guidance (per-repo `AGENTS.md`) notes that `bun run lint` and `bun run type-check` are time-consuming; prefer `bun build:web` after implementation.

## Environments

| Environment | Branch / channel | Purpose | URL |
|---|---|---|---|
| local/dev | any | `bun run dev` HMR web, `bun run electron:dev`, mobile sim | http://localhost:5173 / http://localhost:3001 |
| production (self-hosted, stable) | main (tag `vX.Y.Z`) | Users run locally or on their own servers; npm package, Docker, or desktop app | varies |
| canary (nightly) | `canary` tag, npm `canary` dist-tag | Nightly desktop and npm builds for early testing | varies |

There is no hosted staging or preview environment; deployments are self-hosted and user-driven.
Nightly behavior-net verification runs at 02:17 UTC.
The Canary build runs at 03:00 UTC.

## CI/CD pipelines

| Group | Workflow | Trigger | What it runs |
|---|---|---|---|
| Release | release.yml | tag `v*` push or manual dispatch | Builds macOS arm64 Electron DMG/zip and VS Code VSIX; publishes releases |
| Release | release-windows.yml | manual dispatch | Windows installer build signed via SignPath |
| Release | windows-signed-build.yml | reusable | x64/arm64 Windows SignPath build |
| Release | mirror-release.yml | manual dispatch | Re-mirrors release artifacts to Cloudflare R2 behind downloads.openchamber.dev |
| Release | canary.yml | nightly | Canary desktop and npm canary build |
| Release | vscode-extension.yml | tag push or manual dispatch | VS Code extension build and publish |
| Release | mobile-release.yml | manual dispatch | Mobile release |
| Build | build-macos-arm64-dmg.yml | manual dispatch | macOS Electron DMG build |
| Build | mobile-ci.yml | manual dispatch | Mobile smoke build |
| Build | nix-eval.yml | PR or manual dispatch | Nix builds for server and desktop on x86_64-linux, aarch64-linux, aarch64-darwin |
| Build | sdk-preview.yml | manual dispatch | SDK preview build |
| CI | oc-review.yml | pull_request | PR checks (lint/type-check/tests per repo guidance) |
| CI | oc-integration.yml | PR or comment driven | Integration checks via `opencode` bot |
| CI | pr-intake.yml | pull_request | PR size labeling, contribution gate, and evidence labels |
| CI | label-merge-conflict.yml | pull_request | Merge-conflict labeling |
| CI | pr-review.yml | pull_request | PR review automation |
| CI | opencode.yml | issue/PR comments | Runs `/oc`, `/opencode` commands via bot |
| CI | issue-intake.yml | issues | Issue intake automation |
| CI | stale.yml | schedule | Stale issue and PR cleanup |
| CI | bot-help.yml | issue/PR comments | Bot help commands |
| CI | bot-summarize.yml | issue/PR comments | Bot summarization |
| Smoke | release-desktop-smoke.yml | manual dispatch | Release build smoke test |
| Smoke | opencode-smoke.yml | manual dispatch | OpenCode smoke test |
| Smoke | behavior-net.yml | nightly | Full behavior-net verification |
| Docs | docs-source.yml | push to main | Documentation site build |

## Deployment

Deployment is self-hosted and user-driven. Supported paths:
- **Desktop**: Electron installers produced by the release workflows (macOS DMG/zip, signed Windows installers via SignPath, Linux `.deb`/`.rpm`/AppImage via electron-builder).
- **Server**: run `openchamber` CLI (`packages/web/bin/cli.js`) or `bun start:web`, as a systemd service, or Docker via `Dockerfile` + `docker-compose.yml`.
- **npm package**: published CLI consumed via `npm i -g openchamber` (or the `openchamber` binary).
- **VS Code extension**: published from `vscode-extension.yml`.
- **Canary**: nightly channel published by `canary.yml` (desktop artifacts and the npm `canary` dist-tag).
- **Mirror**: release artifacts mirrored to Cloudflare R2 behind `downloads.openchamber.dev` by `mirror-release.yml`.
- **Nix**: server and desktop packages validated by `nix-eval.yml`.

### Rollback

- Desktop/app releases: reinstall a prior release artifact (release workflow keeps per-tag assets).
- Self-hosted server: redeploy a previous image/tag or previous `openchamber` npm version.
- No automated rollback mechanism exists; rollback is manual.

## Health checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `/health` | 200 OK with JSON containing `status: 'ok'`, `timestamp`, `openchamberVersion`, `runtime`, `compatibility` (including `api.health.v1`), and optional `serverId` | Monitoring |

- Registered in `packages/web/server/lib/server-frame/core-routes.ts`.
- No `/healthz` or `/ready` route exists.
- Guest local services expose their own `/health`.

## Smoke tests

- **Behavior-net (nightly)**: `behavior-net.yml` runs the full behavior net nightly.
- **Desktop release smoke**: `.github/workflows/release-desktop-smoke.yml` + `scripts/test-release-build.sh` (`bun run release:test`).
- **OpenCode smoke**: `.github/workflows/opencode-smoke.yml`.
- **Mobile smoke build**: `mobile-ci.yml` (manual dispatch).
- **Package tests**: `bun run test` (runs isolated tests across scripts, ui, vscode, electron, web).

## Hosting

Self-hosted by the user: local machine, own server, or Docker. No OpenChamber-run hosting for instances.
The private relay is the only OpenChamber-hosted infrastructure, used for E2EE remote access transport only (not for hosting instances).

## Secrets management

Secrets live in user-controlled locations:
- Provider API keys are stored by OpenCode (OpenCode's auth/config, e.g. `~/.local/share/opencode/` and provider auth files).
- OpenChamber-managed credentials (quota provider credentials) are written to `~/.config/openchamber/quota/*.json` with `0o600` permissions (see `packages/web/server/lib/quota/credentials/store.js`).
- Remote-access pairing secrets and signing keys are generated at runtime and stored locally; relay identity/signing key under the OpenChamber config dir.
- Enterprise policy can be supplied via `/etc/openchamber/policy.json`, Windows ProgramData, macOS Application Support, or an environment variable (see `enterprise-mode.ts`).
- No secrets are logged; code and tooling enforce not committing `.env` or credential files.

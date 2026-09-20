# Infrastructure

## Technology stack

| Component | Technology | Version |
|---|---|---|
| Language | TypeScript throughout | 5.8.2 (catalog) |
| Runtime | Bun | 1.3.14 (root `packageManager`) |
| Core runtime | Effect (effect-smol era beta) | 4.0.0-beta.83 |
| HTTP API server | Hono (plus hono-openapi, zod validators) | 4.10.7 |
| Terminal UI | SolidJS plus @opentui/core | 0.4.5 |
| Web app | SolidJS plus Tailwind plus Vite (`packages/app`) | Tailwind 4.1.11, Vite 7.1.4, solid-js 1.9.10 |
| Desktop | Electron plus electron-builder (`packages/desktop`) | electron-vite workflow |
| Docs and marketing site | Astro Starlight with @astrojs/cloudflare adapter (`packages/web`) | 12.6.3 (adapter) |
| Storage | SQLite via Drizzle ORM plus @effect/sql-sqlite-bun | drizzle-orm 1.0.0-rc.2 |
| Storage adapters | Workspace packages `packages/effect-sqlite-node` and `packages/effect-drizzle-sqlite` | Workspace pinned |
| Infrastructure as code | SST | 4.13.1 |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| bun | Package management and script running | `bun install`, `bun run --cwd <package> <script>` |
| oxlint | Linting | `bun run lint` (config `.oxlintrc.json`) |
| prettier | Formatting | `prettier` (config is inline `prettier` key in root `package.json`, ignore file `.prettierignore`) |
| tsgo | Type checking, run per package via turbo | `bun turbo typecheck` from repo root, or `bun run typecheck` in a package (`tsgo --noEmit`) |
| bun test | Unit testing, always from a package dir, never repo root | `bun test --timeout 30000 --only-failures` (`packages/opencode`), `bun test --only-failures` (`packages/core`) |
| httpapi exerciser | HttpApi coverage, auth, and effect gates | `bun run test:httpapi` in `packages/opencode` (`script/httpapi-exercise.ts`) |
| opencode build script | CLI builds, including single-executable local builds | `bun run build` in `packages/opencode` (`script/build.ts`, supports `--single`) |
| husky | Git hooks | Installed via `prepare` script (hooks in `.husky/`) |
| gitleaks | Secret scanning signal | `.gitleaksignore` exists at root |

- Tests must run from package directories, never repo root.
- The root `test` script exits 1 with `do not run tests from root` as a guard.
- Monorepo workspaces are `packages/*`, `packages/console/*`, `packages/stats/*`, `packages/sdk/js`, and `packages/slack`.
- Dev entry points from root scripts are `dev` (`packages/opencode`), `dev:desktop`, `dev:web` (`packages/app`), `dev:console`, and `dev:stats` (via `sst shell --stage=production`).

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| production | production | Live user-facing SST deployment | Note: production branch deploys via `deploy.yml`, exact public URL was not pinned down in this pass |
| dev | dev | Default branch and main integration target | Note: `dev` branch deploys via `deploy.yml`, exact public URL was not pinned down in this pass |

- The default git branch is `dev`.
- SST app name is `opencode` with per-stage behavior.
- Production uses `removal: retain` and `protect: true`, all other stages use `removal: remove`.
- No explicit staging or PR preview environment mapping was found in `sst.config.ts` or `deploy.yml`.

## CI/CD pipelines

- The repo contains 27 workflow files in `.github/workflows/` (the brief said 26, the directory listing shows 27).
- Workflow files are close-issues, close-prs, compliance-close, containers, deploy, docs-locale-sync, docs-update, duplicate-issues, generate, models-snapshot, nix-eval, nix-hashes, notify-discord, opencode, pr-management, pr-standards, publish-github-action, publish-vscode, publish, release-github-action, review, stats, storybook, test, triage, typecheck, and unlock.

| Workflow | Trigger | What it runs |
|---|---|---|
| test.yml | Push to `dev`, pull_request, workflow_dispatch | Unit tests via `bun turbo test` on linux plus windows blacksmith runners, generated-client check, HttpApi exerciser gates, and Playwright e2e for `packages/app` |
| typecheck.yml | Pull request checks | Turbo typecheck across packages |
| deploy.yml | Push to `dev` or `production`, workflow_dispatch | SST deploy to the matching stage |
| publish.yml | Push to `ci`, `dev`, `beta`, `snapshot-*`, workflow_dispatch | Version, CLI builds, Windows signing, Electron builds, then publish |
| containers.yml | Container pipeline | Builds images from `packages/containers` |
| generate.yml | Codegen check | Verifies generated client and protocol output is current |

## Deployment

- SST deployments run through `deploy.yml` on pushes to `dev` or `production` (plus manual dispatch).
- CLI releases run through `publish.yml`, which builds `packages/opencode` and `packages/cli` artifacts for darwin, linux, and windows.
- Desktop builds ship via GitHub releases from the `build-electron` matrix (mac x64 and arm64, windows x64 and arm64, linux x64 and arm64).
- The npm package `opencode-ai` is published from `packages/opencode/script/publish.ts`.
- AUR PKGBUILD updates and a Homebrew tap formula update are handled in `packages/opencode/script/publish.ts` (both verified in that file).
- A root executable `install` script exists for direct installs.
- Container images are defined in `packages/containers` and published via `containers.yml`.
- Scoop, Chocolatey, pacman (beyond AUR), mise, and Nix channels were not verified in this pass.

### Rollback

- No rollback procedure is explicitly documented in the repo.
- SST production uses `removal: retain` with `protect: true`, so a bad deploy is not automatically torn down.
- Reverting a release means cutting a new release or re-running the deploy workflow from a known good ref.

## Health checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| `GET /global/health` (HttpApi) | `{ healthy: true, version }` | HttpApi consumers and operators |

- The health endpoint exists in the HttpApi (`GET /global/health`, handler `GlobalHttpApi.health` in `packages/opencode/src/server/routes/instance/httpapi/handlers/global.ts`), which corrects the brief claim that no health route was found.
- No separate `/ready`, `/live`, or `/ping` routes were found in `packages/opencode/src/server`.

## Smoke tests

- The HttpApi exerciser (`bun run test:httpapi` in `packages/opencode`) acts as the closest smoke suite, covering endpoint coverage, auth, and effect modes.
- App-level e2e runs via Playwright (`bun --cwd packages/app test:e2e:local`), also wired into `test.yml`.
- No standalone post-deploy smoke script was found.

## Hosting

- SST home is Cloudflare, with an AWS provider pinned to `us-east-1` (plus Stripe, Planetscale, Honeycomb, and Random providers in `sst.config.ts`).
- The docs site deploys to Cloudflare via the `@astrojs/cloudflare` adapter.
- Infrastructure definitions live in `infra/` (`app`, `console`, `enterprise`, `lake`, `monitoring`, `secret`, `stage`, `stats`).
- Scaling strategy was not pinned down in this pass.

## Secrets management

- SST secrets are declared in `infra/secret.ts` (R2 keys, Honeycomb API key and webhook secret, support API key, Upstash Redis URL and token).
- The Stripe provider reads `STRIPE_SECRET_KEY` from the environment in `sst.config.ts`.
- Local development uses environment variables.

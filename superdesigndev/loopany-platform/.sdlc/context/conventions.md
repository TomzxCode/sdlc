# Conventions

## Naming

- **Files:** kebab-case throughout (`api.machine.poll.ts`, `loop-kanban.tsx`, `create-loop.ts`); test files use a `<name>.test.ts` suffix next to their source; route files use TanStack's `route-name.tsx`/`route-name.$.tsx` naming.
- **Packages:** scoped npm names `@loopany/server` and `@crewlet/loopany`; directory names are lowercase single words (`packages/server`, `packages/daemon`).
- **Variables:** camelCase for local variables and function parameters.
- **Functions / Methods:** camelCase verbs (`createLoop`, `reclaimRun`, `supersedePendingRun`, `registerRunLease`); async over sync where I/O is involved.
- **Classes:** PascalCase (`MachineGateway`, `CliGateway`, `ArtifactSync`, `Scheduler`).
- **Constants:** UPPER_SNAKE_CASE for module-level tunables (`RUN_TIMEOUT_MS`, `WIRE_TEXT_CAP`, `ONLINE_TTL_MS`).
- **DB identifiers:** snake_case columns and tables (`machines`, `run_leases`, `artifact_files`, `task_file_content`).
- **TypeScript types:** PascalCase interfaces and types (`RunLeaseCaps`, `SnapshotManifest`, `CodingAgent`).
- **Tokens:** `dk_`-prefixed device tokens, `rk_`-prefixed run tokens; machine id derived as `m-sha256(token)[:16]`.

## Directory Structure

- `packages/server/` — the TanStack Start server: `src/db/` (schema + store), `src/gateway/` (machine routes, run lifecycle, sync, CLI dispatch, notify), `src/scheduler/` (cron engine), `src/server/` (boot, adapters, loopApi, team admin), `src/routes/` (pages + route files), `src/components/` (React UI), `src/lib/` (pure helpers), `src/skill/` (all prompt/skill prose, templates, bundles).
- `packages/daemon/` — the machine-side binary: CLI routing (`route.ts`, `cli.ts`), poll loop (`daemon.ts`), runner (`runner.ts`), watcher (`watcher.ts`), MCP bridge, skill install, setup hooks, bin shim.
- `scripts/` — demo and maintenance scripts (`demo-cookie-unified.sh`, `seed-many-runs.py`).
- `docs/` — markdown documentation and static assets.
- `.github/workflows/` — CI/CD (deploy, deploy-prod, publish-daemon).
- `.sdlc/` — SDLC artifacts (context, features, knowledge, templates).

## Coding Standards

- Use TypeScript with strict type checking across both packages; typecheck runs `tsr generate` before `tsc` on the server.
- Server route files use `createFileRoute(path).server.handlers`; dynamic-import heavy/native dependencies inside handlers to stay out of the client bundle.
- `editLoop` and run-token `set-*` surfaces must share the single validator module `gateway/validate.ts`; never fork validation logic.
- Machine routes must apply `machineRouteLimit` (rate limiting); byte-ingress routes (blob PUT, sync POST) are deliberately exempt and require a valid device token.
- Never introduce a raw `fetch(userUrl)`; outbound webhook calls go through `webhookGuard.ts`.
- Enforce the never-syncable dir list and per-file/per-loop byte caps identically on daemon and server (`watcher.ts` and `gateway/artifacts.ts`).
- Anti-pattern: storing plaintext secrets in the DB unless the trust model requires it (machine token re-show is the documented exception; run leases store only the hash).
- Keep prompt/skill markdown and UI copy in English only.
- Do not commit local-only state: `.sdlc/state.yml` and `.sdlc/features/*/progress.md` are gitignored.

## Commit Messages

- Conventional Commits with a scope: e.g. `fix(templates): stop the typed headline crashing under browser translation (#172)`. Type prefixes seen in history: `fix`, `feat`; scopes name the subsystem (e.g. `templates`). PR numbers are appended.

## Branching

- Branch off `main` for a change; keep the branch focused. Open a PR against `main`. The deploy workflow runs on merge to `main`.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff/review.
- Use sentence case for headings, not title case.
- Prefer bullet lists over prose paragraphs.
- Feature directories are named `N-<slug>` (issue number or `p<seq>`); feature IDs are `FEAT-N` in cross-references.
- Requirements and specifications for reverse-engineered features are frontmatter `status: done`.
- Keep artifacts concise and pointed at the authoritative file or command; do not restate what the code already shows.

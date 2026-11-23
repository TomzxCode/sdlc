# Conventions

## Naming

- **Files:** `kebab-case.ts` for TypeScript modules and route/service files; `snake_case.ts` for Drizzle schema files under `packages/db/src/schema/`; `PascalCase.tsx` for React components/pages (e.g. `AgentDetail.tsx`, `CompanySettings.tsx`); `kebab-case.md` for docs.
- **Variables:** `camelCase` for locals and function-scoped variables.
- **Functions / Methods:** `camelCase` (e.g. `createAgent`, `checkOutIssue`).
- **Classes:** `PascalCase`.
- **Constants:** `UPPER_SNAKE_CASE` for module/environment constants; `camelCase` for most exported values.
- **Types / Interfaces:** `PascalCase` (e.g. `AgentAdapter`, `InvokeResult`).
- **DB tables/columns:** `snake_case` (e.g. `company_id`, `assignee_agent_id`, `created_at`).
- **Env vars / config keys:** `UPPER_SNAKE_CASE` (e.g. `DATABASE_URL`, `OTEL_EXPORTER_OTLP_ENDPOINT`).
- **Enums:** string-literal unions in shared types; DB enums as lowercase snake values (e.g. agent status `active | paused | idle`).

## Directory Structure

pnpm workspace monorepo. Each concern lives in its own package:

- `server/` — Express API; routes under `server/src/routes/`, services under `server/src/services/`, adapters under `server/src/adapters/`, auth under `server/src/auth/`, middleware under `server/src/middleware/`, HTTP helpers under `server/src/http/`.
- `ui/` — React app; pages under `ui/src/pages/`, components under `ui/src/components/`, API clients under `ui/src/api/`, hooks under `ui/src/hooks/`, context under `ui/src/context/`.
- `packages/db/` — Drizzle schema files under `packages/db/src/schema/` use snake_case filenames.
- One schema file can define several related tables, e.g. `auth.ts` (4), `muse_runner.ts` (9), `company_skill_sources.ts` (4), and `execution_admissions.ts` (3).
- Migrations live in `packages/db/src/migrations/`.
- `pnpm db:generate` reads compiled `./dist/schema/*.js` per `packages/db/drizzle.config.ts` and writes to that directory.
- `pnpm --filter @paperclipai/db check:migrations` validates migration numbering and safety.
- `rules/database-migration-snapshots.mdc` requires keeping only the five newest schema snapshots.
- `packages/shared/` — shared types, constants, validators; `index.ts` re-exports.
- `packages/adapters/<adapter>-local/` — one package per built-in adapter; gateway/cloud variants use matching non-`-local` names (e.g. `hermes`, `hermes-gateway`, `cursor-cloud`, `openclaw-gateway`).
- `packages/plugins/` — SDK, scaffolder, sandbox providers, example plugins.
- `doc/` — product and operational docs; `doc/plans/` for repo plan files (`YYYY-MM-DD-slug.md`); `doc/spec/` and `doc/experimental/` for deeper specs.

## Coding Standards

- TypeScript throughout; strict types preferred. Run `pnpm -r typecheck` before hand-off.
- Keep contracts synchronized across layers: any schema/API change must update `packages/db` schema + exports, `packages/shared` types/constants/validators, `server` routes/services, and `ui` API clients + pages.
- Company-scoping is mandatory: every domain entity is scoped to a company; enforce `company_id` boundaries in routes/services.
- Preserve control-plane invariants: single-assignee tasks, atomic checkout semantics, approval gates, budget hard-stop auto-pause, and activity logging for all mutations.
- Never expose or log secrets/keys; hash agent API keys at rest; redact secrets in logs and activity payloads.
- Follow AGENTS.md section 2 "Read This First" before making non-trivial changes: `GOAL.md` and `PRODUCT.md` for product scope, `DEVELOPING.md` for setup and commands, `DATABASE.md` for schema and migrations, `doc/connections/CONNECTOR-PLAYBOOK.md` for Apps catalog connections, and `DESIGN.md` for `ui/` changes.
- Anti-patterns: do not assume a library is available without checking `package.json`; do not replace strategic docs wholesale; do not rely on local filesystem paths as the only artifact access path (use Paperclip artifacts/work products).

## Verification

- `pnpm verify` is the default local verification command, selecting affected Vitest files against the merge base with `master` (AGENTS.md section 7).
- Exit 2 means the change needs broader verification: run focused checks and let required CI supply coverage, or use `pnpm verify --full`.

## Commit Messages

Conventional Commits style with scope.
This is weakly verified because this checkout is a shallow clone with one commit.
Recorded patterns:

- `feat: ...`, `feat(scope): ...` (e.g. `feat(skills): ...`)
- `fix: ...`, `fix(scope): ...` (e.g. `fix(server): ...`, `fix(issues): ...`, `fix(workspace-runtime): ...`)
- `docs: ...`
- `refactor: ...`, `refactor(scope): ...` (e.g. `refactor(server): ...`)
- Adapter prefixes allowed inline, e.g. `[codex] Fix mobile issue chat spacing`.
- Keep messages clear and meaningful; one PR = one logical change.

## Branching

- Default branch: `master`.
- Feature work branches: short `kebab-case` names scoped to the change, optionally with a conventional prefix: `feat/...`, `fix/...`, `docs/...`, `chore/...`.
- Do **not** include internal/instance-local Paperclip ticket ids (e.g. `PAPA-123`, `PAP-224`) or instance task slugs in branch names — rename before pushing (see `CONTRIBUTING.md`).
- Fork (HenkDz/paperclip) feature branches may differ (e.g. `feat/externalize-hermes-adapter`).

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff/review.
- Use sentence case for headings, not title case.
- Prefer bullet lists over dense prose paragraphs.
- Reference code locations as `file_path:line_number`.
- Keep artifacts dated and centralized: new repo plan documents go in `doc/plans/` using `YYYY-MM-DD-slug.md` filenames (this does not replace Paperclip issue planning).

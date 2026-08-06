# Conventions

## Naming

- **Files:** kebab-case for modules and config (e.g. `workflow-graph-executor.ts`, `homebrew-importer.ts`, `project-overview.md`)
- **Packages:** scoped `@fusion/*` for private packages; `@runfusion/fusion` for the published CLI; `fusion-workspace` for the root
- **Variables / Functions / Methods:** `camelCase`
- **Classes / Components:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE` for module-level constants
- **Directories:** lowercase, kebab-case where multi-word
- **FNXC comments:** user-facing requirements are encoded as `FNXC:<Area> <yyyy-MM-dd-hh:mm>` comments (timestamp from `date -u`); used with area-of-product prefix and greppable

## Directory Structure

- `packages/<name>/` holds each workspace package; `packages/cli/` (published as `@runfusion/fusion`), `packages/core/` (`@fusion/core`), `packages/engine/` (`@fusion/engine`), `packages/dashboard/` (`@fusion/dashboard`), `packages/desktop/`, `packages/mobile/`, `packages/i18n/`, `packages/plugin-sdk/`, and `pi-*` extension packages
- Dashboard domain: `packages/dashboard/src/routes/` registers API routes via domain registrars; `packages/dashboard/app/` holds the React SPA; `packages/dashboard/app/components/` holds components with co-located `__tests__/`
- Domain source: `packages/core/src/` and `packages/engine/src/`, tests colocated under each package's `__tests__/`
- `docs/` — user, architecture, and solution docs; `docs/solutions/` holds documented solutions to past problems
- `.changeset/` — changesets for the published package; `scripts/` — build/test/maintenance scripts (`.mjs`)

## Coding Standards

- TypeScript with strict typing; rely on workspace typecheck (`pnpm typecheck`, scope: all packages except desktop/mobile)
- Lint with ESLint (`pnpm lint`, `eslint.config.mjs`); run before commit
- Never introduce dynamic cross-`@fusion/*` imports; keep imports statically analyzable
- Never declare a React component inside another component (remount bug rule; enforced by `fusion-react/no-nested-component-definitions`)
- Do not appease flaky tests (no widened timeouts, retries, or softened assertions); quarantine them instead
- Use async `exec` with timeout for user-configured commands; `execSync` only for short deterministic git plumbing
- Use `superviseSpawn(...)` from `@fusion/core` for managed child processes, never raw `nohup`/detached spawn
- Design tokens (`--space-*`, `--radius-*`, etc.) over hardcoded pixels/hex; reuse existing components before forking
- Add a changeset (`.changeset/<name>.md`) only when a change affects published `@runfusion/fusion`
- Fix the invariant, not the repro: regression tests must cover all known surfaces, not the single reported case

## Commit Messages

Conventional Commits with a Fusion task ID prefix: `feat(FN-XXX):`, `fix(FN-XXX):`, `test(FN-XXX):`. One commit per step boundary. Task-worktree commits carry a `Fusion-Task-Id: FN-NNNN` trailer. Release commits are `chore(release): vX.Y.Z`. Branch work uses isolated git worktrees and keeps the primary checkout on `main`.

## Branching

- Direct work and small fixes commit on `main`. Feature/branch-bound work uses isolated worktrees (`wt switch --create <branch>` or `git worktree add -b …`), keeping the primary checkout on `main`
- Merging into main defaults to squash (`directMergeCommitStrategy="always-squash"`); history-preserving merges require opt-in
- Empty cherry-picks are no-ops; already-on-main classification applies for finalize/self-healing recovery
- Shared-branch-group members assemble `branch_groups.branchName` even when auto-merge is off; only shared→default promotion stays gated

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff and review
- Use sentence case for headings, not title case
- Prefer bullet lists over prose paragraphs in artifacts
- Artifact frontmatter uses lowercase `status` (`draft`/`in-review`/`approved`), with feature IDs, FR/NFR and TC IDs unpadded (`FEAT-42`, `FR-1`, `TC-5`)
- Feature directories are `<N>-<slug>` under `.sdlc/features/`, cross-referenced as `FEAT-N`; pending features use `p<seq>` with no `issue` field
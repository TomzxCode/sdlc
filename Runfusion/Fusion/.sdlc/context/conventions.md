# Conventions

## Naming

- **Files:** kebab-case for modules and config (e.g. `workflow-graph-executor.ts`, `emit-bounded-run-audit.ts`, `agent-activity-contract.md`)
- **Dashboard React files:** PascalCase for components and contexts (e.g. `ActiveAgentsPanel.tsx`, `ShellContext.tsx`), camelCase for hooks (e.g. `useActivityLog.ts`), kebab-case for other dashboard modules
- **Packages:** scoped `@fusion/*` for private packages, `@runfusion/fusion` for the published CLI, `runfusion.ai` for the published alias in `packages/cli-alias/`, `fusion-workspace` for the root
- **Variables / Functions / Methods:** `camelCase`
- **Classes / Components:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE` for module-level constants
- **Directories:** lowercase, kebab-case where multi-word
- **FNXC comments:** product requirements and decisions are encoded as `FNXC:<Area> <yyyy-MM-dd-hh:mm>:` comments, where the area names the product area and the timestamp comes from `date -u`; write them as JSDoc or block comments, keep them greppable, and update them as requirements change

## Directory Structure

- `packages/<name>/` holds each workspace package: `packages/cli/` (`@runfusion/fusion`, published), `packages/cli-alias/` (`runfusion.ai`, published alias), `packages/core/` (`@fusion/core`), `packages/engine/` (`@fusion/engine`), `packages/dashboard/` (`@fusion/dashboard`), `packages/desktop/`, `packages/mobile/`, `packages/i18n/`, `packages/plugin-sdk/`, `packages/droid-cli/`, `packages/pi-claude-cli/`, and `packages/pi-llama-cpp/`
- `plugins/` holds the first-party plugin packages (`plugins/fusion-plugin-*/`) and the example plugins under `plugins/examples/`
- Dashboard API: `packages/dashboard/src/routes/` registers API routes through domain registrars; `createApiRoutes` only orchestrates, and the mount order is a tested contract (see `packages/dashboard/src/routes/README.md`)
- Dashboard UI: `packages/dashboard/app/` holds the React SPA; `packages/dashboard/app/components/` holds PascalCase components with a co-located `ComponentName.css`, and the component tests live in a sibling `__tests__/` directory
- Domain source: `packages/core/src/` and `packages/engine/src/`, with tests colocated under each package's `__tests__/` directory
- `docs/` holds user, architecture, and solution docs; `docs/solutions/` holds documented solutions to past problems
- `.changeset/` holds changesets for the published packages; `scripts/` holds build, test, and maintenance scripts (`.mjs`)

## Coding Standards

- TypeScript with strict typing; rely on the workspace typecheck (`pnpm typecheck`, scope: all packages except desktop and mobile)
- Lint with ESLint (`pnpm lint`, `eslint.config.mjs`); run before commit
- Never introduce dynamic cross-`@fusion/*` imports; keep imports statically analyzable
- Never declare a React component inside another component (remount bug rule; enforced by `fusion-react/no-nested-component-definitions`)
- Do not appease flaky tests (no widened timeouts, retries, or softened assertions); quarantine them instead, by adding an entry to `scripts/lib/test-quarantine.json` and a matching `exclude` in that package's vitest config in the same commit, and delete a quarantined file after 14 days unless it is rescued with a root-cause fix
- Use async `exec` with timeout for user-configured commands; `execSync` only for short deterministic git plumbing
- Use `superviseSpawn(...)` from `@fusion/core` for managed child processes, never raw `nohup` or detached spawn
- Design tokens (`--space-*`, `--radius-*`, `--shadow-*`, `--duration-*`, `--transition-*`, `--font-*`, and color or status tokens) over hardcoded pixels, hex, or `rgba()`; reuse existing components before forking a parallel variant
- Put new component CSS in `packages/dashboard/app/components/ComponentName.css`; `packages/dashboard/app/styles.css` holds only tokens, primitives, and cross-component overrides
- Add a changeset (`.changeset/<name>.md`) only when a change affects a published package (`@runfusion/fusion` or the `runfusion.ai` alias); the body uses labeled `summary`, `category`, and optional `dev` fields
- Fix the invariant, not the repro: regression tests must cover all known surfaces, not the single reported case
- A test asserts behavior, never source text or comments; the enforced check is `scripts/check-no-comment-assertions-in-tests.mjs`
- A behavior change owns every test that asserts the old behavior: update or delete the stale tests in the same change, and fix the shared fixture rather than patching tests one by one
- Do not add slow tests: prefer narrow seams, in-memory fakes, shared harnesses, and fake timers over network calls and polling loops
- Scope verification to the changed files: run file-scoped test commands, and do not pass `allowFullSuite: true` unless a full run is genuinely required
- New run-audit emitters use `emitBoundedRunAudit` (`packages/engine/src/util/emit-bounded-run-audit.ts`) or `packages/core/src/run-audit/emit-bounded-run-audit.ts`, so a stalled telemetry sink never blocks the code path that owns it
- User-facing strings go through react-i18next (`t("namespace:key", "English default")`); English is the source of truth, and `pnpm i18n:extract` registers a new key
- Never run a release from inside a task; a human operator runs `pnpm release` on its own
- Port 4040 is reserved; never start a test server on it

## Commit Messages

- Conventional Commits with a Fusion task ID prefix: `feat(FN-XXX):`, `fix(FN-XXX):`, `test(FN-XXX):`, `docs(FN-XXX):`.
- Use one commit per step boundary.
- Task-worktree commits carry a `Fusion-Task-Id: FN-NNNN` trailer.
- Release commits are `chore(release): vX.Y.Z`.

## Branching

- Direct work and small fixes commit on `main`. Feature/branch-bound work uses isolated worktrees (`wt switch --create <branch>` or `git worktree add -b …`), keeping the primary checkout on `main`.
- Merging into main defaults to squash (`directMergeCommitStrategy="always-squash"`); history-preserving merges require opt-in.
- Every squash commit must overlap the task `## File Scope`, unless the task sets `scopeOverride`; never force-add ignored artifacts.
- Empty cherry-picks are no-ops; already-on-main classification applies for finalize/self-healing recovery.
- Shared-branch-group members assemble `branch_groups.branchName` even when auto-merge is off; only shared→default promotion stays gated.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff and review
- Use sentence case for headings, not title case
- Prefer bullet lists over prose paragraphs in artifacts
- Plain language: short direct sentences, active voice, common words over jargon, no em-dashes (use commas or parentheses)
- Avoid "shape", "honest", "load-bearing", "real", "substrate", and "posture" unless one of them is the most accurate term
- Artifact frontmatter uses a lowercase `status` (`draft`, `in-review`, `approved`, `done`), with feature IDs, FR/NFR and TC IDs unpadded (`FEAT-42`, `FR-1`, `TC-5`)
- Feature directories are `<N>-<slug>` under `.sdlc/features/`, cross-referenced as `FEAT-N`; pending features use `p<seq>` with no `issue` field

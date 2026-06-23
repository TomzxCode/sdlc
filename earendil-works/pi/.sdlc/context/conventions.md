# Conventions

## Naming

- **Files:** `kebab-case.ts` for modules (e.g. `agent-session.ts`, `model-registry.ts`).
- **Directories:** `kebab-case` (e.g. `coding-agent`, `interactive/`).
- **Variables / Functions:** `camelCase`.
- **Classes / Types / Interfaces:** `PascalCase`.
- **Constants:** `camelCase` for locals, `UPPER_SNAKE_CASE` for module-level constants (e.g. `CURRENT_SESSION_VERSION`, `DEFAULT_EDITOR_KEYBINDINGS`).
- **Types:** Interfaces generally unprefixed; type aliases for unions and utility types. `T`-prefixed TypeBox schema types (e.g. `TSchema`, `TObject`).
- **Enum-like:** No `enum` (erasable-TS rule); use union string literal types or `as const` objects.
- **IDs:** Feature `FEAT-NNNN`, requirement `FR-NN`, task `NNNN`, etc. (see SDLC ID formats).

## Directory Structure

```
packages/
  ai/             # pi-ai: src/, test/, scripts/ (model generators), providers/, api/, auth/
  agent/          # pi-agent-core: src/ (core), src/harness/, test/
  tui/            # pi-tui: src/, src/components/, test/, native/
  coding-agent/   # pi-coding-agent: src/core/, src/modes/, src/utils/, src/cli/,
                  #   docs/, test/ (flat suite + suite/ + suite/regressions/),
                  #   examples/ (sdk/, extensions/)
scripts/          # repo-level: release, shrinkwrap, version-sync, pinned-dep/TS-import checks
.github/workflows/  # CI
```

Each package owns its own `package.json`, `tsconfig*.json`, `CHANGELOG.md`, and tests.
The root `package.json` defines npm workspaces and the orchestration scripts (`build`, `check`, `test`, `release:*`).
All `.sdlc/` artifacts live at the repo root under `.sdlc/`.

## Coding Standards

- **Erasable TypeScript only** in code checked by the root config (`packages/*/src`, `packages/*/test`, `packages/coding-agent/examples`): no parameter properties, `enum`, `namespace`/`module`, `import =`, `export =`, or other constructs requiring JS emit. Use explicit fields with constructor assignments.
- **Top-level imports only.** No inline imports (`await import()`, `import("pkg").Type`, dynamic type imports).
- **No `any` unless absolutely necessary.** Biome `noExplicitAny` is off but AGENTS.md forbids `any`.
- **Never hardcode key checks** (e.g. `matchesKey(keyData, "ctrl+x")`). Add defaults to `DEFAULT_EDITOR_KEYBINDINGS` or `DEFAULT_APP_KEYBINDINGS` so they stay configurable.
- **Never edit `models.generated.ts` directly.** Update `packages/ai/scripts/generate-models.ts` and regenerate.
- **Inline single-line helpers** that have only one call site.
- **Never remove or downgrade code** to fix type errors from outdated deps; upgrade the dep instead.
- **Ask before removing** functionality or code that appears intentional.
- **Formatting:** Biome — tabs, `indentWidth` 3, `lineWidth` 120, `formatWithErrors: false`. Run via `npm run check` (writes fixes).
- **Type checking:** `tsgo --noEmit` (native TypeScript preview) plus `check:ts-imports` (relative import hygiene) and `check:browser-smoke`.

## Commit Messages

Conventional Commits with package scopes.

- Format: `{feat,fix,docs,chore}[(ai,agent,tui,coding-agent)]: <concise informative message>` (optionally multi-line).
- Scopes are the short package names: `ai`, `agent`, `tui`, `coding-agent`.
- No emojis in commits, issues, PR comments, or code.
- `fixes #<n>` / `closes #<n>` repeat the keyword per issue for auto-close (`closes #1, closes #2`, not `closes #1, #2`).
- Release commits: `Release vX.Y.Z` and `Add [Unreleased] section for next cycle` are produced by the release script.
- Lockfile commits require `PI_ALLOW_LOCKFILE_CHANGE=1` and are reviewed as code.

## Branching

- `main` is the integration branch.
- Topic branches: `feature/...` and `fix/...` prefixes are used, but short bare-slug branches also appear (e.g. `sdlc`, `model-registry`).
- Releases tag `vX.Y.Z` on `main` and push the tag; CI publishes from the tag.
- Multiple agent sessions may share a worktree; never run `git reset --hard`, `git checkout .`, `git clean -fd`, `git stash`, `git add -A`, `git add .`, or `git commit --no-verify` (they stomp other sessions' work or bypass checks).
- Commit only files changed in the current session; stage explicit paths.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff and review.
- Sentence case for headings, not title case.
- Prefer bullet lists over prose paragraphs; tables for structured data.
- No emojis unless explicitly requested.
- Technical prose only; be direct, no filler.
- `## [Unreleased]` sections in per-package `CHANGELOG.md` are the only place new changelog entries go; released version sections are immutable.

## Testing Standards

- **Frameworks:** Vitest for `ai`, `agent`, `coding-agent`; Node's built-in `node --test` for `tui`.
- **Never run the full vitest suite directly** (it includes e2e tests activated by endpoint/auth env vars). Run non-e2e tests via `./test.sh`, or specific files: `node ../../node_modules/vitest/dist/cli.js --run test/specific.test.ts`.
- **coding-agent tests** use `test/suite/harness.ts` + the faux provider. No real provider APIs, keys, or paid tokens.
- **Issue regressions** go under `packages/coding-agent/test/suite/regressions/` named `<issue-number>-<short-slug>.test.ts`.
- If you create or modify a test file, run it and iterate until it passes.
- **Ad-hoc scripts:** write to a temp file (e.g. `/tmp`), run, remove. Do not embed multi-line scripts in bash commands.

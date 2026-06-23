# Conventions

## Naming

- **Files:** `kebab-case.ts` for modules; `PascalCase.tsx` for SolidJS components.
- **Variables:** `camelCase`; prefer concise single-word identifiers when still descriptive.
- **Functions / Methods:** `camelCase`.
- **Classes / Namespaces:** `PascalCase`; exported modules are referenced by namespace (e.g. `Project.ID`).
- **Constants:** `camelCase` or `PascalCase` for true constants where idiomatic.
- **Drizzle schema fields:** `snake_case` so column names need not be redefined as strings.
- **Config namespaces:** self-export pattern at the top of `src/config` files (e.g. `export * as ConfigAgent from "./agent"`).

## Directory Structure

- Monorepo rooted at `packages/*`, with workspaces also covering `packages/console/*`, `packages/stats/*`, `packages/sdk/js`, and `packages/slack`.
- Core logic and server live in `packages/opencode/src/` (e.g. `session/`, `server/`, `tool/`, `provider/`, `config/`, `plugin/`, `system-context`).
- TUI code lives in `packages/opencode/src/cli/cmd/tui/` alongside the `packages/tui` package.
- Shared web UI components live in `packages/app`; Electron wrapping in `packages/desktop`.
- Canonical project specs live under `specs/` (`project.md`, `v2/`, `storage/`, `tui-package.md`).
- Project-specific opencode config and built-in agents/tools/skills live under `.opencode/`.
- Infra (SST) definitions live under `infra/`; CI under `.github/workflows/`.

## Coding Standards

- Keep logic in one function unless composable or reusable; do not extract single-use helpers preemptively.
- Avoid `else` statements; prefer early returns.
- Prefer ternaries or early returns over reassignment; prefer `const` over `let`.
- Avoid unnecessary destructuring; use dot notation to preserve context (`obj.a`, not `const { a } = obj`).
- Avoid `try`/`catch`; prefer `.catch(...)` where possible.
- Avoid the `any` type; reach for precise types and type guards on `filter` to preserve inference.
- Rely on type inference; avoid explicit type annotations unless necessary for exports or clarity.
- Never alias imports (`import { foo as bar }`) and never use star imports; use a module's own exported namespace by name.
- Prefer dynamic imports for heavy modules only needed in selected code paths, especially startup-sensitive entrypoints.
- Use Bun APIs when possible (e.g. `Bun.file()`).
- Prefer functional array methods (`flatMap`, `filter`, `map`) over `for` loops.
- Inline values used only once to reduce total variable count.
- Make the main function read as the happy path; push supporting details into small helpers below it.
- Prefer Effect schema helpers (e.g. `Schema.UnknownFromJsonString`, `Schema.decodeUnknownOption`) over manual `JSON.parse` in `Effect.try`.

## Commit Messages

- Conventional Commits: `type(scope): summary`.
- Valid types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.
- Scopes are optional but encouraged: package or area (`core`, `opencode`, `tui`, `app`, `desktop`, `sdk`, `plugin`, `llm`, `server`, `stats`).
- Examples: `fix(tui): simplify thinking toggle styling`, `chore: generate` (used for SDK/codegen regen), `refactor(core): simplify session input promotion`.

## Branching

- Default branch is `dev`; local `main` may not exist, so diff against `dev` or `origin/dev`.
- Branch names are short, at most three hyphen-separated words, with no slashes or type prefixes (e.g. `session-recovery`, `regenerate-sdk`).
- PR titles follow the same Conventional Commits form as commit messages.
- All PRs must reference an existing issue (`Fixes #123` / `Closes #123`); issue-first policy is enforced.

## SDLC Documentation Style

- One sentence per line in markdown files to make diffs and review easier.
- Use sentence case for headings, not title case.
- Prefer bullet lists over prose paragraphs.
- Do not use em-dashes; use commas or parentheses instead.
- Do not leave `<…>` placeholders in produced artifacts; write a concise note when something genuinely cannot be determined.
- Artifact paths resolve repo-first, then `$SDLC_DIR/{owner}/{repository}/.sdlc/` when `SDLC_DIR` is set; `state.yml` and `features/*/progress.md` are never mirrored.

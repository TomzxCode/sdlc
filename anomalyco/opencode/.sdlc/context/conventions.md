<!-- session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA -->
# Conventions

## Naming

- **Files:** `kebab-case.ts` for modules; `PascalCase.tsx` for SolidJS components.
- **Variables:** `camelCase`; prefer concise single-word identifiers when still descriptive.
- **Functions / Methods:** `camelCase`.
- **Classes / Namespaces:** `PascalCase`; exported modules are referenced by namespace (e.g. `Project.ID`).
- **Constants:** `camelCase` or `PascalCase` for true constants where idiomatic.
- **Drizzle schema fields:** `snake_case` so column names need not be redefined as strings.
- **Config namespaces:** self-export pattern at the top of `src/config` files (e.g. `export * as ConfigAgent from "./agent.js"`).

## Directory Structure

- Monorepo rooted at `packages/*`, with workspaces also covering `packages/plugins/*`, `packages/data/*`, and `services/*`.
- Core runtime lives in `packages/core/src/` (e.g. `session/`, `config/`, `database/`, `plugin/`, tools, agents, providers).
- CLI entry lives in `packages/cli/src/` (TUI launch, ACP server, run commands, server process).
- HTTP API implementation lives in `packages/server/src/` (per-domain `handlers/`); the public contract lives in `packages/protocol/src/` (HttpApi groups).
- Shared Effect Schemas live in `packages/schema`; LLM provider clients live in `packages/ai`.
- Generated clients live in `packages/client`; `packages/sdk` composes Client, Core, and Server.
- Plugin API lives in `packages/plugin`; TUI code lives in `packages/tui`; shared web UI shell in `packages/app`; Electron wrapping in `packages/desktop`; session components in `packages/session-ui`.
- Canonical session specs live under `specs/v2/`; the full Session Core contract also lives in `AGENTS.md`.
- Project-specific opencode config and built-in agents/tools/skills live under `.opencode/`.
- Deployment configuration lives with each service (`services/*/cloudflare.config.ts` or `wrangler.jsonc`); CI under `.github/workflows/`.
- Runtime dependencies point from Schema to Core and Protocol, then from Core and Protocol to Server. Client runtime code may depend on Schema and Protocol but never Core or Server.

## Coding Standards

- Keep logic in one function unless composable or reusable; do not extract single-use helpers preemptively.
- Validate unknown values once at the boundary that owns them, pass typed values inward, and do not revalidate values already guaranteed by a schema, constructor, or internal type.
- Explain the failure mode, likelihood, and complexity cost before adding complexity for a speculative race or security edge case, and get the user's buy-in.
- Avoid `else` statements; prefer early returns.
- Prefer ternaries or early returns over reassignment; prefer `const` over `let`.
- Avoid unnecessary destructuring; use dot notation to preserve context (`obj.a`, not `const { a } = obj`).
- Avoid `try`/`catch` where possible.
- Avoid the `any` type; reach for precise types and type guards on `filter` to preserve inference.
- Rely on type inference; avoid explicit type annotations unless necessary for exports or clarity.
- Never alias imports (`import { foo as bar }`, `resolve as pathResolve`) and never use star imports (`import * as Foo`, `import type * as Foo`).
- Never use type-position `import(...)` references such as `Schema.declare<import("@opencode/plugin/effect/plugin").Plugin["effect"]>`. The only exception is an aliased type import when two imports genuinely collide on a name and no other option exists; avoid even that where possible.
- If a namespace-style value is needed, import the module's own exported namespace by name (`import { Project } from "@opencode/core/project"`) and reference `Project.ID`.
- Prefer dynamic imports for heavy modules only needed in selected code paths, especially startup-sensitive entrypoints. Destructure dynamic import bindings near the top of the narrowest scope that needs them. Avoid inline chains such as `await import("./module").then((mod) => mod.value())`; keep branch-specific imports inside the branch that needs them.
- Use Bun APIs when possible (e.g. `Bun.file()`).
- Prefer functional array methods (`flatMap`, `filter`, `map`) over `for` loops.
- Inline values used only once to reduce total variable count.
- Make the main function read as the happy path; push supporting details into small helpers below it.
- Do not over-abstract simple expressions into single-use helpers; extract only when the helper names a clear concept.
- Do not return `Effect` from helpers unless they perform effectful work; keep synchronous parsing, validation, and option building synchronous.
- Prefer Effect schema helpers (e.g. `Schema.UnknownFromJsonString`, `Schema.decodeUnknownOption`) over manual `JSON.parse` wrapped in `Effect.try` when parsing untrusted JSON strings.
- In Effect generators, bind services to named variables before calling methods; do not use nested service yields such as `yield* (yield* Foo.Service).bar()`.
- Add comments for non-obvious constraints and surprising behavior, not for obvious assignments or control flow.
- After changing the public Protocol or Server `HttpApi`, run `bun run generate` from `packages/client`; never edit generated client files directly.
- Do not add `.changeset` files; this repository does not use Changesets.

## Testing

- Avoid mocks; do not use `globalThis.*` unless it is the only option.
- Test the actual implementation; do not duplicate logic in tests.
- Tests cannot run from the repo root (guard: `do-not-run-tests-from-root`); run them from package directories such as `packages/core`.
- Before writing or changing tests, read the matching skill in `.opencode/skills`: `unit-tests` for Bun tests, `tui-tests` for OpenTUI renderer tests, `app-e2e-tests` for Playwright in `packages/app/e2e`, or `component-tests` for Playwright on stories in `packages/stories`.
- For live TUI checks, run `bun run dev:live [directory]` from a development worktree. It uses the elected background server and the `dev` TUI storage channel.
- For live desktop diagnostics, attach Playwright with `chromium.connectOverCDP(endpoint, { noDefaults: true })` and do not emulate color scheme or reduced motion on the live window unless requested.

## Checks

- Run `bun run check` from the repository root as the canonical full lint and type-check verification.
- During focused iteration, run `bun typecheck` from the affected package directory (e.g. `packages/core`); never run `tsc` directly.
- Local `typecheck` scripts use `bun check`. CI and package publishing use `typecheck:tsc` with the official TypeScript compiler (`@typescript/native`), which is the source of truth when the two disagree; reproduce with `bun run typecheck:tsc` from the package directory.
- Use two-space indentation, LF endings, UTF-8, and a final newline. Prettier writes no semicolons and uses a 120-character print width.

## Experimental API

- An experimental endpoint lives under `/api/experimental/`, its OpenAPI identifier starts with `experimental.`, and its SDK path starts with `client.experimental.`. Its description says "Experimental: may change without compatibility guarantees."
- `packages/protocol/test/experimental-identifiers.test.ts` enforces the path and identifier match in both directions; the SDK namespace follows from the path.
- An experimental field or parameter on a stable endpoint goes under an `experimental` key, like config's `config.experimental.*`.
- New endpoints and new default behaviors start experimental.
- To graduate one, move the route out of `/api/experimental`, drop the `experimental.` prefix, and note it in `CHANGELOG.md`.
- Experimental HTTP routes change without aliases: rename or remove the route and update callers.
- A breaking move of shipped SDK or plugin API, including moving it under `experimental`, keeps the old path and type names as deprecated aliases until the next minor. Mark each alias `@deprecated` with the replacement and "Removed in the next minor". Generated SDK moves come from codegen (`compile(..., { aliases: true })` in `packages/client/script/generate.ts`), not by hand.
- Experimental plugin hooks start with `experimental.`, e.g. `experimental.ws.handshake`.

## Feature Flags

- Decide at PR time whether a change needs a flag: new user-visible behavior, risky core changes, and partially landed work get one; fixes, refactors, docs, and tests do not.
- Gate risky or multi-PR behavior with a key and description in `packages/schema/src/config/flag.ts`, and read it with `Flag.enabled()` from `@opencode/core/flag`.
- Flags default on in local and dev builds and off in releases, except `optInOnly` flags such as `todo`, which require an explicit `OPENCODE_FLAGS` entry or `experimental` config entry in every build.
- Name the flag in the PR body. `OPENCODE_FLAGS=all` and `experimental.all_flags: true` skip opt-in-only flags; opt out with `all,-flag_name` or by setting that experimental key to `false`.
- Ship a feature by deleting its flag and the checks that read it.

## UI conventions

- Choose TUI theme tokens by semantic role, not current color. Do not use raw `theme.hue` values or borrow unrelated tokens.
- Use `text.feedback` and `background.feedback` only for outcome or status feedback; use `formfield` states for form text, ordinals, and selection markers, and `action` states for actions.
- If a semantic role has no token, extend the theme schema, defaults, resolution, and types before using it. Verify light and dark defaults plus the custom-theme fallback when the public theme surface changes.
- TUI stories are fixture-driven under `packages/tui/src/feature-plugins/system/storybook`, registered in `index.tsx`, render the production component, expose state dimensions through keybindings listed in `StoryFooter`, and include a reset command when needed.
- Run a story with `OPENCODE_STORY` set to the story id from the development worktree, and exercise narrow and wide sizes when layout matters.

## Runtime invariants

- Plugins load asynchronously. Server handlers never wait for activation, retry until a plugin appears, or turn slow plugins into timeouts or 503s. Lists may be partial on a cold Location, and missing models, providers, or RPCs return not-found.
- Clients wait for what they need: long-lived clients refresh on matching `*.updated` events, and one-shot callers poll `plugin.list` or the entry they need (see `packages/cli/src/services/plugin-startup.ts`). Running registered hooks and awaiting their result is allowed.
- Session Core follows `AGENTS.md` and `specs/v2/`: durable events record irreducible facts, prompt admission is separate from execution, each step is one explicit `llm.stream` call from reloaded history, and local drains stay process-local until clustering exists.

## Commit Messages

- Conventional Commits: `type(scope): summary`.
- Valid types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.
- Scopes are optional; use the affected package or area when helpful (e.g. `core`, `opencode`, `tui`, `app`, `desktop`, `sdk`, `plugin`).
- Examples: `fix(tui): simplify thinking toggle styling`, `docs: update contributing guide`, `chore(sdk): regenerate types`.
- Keep PR descriptions and issue bodies brief. Long, AI-generated walls of text may be ignored.

## Branching

- Default branch is `dev`. Base branches and worktrees on `origin/dev`, target PRs at `dev`, and diff against `origin/dev` unless told otherwise.
- Branch names are short, at most three hyphen-separated words, with no slashes or type prefixes (e.g. `session-recovery`, `fix-scroll-state`, `regenerate-sdk`).
- PR titles follow the same Conventional Commits form as commit messages.
- Bug fixes, chores, and tests must reference an existing issue with `Fixes #123` or `Closes #123`; documentation, refactor, and feature PRs are exempt from the automated linked-issue check.
- Before implementing new functionality, open a feature request describing the problem and get design approval before the implementation PR.

## SDLC Documentation Style

- One sentence per line in markdown files to make diffs and review easier.
- Use sentence case for headings, not title case.
- Prefer bullet lists over prose paragraphs.
- Do not use em-dashes; use commas or parentheses instead.
- Do not leave placeholders in produced artifacts; write a concise note when something genuinely cannot be determined.
- Avoid the terms `shape`, `honest`, `load bearing`, `load-bearing`, `real`, `substrate`, and `posture` unless one is genuinely the most appropriate term.
- Artifact paths resolve repo-first, then `$SDLC_DIR/{owner}/{repository}/.sdlc/` when `SDLC_DIR` is set; `state.yml`, `features/*/progress.md`, and `status-report.html` are local-only and never mirrored.

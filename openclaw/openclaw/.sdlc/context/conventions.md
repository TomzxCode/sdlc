<!-- session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3 -->
# Conventions

## Naming

- **Files and directories:** kebab-case for source, test, and config files, and for `src/` subdirectories, `packages/` names, `apps/` names, and `extensions/` plugin directories; standard root config filenames (`package.json`, `tsconfig.json`, `.oxlintrc.json`) keep their canonical names.
- **UI components:** kebab-case `*.tsx` files, with `*.test.tsx` files for their tests; no PascalCase or snake_case TypeScript source files remain anywhere, while Rust files under `crates/` use snake_case.
- **Identifiers:** camelCase for variables, functions, and methods; PascalCase for classes, types, and interfaces; UPPER_SNAKE_CASE for true constants and camelCase for module-level const values; a `Type` suffix marks string-union and discriminated-union types.
- **Test files:** the file suffix selects the suite; shared test code uses `*.test-support.ts`, `*.test-helpers.ts`, `*.test-fixtures.ts`, `*.test-mocks.ts`, or `*.test-harness.ts`.

| Suffix | Purpose |
| --- | --- |
| `*.test.ts` | Unit test |
| `*.integration.test.ts` | Cross-module integration test |
| `*.contract.test.ts` | Contract test for a provider, channel, or other published surface |
| `*.e2e.test.ts` | End-to-end test |
| `*.live.test.ts` | Live test against real providers or models |
| `*.browser.test.ts` | Control UI Playwright browser test |

## Directory Structure

```
./
├── .agents/              # Agent skill library
├── .github/              # Workflows, issue and PR templates, CODEOWNERS
├── .sdlc/                # SDLC artifacts
├── apps/                 # Native and desktop companion apps (macos, ios, android, linux, swabble, shared, macos-mlx-tts)
├── config/               # Lint, format, and budget configuration and baselines
├── crates/               # Rust workspace (gateway client, node host)
├── custodian-skills/     # Custodian agent skill definitions
├── deploy/               # Deployment manifests
├── docs/                 # Documentation
├── examples/             # Runnable examples
├── extensions/           # Plugin packages (one directory per plugin)
├── git-hooks/            # Repository Git hooks
├── packages/             # Workspace packages (SDK, protocol, core libraries)
├── patches/              # pnpm package patches
├── qa/                   # QA Lab scenarios and maturity scores
├── scripts/              # Build, CI, and release scripts
├── security/             # Security rules (OpenGrep)
├── skills/               # Bundled agent skills shipped with the package
├── src/                  # Core TypeScript source in kebab-case subdirectories (agents, channels, cli, config, gateway, skills, state, tui, worker, ...)
├── test/                 # Repo-level test suites and helpers
├── tools/                # Isolated tool dependencies (Solid lint)
└── ui/                   # Control UI (Solid 2 web components)
```

## Coding Standards

- TypeScript ESM strict mode; `any` is banned by the `typescript/no-explicit-any` rule outside test and test-support files, so use `unknown` with narrow adapters.
- No `@ts-nocheck` anywhere in the tree; lint suppressions must be intentional and explained.
- Use zod for external boundaries and config schemas; prefer discriminated unions over freeform strings for routing and state.
- Prefer `satisfies` for registries and config maps, and prefer ctor parameter properties for injected deps and config.
- Keep APIs narrow and export only what current callers need; classes use inheritance or composition, not prototype mixins or mutations.
- Prefer small clear code and split on an ownership change, not on an arbitrary line count.
- Delete branches, modes, adapters, and tests when possible, because a refactor that adds a second path has probably failed.
- Inline simple one-use objects when clearer; extract only to remove duplication or hard logic.
- Split code into gather -> normalize -> decide -> act, and prefer early returns over nested condition pyramids.
- Import cycles stay green: `pnpm check:import-cycles` covers `src`, `extensions`, and `scripts`; `pnpm check:madge-import-cycles` covers `src`, `extensions`, and `ui`; `pnpm check:architecture` runs both.
- File size cap: the oxlint `max-lines` rule allows 700 counted lines (blank lines and comments skipped) for TypeScript and JavaScript under `src`, `ui/src`, `packages`, and `extensions`, and 800 for `.mjs` and `.cjs`; `pnpm check:line-cap-ratchet` and `pnpm check:max-lines-ratchet` keep `config/max-lines-baseline.txt` shrinking.
- Lint, format, and types: `pnpm lint` runs the full pipeline through `scripts/run-lint.mts` with oxlint 1.89.0 and oxlint-tsgolint, `pnpm lint:all` runs `scripts/run-oxlint.mjs` directly, `pnpm format` and `pnpm format:check` run `scripts/run-format.mts` with oxfmt 0.74.0, `pnpm lint:docs` runs markdownlint on the docs, `pnpm tsgo` type-checks the core project, and `pnpm tsgo:all` adds the UI, extensions, scripts, and tests.
- Generated files are never hand-edited: `docs/plugins/reference/**` and `docs/plugins/plugin-inventory.md` come from `pnpm plugins:inventory:gen`, `docs/maturity/**` comes from `taxonomy.yaml` and `qa/maturity-scores.yaml` via `pnpm maturity:render`, and `CHANGELOG.md` plus `CHANGELOG/**` are release-owned.

## Commit Messages

- Use a Conventional Commits style `type: description`, as required by the PR template, for example `fix(ui): keep a reader who reaches the top of a chat at the top (#204220)`.
- The PR template lists `feat`, `fix`, `improve`, `refactor`, `docs`, and `chore`; merged commit subjects also use `test`, `perf`, and `ci`.
- A parenthesized scope names the affected area (channel, component, or package name) and is optional; add it only when it helps the reader.
- A `!` after the type or scope marks a breaking change.
- Squash merges append the PR number in parentheses at the end of the subject.

## Branching

- `main` is the primary branch.
- PRs land with squash merge; `OPENCLAW_PR_MERGE_METHOD` defaults to `squash` in `scripts/pr-lib/merge.sh`.
- Do not rebase onto `main` just because `main` advanced; refresh only for a conflict, a failing guard, an explicit request, or material stale-base risk.
- Open PRs from a branch maintainers can push to, and keep **Allow edits from maintainers** enabled; branch names are not restricted by a naming convention.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff/review
- Use sentence case for headings, not title case
- Prefer bullet lists over prose paragraphs for enumerations
- American English spelling and grammar
- Avoid em dashes; use commas or parentheses instead
- Tables for structured data (requirements, specs, comparisons)
- ASCII diagrams for architecture flows

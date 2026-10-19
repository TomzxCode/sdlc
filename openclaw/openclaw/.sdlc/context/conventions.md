# Conventions

## Naming

- **Files and directories:** kebab-case for source, test, and config files, and for `src/` subdirectories, `packages/` names, `apps/` names, and `extensions/` plugin directories; UI components are kebab-case `*.tsx` files with `*.test.tsx` siblings, and no PascalCase source files remain anywhere.
- **Identifiers:** camelCase for variables, functions, and methods; PascalCase for classes, types, and interfaces; UPPER_SNAKE_CASE for true constants and camelCase for module-level const values; a `Type` suffix marks string-union and discriminated-union types.
- **Test files:** the file suffix selects the suite; shared test code uses `<module>.test-support.ts`, `<module>.test-helpers.ts`, `<module>.test-fixtures.ts`, `<module>.test-mocks.ts`, or `<module>.test-harness.ts`.

| Suffix | Purpose |
| --- | --- |
| `<module>.test.ts` | Unit test |
| `<module>.integration.test.ts` | Cross-module integration test |
| `<module>.contract.test.ts` | Contract test for a provider, channel, or other published surface |
| `<module>.e2e.test.ts` | End-to-end test |
| `<module>.live.test.ts` | Live test against real providers or models |
| `<module>.browser.test.ts` | Control UI Playwright browser test |

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
├── extensions/           # Plugin packages (175 directories, 171 packages)
├── git-hooks/            # Repository Git hooks
├── packages/             # Workspace packages (SDK, protocol, core libraries)
├── patches/              # pnpm package patches
├── qa/                   # QA Lab scenarios and maturity scores
├── scripts/              # Build, CI, and release scripts
├── security/             # Security rules (OpenGrep)
├── skills/               # Bundled agent skills shipped with the package
├── src/                  # Core TypeScript source (77 kebab-case subdirectories: agents, channels, cli, config, gateway, skills, state, tui, worker, ...)
├── test/                 # Repo-level test suites and helpers
├── tools/                # Isolated tool dependencies (Solid lint)
└── ui/                   # Control UI (Solid 2 web components)
```

## Coding Standards

- TypeScript ESM strict mode; `any` is banned by the `typescript/no-explicit-any` rule outside test support files, so use `unknown` with narrow adapters.
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
- Lint, format, and types: `pnpm lint` runs the full pipeline through `scripts/run-lint.mts` with oxlint 1.87.0 and oxlint-tsgolint, `pnpm lint:all` runs `scripts/run-oxlint.mjs` directly, `pnpm format` and `pnpm format:check` run `scripts/run-format.mts` with oxfmt 0.72.0, `pnpm lint:docs` runs markdownlint on the docs, `pnpm tsgo` type-checks the core project, and `pnpm tsgo:all` adds the UI, extensions, scripts, and tests.
- Generated files are never hand-edited: `docs/plugins/reference/**` and `docs/plugins/plugin-inventory.md` come from `pnpm plugins:inventory:gen`, `docs/maturity/**` comes from `taxonomy.yaml` and `qa/maturity-scores.yaml` via `pnpm maturity:render`, and `CHANGELOG.md` plus `CHANGELOG/**` are release-owned.

## Commit Messages

- Conventional Commits: `type(scope): description`, for example `fix(doctor): reclaim runtimes despite unrelated Node processes (#177407)`.
- Types include `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`, `ci`, `build`, and `style`; a `!` after the type or scope marks a breaking change, and the scope is the affected area (channel, component, or package name).
- The PR number goes in parentheses at the end.

## Branching

- `main` is the primary branch.
- PRs land with squash merge; `OPENCLAW_PR_MERGE_METHOD` defaults to `squash` in `scripts/pr-lib/merge.sh`.
- Do not rebase onto `main` just because `main` advanced; refresh only for a conflict, a failing guard, an explicit request, or material stale-base risk.
- Keep one issue or topic per PR, and note that branch names are not enforced by tooling.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff/review
- Use sentence case for headings, not title case
- Prefer bullet lists over prose paragraphs for enumerations
- American English spelling and grammar
- Tables for structured data (requirements, specs, comparisons)
- ASCII diagrams for architecture flows

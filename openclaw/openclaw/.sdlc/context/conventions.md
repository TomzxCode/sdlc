# Conventions

## Naming

- **Files:** kebab-case for extension directories and config files; PascalCase for TypeScript component files
- **Variables:** camelCase
- **Functions / Methods:** camelCase
- **Classes:** PascalCase
- **Constants:** UPPER_SNAKE_CASE for true constants; camelCase for module-level const values
- **TypeScript interfaces/types:** PascalCase with `Type` suffix for discriminated union types
- **Test files:** `<module>.test.ts` for unit tests, `<module>.e2e.test.ts` for end-to-end tests, `<module>.live.test.ts` for live integration tests

## Directory Structure

```
./
├── .sdlc/               # SDLC artifacts
├── apps/                # Native companion applications
│   ├── macos/           # macOS desktop app (Swift/SwiftUI)
│   ├── ios/             # iOS app (Swift/SwiftUI)
│   ├── android/         # Android app (Kotlin)
│   └── shared/          # Shared app code
├── config/              # Generated config files
├── docs/                # Documentation
├── extensions/          # Plugin packages (152+ extensions)
├── packages/            # Shared packages (SDK, protocol, core libraries)
├── scripts/             # Build and CI scripts
├── src/                 # Core TypeScript source
│   ├── agents/          # Agent runtime
│   ├── channels/        # Channel system
│   ├── cli/             # CLI commands
│   ├── config/          # Config system
│   ├── gateway/         # Gateway server
│   └── ...
├── test/                # Test helpers
└── ui/                  # Control UI (Lit web components)
```

## Coding Standards

- TypeScript ESM strict mode; no `any` types; use `unknown` with narrow adapters
- Prefer discriminated unions over freeform strings for routing/state
- Early returns over nested condition pyramids
- Split code into gather -> normalize -> decide -> act
- Prefer small clear code; maintainability includes not growing LOC without payoff
- Refactors should reduce non-test LOC; if LOC grows, the new ownership must clearly pay for it
- Delete branches, modes, adapters, and tests when possible; a refactor that adds a second path has probably failed
- Keep APIs narrow; export only current caller needs
- Inline simple one-use objects when clearer; extract only when it removes duplication or hard logic
- Prefer ctor parameter properties for injected deps/config
- Prefer `satisfies` for registries/config maps
- Classes should use inheritance/composition, not prototype mixins/mutations
- No `@ts-nocheck`; lint suppressions only when intentional and explained
- Use zod for external boundaries
- Cycle prevention: keep `pnpm check:import-cycles` green
- File size ~700 LOC as a guideline for when to split

## Commit Messages

Conventional Commits format: `type(scope): description` (e.g. `fix(discord): add timeouts to voice upload requests (#102863)`).
Types include `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`.
Scope is the affected area (channel name, component, package).
PR number referenced in parentheses at end.

## Branching

- `main` is the primary development branch
- Feature branches: `feat/<description>` or `impl/<issue-number>`
- Fix branches: `fix/<description>`
- No merge commits on `main`; rebase before push
- PRs should be one issue/topic; do not bundle unrelated changes

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff/review
- Use sentence case for headings, not title case
- Prefer bullet lists over prose paragraphs for enumerations
- American English spelling and grammar
- Tables for structured data (requirements, specs, comparisons)
- ASCII diagrams for architecture flows

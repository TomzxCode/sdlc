<!-- session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8 -->
# Conventions

## Naming

- **Files:** `kebab-case.ts` for modules (e.g. `agent-session.ts`, `model-registry.ts`).
- **Directories:** `kebab-case` (e.g. `coding-agent`, `modes/interactive/`).
- **Variables / Functions:** `camelCase`.
- **Classes / Types / Interfaces:** `PascalCase`.
- **Constants:** `camelCase` for locals, `UPPER_SNAKE_CASE` for module-level constants (e.g. `CURRENT_SESSION_VERSION` in `packages/coding-agent/src/core/session-manager.ts`, `DEFAULT_TOOL_NAMES` in `packages/coding-agent/src/core/settings-manager.ts`, `CODEMODE_TOOL_NAME` in `packages/durable/src/codemode/codemode.ts`).
- **Types:** Interfaces generally unprefixed; type aliases for unions and utility types. TypeBox schema types keep the `T` prefix (`TSchema`, `TSchemaOptions`, `TProperties`).
- **Enum-like:** No `enum` (erasable TypeScript rule); use union string literal types or `as const` objects.
- **IDs:** Feature `FEAT-N`, requirement `FR-N`, task `N`. Never zero-padded (`FEAT-42`, not `FEAT-0042`). The `p` prefix marks a pending feature (`FEAT-p1`).

## Directory Structure

| Path | Contents |
|---|---|
| `packages/ai/` | `@earendil-works/pi-ai`. `src/` (flat modules plus `api/`, `auth/`, `compat/`, `providers/`, `utils/`), `test/`, `scripts/` (model generators, `generate-models.ts`). `src/providers/data/` is gitignored and generated at build time. |
| `packages/agent/` | `@earendil-works/pi-agent-core`. `src/` is flat (`agent.ts`, `agent-loop.ts`, `proxy.ts`, `stream-fn.ts`, `types.ts`, `index.ts`), `test/` (plus `test/utils/`), `examples/mcp-codemode/`. |
| `packages/tui/` | `@earendil-works/pi-tui`. `src/` (flat modules plus `src/components/`), `test/`, `native/` (`darwin/`, `linux/`, `win32/`, plus `clipboard.h` and `napi.h`). No `exports` map and no `bin`. |
| `packages/coding-agent/` | `@earendil-works/pi-coding-agent`. `src/` (`core/`, `modes/`, `cli/`, `utils/`, `extensions/`, `experimental/`, `bun/`), `test/` (flat tests plus `suite/`, `suite/regressions/`, `mcp-conformance/`), `docs/` (44 pages), `examples/` (`sdk/`, `extensions/`), `scripts/`, `schemas/`, `install-lock/` (generated npm project that pins the CLI runtime tree). |
| `packages/chord/` | `@earendil-works/chord`. `src/` (flat host/link/contract modules plus `context/`, `delta/`, `sqlite/`), `test/` (plus `delta-benchmark/`, `delta-tracker/`, `fixtures/`, `sqlite/`), `docs/` (`spec.md`, `guide.md`, `tutorial.md`), `src/delta/README.md`. |
| `packages/durable/` | `@earendil-works/pi-durable`. `src/` (flat `index.ts`, `types.ts`, `documents.ts`, `entries.ts`, `tasks.ts`, `errors.ts`, `ids.ts`, `search.ts`, `truncate.ts`, `timers.ts` plus `harness/`, `session/`, `storage/` (`memory.ts`, `scan.ts`, `sqlite/`, `jsonl/`), `env/`, `tools/`, `codemode/`, `images/`, `tool-search/`, `testing/`), `test/` (harness, session, sqlite, jsonl, tools, codemode, env and image tests plus `examples/`, `fixtures/`, and `*-bench.ts` files), `test-workers/` (separate Vitest project in workerd), `docs/spec.md`. |
| `packages/telemetry/` | `@earendil-works/pi-telemetry`. `src/` (flat `index.ts`, `memory.ts`, `metrics.ts`, `noop.ts` plus `src/testing/`), `test/`. |
| `packages/evals/` | `@earendil-works/pi-evals` (private). `src/` (flat `cli.ts`, `docker.ts`, `harness.ts`, `plan.ts`, `report.ts`), `evals/`, `docker/`, `test/`, `vitest.test.config.ts`, `vitest.evals.config.ts`, `tsconfig.json`. No `src/index.ts`, no `exports` map, no `CHANGELOG.md`. |
| `packages/codemode/` | `@earendil-works/pi-codemode`. `src/` (flat `portable.ts`, `cloudflare.ts`, `declarations.ts`, `source.ts`, `identifier.ts`, `wasm.ts`, `types.ts` plus `src/runtime/`), `test/`, `examples/cloudflare/`. No internal pi dependencies. |
| `packages/env/` | `@earendil-works/pi-env`. `src/` (flat `connection.ts`, `errors.ts`, `index.ts`, `list-files.ts`, `remote-env.ts`, `ssh.ts`, `terminal.ts`, `watch.ts`), `daemon/` (Rust crate: `Cargo.toml`, `build.rs`, `rust-toolchain.toml`, and `daemon/src/` with `main.rs`, `frame.rs`, `decode.rs`, `errors.rs`, `exec.rs`, `fs.rs`, `list.rs`, `output.rs`, `pty.rs`, `scan.rs`, `watch.rs`, `window.rs`, `sys/`), `docs/` (`protocol.md`, `semantics.md`), `test/`. |
| `packages/mcp/` | `@earendil-works/pi-mcp`. `src/` (flat `client.ts`, `auth-provider.ts` plus `protocol/`, `transports/`, `oauth/`, `testing/`), `test/` (plus `fixtures/`), `LICENSES/`. |
| `scripts/` | 60 script files plus two directories. Release and publish (`release.mjs`, `publish.mjs`, `release-notes.mjs`, `local-release.mjs`, `publish-release-announcement.mjs`), model catalog (`publish-model-catalog.mjs`, `diff-model-catalog.mjs`, `update-model-catalog-pin.mjs`, `model-catalog-protocol.ts`, `model-catalog-minimum-version.mjs`), packaging and artifacts (`pack-packages.mjs`, `package-artifacts.mjs`, `package-workspaces.mjs`, `release-packages.mjs`, `generate-coding-agent-install-lock.mjs`, `build-binaries.sh`, `create-source-archive.sh`), local install and smoke (`local-package-install.mjs`, `use-local-packages.mjs`, `check-package-install.mjs`, `coding-agent-smoke.mjs`, `check-browser-smoke.mjs`, `smoke-test-codemode-binary.mjs`), repository checks (`biome-check.mjs`, `check-pinned-deps.mjs`, `check-runtime-deps.mjs`, `check-ts-relative-imports.mjs`, `check-entry-graphs.mjs`, `check-lockfile-commit.mjs`, `check-model-catalog-compat.mjs`, `npm-audit.mjs`), version sync (`sync-versions.js`), profiling and session stats (`profile-coding-agent-node.mjs`, `session-transcripts.ts`, `session-context-stats.mjs`, `stats.ts`, `cost.ts`, `tool-stats.ts`, `read-tool-stats.mjs`, `edit-tool-stats.mjs`), `scripts/biome/` (the Grit plugin) and `scripts/issues/` (the local issue triage tool with `run.sh`, `main.ts`, `triage.ts`, `github.ts`, `prompt.md`, `ui.html`, `categories/`). |
| `.github/workflows/` | 13 workflows: `ci`, `env`, `env-daemons`, `build-binaries`, `nix`, `publish-model-catalog`, `npm-audit`, `approve-contributor`, `issue-gate`, `pr-gate`, `issue-triage-labels`, `remove-inprogress-on-close`, `issue-analysis`. All actions are pinned to commit SHAs. |
| `nix/`, `flake.nix` | Offline Nix build of the `pi` package, with the model catalog pinned in `nix/model-catalog.json`. |
| `.husky/pre-commit` | Lockfile guard (`PI_ALLOW_LOCKFILE_CHANGE=1`), `npm run check`, browser smoke when `packages/ai` or `packages/web-ui` changed, and re-staging of formatted files. |
| `test.sh`, `pi-test.sh`, `pi-test.ps1`, `pi-test.bat` | Test runner and source-checkout CLI wrappers. |
| `vitest.base.ts` | Shared Vitest alias map that resolves workspace packages to their `src/` entry points. |
| `biome.json`, `tsconfig.json`, `tsconfig.base.json` | Formatter, linter, and compiler configuration. |
| `.npmrc` | `save-exact=true` and `min-release-age=2`. |

Each published package owns its own `package.json`, `tsconfig.build.json`, `CHANGELOG.md`, and tests.
`packages/evals` is private and owns only a `tsconfig.json`.
The root `package.json` defines npm workspaces as `packages/*`, `apps/*`, plus the five `packages/coding-agent/examples/extensions/*` entries.
The `apps/*` workspace glob is declared but no `apps/` directory exists in this checkout.
All `.sdlc/` artifacts live at the repo root under `.sdlc/`.

## Coding Standards

- **Erasable TypeScript only** in the code covered by the root `tsconfig.json` (`packages/*/src`, `packages/*/test`, `packages/durable/test-workers`, `packages/coding-agent/examples`, `packages/agent/examples`, and the two model-catalog protocol scripts): no parameter properties, `enum`, `namespace`/`module`, `import =`, `export =`, or other constructs needing JS emit. Use explicit fields with constructor assignments. The compiler flag is `erasableSyntaxOnly`.
- **Top-level imports only.** No inline imports (`await import()`, `import("pkg").Type`, dynamic type imports).
- **No `any` unless absolutely necessary.** Biome `noExplicitAny` is off but AGENTS.md forbids `any`.
- **Never hardcode key checks** (e.g. `matchesKey(keyData, "ctrl+x")`). AGENTS.md names the defaults `DEFAULT_EDITOR_KEYBINDINGS` and `DEFAULT_APP_KEYBINDINGS`; the code currently defines `KEYBINDINGS` in `packages/coding-agent/src/core/keybindings.ts` and `TUI_KEYBINDINGS` in `packages/tui/src/keybindings.ts`, so confirm the target map before editing.
- **Never edit `packages/ai/src/models.generated.ts` directly.** Update `packages/ai/scripts/generate-models.ts` and regenerate. The generated file is excluded from Biome formatting.
- **Resolve package assets** in `packages/coding-agent` through the helpers in `src/config.ts`, never `__dirname`.
- **Inline single-line helpers** that have only one call site.
- **Never remove or downgrade code** to fix type errors from outdated deps; upgrade the dep instead.
- **Ask before removing** functionality or code that appears intentional.
- **Formatting:** Biome 2.3.5 with tabs, `indentWidth` 3, `lineWidth` 120, and `formatWithErrors: false`. `npm run check` runs `node scripts/biome-check.mjs --write`, which is `biome check --error-on-warnings` and falls back to the Biome WASM build on platforms with no native binary.
- **Biome scope:** `files.includes` limits linting and formatting to `packages/*/src/**/*.ts`, `packages/*/test/**/*.ts`, `packages/coding-agent/examples/**/*.ts`, `packages/agent/examples/**/*.ts`, `scripts/model-catalog-protocol.ts`, and `scripts/model-catalog-protocol.test.ts`. `apps/` is excluded, and `**/models.generated.ts`, `**/*.models.ts`, and `**/test-sessions.ts` are excluded.
- **Biome rules:** the `recommended` set is on; `noExplicitAny`, `noNonNullAssertion`, `useNodejsImportProtocol`, `noControlCharactersInRegex`, and `noEmptyInterface` are off, and `useConst` is an error. The custom Grit plugin `scripts/biome/model-type-comparison.grit` rejects direct `model.type === "chat"` comparisons.
- **Type checking:** `tsc --noEmit` from the root `typescript` devDependency (version 7.0.2), using `tsconfig.json` (which extends `tsconfig.base.json` and sets `noEmit`, `module` and `moduleResolution` to `NodeNext`, `strict`, `erasableSyntaxOnly`, `verbatimModuleSyntax`, `allowImportingTsExtensions`, and `rewriteRelativeImportExtensions`).
- **Relative imports carry the `.ts` extension** (e.g. `export * from "./agent.ts"`). `scripts/check-ts-relative-imports.mjs` fails the build on relative `.js` specifiers inside `.ts` files.
- **Entry points are cost contracts.** `scripts/check-entry-graphs.mjs` walks the value-import graph of every declared export and enforces a per-entry file budget plus a list of forbidden paths, so a narrow entry cannot silently pull in a whole barrel.
- **Dependencies are pinned.** `scripts/check-pinned-deps.mjs` requires an exact `x.y.z` version for every registry dependency in `dependencies`, `devDependencies`, and `optionalDependencies` of every workspace `package.json`. `scripts/check-runtime-deps.mjs` verifies that runtime imports resolve to declared dependencies and to Node built-ins.
- **Install lock stays in sync.** `node scripts/generate-coding-agent-install-lock.mjs` regenerates `packages/coding-agent/install-lock/`; `npm run check:install-lock:coding-agent` verifies it byte for byte.
- **`npm run check` order:** Biome with `--write`, pinned-deps, runtime-deps, ts-imports, entry-graphs, install-lock check, `tsc --noEmit`, then browser smoke. It does not run tests.

## Commit Messages

Conventional Commits with package scopes.

- Format: `{feat,fix,docs}[(ai,tui,agent,coding-agent)]: <concise informative message>` (optionally multi-line). AGENTS.md line 62 is the only statement of the type list, and it names exactly `feat`, `fix`, and `docs`.
- This scope list is unchanged in AGENTS.md: still only `ai`, `tui`, `agent`, `coding-agent`.
- No agreed scope token exists yet for `chord`, `durable`, `telemetry`, `evals`, `codemode`, `env`, or `mcp`; confirm before using one in a commit message.
- No emojis in commits, issues, PR comments, or code.
- `fixes #<n>` / `closes #<n>` repeat the keyword per issue for auto-close (`closes #1, closes #2`, not `closes #1, #2`).
- Release commits: `Release vX.Y.Z` and `Add [Unreleased] section for next cycle` are produced by `scripts/release.mjs`.
- Lockfile commits require `PI_ALLOW_LOCKFILE_CHANGE=1` and are reviewed as code.

## Branching

- `main` is the integration branch; CI runs on pushes and pull requests against `main`.
- The environment workflow also triggers on pushes to `durable-env-*` branches, so a `durable-env-` prefix is the one topic branch pattern visible in the workflows.
- The Nix workflow fast-forwards the `stable` branch to the release tag.
- Releases tag `vX.Y.Z` on `main`; the `build-binaries.yml` workflow publishes from `v*` tags.
- No `feature/` or `fix/` prefix rule is documented in AGENTS.md, CONTRIBUTING.md, or the workflows, and this checkout has a shallow history (a single commit), so the earlier claim about `feature/...`, `fix/...`, and bare-slug topic branches could not be verified. Use `main` plus a descriptive topic branch and confirm the naming with a maintainer.
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

- **Frameworks:** Vitest (`vitest --run`) for `ai`, `agent`, `coding-agent`, `chord`, `durable`, `telemetry`, `codemode`, `env`, and `mcp`; `evals` runs Vitest with an explicit config (`vitest run --config vitest.test.config.ts`); Node's built-in `node --test` for `tui` (`node --test --test-reporter=dot --test-reporter-destination=stdout test/*.test.ts`).
- `vitest.config.ts` files exist in `agent`, `ai`, `codemode`, `coding-agent`, `durable`, `env`, and `mcp`; `evals` uses `vitest.test.config.ts` (unit) plus `vitest.evals.config.ts` (the `docs` and `host` projects), while `chord`, `telemetry`, and `tui` carry no `vitest.config.ts` at the package root.
- `packages/coding-agent` and `packages/evals` extend the shared root `vitest.base.ts` alias map, so tests resolve workspace packages to their `src/` entry points instead of built output.
- `packages/durable` runs three projects: the default `vitest --run`, a second `vitest --run` with `PI_DURABLE_DOCUMENT_RETENTION_MS=0`, and `npm run test:workers`, which is a separate Vitest project in `test-workers/` running under `@cloudflare/vitest-plugin` (`cloudflareTest`) in workerd against `test-workers/wrangler.jsonc`. The main `vitest.config.ts` excludes `test-workers/**`. A separate `vitest.benchmark.config.ts` runs `test/**/*.bench.ts`.
- The root `scripts/*.test.mjs` and `scripts/*.test.ts` run under `node --test` (`npm run test:scripts`), and the root `npm test` is `npm run test:scripts && npm run test --workspaces --if-present`.
- SQLite storage tests live under `packages/durable/test/` (`sqlite-storage.test.ts`, `sqlite-migrations.test.ts`, `sqlite-facade.test.ts`, `sqlite-cloudflare.test.ts`) against `packages/durable/src/storage/sqlite`.
- **Never run the full vitest suite directly** (it includes e2e tests activated by endpoint/auth env vars). Run non-e2e tests via `./test.sh` from the repo root, which runs `npm test` under `env -i` with an isolated HOME, `PI_NO_LOCAL_LLM=1`, and no provider keys, or run specific files from the package root: `node "$(git rev-parse --show-toplevel)/node_modules/vitest/dist/cli.js" --run test/specific.test.ts`, and `node --test test/specific.test.ts` for `packages/tui`.
- **coding-agent tests** use `test/suite/harness.ts` + the faux provider. No real provider APIs, keys, or paid tokens.
- **Issue regressions** go under `packages/coding-agent/test/suite/regressions/` named `<issue-number>-<short-slug>.test.ts`, with a comment carrying the issue number.
- **MCP conformance** runs with `npm run test:mcp-conformance` from `packages/coding-agent/test/mcp-conformance/`, against the pinned `baseline.json`.
- If you create or modify a test file, run it and iterate until it passes.
- **Ad-hoc scripts:** write to a temp file (e.g. `/tmp`), run, remove. Do not embed multi-line scripts in bash commands.

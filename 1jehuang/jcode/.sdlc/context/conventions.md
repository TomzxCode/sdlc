# Conventions

## Naming

- **Files:** snake_case for Rust source (e.g. `turn_execution.rs`), kebab-case for config slugs (e.g. `openai-compatible`); release tags use `v<semver>`.
- **Variables:** snake_case; Rust-idiomatic.
- **Functions / Methods:** snake_case.
- **Classes / Types:** `PascalCase` (e.g. `SessionStatus`, `ResumeTarget`, `PlanItem`).
- **Constants:** `SCREAMING_SNAKE_CASE` for module-level constants (e.g. `BACKGROUND_QUEUE_CAPACITY`).
- **Crates:** prefixed `jcode-`; data-model crates suffixed `-types` (e.g. `jcode-message-types`); provider runtimes `jcode-provider-<name>-runtime`; TUI subcomponents `jcode-tui-*`.
- **Unit test modules:** `*_tests.rs` files or `*_tests/` directories mounted with `#[path = "..."] mod tests`.

## Directory Structure

- `src/` — root crate: `main.rs`, `lib.rs`, `cli/` (args, dispatch, subcommands), `bin/` (dev/test binaries).
- `crates/` — workspace crates layered base → app-core → tui → root; provider runtimes kept downstream of `jcode-base` so provider edits do not rebuild the app spine.
- `tests/` — top-level integration tests plus `tests/e2e/` (end-to-end scenarios), `tests/fixtures/`, `tests/support/` (shared helpers), and Python test scripts that CI runs directly.
- `sdk/` — `typescript/` (npm SDK) and `npm/` (platform launcher packages).
- `ios/` — native iOS app (JCodeKit + JCodeMobile).
- `telemetry-worker/` — Cloudflare Worker + D1 schema and migrations.
- `docs/` — reference documentation: top-level docs describe current behavior, `plans/` are forward-looking, `proposals/` are uncommitted ideas, `audits/` hold dated audit reports, `dev/` holds process notes, `discovery-baselines/`, `images/`, and `sponsors/` hold supporting assets.
- `scripts/` — release, install, test, and QA scripts; budget-checker scripts plus `check_module_files.py` and `check_dependency_boundaries.py` enforce CI quality gates.
- `changelog/` — one JSON file per release (`v<version>.json` plus `index.json`).

## Coding Standards

- Rust edition 2024; `cargo fmt` enforced, `clippy --all-targets --all-features -D warnings` in CI.
- No comments unless they add value; prefer named types and clear code over explanatory comments.
- Keep the layered dependency spine: `jcode-base` (must not depend on any `jcode-tui-*` or `jcode-app-core` crate) → `jcode-app-core` (must not depend on any `jcode-tui-*` crate) → `jcode-tui` → root crate.
- Data models shared across layers live in `-types` crates; keep them lean.
- Log via `crate::logging` (file logging); do not `println!`/`eprintln!` in production paths (throwaway diagnostics only).
- Respect the CI budget ratchets (warning, panic, code-size, test-size, swallowed-error, wildcard-reexport, dependency-boundary).
- Hot render/embedding dependency stacks are pinned to `opt-level = 3` in dev/selfdev/test profiles; keep those profile pins when adding hot third-party crates.
- Do not add zero-padding to SDLC numeric identifiers.

## Commit Messages

Commit messages in the current history are plain sentences (for example `Test KV account-failover attribution end to end through the agent turn loop`).
Release automation commits `Update to <version>`.
The full history is not available in a fresh clone, so use Conventional Commits only when the contributor asks for it.

## Branching

Single default branch: `master` (also referenced as `main` in some workflow triggers).
PRs target the default branch and must reference an issue (enforced by `.github/workflows/require-issue.yml`).
Work directly on `master` by default.
Create a branch or worktree only when the user asks, or when isolation is genuinely necessary, and say why first.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diffs and review.
- Use sentence case for headings, not title case.
- Prefer bullet lists over prose paragraphs.
- Feature IDs are unpadded (`FEAT-42`, `FR-1`); pending features use `FEAT-pN`.
- Never commit local-only state: `.sdlc/state.yml` and `.sdlc/features/*/progress.md`.

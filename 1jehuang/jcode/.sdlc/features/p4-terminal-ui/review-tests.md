---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

| ID | Documented input | Reality | Correction |
|---|---|---|---|
| TC-4 | `crates/jcode-tui/src/tui/auth*_tests.rs` | No file matches that glob. The auth tests moved into the app module: `crates/jcode-tui/src/tui/app/auth_tests.rs` (21 tests) plus `crates/jcode-tui/src/tui/app/auth_subscription_status_tests.rs`. The account-picker UI is now a separate crate (`crates/jcode-tui-account-picker/`) with no test file. | Point TC-4 at the two real files. |
| TC-7 | `crates/jcode-desktop2` profile tests | That crate does not exist. `crates/jcode-build-support/src/paths.rs:798` lists "desktop", "desktop2", and "jcode-desktop2" among removed paths. The Jcode Desktop app lives in a separate repository. | Replace with a render-core parity entry over `crates/jcode-tui-markdown/src/render_core_adapter_tests.rs` (per `docs/RENDER_PARITY_ACCEPTANCE_CRITERIA.md`). |
| TC-8 | "Mermaid rendering acceptance / `docs/RENDER_PARITY_ACCEPTANCE_CRITERIA.md` checks" | That document is the Render-Core Parity harness, not Mermaid. Mermaid acceptance lives in `docs/MERMAID_RENDERING_REDESIGN.md`, with tests in `crates/jcode-tui-mermaid/src/mermaid_tests/` and `crates/jcode-tui/src/tui/ui_tests/diagrams/`. | Point TC-8 at the Mermaid doc and test files. |

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-tui/src/tui/session_picker/loading_tests.rs` (1564 lines: session list loading, disk cache, external session discovery)
- `crates/jcode-tui/src/tui/session_picker_tests/live_presence.rs`
- `crates/jcode-tui/src/tui/ui_tests/rendering.rs`, `tools.rs`, `prepare.rs`, `swarm_buffer.rs`, and the `basic/` set (`frame_flicker`, `reload_render`, `redraw_cadence`, `input_layout`, `body_cache`, `image_regions`, `idle_animation_partial`, `interaction_links`)
- `crates/jcode-tui/src/tui/ui_tests/diagrams/{part_01,part_02}.rs` (36 tests)
- `crates/jcode-tui/src/tui/ui_tests/onboarding.rs` and `crates/jcode-tui/src/tui/app/tests/onboarding_flow.rs`
- `crates/jcode-tui/src/tui/ui_tests/pinned_todo_regressions.rs` and `crates/jcode-tui/src/tui/ui_pinned_tests.rs`
- `crates/jcode-tui/src/tui/app/tests/` (the app state machine suite, including `model_picker_startup_tests.rs` and the remote reload and startup input suites)
- `crates/jcode-tui-markdown/src/render_core_adapter_tests.rs` and `markdown_latex_image_tests.rs`
- `crates/jcode-tui-render/src/swarm_gallery_tests.rs`
- `crates/jcode-tui/src/tui/app/command_registry_tests.rs`, `saved_account_route_tests.rs`, `auth_subscription_status_tests.rs`
- `crates/jcode-terminal-launch/src/windows_portable_tests.rs` and `crates/jcode-terminal-prompt/src/secret_pty_tests.rs`

## Quality

The Test Infrastructure section lists only the benchmark binaries `tui_bench` and `mermaid_side_panel_probe`.
Add `src/bin/session_memory_bench.rs`, `src/bin/memory_recall_bench.rs`, `src/bin/tui_bench/`, and the scripts `scripts/bench_startup.py`, `scripts/bench_reload_storm.py`, `scripts/bench_resume_picker.py`, `scripts/count_idle_draws.py`.
Point the flakiness guidance at `docs/TUI_TEST_FLAKINESS.md`.

## Correctness

No issues found.

## Maintainability

No issues found.

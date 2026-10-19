---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Overview | "rendering helpers in `jcode-tui-mermaid`, `jcode-tui-anim`, `jcode-fuzzy`, `jcode-math`, and a shared render model in `jcode-render-core`." | `crates/jcode-math` does not exist. The math kernels moved into `crates/jcode-tui-anim` (`crates/jcode-tui/Cargo.toml:29-31`). The TUI was also split into 13 sibling crates the spec does not mention: `jcode-tui-core`, `jcode-tui-markdown`, `jcode-tui-messages`, `jcode-tui-permissions`, `jcode-tui-render`, `jcode-tui-session-picker`, `jcode-tui-account-picker`, `jcode-tui-style`, `jcode-tui-tool-display`, `jcode-tui-usage-overlay`, `jcode-tui-visual-debug`, `jcode-tui-workspace`. | Replace the sentence with a description of the 14-way `jcode-tui-*` split, `jcode-fuzzy` for picker matching, and `jcode-render-core` for the shared render model. |
| Architecture | "├── tui/video_export — offline replay + video export (jcode replay)" | The module is at the crate root, not under `tui/` (`crates/jcode-tui/src/video_export.rs`). The replay timeline builder now lives in app-core (`crates/jcode-app-core/src/replay.rs`, tests in `crates/jcode-app-core/src/replay/tests.rs`). | Reword as "video_export.rs — offline replay video export (jcode replay --video) [crate root, not tui/]" and name the app-core replay builder. |
| Architecture | "├── tui/keybind — configurable keybindings" | The shared key primitives, including `SpeedSwitchKeys`, live in `crates/jcode-tui-core/src/keybind.rs:445`; the config-side keybinding catalogue is `crates/jcode-config-types/src/keybindings.rs`. | Reword to name both locations. |
| Data Models | "`[display]` \| display modes, centered mode, timestamps, message timestamps" and "`[features]` \| mermaid, idle animation, etc." | `message_timestamps` is in `[features]` (`crates/jcode-config-types/src/lib.rs:1213`), not `[display]`. `idle_animation` is in `[display]` (`crates/jcode-config-types/src/display.rs:58`), not `[features]`. `DisplayConfig` also carries `theme`, `external_sessions`, `resume_project_scope`, `usage_display`, `active_sessions_manager`, `disabled_animations`, `performance`, `animation_fps`, `redraw_fps`, `pin_images`, `pin_todos`, `prompt_preview`. A new top-level `[session]` section holds the hibernation config. | Move `message_timestamps` to the `[features]` row, move `idle_animation` to the `[display]` row, list the real keys in each, and add a `[session]` row. |
| Data Models | "TUI state is decomposed into widgets via the TUISTATE trait (see `docs/TUISTATE_TRAIT_DECOMPOSITION.md`), which keeps rendering logic testable headlessly." | The trait is `TuiState` (`crates/jcode-tui/src/tui/mod.rs:696`). The proposed sub-trait split in `docs/TUISTATE_TRAIT_DECOMPOSITION.md:3` has not been applied; the trait is now one flat interface of roughly 150 methods, and the document's method inventory is stale. | Reword: "TUI state is exposed to renderers through the `TuiState` trait (`crates/jcode-tui/src/tui/mod.rs`), a single wide read-only presentation interface that keeps rendering logic testable headlessly (`TestState` in `crates/jcode-tui/src/tui/ui_tests/mod.rs`). A planned split into composable sub-traits is described in `docs/TUISTATE_TRAIT_DECOMPOSITION.md`; that split has not been applied." |
| API Contracts | "Flags: `--swarm`, `--export`, `--video`, `--auto-edit`, `--timeline`, `--speed`, `--fps`." | `src/cli/args.rs:440-487` also defines `--cols` (default 120), `--rows` (default 40), and the mutually exclusive `--centered` and `--no-centered`. | Add the four missing flags. |
| Sequences | "Server sends ServerEvent (TextDelta, ToolUseStart/End, ...) over socket" | `crates/jcode-protocol/src/wire/events.rs` has `TextDelta` (`:120`) but the tool events are `ToolCall` (`:89`), `ToolStart` (`:161`), `ToolInput` (`:165`), `ToolExec` (`:173`), `ToolDone` (`:177`). There is no `ToolUseStart` or `ToolUseEnd`, and `ServerEvent` now has roughly 89 variants. | Reword the event list. |
| Technical Decisions | "TUISTATE decomposition \| trait-based widget state \| Headless testability (NFR-4)." | No decomposition has happened. | Reword to "Single `TuiState` presentation interface \| `crates/jcode-tui/src/tui/mod.rs` plus `TestState` in `ui_tests/mod.rs` \| Headless testability (NFR-4). A sub-trait split is planned but not applied." |

## Missing Information

- The Risks and Unknowns section lists only two items.
  Add: "3. Catalog, session-list and account-inventory loads run off the render thread; a refresh that lands after a newer request is discarded by request id, so a stale result may be silently dropped."
- The interactive inline prompt subsystem (`crates/jcode-tui/src/tui/ui_inline_interactive.rs`, `crates/jcode-tui/src/tui/app/inline_interactive/`) is a large TUI surface with no requirement or spec entry.
- The split view, diff pane, diagram pane, copy-selection, pinned layout, and workspace map surfaces are likewise not described.

## Implementability

No issues found beyond the corrections above.

## Reversibility

No issues found.

## Forward Compatibility

No issues found.

## Ambiguities

No issues found.

## Incoherences

No issues found.

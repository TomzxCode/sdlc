---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.
Five TUI behaviors shipped in that window are not covered by any requirement.

## Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-2 | "The system shall provide a session picker to browse and resume past sessions." | The picker now opens before the scan finishes and swaps the list in when the background scan lands (`crates/jcode-tui/src/tui/app/inline_interactive.rs:2651-2673,2728-2736,2821-2871`; regression test `crates/jcode-tui/src/tui/session_picker_tests.rs:103`). | "The system shall provide a session picker to browse and resume past sessions. The picker shall open immediately, showing the cached session list, and shall refresh from a background scan without blocking the UI or discarding the user's selection, scroll position, or search text." |
| FR-5 | "The system shall render side panels such as the session list and usage overlay." | The session list is a picker overlay and the usage card is a separate overlay. The TUI side panel is a multi-page markdown and PDF pane driven by the `panel` tool (`crates/jcode-side-panel-types/src/lib.rs:62-80`, `docs/PANELS.md`). | "The system shall render a side panel of session-scoped pages (markdown and PDF) and the picker overlays for sessions, accounts, login, and usage, and shall allow each side panel to be dismissed and toggled from the TUI." |
| FR-3 | "The system shall display info widgets (session info, model, provider, usage) in the UI." | The v0.99.0 startup account router and usage cards are not covered (`crates/jcode-tui/src/tui/ui_header/account_router.rs`, `crates/jcode-tui/src/tui/info_widget_usage.rs:222-262`). | "The system shall display info widgets (session info, model, provider, usage) in the UI, including a startup account row that lists saved accounts, cached quotas and available reset times, and usage cards with a responsive limit gauge and compact token totals. Account and quota inventory shall be gathered off the render thread." |
| FR-4 | "The system shall support configurable keybindings and display options (e.g. centered mode, message timestamps, theme detection)." | `speed_increase` and `speed_decrease` are first-class keybindings driving the Standard, Fast, and Ultrafast tier ladder (`crates/jcode-config-types/src/keybindings.rs:254-263`; defaults `alt+up` and `alt+down` in `crates/jcode-base/src/config/default_file.rs:49-50`). | "The system shall support configurable keybindings and display options (e.g. centered mode, message timestamps, theme detection, and speed-tier cycling hotkeys)." |

## Non-functional requirements

NFR-2 reads "RAM usage shall stay low; additional clients shall scale memory gracefully."
Extend it: "Idle sessions and idle clients shall release reloadable memory after a configurable idle period, report the measured RSS change, and wake transparently on the next interaction."
The server and agent half of hibernation is owned by FEAT-p19; this requirement covers the client notice and the measured RSS banner.

## Constraints

"Config via `[keybindings]` and `[display]` sections in `~/.jcode/config.toml`." understates the surface.
The TUI also reads `[features]` (mermaid, message timestamps) and `[session]` (hibernation).
Reword to: "Config via the `[keybindings]`, `[display]`, `[features]` and `[session]` sections in `~/.jcode/config.toml`."

## Completeness

Missing functional requirements for shipped capabilities:

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-10 | The system shall build the model picker catalog off the render thread so large remote catalogs do not stall the UI. | `crates/jcode-tui/src/tui/app/inline_interactive.rs:1519-1545` (start) and the poll path, `PendingModelPickerLoad` at `crates/jcode-tui/src/tui/app.rs:329-335`, `ModelPickerCacheSignature` at `:362-381`; tests in `crates/jcode-tui/src/tui/app/tests/model_picker_startup_tests.rs`. |
| FR-11 | The system shall keep startup headers and account rows on a single line at narrow terminal widths, truncating with an ellipsis. | `crates/jcode-tui/src/tui/ui_header.rs:15-35` (`fit_header_lines`), test `crates/jcode-tui/src/tui/ui_header.rs:1032`. |
| FR-12 | The system shall offer saved accounts in the login picker and allow reauthenticating a saved account from it. | `crates/jcode-tui/src/tui/app/auth_account_picker_saved_accounts.rs:5-65,69-98,138-179`, `crates/jcode-tui/src/tui/app/auth_account_add_replace.rs`. |
| FR-13 | The system shall show inline cache-miss diagnostics alongside cache reuse information. | `crates/jcode-tui/src/tui/info_widget.rs:1737-1757`, `crates/jcode-config-types/src/lib.rs:1217-1222` (`kv_cache_miss_notices`). |

## Testability

The acceptance criteria for FR-8 read "Then a guided walkthrough is shown".
The onboarding flow is multi-stage with a repair path, a rehearsal mode, and a state graph (`crates/jcode-tui/src/tui/app/onboarding_flow.rs`, `onboarding_repair.rs`, `onboarding_sim.rs`; `docs/ONBOARDING_STATE_GRAPH.md`; the `--onboarding-sim` flag at `src/cli/args.rs:91-94`).
Reword to: "Given a first-time user / When onboarding is enabled / Then a guided, resumable walkthrough is shown, and a rehearsal mode is available to replay the flow on an existing install."

## Feasibility

No issues found.

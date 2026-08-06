---
title: "Terminal UI"
status: done
---

# Test Plan: Terminal UI

## Scope

Covers session picker, info widgets, pinned UI state, mermaid rendering, and TUI serial/test harness behavior. Out of scope: live terminal interaction and image-protocol rendering on physical terminals.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Session picker behavior | `crates/jcode-tui/src/tui/session_picker_tests.rs` | Sessions listed and selected correctly |
| TC-2 | Info widget rendering | `crates/jcode-tui/src/tui/info_widget_*_tests.rs` | Widgets render expected content |
| TC-3 | Pinned UI state | `crates/jcode-tui/src/tui/ui_pinned_tests.rs` | Pinned elements behave as configured |
| TC-4 | Auth/account pickers | `crates/jcode-tui/src/tui/auth*_tests.rs` | Account pickers render and select correctly |
| TC-5 | TUI frame timing | `src/bin/tui_bench.rs` | Frame timing within budget |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Serial TUI lib tests in CI | Linux/macOS build matrix | TUI state tests pass headlessly |
| TC-7 | Desktop2 frame-budget parity | `crates/jcode-desktop2` profile tests | Shared render model stays within budget |
| TC-8 | Mermaid rendering acceptance | `docs/RENDER_PARITY_ACCEPTANCE_CRITERIA.md` checks | Diagram output matches acceptance criteria |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-9 | Terminal without kitty/sixel support | Image/Mermaid degrades to fallback rendering |
| TC-10 | Rapid streaming with many frames | Input line stays responsive (no visible lag) |
| TC-11 | Empty session list | Picker shows empty state without error |

## Test Infrastructure

- Headless TUI test harness via TUISTATE trait decomposition.
- Benchmark binaries (`tui_bench`, `mermaid_side_panel_probe`).
- CI serial TUI test cohort to avoid terminal flakiness.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-2 | TC-1, TC-11 |
| FR-3 | TC-2 |
| FR-6 | TC-8, TC-9 |
| NFR-1 | TC-5, TC-10 |
| NFR-4 | TC-6 |

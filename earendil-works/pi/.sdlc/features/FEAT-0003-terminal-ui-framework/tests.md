---
title: "Terminal UI Framework"
status: done
---

# Test Plan: Terminal UI Framework

## Scope

Covers `pi-tui` rendering pipeline, components, key handling, terminal abstraction, overlays, and differential rendering.

## Unit Tests

Test files under `packages/tui/test/` cover:
- Differential render engine (tui-render.test.ts, tui-shrink.test.ts, tui-cell-size-input.test.ts, tui-overlay-style-leak.test.ts)
- Editor component (editor.test.ts)
- Input handling (input.test.ts, keys.test.ts)
- Keybindings (keybindings.test.ts)
- Markdown rendering (markdown.test.ts)
- SelectList component (select-list.test.ts, truncated-text.test.ts)
- Overlay system (overlay-options.test.ts, overlay-short-content.test.ts, overlay-non-capturing.test.ts)
- Autocomplete (autocomplete.test.ts)
- Fuzzy matching (fuzzy.test.ts)
- Terminal abstraction (terminal.test.ts, terminal-colors.test.ts, terminal-image.test.ts)
- String utilities (truncate-to-width.test.ts, wrap-ansi.test.ts, tab-width.test.ts, word-navigation.test.ts)
- Stdin buffer (stdin-buffer.test.ts)
- Regression tests (regression-overlay-cjk-boundary.test.ts, regression-regional-indicator-width.test.ts, bug-regression-isimageline-startswith-bug.test.ts)

## Integration Tests

Terminal tests run against `VirtualTerminal` for deterministic render assertions without a real terminal.

## Edge Cases and Failure Scenarios

- CJK character boundary in overlays
- Regional indicator (flag) width
- Tab width handling
- Image protocol capability detection fallback
- Non-capturing overlay focus management
- Short overlay content positioning

## Test Infrastructure

- `VirtualTerminal` for headless render assertions
- Mock terminal color scheme (OSC 11)
- Kitty keyboard protocol negotiation simulation

## Coverage Matrix

| Requirement | Test Files |
|---|---|
| FR-01 (Component model) | editor.test.ts, input.test.ts, markdown.test.ts |
| FR-02 (TUI manager) | tui-render.test.ts |
| FR-03 (Differential rendering) | tui-render.test.ts |
| FR-04 (Synchronized output) | tui-render.test.ts |
| FR-05 (Frame throttling) | tui-render.test.ts |
| FR-06 (Built-in components) | editor.test.ts, markdown.test.ts, select-list.test.ts |
| FR-07 (Overlay system) | overlay-*.test.ts |
| FR-08 (Key handling) | keys.test.ts, keybindings.test.ts |
| FR-09 (Column-aware string utils) | truncate-to-width.test.ts, wrap-ansi.test.ts, tab-width.test.ts |
| FR-10 (Terminal interface) | terminal.test.ts |
| FR-11 (Terminal images) | terminal-image.test.ts |
| FR-12 (IME support) | (covered by tui-render cursor positioning) |
| FR-13 (Keybindings manager) | keybindings.test.ts |
| FR-15 (Fuzzy match/autocomplete) | fuzzy.test.ts, autocomplete.test.ts |
| NFR-01 (Width validation) | tui-render.test.ts |
| NFR-03 (SGR resets per line) | tui-render.test.ts |
| NFR-04 (Virtual terminal testing) | terminal.test.ts |

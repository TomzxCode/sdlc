---
title: "Mini Chat (Electron)"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test Plan: Mini Chat (Electron)

## Scope

This plan records the test files that currently cover the Electron mini chat feature.
It covers shortcut selection and conversion, shortcut conflicts, the mini chat app shell, shared session state, mini chat surface behavior, and app window command routing.
It does not claim coverage for saved mini chat bounds, edge docking, or independent operation, which have no tests in the current tree.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | `packages/electron/mini-chat-global-shortcut.test.mjs` verifies that single-chord combos convert to Electron accelerators. | Combos such as `mod+alt+n`, `shift+f2`, `alt+[`, and a four-modifier hyper key. | Converted accelerators such as `CommandOrControl+Alt+N` and `Alt+[`. |
| TC-2 | The same file rejects combos that cannot be registered globally. | Multi-chord, keyless, unknown, unassigned, and grabbing-modifier-free combos. | `null` from `convertShortcutComboToAccelerator`. |
| TC-3 | The same file normalizes stored combo values. | Padded, empty, unassigned, undefined, and numeric values. | A trimmed combo or `null`. |
| TC-4 | The same file selects the global shortcut action from window state. | A focused mini chat, unfocused mini chats with focus timestamps, no mini chat with a live renderer, and no windows at all. | `hide`, `focus` of the most recently focused mini chat, `open-draft`, or `reveal-main`. |
| TC-5 | `packages/ui/src/components/chat/composer/state/abortShortcutReach.test.ts` checks double Escape reach by surface. | `main` and `mini-chat` surfaces with keyboard and touch input. | The shortcut reaches the composer only with a keyboard on a wired surface. |
| TC-6 | `packages/ui/src/lib/shortcuts/schema.test.ts` checks that a desktop global combo conflict is reported as replaceable. | A `new_chat` binding of `mod+alt+m` with `mini_chat_global` set to the same combo. | A conflict of kind `exact` for the customizable `mini_chat_global` action. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | `packages/ui/src/apps/ElectronMiniChatApp.abort.test.tsx` mounts the real mini chat app under the sync provider. | A happy-dom window with a mini chat URL, stubbed fetch, and web APIs from `createWebAPIs`. | The app renders without a provider error and selects the session it opened on. |
| TC-8 | The same file drives double Escape in the mini chat composer while its session is running. | A typed draft, a busy session in the sync child store, and a stubbed interrupt endpoint. | The first Escape is consumed, the second sends one interrupt, and the draft stays typed. |
| TC-9 | `packages/ui/src/components/chat/message/SessionNoticeBlock.test.tsx` renders a pull request notice in the `mini-chat` chat surface. | A `ChatSurfaceProvider` in `mini-chat` mode and a pull request notice. | The link opens in the browser on click, with the browser's modified-click behavior preserved. |
| TC-10 | `packages/ui/src/components/chat/composer/ui/ComposerActionButtons.test.tsx` checks composer actions for a `mini-chat` surface with a running session and a draft. | `surface: 'mini-chat'`, `canAbort: true`, and `hasContent: true`. | The run stays stoppable with the draft kept, and only the Queue message button renders. |
| TC-11 | `packages/ui/src/lib/guests/navigation.test.ts` checks mini chat guest navigation. | `markMiniChatWindow` marks the current window as Mini Chat. | `openWalkthrough` returns `HOST_UNAVAILABLE` before the mark and `UNSUPPORTED` after it, and the base branch store stays empty. |
| TC-12 | `packages/electron/menu-copy-action.test.mjs` routes a copy command to the focused app window. | A main window and a mini chat window in the app window list. | Copy dispatches to the focused window, including the mini chat window. |
| TC-13 | `packages/electron/renderer-recovery.test.mjs` exercises renderer recovery with a mini chat label. | A fake window that emits a render-process-gone crash. | The window reloads, a safe start is recorded, and the warning payload reports the `mini chat` surface. |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-14 | No end-to-end test file exercises a live Electron mini chat window against a running server. | None. | No end-to-end coverage is recorded for this feature. |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-15 | A focused main window competes with an unfocused mini chat for the global shortcut. | The mini chat is focused rather than the main window. |
| TC-16 | Two mini chats share the same most recent focus time. | The first mini chat in the list is focused. |
| TC-17 | No mini chat exists but a renderer window is alive. | A draft opens. |
| TC-18 | No mini chat and no renderer window exist. | The main window is revealed. |
| TC-19 | Double Escape fires in a touch-only or unwired surface. | The abort shortcut does not reach the composer. |
| TC-20 | A modified click hits a pull request link in mini chat. | The browser keeps its own meaning for the click. |

## Test Infrastructure

- Node built-in `node:test` and `node:assert/strict` run the Electron `.test.mjs` files.
- Bun test runs the UI tests with `happy-dom`, React `act`, and `createRoot`.
- The Electron tests use fake windows, fake listeners, and direct calls into the shortcut, copy, and recovery helpers.
- The UI tests stub `fetch`, replace selected globals, and restore them after each test.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-12 and TC-13 treat the mini chat as an app window, with no test of always-on-top or compact layout. |
| FR-02 | No test covers saved mini chat position or size. |
| FR-03 | TC-7, TC-8, TC-9, TC-11, and TC-12 |
| FR-04 | TC-1, TC-2, TC-3, TC-4, TC-5, TC-6, TC-8, TC-10, TC-15, TC-16, TC-17, and TC-18 |
| FR-05 | No test covers edge docking. |
| FR-06 | TC-9, TC-10, and TC-11 |
| FR-07 | TC-13 covers mini chat renderer recovery only, with no test for the main window web server requirement. |
| FR-08 | TC-4, TC-15, TC-16, TC-17, and TC-18 cover multiple mini chats at the shortcut layer, with no tab-related test. |

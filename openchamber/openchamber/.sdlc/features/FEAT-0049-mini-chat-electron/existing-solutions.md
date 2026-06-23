---
issue: ""
title: "Mini Chat (Electron)"
status: draft
---

# Existing Solutions: Mini Chat (Electron)

## Overview

The codebase already has a substantial mini chat implementation. The Electron main process (`packages/electron/main.mjs`) has `createMiniChatWindow()`, `buildMiniChatUrl()`, IPC handlers for `desktop_open_session_mini_chat_window` and `desktop_open_draft_mini_chat_window`, and `BrowserWindow` management with session-to-window tracking via `miniChatWindowsBySession` Map. The UI (`packages/ui/src/components/mini-chat/MiniChatLayout.tsx`) has full header with session switcher, branch display, diff stats, context usage, pin/unpin button, and "open in main app" button. The chat surface uses `ChatSurfaceProvider` with `mode="mini-chat"` throughout the shared UI. The remaining gaps are: persistent window position and size (FR-02), screen-edge docking (FR-05), and keyboard shortcut toggle (FR-04).

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/electron/main.mjs` (createMiniChatWindow, buildMiniChatUrl, IPC handlers), `packages/ui/src/components/mini-chat/MiniChatLayout.tsx`, `packages/ui/src/components/layout/Header.tsx`, `packages/ui/src/components/session/sidebar/SessionNodeItem.tsx`, i18n strings, `consts.js`, `preload.mjs` |
| Open-source | Yes | QuickChat, ChatDock, Clippy AI, Gemini Wrapper, chat-box-overlay (all Electron-based mini chat implementations) |
| Commercial / SaaS | Yes | Slack's mini window, Discord popout chat, Notion Quick Find |
| Standards / protocols | No | N/A |
| Reference material | Yes | Electron BrowserWindow API (alwaysOnTop, setPosition, setSize, restore), Electron screen (getCursorScreenPoint, getDisplayNearestPoint), Tray API |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing OpenChamber mini chat | Internal | MIT | Mature | FR-01 (compact always-on-top), FR-03 (shared state), FR-06 (minimal UI), FR-07 (requires main window), FR-08 (one session per window) | FR-02 (persistent position/size), FR-04 (keyboard shortcut), FR-05 (docking) |
| QuickChat (reference) | Open-source | MIT | Mature | Global hotkey (Ctrl+Shift+Space), frameless always-on-top, auto-hide on focus loss, copy/clear shortcuts | Single-session only, no persistence, no shared state with main app |
| ChatDock (reference) | Open-source | MIT | Active | Global shortcut, system tray, model selector, streaming, background running | Agent-focused, not a simple mini chat, more complex architecture |
| Electron BrowserWindow API | API (Electron 41) | MIT | Mature | `alwaysOnTop`, `setPosition()`/`setSize()`/`getBounds()`, `screen.getCursorScreenPoint()`, `globalShortcut` registration | Low-level, requires manual state management |
| Electron `globalShortcut` | API | MIT | Mature | `globalShortcut.register()` for system-wide hotkeys | Main process only, must unregister on quit |

## Evaluation

### Existing OpenChamber Mini Chat

- **Strengths:** Already implements FR-01, FR-03, FR-06, FR-07, and FR-08. Full UI with session switcher, branch display, context usage, pin/unpin, "open in main app", and macOS traffic light support. Session-to-window tracking prevents duplicate windows for the same session. ChatSurfaceProvider with `mode="mini-chat"` is integrated throughout the shared UI, hiding non-relevant actions (fork, multi-run, project actions, etc.). Share state via the same Zustand stores and SSE pipeline as the main window.
- **Weaknesses:** Window geometry is not persisted (starts at 600x400 default position). No keyboard shortcut (must use header button or sidebar context menu). No screen-edge docking. No global shortcut (e.g., `Ctrl+Shift+Space` from any app).
- **Integration effort:** Low for FR-04 and FR-02. Medium for FR-05 (docking requires geometry tracking).
- **Cost:** None.
- **Risks:** None.

### QuickChat (Reference Pattern)

- **Strengthens:** Well-proven pattern for mini chat: global hotkey toggle, frameless window, always-on-top, auto-hide on focus loss. Clean UX with minimal chrome. Uses Electron's `globalShortcut` API.
- **Weaknesses:** Standalone app, no shared state with a main application. No window position persistence. No multi-session support.
- **Integration effort:** Not applicable (reference only). The global shortkey pattern using `globalShortcut.register('Ctrl+Shift+Space', ...)` is directly applicable.
- **Cost:** N/A.
- **Risks:** N/A.

### Electron BrowserWindow API (Window Management)

- **Strengths:** `getBounds()`/`setBounds()` for position/size persistence. `screen.getCursorScreenPoint()` and `screen.getDisplayNearestPoint()` for docking detection. `globalShortcut.register()` for keyboard shortcut. `win.setAlwaysOnTop(true)` (already set in the existing implementation). `BrowserWindow.on('move')` and `BrowserWindow.on('resize')` for tracking geometry changes.
- **Weaknesses:** Manual implementation required. No built-in docking behavior.
- **Integration effort:** Low. Add `saveBounds()`/`restoreBounds()` using Electron's `settings` module. Register `globalShortcut` on app ready. Add move/resize event listeners.
- **Cost:** None.
- **Risks:** None.

## Recommendation

**Direction:** Adopt and extend

The existing mini chat implementation already covers FR-01, FR-03, FR-06, FR-07, and FR-08. Remaining work:
- FR-02 (persistent position/size): Save `BrowserWindow.getBounds()` to Electron's `settings` store on move/resize; restore on creation. Existing `createBrowserWindow` in `main.mjs` already has a `restoreGeometry` parameter as a pattern to follow.
- FR-04 (keyboard shortcut): Register `globalShortcut.register('Ctrl+Shift+Space', () => toggleMiniChat())` in main process. Unregister on `app.will-quit`.
- FR-05 (docking): Track `BrowserWindow.on('move')` positions relative to display bounds; snap to edge within a threshold. This is the lowest priority and may be deferred.

The QuickChat and ChatDock projects validate the global hotkey + always-on-top pattern. OpenChamber's implementation is already more sophisticated (shared state, session management, multi-window).

## Sources of Information

- Existing `packages/electron/main.mjs` lines 1547-1619: `buildMiniChatUrl()` and `createMiniChatWindow()`
- Existing `packages/ui/src/components/mini-chat/MiniChatLayout.tsx`: full mini chat UI component
- Electron BrowserWindow: `https://electronjs.org/docs/latest/api/browser-window`
- Electron globalShortcut: `https://electronjs.org/docs/latest/api/global-shortcut`
- QuickChat: `https://github.com/shaltielshmid/QuickChat`
- ChatDock: `https://github.com/abhaymundhara/ChatDock`

## Open Questions

1. Should the keyboard shortcut be configurable in the Settings UI, or hardcoded as `Ctrl+Shift+Space`?
2. Should window position be persisted per-screen (to handle multi-monitor setups) or globally?
3. For docking: snap to edges of the current display, or allow custom anchor positions?

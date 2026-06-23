---
issue: ""
title: "Open In External Apps"
status: draft
---

# Existing Solutions: "Open In" External Apps

## Overview

A comprehensive solution for opening project directories in external applications already exists in the codebase. `packages/ui/src/lib/openInApps.ts` defines a catalog of 23 apps, `packages/ui/src/stores/useOpenInAppsStore.ts` manages detection and selection, `packages/ui/src/components/desktop/OpenInAppButton.tsx` renders the UI, and `packages/electron/main.mjs` implements the OS-level launch logic for both macOS and Windows via `desktop_open_in_app` IPC. The recommended direction is to document and refine the existing implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `openInApp`, `OPEN_IN_APPS`, `useOpenInAppsStore`, `OpenInAppButton`, `desktop_open_in_app`, `shell.openPath`, `shell.openExternal` |
| Open-source | Yes | npm libraries for cross-platform app launching, `electron` shell API |
| Commercial / SaaS | No | N/A |
| Standards / protocols | No | N/A |
| Reference material | Yes | Electron `shell.openPath` / `shell.openExternal` docs, Tauri `shell` plugin docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal implementation | Internal | MIT | Production | FR-01, FR-02 (23 apps), FR-03, FR-04, FR-05 | FR-07 (global preference storage in localStorage, not server-side) |
| Electron `shell.openExternal` | API | MIT | Mature | FR-01, FR-03 (partially) | Does not detect installed apps; no catalog |
| Tauri `desktop_open_in_app` (Rust) | API | MIT | Maintenance-only | FR-01, FR-03 | Legacy path only; no new features |
| Custom `open` npm package (`sindresorhus/open`) | Library | MIT | Mature | FR-01 | No detection or catalog; raw system open |

## Evaluation

### Existing internal implementation

- **Strengths:** Already production-ready. `packages/ui/src/lib/openInApps.ts` defines 23 apps (Finder, Terminal, iTerm2, Ghostty, VS Code, IntelliJ, Cursor, Zed, Xcode, etc.) matching the FR-02 requirement. `useOpenInAppsStore` at `packages/ui/src/stores/useOpenInAppsStore.ts:1-283` handles: installed app detection via `fetchDesktopInstalledApps`, retry logic with exponential backoff (3 attempts), caching with TTL, event-driven refresh on `openchamber:installed-apps-updated`, fallback to always-available apps (Finder, Terminal). `OpenInAppButton` at `packages/ui/src/components/desktop/OpenInAppButton.tsx:1-213` renders the dropdown UI with app icons (loaded dynamically from the system or fallback data URLs), selection state, copy path action. Electron `main.mjs:2416-2481` implements `desktop_open_in_app`, `desktop_open_file_in_app`, `desktop_filter_installed_apps`, `desktop_fetch_app_icons`, and `desktop_get_installed_apps` IPC handlers with macOS bundle detection and Windows registry-based detection. Tauri has equivalent handlers in `packages/desktop/src-tauri/src/main.rs:777`. The preference is stored in localStorage per FR-07 constraint.
- **Weaknesses:** Detection only works on Electron and Tauri (desktop shells). Web/PWA users cannot detect installed apps (expected, since `open in app` is a desktop-only feature). The app catalog is hardcoded per FR-06 (no custom apps). Some Electron-only apps (e.g., Windsurf, Kiro, Antigravity) use custom detection that may be fragile on different macOS versions.
- **Integration effort:** Low. The system is already wired through `FilesView.tsx` (line 2759), `OpenInAppButton` (used in header), and the shared UI layer via `lib/desktop.ts`.
- **Cost:** Free (MIT, existing code).
- **Risks:** Windows support in `desktop_open_in_app` is newly added (hardcoded app-specific `open` commands may need maintenance). Only macOS and Windows are supported per `packages/electron/main.mjs:2426-2428`.

### Electron shell.openExternal / shell.openPath

- **Strengths:** Native OS file opening. Works for any app registered for a file/URL scheme.
- **Weaknesses:** `shell.openExternal` opens URLs, not apps. `shell.openPath` opens files/folders in the default app, not a specific chosen app. Neither provides app detection or a catalog.
- **Integration effort:** N/A (used internally by the existing implementation as fallback).
- **Cost:** Free (built into Electron).
- **Risks:** None.

## Recommendation

**Direction:** Adopt and extend (refine existing implementation)

The existing implementation satisfies all functional requirements. No new libraries are needed. The remaining work is:
- Verify all 23 apps from the catalog are launchable on macOS (particularly niche ones like Kiro, Antigravity, Trae)
- Ensure the preference storage in localStorage persists across worktree switches (FR-07)
- Confirm the `OpenInAppButton` is accessible from both the header and file viewer (FR-05)
- The app catalog is already fixed at 23 apps per FR-06; no customization is needed

## Sources of Information

- `packages/ui/src/lib/openInApps.ts:1-56` — 23-app catalog definition
- `packages/ui/src/stores/useOpenInAppsStore.ts:1-283` — detection, caching, and selection state management
- `packages/ui/src/components/desktop/OpenInAppButton.tsx:1-213` — UI dropdown with icons
- `packages/electron/main.mjs:2400-2500` — Electron IPC handlers for app launch and detection
- `packages/desktop/src-tauri/src/main.rs:777-885` — Tauri Rust handler (legacy)
- `packages/ui/src/lib/desktop.ts:682` — `openDesktopProjectInApp` wrapper
- `packages/ui/src/components/views/FilesView.tsx:2759` — Open In button in file viewer

## Open Questions

1. Does each of the 23 app entries have a working launch specification for both macOS .app bundle detection and Windows executable path?
2. Should the `OpenInAppButton` also appear in the directory explorer dialog (`DirectoryExplorerDialog.tsx`)?
3. How should the system handle the case where a user's preferred app is not installed (graceful fallback or visible warning)?

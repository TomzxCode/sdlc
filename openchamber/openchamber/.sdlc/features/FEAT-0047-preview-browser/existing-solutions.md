---
issue: ""
title: "Preview & Embedded Browser"
status: draft
---

# Existing Solutions: Preview & Embedded Browser

## Overview

The codebase already has a comprehensive preview system including a proxy middleware (`packages/web/server/lib/preview/proxy-runtime.js`) that handles URL rewriting, WebSocket forwarding, bridge script injection, and resource noise filtering. The UI (`ContextPanel.tsx`) provides an iframe preview with a URL bar, reload button, external open action, inspect mode with element highlighting, and a console overlay with filter/copy/attach capabilities. Dev server auto-detection (`packages/ui/src/lib/detectDevServer.ts`) works across project actions and package.json scripts. The remaining gaps are: full Electron `WebContentsView`-based browser tab with navigation chrome, annotation screenshot capture, and console log attachment to sessions.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/preview/proxy-runtime.js`, `proxy-runtime.test.js`, `packages/ui/src/lib/detectDevServer.ts`, `packages/ui/src/components/layout/ContextPanel.tsx`, `packages/ui/src/lib/preview/screenshot-capture.ts`, `packages/electron/main.mjs`, i18n strings for dev server |
| Open-source | Yes | `http-proxy-middleware` (already a dependency), Electron `WebContentsView` API, `BrowserView` (deprecated), `electron webview` tag |
| Commercial / SaaS | No | N/A |
| Standards / protocols | Yes | iframe sandbox restrictions, WebSocket upgrade protocol, Content Security Policy |
| Reference material | Yes | Electron web embeds docs, Electron `WebContentsView` API, `BrowserView` deprecation notice, Chromium out-of-process iframes |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing iframe preview + proxy | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-07, FR-10 | FR-08 (no full Electron browser tab), FR-09 (no annotation screenshots) |
| Electron WebContentsView | API (Electron 41) | MIT | Mature | FR-08: full embedded browser tab with navigation, DevTools | Main process only, requires IPC coordination |
| Electron webview tag | Tag | MIT | Maintenance (deprecated in favor of WebContentsView) | FR-08: full embedded browser in renderer | Chromium architectural changes, stability concerns |
| Electron BrowserView | API | MIT | Deprecated (replaced by WebContentsView) | FR-08 | Deprecated in Electron 41, use WebContentsView |
| Existing proxy-runtime.js | Internal | MIT | Mature | FR-01 through FR-05, FR-10 | Server-side only, no Electron-specific features |

## Evaluation

### Existing iframe Preview + Proxy

- **Strengths:** Already implements FR-01 (iframe), FR-02 (URL bar + reload + external open), FR-03 (URL rewriting + WebSocket proxy with `ws: true`), FR-04 (console overlay with filter/copy/attach), FR-07 (auto-detect from project actions and `package.json` scripts), FR-10 (script name pattern matching: `dev`, `start`, `preview`, `serve`, `develop`). Sandboxed iframe with `allow-scripts allow-same-origin allow-forms` for loopback, stricter sandbox for external URLs. Bridge script injection (`openchamber-preview-bridge`) for console capture, URL navigation, and inspect mode. URL rewriting handles Vite HMR, webpack-dev-server, and other framework-specific paths.
- **Weaknesses:** iframes cannot access DevTools, cannot load pages with `X-Frame-Options: DENY`, cannot handle certain CSP configurations. No Electron-specific full browser tab.
- **Integration effort:** None (already integrated).
- **Cost:** None.
- **Risks:** None.

### Electron WebContentsView

- **Strengths:** The forward path for embedded web content in Electron 41+. Provides `webContents` API for DevTools, navigation events, URL bar updates, page load progress. Separate renderer process with configurable `webPreferences`. `setBounds()` for positioning within the `BrowserWindow`. `webContents.loadURL()` for navigation. `webContents.openDevTools()` for debugger access. Event-based URL change tracking via `did-navigate` and `page-title-updated`.
- **Weaknesses:** Requires main process coordination (cannot be rendered inside the React tree like a DOM element). Position/size must be managed imperatively via IPC. Multiple `WebContentsView` instances require manual z-ordering.
- **Integration effort:** Medium. Add a new IPC handler in `packages/electron/main.mjs` to create/manage/destroy `WebContentsView` instances. Add a React component in the UI that requests a `WebContentsView` by ID and sends resize/navigation commands via IPC.
- **Cost:** None (built into Electron).
- **Risks:** `WebContentsView` is newer than `BrowserView` and may have edge cases around keyboard focus and window management. Test thoroughly on macOS.

### Electron webview Tag

- **Strengths:** Declarative, works in renderer process with `webviewTag: true` in `webPreferences`. Has its own IPC channel (`ipcRenderer.sendToHost`). Supports `devtools` and navigation events.
- **Weaknesses:** Electron docs recommend against it for new development due to Chromium architectural changes. Stability concerns. The `webview` tag is an out-of-process iframe with async communication overhead.
- **Integration effort:** Low. Enable `webviewTag: true` in the Electron BrowserWindow webPreferences and add `<webview>` tags to the mini-chat HTML.
- **Cost:** None.
- **Risks:** Electron explicitly recommends `iframe` or `WebContentsView` instead. Future Electron versions may remove it.

## Recommendation

**Direction:** Adopt and extend

The existing iframe + proxy approach already satisfies FR-01 through FR-07 and FR-10. For the Electron-specific FR-08 (full embedded browser tab), use `WebContentsView` from the main process, managed via IPC from the renderer. This aligns with Electron 41's recommended path and avoids the deprecated `BrowserView` and the unstable `webview` tag.

For FR-09 (annotation screenshots), the existing `packages/ui/src/lib/preview/screenshot-capture.ts` already has `renderPreviewScreenshot()` which captures iframe content via `html2canvas`-like pixel extraction. Extend this for the `WebContentsView` by capturing via `webContents.capturePage()`.

## Sources of Information

- Electron `WebContentsView`: `https://electronjs.org/docs/latest/api/web-contents-view`
- Electron `BrowserView` (deprecated): `https://electronjs.org/docs/latest/api/browser-view`
- Electron `webview` tag: `http://www.electronproject.org/webview-tag.html`
- Electron web embeds guide: `https://electronjs.org/docs/latest/tutorial/web-embeds`
- Existing `packages/web/server/lib/preview/proxy-runtime.js`: 1400 lines of proxy middleware, bridge script, URL rewriting, resource noise filtering
- Existing `packages/ui/src/lib/detectDevServer.ts`: dev server auto-detection from project actions and `package.json` script patterns
- Existing `packages/ui/src/lib/preview/screenshot-capture.ts`: screenshots via pixel extraction and `capturePage()`

## Open Questions

1. Should the full Electron browser tab be a separate `BrowserWindow` (like a popup) or embedded as a `WebContentsView` inside the main window's side panel?
2. Does the `WebContentsView` integration need to share cookies/session with the main Electron window, or should it be isolated?
3. Should annotation screenshots be stored locally or attached to the chat session as file references?

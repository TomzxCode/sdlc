---
issue: ""
title: "Electron Desktop App"
status: draft
---

# Existing Solutions: Electron Desktop App

## Overview

The Electron desktop app at `packages/electron/` is already the primary desktop runtime for OpenChamber. It boots the web server in-process via `startWebUiServer`, loads the UI from `http://127.0.0.1:<port>`, and provides native integrations including macOS menu, deep-links, SSH remote connections, auto-update via `electron-updater`, Mini Chat windows, multi-window support, and a preload shim for Tauri backward compatibility. The architecture matches the requirements closely — the forward path is refinement and gap-filling, not rebuilding.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/electron/main.mjs` (3298 lines), `preload.mjs`, `ssh-manager.mjs`, `package.json`, `scripts/`, `resources/` |
| Open-source | Yes | Electron 41, electron-updater, electron-context-menu, other Electron distributions (VS Code, Slack, Discord, Figma) |
| Commercial / SaaS | No | Electron is an open-source framework |
| Standards / protocols | No | Deep-link protocol `openchamber://` |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| **Electron** (already adopted) | Framework | MIT | Mature (v41, 2025) | All FRs — foundation | Platform-specific work for Windows/Linux |
| **electron-updater** (already adopted) | Library | MIT | Mature (v6.8) | FR-03 | Requires GitHub releases; notarization needed for macOS |
| **electron-context-menu** (already adopted) | Library | MIT | Mature (v4.1) | Native context menus | — |
| **Tauri v2** (legacy, being replaced) | Framework | Apache-2.0 / MIT | Mature | Same UI via sidecar | Sidecar process model, smaller ecosystem, migration target |
| **ssh2** (via ssh-manager.mjs) | Internal | MIT (custom) | Production (1249 lines) | FR-06 | Uses native `ssh` command via spawn, not Node.js ssh2 library |

## Evaluation

### Electron (already adopted)

- **Strengths:** Battle-tested framework used by VS Code, Slack, Discord, Figma, WhatsApp Desktop. Full OS integration: native menus, notifications, taskbar, deep-links, file dialogs, window management. Hardened runtime + notarization support for macOS. Large plugin ecosystem (electron-builder, electron-updater, electron-context-menu, electron-log). Electron 41 supports modern Chromium, improved performance, and Wayland on Linux.
- **Weaknesses:** Larger bundle size than Tauri (bundles Chromium). Higher memory usage. Windows/Linux support on roadmap (FR-11) — current focus is macOS.
- **Integration effort:** Low — already implemented. The main.mjs (3298 lines) covers server bootstrap, window management, IPC, menu, deep-links, SSH, auto-update, and notifications.
- **Cost:** MIT license, free. macOS notarization requires Apple Developer Program ($99/year).
- **Risks:** Minimal. Electron is well-maintained by the OpenJS Foundation. The Tauri-to-Electron migration (FR-12) is already documented in `docs/TAURI_TO_ELECTRON_CUTOVER.md`.

### electron-updater (already adopted)

- **Strengths:** Auto-update with GitHub releases, differential updates, staged rollouts, signing verification. Integrated with electron-builder.
- **Weaknesses:** Requires manual release publishing flow.
- **Integration effort:** Low — already configured in `main.mjs`.
- **Cost:** MIT, free.
- **Risks:** Low.

### SSH via ssh-manager.mjs (custom implementation)

- **Strengths:** Uses native `ssh` command via `spawn` with control sockets, connection multiplexing, config file parsing (`Include` directives, glob expansion), local port forwarding, SOCKS5 proxy, health monitoring, automatic reconnection (up to 5 attempts), status events. 1249 lines of production code.
- **Weaknesses:** Relies on OpenSSH being installed on the system (standard on macOS/Linux, requires optional install on Windows). Uses process spawning rather than an embedded library like `ssh2`.
- **Integration effort:** Already implemented and wired in `main.mjs`.
- **Cost:** MIT, free.
- **Risks:** Windows SSH availability. Works well on macOS.

## Recommendation

**Direction:** Adopt (existing solution)

The Electron desktop app is already the primary runtime. All requirements FR-01 through FR-12 are either implemented or have clear paths. The focus should be on:
- Filling remaining gaps (Windows/Linux builds, workspace-first startup flow)
- Hardening existing features (Mini Chat window state management, deep-link routing)
- Completing the Tauri-to-Electron migration cutover documented in `docs/TAURI_TO_ELECTRON_CUTOVER.md`
- Adding window state persistence (NFR-03)

## Sources of Information

- `packages/electron/main.mjs` — full implementation (3298 lines) covering bootstrap, menu, windows, IPC, deep-links, SSH, auto-update.
- `packages/electron/preload.mjs` — IPC shim exposing `__TAURI__` compat layer to renderer.
- `packages/electron/ssh-manager.mjs` — SSH connection manager (1249 lines).
- `packages/electron/package.json` — electron 41.2.1, electron-updater 6.8.3, electron-context-menu 4.1.2.
- `docs/TAURI_TO_ELECTRON_CUTOVER.md` — migration plan.
- `packages/web/server/index.js` — `startWebUiServer` export consumed by Electron.

## Open Questions

1. Windows and Linux builds are FR-11 (May). What is the target timeline? Electron 41 supports Windows x64/arm64 and Linux x64/arm64 natively.
2. Window state persistence (NFR-03): should this use `electron-store` or a simple JSON file in `userData`? The current codebase does not use `electron-store`.
3. Should the SSH manager also support a Node.js `ssh2` library fallback for environments without OpenSSH? Currently it requires `ssh` on PATH.

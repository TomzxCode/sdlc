---
issue: ""
title: "Notifications & Updates"
status: draft
---

# Existing Solutions: Notifications & Updates

## Overview

OpenChamber already has a complete notifications and update infrastructure. The server-side `packages/web/server/lib/notifications/` module handles web push (VAPID), desktop notification emission, cross-tab session activity tracking, notification templates with truncation, and push subscription persistence. Electron desktop notifications flow via the `onDesktopNotification` callback. VS Code notifications use the extension host's `vscode.window.showInformationMessage`. In-app update checks are not yet implemented. The existing `web-push` library (v3.6.7) is mature but newer alternatives like `@pushforge/builder` and `node-webpush` offer zero-dependency, edge-runtime-compatible implementations.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/notifications/`, `packages/web/server/index.js`, `packages/web/package.json` (web-push dep), `packages/electron/main.mjs`, `packages/vscode/src/extension.ts` |
| Open-source | Yes | `web-push`, `@pushforge/builder`, `node-webpush`, `@mmmike/web-push`, `next-push`, `electron-updater` |
| Commercial / SaaS | No | OneSignal, Firebase Cloud Messaging exist but out of scope |
| Standards / protocols | Yes | Web Push (RFC 8030), VAPID (RFC 8292), Message Encryption (RFC 8291), W3C Push API, Electron autoUpdater API |
| Reference material | Yes | Electron update docs, web-push docs, electron-updater docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber built-in notifications | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-06, FR-07, FR-09, FR-11, NFR-02, NFR-03 | FR-05 (in-app update checks), FR-08 (disable update notifications), FR-10 (PWA web push) |
| `web-push` v3.6.7 | Library | MPL-2.0 | Mature | VAPID key generation, payload encryption, send notification | Node.js only, 5 dependencies, last publish Jan 2024 |
| `@pushforge/builder` | Library | MIT | Active | Zero-dependency, Cloudflare Workers, Deno, Bun | Newer library (2025), smaller ecosystem |
| `node-webpush` | Library | Apache-2.0 | Active | Zero-dependency, TypeScript-first, RFC 8291/8292 | Single maintainer, smaller community |
| `electron-updater` | Library | MIT | Mature | Auto-update with electron-builder, checkForUpdatesAndNotify | Electron-specific, does not handle in-app OpenCode updates |
| Electron autoUpdater | Built-in | MIT | Mature | Squirrel-based auto-update, `update-downloaded` event | Low-level, no notification UI |

## Evaluation

### OpenChamber built-in notifications

- **Strengths:** Full-featured notification system with push subscription CRUD, VAPID key management, session activity tracking, visibility state, cross-tab coordination via SSE, notification text truncation, desktop notification emission for Electron and stdout, and VS Code native notification support. Push subscriptions persist to disk with 10-per-token limit (NFR-03). Duplicate suppression across panels (NFR-01) is handled.
- **Weaknesses:** In-app OpenCode update checks (FR-05) are not implemented. No dismissible update or PWA install prompt (FR-06). No setting to disable update notifications (FR-08). Web push for PWA background (FR-10) is not implemented in the service worker.
- **Integration effort:** Low (already integrated).
- **Cost:** None.
- **Risks:** None.

### `web-push` (current dependency)

- **Strengths:** 5.2M weekly downloads, 3.5K GitHub stars, supports all browsers, battle-tested.
- **Weaknesses:** 5 dependencies, Node.js-only, last published Jan 2024, MPL-2.0 license, no TypeScript types natively.
- **Integration effort:** Low (already used).
- **Cost:** None.
- **Risks:** Maintenance has slowed; if issues arise, migration to `@pushforge/builder` or `node-webpush` is possible.

### `electron-updater` (for Electron desktop updates)

- **Strengths:** Official companion to electron-builder, supports GitHub releases, generic S3, and other providers, emits `update-available` and `update-downloaded` events, built-in notification dialog support.
- **Weaknesses:** Only handles Electron app updates, not OpenCode CLI updates. Requires `electron-builder` publish config.
- **Integration effort:** Medium (requires configuring publish provider in electron-builder config and wiring `electron-updater` into `main.mjs`).
- **Cost:** None (MIT).
- **Risks:** None.

## Recommendation

**Direction: Adopt and extend**

Keep the existing notification system and `web-push` library. Extend with:
- In-app OpenCode update checks (FR-05) by fetching the latest version from GitHub releases or npm and comparing against the installed version.
- Dismissible update and PWA install prompts (FR-06) with dismissal state persisted to settings.
- Setting to disable update notifications (FR-08).
- Web push for PWA background notifications (FR-10) by implementing `push` event handler in the service worker at `packages/web/src/sw.ts`.
- If `web-push` maintenance becomes a problem, migrate to `@pushforge/builder` (zero dependency, edge-compatible) or `node-webpush` (TypeScript-first, RFC compliant).

## Sources of Information

- `push-runtime.js` at `packages/web/server/lib/notifications/push-runtime.js` - VAPID key management, subscription CRUD
- `routes.js` at `packages/web/server/lib/notifications/routes.js` - push subscription, visibility, session activity endpoints
- `runtime.js` at `packages/web/server/lib/notifications/runtime.js` - event-driven notification trigger fanout
- `emitter-runtime.js` at `packages/web/server/lib/notifications/emitter-runtime.js` - desktop/stdout + SSE emission
- `message.js` at `packages/web/server/lib/notifications/message.js` - text truncation helpers
- Electron autoUpdater docs at `electronjs.org/docs/latest/api/auto-updater`
- `electron-updater` at `electron.build/auto-update`

## Open Questions

1. Should OpenCode update checks poll the npm registry, GitHub releases API, or use the OpenCode CLI's own version command?
2. How should the PWA push service worker be registered and updated to support web push (FR-10)?
3. Should dismissed update prompts be tracked per-version (don't show again for vX.Y.Z) or universally (don't show any updates)?

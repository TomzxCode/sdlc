---
issue: ""
title: "PWA Support"
status: draft
---

# Existing Solutions: PWA Support

## Overview

The codebase already has a comprehensive PWA implementation using `vite-plugin-pwa` with `injectManifest` strategy. The service worker handles push notifications (`packages/web/src/sw.ts`), the manifest is dynamically generated (`pwa-manifest-routes.js`), and React hooks cover display mode detection, install prompt management, manifest sync, window controls overlay, and visibility beacons. The recommended direction is to adopt the existing implementation as-is and address remaining gaps (full requirement coverage audit).

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/src/sw.ts`, `packages/ui/src/lib/pwa.ts`, `packages/ui/src/hooks/usePwa*.ts`, `packages/web/server/lib/opencode/pwa-manifest-routes.js`, `packages/web/vite.config.ts` |
| Open-source | Yes | `vite-plugin-pwa` on npm, `workbox` strategies |
| Commercial / SaaS | Yes | Push notification vendor libraries |
| Standards / protocols | Yes | W3C Web App Manifest, Service Worker API, Push API, display-mode media queries |
| Reference material | Yes | `vite-plugin-pwa` docs, `workbox` docs, Chrome PWA guides |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| vite-plugin-pwa + injectManifest (current) | Library | MIT | Mature | SW setup, manifest injection, precaching | Out of scope: push notification server integration |
| Workbox (bundled via vite-plugin-pwa) | Library | MIT | Mature | Runtime caching, precaching, navigation routes | FR-02 requires custom push handler (already implemented in sw.ts) |
| Custom service worker (current sw.ts) | Internal | MIT | Active | Push notifications, notification click routing | FR-08 cached-shell offline mode not yet validated |
| `usePwaDetection.ts` | Internal | MIT | Active | FR-04 display mode detection | None |
| `usePwaInstallPrompt.ts` | Internal | MIT | Active | FR-03 install prompt with dismissible toast | None |
| `usePwaManifestSync.ts` | Internal | MIT | Active | FR-05 dynamic manifest shortcuts | None |
| `pwa-manifest-routes.js` | Internal | MIT | Active | Dynamic manifest with orientation, shortcuts | None |
| `useWindowControlsOverlayLayout.ts` | Internal | MIT | Active | FR-06 window controls overlay layout | None |
| `usePushVisibilityBeacon.ts` | Internal | MIT | Active | FR-02 notification suppression when visible | None |

## Evaluation

### vite-plugin-pwa

- **Strengths:** Zero-config PWA for Vite; handles service worker generation, manifest injection, and precaching. Already integrated and working.
- **Weaknesses:** Push notifications are out of scope; requires custom SW code. `injectManifest` strategy requires manual SW authoring.
- **Integration effort:** Low - already fully integrated in `packages/web/vite.config.ts:42-60`
- **Cost:** Free (MIT)
- **Risks:** Low; well-maintained library with active community

### Custom service worker (sw.ts)

- **Strengths:** Minimal, iOS-safe (IIFE bundle). Handles push, notification click, install, activate. No Workbox runtime dependencies reducing fragility.
- **Weaknesses:** Does not implement runtime caching strategies; only precaches via Workbox build injection. No offline fallback for API routes.
- **Integration effort:** Already in place at `packages/web/src/sw.ts`
- **Cost:** Free (MIT)
- **Risks:** iOS Safari PWA fragility documented in code comments

### PWA detection and manifest hooks

- **Strengths:** `usePwaDetection.ts` correctly handles display-mode media queries, iOS `navigator.standalone`, and TWA (Trusted Web Activity). `pwa-manifest-routes.js` dynamically generates manifest with user configurable app name, orientation, and recent session shortcuts.
- **Weaknesses:** Dynamic manifest re-fetch on shortcut change relies on a global window function `__OPENCHAMBER_UPDATE_PWA_MANIFEST__` that is set by `pwa-manifest-routes.js`.
- **Integration effort:** Already in place
- **Cost:** Free
- **Risks:** None identified

## Recommendation

**Direction:** Adopt and extend

The existing PWA implementation covers the key requirements:
- FR-01: Service worker via `vite-plugin-pwa` with `injectManifest` (`packages/web/vite.config.ts:42-60`)
- FR-02: Push notification handling in `packages/web/src/sw.ts:36-71` with visibility-based suppression via `usePushVisibilityBeacon.ts`
- FR-03: Install prompt toast in `usePwaInstallPrompt.ts` with local storage dismissed state
- FR-04: Display mode detection in `usePwaDetection.ts` + `packages/ui/src/lib/pwa.ts`
- FR-05: Dynamic manifest shortcuts in `usePwaManifestSync.ts` + `pwa-manifest-routes.js`
- FR-06: Window controls overlay in `useWindowControlsOverlayLayout.ts`
- FR-07: Configurable orientation handled in `pwa-manifest-routes.js` with `normalizePwaOrientation`

Gaps to address: FR-08 (cached-shell offline mode) should be verified. The injectManifest strategy with `globPatterns: ['**/*.{js,css,html,ico,png,svg,woff,woff2,ttf,otf,eot}']` in `vite.config.ts:50` should precache the shell, but offline behavior needs explicit testing and may need a navigation route fallback.

## Sources of Information

- vite-plugin-pwa docs for injectManifest strategy: https://github.com/vite-pwa/vite-plugin-pwa
- Workbox injectManifest: https://developer.chrome.com/docs/workbox/modules/workbox-build/#injectmanifest
- Web App Manifest spec: https://www.w3.org/TR/appmanifest/
- Push API spec: https://www.w3.org/TR/push-api/

## Open Questions

1. Does the current `injectManifest` glob pattern precache all assets needed for cached-shell offline mode (FR-08)?
2. Should push notification subscription be managed client-side (web-push VAPID) or server-side integrated with OpenCode server events?
3. Does the window-controls-overlay CSS adaptation handle both macOS and Windows title bar layouts?

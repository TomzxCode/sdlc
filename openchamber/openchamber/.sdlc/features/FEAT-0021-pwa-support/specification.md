---
title: "PWA Support"
status: draft
---

# Specification: PWA Support

## Overview

PWA infrastructure includes a service worker (`packages/web/src/sw.ts`), PWA detection hooks (`usePwaDetection.ts`), install prompt management (`usePwaInstallPrompt.ts`), manifest sync (`usePwaManifestSync.ts`), and window controls overlay layout (`useWindowControlsOverlayLayout.ts`). Built with `vite-plugin-pwa`.

## Architecture

```
Service Worker (packages/web/src/sw.ts)
    +---> Push notification handling
    +---> Notification click routing to session
    |
PWA Hooks (packages/ui/src/hooks/)
    +---> usePwaDetection (display mode detection)
    +---> usePwaInstallPrompt (install toast, dismissed state)
    +---> usePwaManifestSync (dynamic shortcuts)
    +---> useWindowControlsOverlayLayout
    |
Visibility Beacon (usePushVisibilityBeacon.ts)
    Signals server about focus state for notification suppression
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Service worker | vite-plugin-pwa | Standard PWA tooling for Vite; handles manifest and SW generation |
| Install prompt | Dismissible with persisted state | Prevents annoying repeated install prompts |
| Visibility beacon | Signal server about focus | Server suppresses redundant push when app is visible |

## Out of Scope

- Full offline mode (requires server connection for OpenCode)
- Background sync for queued messages

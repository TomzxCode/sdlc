---
title: "Mobile UI & Touch Gestures"
status: done
---

# Specification: Mobile UI & Touch Gestures

## Overview

Mobile adaptation uses dedicated hooks (`useDrawerSwipe.ts`, `useEdgeSwipe.ts`, `useVisualViewport.ts`, `useLongPress.ts`) and mobile-specific components (`MobileOverlayPanel.tsx`, `MobileAgentButton.tsx`, `MobileModelButton.tsx`, `MobileSessionStatusBar.tsx`). Keyboard handling uses `mobileKeyboardMode.ts`.

## Architecture

```
Mobile-specific hooks (packages/ui/src/hooks/)
    +---> useDrawerSwipe (swipe-to-dismiss panels)
    +---> useEdgeSwipe (edge gesture for session switcher)
    +---> useVisualViewport (keyboard-aware viewport)
    +---> useLongPress (context menu trigger)
    |
Mobile components (packages/ui/src/components/)
    +---> MobileOverlayPanel (full-screen dialog overlays)
    +---> MobileAgentButton / MobileModelButton (touch-optimized selectors)
    +---> MobileSessionStatusBar (compact session info)
    |
mobileKeyboardMode.ts (resize vs overlay preference)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Viewport | visualViewport API over legacy hacks | Modern, reliable keyboard detection |
| Gestures | Custom hooks (not a gesture library) | Lightweight; only the specific gestures needed |

## Out of Scope

- Native mobile app (React Native / Flutter)
- Split-screen multitasking support

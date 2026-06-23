---
issue: ""
title: "Mobile UI & Touch Gestures"
status: draft
---

# Existing Solutions: Mobile UI & Touch Gestures

## Overview

The codebase already has a comprehensive mobile adaptation layer using custom React hooks (no gesture library). `useLongPress.ts`, `useEdgeSwipe.ts`, `useDrawerSwipe.ts`, `useVisualViewport.ts`, `mobileKeyboardMode.ts`, and `mobile.css` provide the core functionality. Mobile detection uses pointer type and viewport width (768px breakpoint). The recommended direction is to adopt the existing custom-hook approach and validate coverage of all requirements.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/hooks/useLongPress.ts`, `useEdgeSwipe.ts`, `useDrawerSwipe.ts`, `useVisualViewport.ts`, `mobileKeyboardMode.ts`, `mobile.css`, `chat/mobileControlsUtils.ts` |
| Open-source | Yes | `@use-gesture/react`, `react-use-gesture`, `react-swipeable`, `framer-motion` gestures |
| Commercial / SaaS | No | |
| Standards / protocols | Yes | W3C Pointer Events, Touch Events, `visualViewport` API |
| Reference material | Yes | MDN touch events, pointer events, `visualViewport` |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Custom hooks (current) | Internal | MIT | Active | FR-03 edge-swipe, long-press, swipe-to-dismiss, FR-02 visual viewport, FR-05 keyboard mode | FR-08 web-standard gesture APIs |
| @use-gesture/react | Library | MIT | Mature | Unified pointer/touch/mouse gesture handling | Adds dependency; Framer Motion already in project |
| react-swipeable | Library | MIT | Mature | Swipe detection only | Limited to swipe; no long-press |
| framer-motion gestures | Library | MIT | Mature | Drag, swipe, pan with spring animations | `motion` is already used in DrawerSwipe (`animate` import) |

## Evaluation

### Custom hooks (current approach)

- **Strengths:** Lightweight, no extra dependency. Each hook is focused on one gesture. `useEdgeSwipe.ts` uses document-level touch event listeners with passive:true/false for performance. `useLongPress.ts` correctly prevents context menu, provides haptic feedback via `navigator.vibrate`, and cancels on drag >10px. `useDrawerSwipe.ts` integrates with `framer-motion`'s `animate` for spring-physics smooth transitions. `useVisualViewport.ts` uses the standard `visualViewport` API with RAF coalescing. `mobileKeyboardMode.ts` handles resize-content vs native viewport modes.
- **Weaknesses:** No gesture conflict resolution. `useEdgeSwipe` uses passive:true for touchstart but passive:false for touchmove (needed for `preventDefault`), which may cause scroll performance issues. Drawer swipe and edge swipe may conflict.
- **Integration effort:** Already fully implemented
- **Cost:** Free
- **Risks:** Low; custom hooks are well-structured

### @use-gesture/react

- **Strengths:** Unified gesture API (drag, pinch, scroll, wheel, move, hover). Framer Motion integration. Handles gesture conflict resolution. Good TypeScript support.
- **Weaknesses:** Adds ~5KB to bundle. The existing custom hooks cover the exact needed gestures; @use-gesture's broader API is unused. Project already uses `motion` from `framer-motion` directly.
- **Integration effort:** Medium - would replace custom hooks
- **Cost:** Free (MIT)
- **Risks:** Low; well-maintained library with 5K+ stars

### mobile.css (current)

- **Strengths:** Comprehensive CSS adaptation layer (511 lines). Covers safe areas (`env(safe-area-inset-*)`), iOS PWA standalone mode, touch target sizing (min 36px), typography scaling, scroll containers, viewport height fixes (`-webkit-fill-available`), home indicator blur gradient. Uses `@media (display-mode: standalone)` queries for PWA adaptation.
- **Weaknesses:** Uses `!important` extensively for typography overrides. Some iOS-specific selectors are duplicated in both `@supports (-webkit-touch-callout: none)` and the fallback `@supports not` blocks (lines 225-381).
- **Integration effort:** Already in use
- **Cost:** Free
- **Risks:** Low; CSS-only concerns

### Mobile UI components (spec referenced)

- **Strengths:** Modular component architecture planned per `packages/ui/src/lib/i18n/messages/en.ts` + spec. MobileOverlayPanel, MobileAgentButton, MobileModelButton, MobileSessionStatusBar.
- **Weaknesses:** Some components may not be fully implemented yet; need verification.
- **Integration effort:** Partial; completion work needed
- **Cost:** Free
- **Risks:** Low

## Recommendation

**Direction:** Adopt and extend

The existing custom hook approach is the right choice per the specification's decision: "Custom hooks (not a gesture library) — Lightweight; only the specific gestures needed" (`specification.md:34`).

Requirement coverage assessment:
- FR-01: Mobile chat controls - `packages/ui/src/components/chat/mobileControlsUtils.ts` exists; `MobileAgentButton`/`MobileModelButton` in spec
- FR-02: Visual viewport handling - `useVisualViewport.ts` with RAF coalescing; `mobile.css` typography/scroll adjustments at lines 163-195
- FR-03: Touch gestures - `useEdgeSwipe.ts` (session switcher), `useLongPress.ts` (context menu, 500ms delay, 10px drag cancel), `useDrawerSwipe.ts` (panel dismiss with spring animation via framer-motion)
- FR-04: Mobile overlay panels - `pwa-dialog-content` CSS in `mobile.css` lines 385-458; MobileOverlayPanel in spec
- FR-05: Keyboard mode preference - `mobileKeyboardMode.ts` with resize-content vs native mode, localStorage persistence, `<meta>` viewport updates
- FR-06: Mobile session status bar - `MobileSessionStatusBar` in spec
- FR-07: Touch target sizing - `mobile.css` lines 81-102 (36px min for buttons, inputs, selects)
- FR-08: Web-standard APIs - hooks use PointerEvent, TouchEvent, visualViewport; no platform branching
- FR-09: Configurable PWA orientation - handled in `pwa-manifest-routes.js` with `normalizePwaOrientation`

Minor optimizations: UseResizeObserver could replace RAF coalescing for `useVisualViewport` in certain cases. The `!important` usage in `mobile.css` should be reviewed. Gesture conflict resolution between edge-swipe and drawer-swipe needs validation.

## Sources of Information

- `visualViewport` API: https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport
- Pointer Events spec: https://www.w3.org/TR/pointerevents/
- Touch Events spec: https://www.w3.org/TR/touch-events/
- `@use-gesture/react`: https://github.com/pmndrs/use-gesture
- Safe area env variables: https://developer.mozilla.org/en-US/docs/Web/CSS/env

## Open Questions

1. Does `useEdgeSwipe` conflict with `useDrawerSwipe` when the user starts a swipe from the left edge?
2. Are the `!important` typography overrides in `mobile.css` still needed after the theme system migration?
3. Should MobileAgentButton, MobileModelButton, and MobileSessionStatusBar be implemented as mobile-specific variants or responsive versions of the existing components?
4. Does the `window-controls-overlay` display mode interact correctly with the mobile CSS layout?

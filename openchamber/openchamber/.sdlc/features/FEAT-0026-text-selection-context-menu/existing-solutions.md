---
issue: ""
title: "Text Selection Context Menu"
status: draft
---

# Existing Solutions: Text Selection Context Menu

## Overview

The codebase already uses Radix UI `DropdownMenu` for file-tree context menus and `navigator.clipboard` for copy actions, but no floating text-selection popup exists for chat messages. The recommended direction is to build a lightweight floating menu using the existing Base UI Popover or Floating UI primitives, positioned via `getSelection()` coordinates, with four fixed actions (copy, add to notes, ask AI, add as todo).

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `context.?menu`, `getSelection`, `selectedText`, `DropdownMenu`, `navigator.clipboard` across `packages/ui/src` |
| Open-source | Yes | Floating UI, `@floating-ui/react`, `react-float-menu`, `@omsimos/react-highlight-popover`, `@floating-ui/react` context menu patterns |
| Commercial / SaaS | No | N/A (standard browser feature, no SaaS product needed) |
| Standards / protocols | Yes | `Selection API` (MDN), `Pointer Events`, `Touch Events` |
| Reference material | Yes | Floating UI docs for context menu positioning, CodeSandbox examples |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Base UI Popover (already in deps) | Library | MIT | Mature | FR-01, FR-03 | Not designed for selection-anchored popup; needs manual position logic |
| `@floating-ui/react` (not in deps) | Library | MIT | Mature | FR-01, FR-03, FR-04 | Not in project; would add dependency |
| `@omsimos/react-highlight-popover` | Library | MIT | Active | FR-01, FR-03, FR-04 | Lightweight zero-dep; covers floating on selection well |
| Custom built-in approach (Radix DropdownMenu positioned via selection rect) | Internal | MIT | N/A | FR-01, FR-02, FR-03, FR-06 | Must handle mobile touch, scroll, resize edge cases |
| `react-float-menu` | Library | MIT | Stale (4yr) | FR-01, FR-03 | Unmaintained; no selection-anchoring |

## Evaluation

### Base UI Popover (existing dep)

- **Strengths:** Already in `package.json` (`@base-ui/react`). Provides Popover.Positioner with anchor alignment. No new dependency.
- **Weaknesses:** Not designed for text-selection anchoring; needs manual `getSelection().getRangeAt(0).getBoundingClientRect()` as the anchor reference. Base UI anchor expects an element ref, not a dynamic rect.
- **Integration effort:** Medium. Requires a wrapper that converts selection rects to a virtual anchor element pattern.
- **Cost:** Free (MIT).
- **Risks:** Base UI may not support virtual/anchorless positioning cleanly. Workaround needed.

### Floating UI (@floating-ui/react)

- **Strengths:** Designed for floating elements anchored to arbitrary rects. Has explicit `FloatingFocusManager`, `useRole`, and `useDismiss` for context menus. Large community (32k stars).
- **Weaknesses:** Not in `package.json`. Adds ~20KB to bundle.
- **Integration effort:** Medium. Well-documented context menu example. Straightforward to integrate.
- **Cost:** Free (MIT).
- **Risks:** Already using Base UI for other components; adding Floating UI introduces a second positioning library.

### Custom built-in (no new deps)

- **Strengths:** Zero new dependencies. Full control. Uses existing Radix DropdownMenu or Base UI Popover with manual positioning via CSS `position: fixed` and selection rect.
- **Weaknesses:** Must handle: scroll position updates, resize, mobile touch dismissal, `selectionchange` event cleanup, re-anchoring when content changes. Higher implementation effort.
- **Integration effort:** High. Edge cases are numerous (overlapping menus, iframes, shadow DOM, multi-window).
- **Cost:** Free (MIT).
- **Risks:** Prone to positioning bugs in edge cases. Native `contextmenu` event suppression needed for mobile.

## Recommendation

**Direction:** Build

Use the existing Base UI Popover with a virtual anchor pattern that adapts the selection rect on `selectionchange` and `scroll` events. If Base UI proves inadequate for virtual anchoring, add `@floating-ui/react` as a focused dependency.

Rationale: The feature is small (4 fixed actions in a popup) and does not justify the overhead of a new library unless the existing positioning stack cannot support it. The codebase already has Radix DropdownMenu patterns in `packages/ui/src/components/views/FilesView.tsx` and `packages/ui/src/components/layout/SidebarFilesTree.tsx` that can serve as reference. The copy-to-clipboard helper already exists in `packages/ui/src/lib/clipboard.ts`.

## Sources of Information

- Floating UI context menu example: <https://codesandbox.io/s/trusting-rui-2duieo>
- Selection API: <https://developer.mozilla.org/en-US/docs/Web/API/Selection>
- `react-highlight-popover`: <https://github.com/omsimos/react-highlight-popover>
- i18n keys for copy and selection already exist in `packages/ui/src/lib/i18n/messages/en.ts` at lines 2199, 1445

## Open Questions

1. Should the menu appear on `mouseup` (desktop) and `touchend` (mobile) or on a dedicated selection handle button?
2. How should the "Add to notes" action create the note, and what is the project notes storage mechanism?
3. Should the "Ask AI about this" action insert the selection into the composer as context or send it as an immediate prompt?
4. How should the floating menu interact with the existing code-block-level copy button in `MarkdownRendererImpl.tsx`?

---
issue: ""
title: "Session Pinning & Multi-Select"
status: draft
---

# Existing Solutions: Session Pinning & Multi-Select

## Overview

OpenChamber already has session pinning via `useSessionPinnedStore` (Zustand + localStorage persistence) with a pin icon in the session list, pinned-first sorting, and PINNED i18n keys. A `BulkActionBar` component exists with delete, archive, move-to-folder, and remove-from-folder actions. However, the multi-select infrastructure is incomplete — the i18n keys for bulk actions exist across all 8 locales, but the UI pattern for entering selection mode (shift-click range selection, checkbox toggle) and the full bulk action flow need completion. No external library is needed; the remaining work is plumbing the selection state into the session list.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/stores/useSessionPinnedStore.ts`, `packages/ui/src/components/session/sidebar/BulkActionBar.tsx`, `packages/ui/src/components/session/sidebar/SessionNodeItem.tsx`, i18n bulk action keys, `packages/ui/src/components/session/SessionSidebar.tsx` |
| Open-source | Yes | @dnd-kit (already used for sorting), TanStack Table (react-table), react-beautiful-dnd |
| Commercial / SaaS | No | |
| Standards / protocols | No | |
| Reference material | No | |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| **useSessionPinnedStore** (already built) | Internal | MIT (codebase) | Production | FR-01, FR-05, FR-07 | No UI for pin/unpin from context menu? Already has context menu entries |
| **BulkActionBar** (already built) | Internal | MIT (codebase) | Production | FR-04 | Requires selection state upstream — not wired to session list |
| **@dnd-kit** (already used) | Library | MIT | Mature | Not directly relevant | Could support drag-to-reorder pinned sessions |
| **TanStack Table / react-table** | Library | MIT | Mature | Multi-select, shift-click range | Heavy for a list — not aligned with current DOM-based session rendering |

## Evaluation

### useSessionPinnedStore (already built)

- **Strengths:** Zustand store with localStorage persistence (SESSION_PINNED_STORAGE_KEY = `oc.sessions.pinned`), Set-based ID tracking, `toggle(sessionId)` action, `compareSessionsByPinnedAndTime` utility in `utils.tsx`. Pinned sessions appear first in every sorted list via `compareSessionsByPinnedAndTime`. Pin/unpin context menu items exist with i18n keys. Pin icon (`pushpin`) rendered in `SessionNodeItem.tsx:563`.
- **Weaknesses:** Persisted to localStorage — not sync'd across devices, not stored on the server. This matches the requirement (localStorage).
- **Integration effort:** Low — already wired in `SessionSidebar.tsx`, `SessionGroupSection.tsx`, `useSwitcherItems.ts`, `useSessionGrouping.ts`.
- **Cost:** MIT, free.
- **Risks:** No limit enforcement (FR-07 requires unlimited). Current Set-based storage works for any number; no cap exists.

### BulkActionBar (already built)

- **Strengths:** Displays selected count, move-to-folder dropdown (with existing folder list, new folder creation, remove from folder), delete/archive button, done button. Uses Base UI DropdownMenu for folder selection. Properly handles archived bucket (shows Delete instead of Archive). Accessible with aria-labels.
- **Weaknesses:** Currently only used for folder-scoped selection. The upstream selection state management (which sessions are selected, enter/exit selection mode, shift-click range logic) is not yet connected to the session list.
- **Integration effort:** Medium — needs a selection mode state (likely in Zustand), wire checkbox clicks and shift-click range detection in the session list, and connect selection to the BulkActionBar's delete/archive actions.
- **Cost:** MIT, free.
- **Risks:** None. The component is already tested in production for folder operations.

## Recommendation

**Direction:** Adopt and extend

Both pinning and bulk actions have existing implementations that cover the core requirements. The gaps are:
1. **Selection mode UX:** Add a selection state to the session list (could be a new Zustand slice or local state in `SessionSidebar`). Implement shift-click range selection by tracking last-clicked index.
2. **Checkbox multi-select:** Add a checkbox column to session nodes when in selection mode. The existing `BulkActionBar` handles the actions once items are selected.
3. **Wire actions:** Connect `archiveSessions` / `deleteSessions` from `useSessionUIStore` to the BulkActionBar's `onDelete` callback.

No external libraries are needed. The existing Zustand stores, sorting utilities, and BulkActionBar component provide everything required.

## Sources of Information

- `packages/ui/src/stores/useSessionPinnedStore.ts` — pin store with localStorage persistence.
- `packages/ui/src/components/session/sidebar/BulkActionBar.tsx` — bulk action bar component (131 lines).
- `packages/ui/src/components/session/sidebar/SessionNodeItem.tsx:338,563` — pin icon rendering and isPinnedSession check.
- `packages/ui/src/components/session/sidebar/utils.tsx:130-151` — `compareSessionsByPinnedAndTime` utility.
- `packages/ui/src/components/session/SessionSidebar.tsx:88` — SESSION_PINNED_STORAGE_KEY definition.
- i18n keys for pinning and bulk actions across all 8 locale files under `packages/ui/src/lib/i18n/messages/`.
- `packages/ui/src/sync/session-ui-store.ts:950-958` — `archiveSessions` and `deleteSessions` bulk action implementations.

## Open Questions

1. Should selection mode be modal (enter via a button/long-press) or transient (checkboxes always visible)? Current i18n keys reference "exit selection" suggesting a modal approach.
2. Should pinned sessions support drag-to-reorder within the pinned section? The codebase already uses @dnd-kit for folder sorting. This could use the drag-to-reorder skill pattern.
3. Should batch pin/unpin be available in bulk actions? Not in current requirements but a natural extension.

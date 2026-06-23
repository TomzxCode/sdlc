---
issue: ""
title: "Timeline / Undo / Redo"
status: draft
---

# Existing Solutions: Timeline / Undo / Redo

## Overview

OpenChamber already has a TimelineDialog component with full-text search, revert-to-message, fork-from-message, and keyboard turn navigation. Undo/redo is partially implemented via `revertToMessage` with a `skipRedoPush` option in the session-ui-store. The remaining gaps are: a persistent redo stack (currently a single-level flag), unbounded undo depth, deferred/staged rendering for large histories, and full-text search within the existing dialog. The recommendation is to adopt `zundo` for Zustand undo/redo middleware and extend the existing TimelineDialog.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | packages/ui/src/components/chat/TimelineDialog.tsx; session-ui-store.ts (revertToMessage, forkFromMessage); session-actions.ts; i18n strings for timeline/undo/redo |
| Open-source | Yes | npm for Zustand undo/redo middleware, React timeline/virtual-scroll libraries |
| Commercial / SaaS | No | Not applicable |
| Standards / protocols | No | Custom domain |
| Reference material | Yes | zundo, zustand-travel, react-window, TanStack Virtual |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal implementation | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06 | FR-07 (deferred rendering), FR-08 (unbounded depth) |
| zundo (zustand undo/redo middleware) | Library | MIT | Mature (2.3.0, 872 stars) | FR-04, FR-08 | FR-01, FR-02, FR-03, FR-05, FR-06, FR-07 — only undo/redo mechanics |
| zustand-travel (patch-based undo/redo) | Library | MIT | Active (1.0.0, 29 stars) | FR-04, FR-08 | Same as zundo, plus heavier deps (mutative, travels) |
| TanStack Virtual | Library | MIT | Mature | FR-07 (virtual scrolling) | No undo/redo, no timeline UI |
| react-window | Library | MIT | Mature | FR-07 | Same as TanStack Virtual |

## Evaluation

### Existing Internal Implementation

- **Strengths:** Fully functional TimelineDialog with search, revert, fork, keyboard navigation, relative timestamps, i18n translations across 7 locales. Undo/redo works as a single-level operation (revert pushes to redo, redo restores).
- **Weaknesses:** Redo stack is not persisted as an array — `skipRedoPush` flag works but is a single slot. No explicit undo/redo depth limit but also no formal stack management. TimelineDialog shows all messages without virtualization.
- **Integration effort:** Low — enhancements are additive to existing components and store actions
- **Cost:** Already maintained
- **Risks:** None — code is stable and production-used

### zundo

- **Strengths:** Lightweight (<700 bytes), zero dependencies, works as Zustand middleware, supports partialize/limit/equality/diff options, pause/resume tracking, unlimited history depth, works with Zustand v5
- **Weaknesses:** Only provides the undo/redo history mechanism — no UI, no timeline display, no search, no fork
- **Integration effort:** Low — wrap the session UI store's temporal state with zundo middleware, then wire undo/redo buttons
- **Cost:** Free
- **Risks:** Minimal — popular (267K weekly downloads), well-maintained

### TanStack Virtual

- **Strengths:** Headless virtualization, 60fps with 10,000+ items, React adapter, small bundle (10-15kb)
- **Weaknesses:** No undo/redo, no timeline UI — just virtual scrolling
- **Integration effort:** Low — can be added to TimelineDialog for deferred rendering of large histories
- **Cost:** Free
- **Risks:** None — mature library

## Recommendation

**Direction:** Adopt and extend

Adopt `zundo` as Zustand middleware for the undo/redo stack mechanics (replaces the current single-slot `skipRedoPush` pattern with a proper history stack). Extend the existing TimelineDialog with TanStack Virtual for deferred rendering. The timeline revert, fork, search, and keyboard navigation already exist and need only polish for unbounded undo (zundo handles this naturally).

## Sources of Information

- `packages/ui/src/components/chat/TimelineDialog.tsx`: Existing timeline with search, revert, fork, keyboard nav
- `packages/ui/src/sync/session-ui-store.ts`: Lines 977-1077 — revertToMessage and forkFromMessage actions
- `packages/ui/src/sync/session-actions.ts`: Lines 578-793 — actual revert/fork server calls
- `zundo` on npm: <https://www.npmjs.com/package/zundo> — Zustand undo/redo middleware
- `zustand-travel` on npm: <https://github.com/mutativejs/zustand-travel> — Patch-based alternative
- `TanStack Virtual`: <https://tanstack.com/virtual/latest> — Headless virtual scrolling

## Open Questions

1. Should the undo/redo stack be scoped to a single session or global across all sessions?
2. Should zundo's `partialize` filter out non-message state (scroll position, selectedModel) from undo history?
3. Is TanStack Virtual needed or is the typical session length (<500 messages) small enough for naive rendering?

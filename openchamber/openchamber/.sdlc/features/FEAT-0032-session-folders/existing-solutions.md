---
issue: ""
title: "Session Folders"
status: draft
---

# Existing Solutions: Session Folders

## Overview

Session folders are a UI-only feature — sessions already exist in the OpenCode backend, and folders are a client-side organizational layer. The codebase already has a complete session folders implementation in `useSessionFoldersStore` with create/rename/delete/drag-and-drop reorder/collapse-expand. The i18n keys confirm all operations (new folder, rename, delete with confirmation, move to folder, remove from folder, nested subfolders, empty folder state) are already translated. The gap is FR-06 (auto-cleanup of folders when all sessions are deleted). The recommended direction is to extend the existing implementation. For the drag-and-drop tree, the codebase already uses `@dnd-kit` infrastructure, so using it for folder reorder is consistent.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/stores/useSessionFoldersStore.ts`, i18n keys in all 10 languages showing full folder operations (new, rename, delete with confirmation, move, remove, nested, expand/collapse, empty state), `packages/ui/src/components/session/sidebar/`, `packages/ui/src/components/session/` |
| Open-source | Yes | npm search for React tree/sortable libraries with drag-and-drop, nested hierarchy, collapsible |
| Commercial / SaaS | No | Not applicable (IDE feature) |
| Standards / protocols | No | No standard for session folder organization |
| Reference material | Yes | VS Code session/workspace organization patterns, linear.app folder model |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber's existing session folders (internal) | Internal | MIT | Production (v1.11.7) | FR-01 (create), FR-02 (nested), FR-03 (drag-reorder), FR-04 (rename/delete), FR-05 (collapse/expand) | FR-06 (auto-cleanup on session delete) |
| Arborix (arborix on npm) | Library | MIT | Active (v2.1) | Headless React tree with drag-drop, virtualization, inline editing, keyboard nav, checkboxes | Heavy (15 dependencies), opinionated compound component API, session folders is simpler than full file tree |
| @headless-tree/react | Library | MIT | Mature (v1.7, 149K weekly downloads) | Headless tree with drag-drop, keyboard nav, search, renaming, async data, virtualization support | No opinions on session-specific state; zero dependencies is plus |
| react-tree-x (fork of react-arborist) | Library | MIT | Active | Full tree view with DnD, inline rename, virtualization, keyboard nav, tree filtering | Heavy (react-arborist fork), built for file explorer use cases |
| @clevertask/react-sortable-tree | Library | MIT | Active (v0.0.14) | dnd-kit based sortable tree with collapsible items, drop indicator, auto-expand on hover | Early stage (v0.x), focused on custom rendering, no virtualization yet |
| @nosferatu500/react-sortable-tree | Library | MIT | Mature (v5.0, 33K weekly) | Drag-drop sortable tree with virtualization, react-dnd based | Uses react-dnd (not dnd-kit which codebase already uses), requires separate CSS |
| dnd-block-tree | Library | MIT | Active (v2.x) | Headless dnd-kit based tree for hierarchical drag-drop interfaces | Headless only, requires building all UI; SSR compatible |

## Evaluation

### OpenChamber's existing session folders (internal)

- **Strengths:** Fully implemented for all core operations. Store has create, rename, delete, move to folder, drag reorder, nested subfolders, collapse/expand. Complete i18n in 10 languages. Uses existing `@dnd-kit` infrastructure for drag-and-drop. Tightly integrated with session state.
- **Weaknesses:** FR-06 (auto-cleanup when sessions are deleted) is the only gap — must detect when the last session in a folder is removed and either delete the folder or mark it as orphaned.
- **Integration effort:** Low — just add the auto-cleanup hook.
- **Cost:** None (MIT, in-house).
- **Risks:** None significant.

### Arborix / @headless-tree/react / dnd-block-tree

- **Strengths:** Provide complete tree management with drag-drop, indentation, expansion/collapse. Could theoretically replace a hand-rolled tree.
- **Weaknesses:** The session folders feature is not a file tree — folders contain sessions, not files. These libraries are optimized for tree-of-files patterns. The existing implementation already works with `@dnd-kit` and Zustand; adopting an external tree library would add complexity without clear benefit. Session folders have their own state shape (folderName, sessions array, subfolders, expanded state) that doesn't map cleanly to generic tree item types.
- **Integration effort:** High — would require replacing store logic and UI components already in production.
- **Cost:** Free (MIT).
- **Risks:** Abandonment risk for smaller libraries. Breaking changes between versions.

## Recommendation

**Direction:** Adopt and extend (add FR-06 to existing implementation)

The existing `useSessionFoldersStore` is production-ready for FR-01 through FR-05. The only gap is FR-06 (auto-cleanup of folders when sessions are deleted). This requires adding a reactive check in the store or in the sync event handler that detects when a folder's session list becomes empty and removes it. The drag-and-drop infrastructure (`@dnd-kit`) is already used elsewhere in the codebase (sidebar project reorder), so folder DnD is consistent. No external library is needed.

## Sources of Information

- `packages/ui/src/stores/useSessionFoldersStore.ts`: Complete store with folder CRUD, DnD state, collapse/expand, and i18n integration.
- i18n keys across 10 languages (en, pl, uk, ko, pt-BR, es, zh-CN, zh-TW, etc.): Confirm all folder operations are already translated.
- Arborix (`github.com/wesleyxmns/Arborix`): Reference for tree utility functions (sort, filter, flatten, find by ID) that could inform the folder store helpers if refactored.
- VS Code's workspace storage model: Sessions map to files on disk; folders organize them. OpenChamber sessions are in-memory objects stored by the server, so folders are a presentation-only layer.

## Open Questions

1. Should auto-cleanup (FR-06) happen eagerly (on every session delete event) or lazily (when the folder list is rendered)? Eager is cleaner UX but requires the sync event pipeline to check folder emptiness on every session eviction.
2. Should empty folders with subfolders that are non-empty be preserved? The requirements say "folders whose sessions are all deleted are cleaned up" — ambiguous about whether subfolder contents count.

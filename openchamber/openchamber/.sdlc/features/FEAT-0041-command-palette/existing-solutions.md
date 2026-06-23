---
issue: ""
title: "Command Palette"
status: draft
---

# Existing Solutions: Command Palette

## Overview

OpenChamber already has a production command palette built on `cmdk` (v1.1.1) and `fuse.js` (v7.1.0). It supports session switching, file search via the server API, settings navigation, action commands (new session, toggle sidebar/terminal), and keyboard shortcuts via the existing shortcut system. The remaining work is incremental: adding git branch switching and refining the existing implementation. There is no need to adopt a new library.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/components/ui/CommandPalette.tsx`, `packages/ui/src/lib/search/fuzzySearch.ts`, `packages/ui/src/lib/shortcuts.ts`, `packages/ui/src/hooks/useKeyboardShortcuts.ts`, `packages/ui/src/stores/useUIStore.ts` |
| Open-source | Yes | cmdk (npm), fuse.js (npm), kbar, react-cmdk, react-command-palette |
| Commercial / SaaS | No | Command palettes are a UI pattern, not a SaaS category |
| Standards / protocols | No | No applicable standards |
| Reference material | Yes | cmdk docs, fuzzy search patterns |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| **cmdk** (already adopted) | Library | MIT | Mature (12k+ stars, v1.1.1, React 19 compatible) | FR-01, FR-06, FR-07, FR-08 | Fuzzy search is basic; needs fuse.js augmentation |
| **fuse.js** (already adopted) | Library | Apache-2.0 | Mature (20k+ stars, v7.1.0, zero-dependency) | NFR-01 (fuzzy search perf) | Standalone — not a palette UI |
| **kbar** | Library | MIT | Stale (no updates since 2023, ~5k stars) | FR-01, FR-06, FR-07, FR-08 | Unmaintained, no React 19 support, larger bundle than cmdk |
| **react-cmdk** | Library | MIT | Stale (last update 2022) | FR-01, FR-07 | Pre-styled (hard to theme), no fuzzy search, stale |
| **react-command-palette** | Library | MIT | Stale | FR-01 | Single-component API, hard to compose with custom data sources |

## Evaluation

### cmdk (already adopted)

- **Strengths:** Composable API, accessible (WAI-ARIA), built-in keyboard navigation, Dialog integration, Tailwind-friendly, React 19 compatible, small bundle (~15KB gzipped), 38M weekly downloads.
- **Weaknesses:** Built-in filtering is basic (uses `command-score`); for rich fuzzy search on server-side results, `shouldFilter={false}` + `fuse.js` is the right pattern (already used).
- **Integration effort:** Low — already imported and wired in `CommandPalette.tsx`. Adding git branch search is just another `CommandGroup`.
- **Cost:** MIT license, free.
- **Risks:** Maintainer (pacocoursey) is reliable, project is actively maintained.

### fuse.js (already adopted)

- **Strengths:** Zero-dependency, tiny bundle (~8KB gzipped for full build), configurable threshold/field weights, TypeScript types included. Codebase already has `scoreByFuzzyQuery` wrapper in `packages/ui/src/lib/search/fuzzySearch.ts`.
- **Weaknesses:** Purely client-side — not suitable for full-text search on large file trees (server-side file search already handles that).
- **Integration effort:** Low — already used for session/command/settings scoring in the palette.
- **Cost:** Apache-2.0, free.
- **Risks:** None. Very mature library (since 2013).

### kbar

- **Strengths:** Built-in keyboard shortcut registration, virtualized lists for large datasets, multi-platform.
- **Weaknesses:** Repository archived / inactive since late 2023, no React 19 compatibility confirmed, larger bundle than cmdk (~17KB gzipped).
- **Integration effort:** High — replacing the entire existing implementation.
- **Risks:** Unmaintained. Not recommended.

## Recommendation

**Direction:** Adopt and extend

The codebase already has cmdk and fuse.js as dependencies with a working command palette covering FR-01 through FR-08 except FR-04 (git branch switching). The existing architecture — `CommandPalette.tsx` with lazy data fetching, `useKeyboardShortcuts.ts` for activation, and `useUIStore` state management — is sound. Adding git branch search requires adding a new `CommandGroup` sourced from `useGitAllBranches()` and wiring branch-switch actions.

## Sources of Information

- `packages/ui/src/components/ui/CommandPalette.tsx` — full existing palette with sessions, files, commands, settings.
- `packages/ui/src/lib/search/fuzzySearch.ts` — existing `scoreByFuzzyQuery` wrapper used by palette.
- `packages/ui/src/lib/shortcuts.ts` — shortcut definitions including `open_command_palette`.
- `packages/ui/src/hooks/useKeyboardShortcuts.ts` — keyboard shortcut handler already opens palette.
- `packages/ui/src/stores/useUIStore.ts:518,654-655,1386-1391` — palette state and toggle actions.
- `packages/ui/src/stores/useGitStore.ts:1018` — `useGitAllBranches` hook available for branch data.
- cmdk docs: <https://github.com/pacocoursey/cmdk>
- fuse.js docs: <https://fusejs.io>

## Open Questions

1. Should git branch switching within the palette create a new session or switch the active worktree branch? This affects the action wiring.
2. Should branch results appear as a separate group or interleaved with sessions? The current palette groups results by category; branches would be a natural fourth group (alongside commands, sessions, files).

---
issue: ""
title: "Settings"
status: draft
---

# Existing Solutions: Settings

## Overview

OpenChamber already has a comprehensive settings system with 21+ pages, sidebar navigation, split-page layouts, resizable nav, mobile support, and persistence to `OPENCHAMBER_DATA_DIR/settings.json`. The server-side `settings-runtime.js` manages read/write with locking, migration, and project/recovery logic. The client-side `SettingsView.tsx` orchestrates page rendering with lazy-loaded stores. Shared UI primitives in `packages/ui/src/components/sections/shared/` provide consistent layout patterns. The existing system covers FR-01 through FR-09 with the exception of keyboard shortcut customization (FR-05), import/export (FR-08), and per-section reset (FR-10).

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/components/views/SettingsView.tsx`, `packages/ui/src/components/sections/`, `packages/ui/src/components/sections/shared/`, `packages/web/server/lib/opencode/settings-runtime.js`, `packages/web/server/lib/opencode/settings-helpers.js` |
| Open-source | Yes | Zustand persist middleware, Base UI dialog/sidebar patterns, Radix UI collapsible |
| Commercial / SaaS | No | Settings UIs are application-specific |
| Standards / protocols | No | N/A |
| Reference material | Yes | Zustand docs, shadcn/ui settings dialog patterns |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber built-in settings | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-06, FR-07, FR-09 | FR-05 (keyboard shortcut UI), FR-08 (import/export), FR-10 (per-section reset) |
| Zustand persist middleware | Library | MIT | Mature | Client-side settings persistence | Does not cover server sync, validation, or project settings |
| Base UI Dialog / Sidebar | Library | MIT | Mature | Settings dialog shell, sidebar navigation | UI primitives only, not a settings system |

## Evaluation

### OpenChamber built-in settings

- **Strengths:** 21 pages organized with sidebar navigation, split-view layouts, resizable nav (176-280px), mobile responsive design with stage-based navigation, lazy-loaded store data per page, persistent to `settings.json`, and server-side sync with OpenCode. Shared primitives (`SettingsPageLayout`, `SettingsSection`, `SettingsSidebarLayout`, `SidebarGroup`) enforce consistent UI.
- **Weaknesses:** Keyboard shortcut customization (FR-05) is not yet exposed in the settings UI. Import and export (FR-08) of settings is missing. Per-section reset-to-default (FR-10) is not implemented. Some pages use the generic `OpenChamberPage` wrapper with section-based rendering which limits page-specific behavior.
- **Integration effort:** Low (already integrated).
- **Cost:** None.
- **Risks:** None.

### Zustand persist middleware

- **Strengths:** Built into Zustand v5, supports `localStorage`, `sessionStorage`, custom async storage, versioned migration, and selective persistence via `partialize`. Already used in the codebase.
- **Weaknesses:** Client-side only. Does not handle server sync, file-system persistence, or server-side validation.
- **Integration effort:** Low (already in use).
- **Cost:** None (MIT).
- **Risks:** None. Complementary to the existing system.

## Recommendation

**Direction: Adopt and extend**

The existing settings system is production-ready. Extend it with:
- Keyboard shortcut customization page (FR-05) using the existing shortcut infrastructure.
- Settings import/export (FR-08) via JSON file download/upload.
- Per-section reset-to-default (FR-10) by storing default values per section.
- Ensure collapsible sidebar groups (NFR-02) using `@radix-ui/react-collapsible` which is already a dependency.

## Sources of Information

- `SettingsView.tsx` at `packages/ui/src/components/views/SettingsView.tsx` - main settings orchestrator
- `SettingsPageLayout.tsx` at `packages/ui/src/components/sections/shared/SettingsPageLayout.tsx` - shared page layout
- `settings-runtime.js` at `packages/web/server/lib/opencode/settings-runtime.js` - server-side settings persistence
- `settings-helpers.js` at `packages/web/server/lib/opencode/settings-helpers.js` - settings validation and normalization
- Zustand persist middleware docs at `zustand.docs.pmnd.rs`

## Open Questions

1. Should settings import/export include all settings or allow selective section export?
2. How should keyboard shortcut customization handle conflicts with VS Code's built-in shortcuts?
3. What is the migration strategy when the settings schema changes between versions?

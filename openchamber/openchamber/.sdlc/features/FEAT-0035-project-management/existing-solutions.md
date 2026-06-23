---
issue: ""
title: "Project Management (Multi-Project)"
status: draft
---

# Existing Solutions: Project Management (Multi-Project)

## Overview

OpenChamber already has a multi-project system that is deeply integrated. The `useProjectsStore` manages project CRUD, active project state, settings synchronization, and per-project configurations. The `SidebarProjectsList` and `SortableProjectItem` components handle drag-to-reorder, project display with icons/colors/custom images, and per-project sessions. The `ProjectsSidebar` and `ProjectsPage` settings sections provide project management UI with icon selection, color picker, custom image upload, favicon discovery, rename, and delete. The requirements FR-01 through FR-07 map closely to the existing implementation. The recommended direction is to build on the existing infrastructure.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/stores/useProjectsStore.ts` (project CRUD, active project, settings sync, per-project git identity), `packages/ui/src/components/session/sidebar/SidebarProjectsList.tsx` and `sortableItems.tsx` (drag-to-reorder, project icons/colors/images), `packages/ui/src/components/sections/projects/` (ProjectsSidebar, ProjectsPage, ProjectActionsSection), `packages/ui/src/components/session/sidebar/hooks/useSessionSidebarSections.ts`, `packages/ui/src/components/layout/ProjectEditDialog.tsx` (edit dialog with icons, colors, image upload, favicon discovery) |
| Open-source | Yes | npm/GitHub for IDE workspace management patterns |
| Commercial / SaaS | Yes | JetBrains IDEA workspace management, VS Code multi-root workspaces, Cursor projects, Windsurf |
| Standards / protocols | No | No standard for IDE project organization |
| Reference material | Yes | VS Code multi-root workspace (.code-workspace), JetBrains IDEA project model |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber's existing project management | Internal | MIT | Production (v1.11.7) | FR-01 through FR-07 | See gaps below |
| VS Code multi-root workspaces | Product | MIT | Mature | Per-project sessions, directory-based, git identity | Desktop-only, VS Code-specific, not a library |
| pane-tabs-layout (umakantv/pane-tabs-layout) | Library | MIT | Active | Tab/pane management with drag-split, persistent state, tab pinning | No project model, not applicable |
| react-ide-workspace-layout (leoweyr) | Library | MIT | Active | JetBrains IDEA-like draggable/dockable workspace layout | Layout management only, no project abstraction |

## Evaluation

### OpenChamber's existing project management

- **Strengths:** `useProjectsStore` already supports add/rename/reorder/delete projects, per-project directory, sessions, git identity, and configuration. `ProjectEditDialog` provides icon selection from a predefined set, color picker with PROJECT_COLOR_MAP, custom image upload, favicon discovery (FR-05). `SidebarProjectsList` renders projects with visual indicators using `SortableProjectItem` with `@dnd-kit` drag-to-reorder (FR-03). Per-project sessions are handled via directory-scoped sync stores. Complete i18n coverage across 10 languages.
- **Weaknesses:** FR-06 (clone repository as part of project setup) may need integration with the git clone flow. Project icon image upload and favicon discovery exist in `ProjectEditDialog` (FR-05) but may need refinement.
- **Integration effort:** Low — project management is already a mature feature.
- **Cost:** None (MIT, in-house).
- **Risks:** None significant.

### External tools (VS Code multi-root, pane-tabs-layout, etc.)

- **Strengths:** VS Code's `.code-workspace` format is a mature multi-root workspace standard. pane-tabs-layout provides sophisticated IDE-like pane/tab management.
- **Weaknesses:** Not directly applicable — VS Code workspaces are an IDE-specific concept, not a library. pane-tabs-layout manages pane/tab layout, not the project abstraction layer that OpenChamber needs. OpenChamber's project model is tightly coupled to OpenCode's per-directory session architecture.
- **Integration effort:** N/A — these are reference patterns, not direct candidates.
- **Cost:** Free.
- **Risks:** N/A.

## Recommendation

**Direction:** Adopt and extend

OpenChamber already has a complete multi-project workspace system. The `useProjectsStore` provides all CRUD operations, per-project state isolation, and drag-to-reorder. The `ProjectEditDialog` covers icon/color/image customization and favicon discovery. The main gap is FR-06 (clone repository during project setup), which requires integrating git clone into the project creation flow — likely using the existing `simple-git` dependency in the server and the git clone workflow already present in the git section. No external library is needed.

## Sources of Information

- `packages/ui/src/stores/useProjectsStore.ts`: Defines project model with id, name, directory, icon, color, iconImage, iconBackground. Methods: `addProject`, `removeProject`, `renameProject`, `reorderProjects`, `getActiveProject`, `synchronizeFromSettings`. Per-project state includes git identity, preferences, and directory-scoped sessions.
- `packages/ui/src/components/layout/ProjectEditDialog.tsx`: Full project edit dialog with icon picker (PROJECT_ICON_MAP), color picker (PROJECT_COLOR_MAP), custom image upload (FileUpload for .png/.jpg/.svg/.webp), favicon discovery (`discoverFavicon`), icon background, rename field, and delete with confirmation.
- `packages/ui/src/components/session/sidebar/sortableItems.tsx`: Drag-to-reorder using `@dnd-kit/sortable` with `SortableProjectItem` showing icon/color/image/background.
- `packages/ui/src/components/sections/projects/ProjectsPage.tsx`: Full settings page for project listing, creation, and management.
- VS Code multi-root workspaces: Reference pattern for .code-workspace files as portable project definitions. OpenChamber could adopt a similar export/import format for project configurations.
- JetBrains IDEA project model: Each project has its own `.idea/` directory. OpenChamber's per-directory project model follows the same principle.

## Open Questions

1. FR-06 (clone repository): Should cloning be a wizard step in project creation (directory picker with "Clone from URL" option), or should it be a separate action in the project management area?
2. How should per-project git identity (FR-02) be surfaced in the UI? The existing `GitIdentityEditorDialog` may need wiring to the project context.

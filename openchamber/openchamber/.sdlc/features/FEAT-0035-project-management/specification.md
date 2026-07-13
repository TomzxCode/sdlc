---
title: "Project Management (Multi-Project)"
status: done
---

# Specification: Project Management

## Overview

Projects are managed via `useProjectsStore.ts` with server-side persistence via `packages/web/server/lib/projects/`. The sidebar uses `SidebarProjectsList.tsx` with `ProjectEditDialog.tsx` for customization.

## Architecture

```
SidebarProjectsList (packages/ui/src/components/session/sidebar/)
    +---> Project list with icons and colors
    +---> Add project (DirectoryExplorerDialog, clone)
    +---> Edit project (ProjectEditDialog)
    |
useProjectsStore.ts (project definitions, icon/color, order)
    |
Server (packages/web/server/lib/projects/project-config.js)
    Per-project config persistence
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Persistence | Server-side with deterministic identity | Project identity must be stable across client refreshes |
| Icons | Upload + favicon discovery | Flexible; covers custom and auto-detected icons |

## Out of Scope

- Project templates
- Project sharing

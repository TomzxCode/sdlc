---
title: "Permission / Edit Mode"
status: done
---

# Specification: Permission / Edit Mode

## Overview

Permissions are managed in `permissionStore.ts` with UI components `PermissionCard.tsx`, `PermissionRequest.tsx`, and `PermissionToastActions.tsx`. Edit mode configuration lives in `packages/ui/src/lib/permissions/` with `editModeColors.ts` and `editPermissionDefaults.ts`.

## Architecture

```
PermissionCard / PermissionRequest (packages/ui/src/components/chat/)
    +---> Approve/Deny UI
    +---> File change preview
    |
permissionStore.ts (pending permissions, auto-accept state)
    |
packages/ui/src/lib/permissions/
    +---> editModeColors.ts (visual coding by mode)
    +---> editPermissionDefaults.ts (default permission levels)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Auto-accept scope | Session tree (parent accepts for children) | Sub-agents inherit parent trust; avoids repeated prompts |
| Visual coding | Color by edit mode | Users can see at a glance what level of autonomy is active |

## Out of Scope

- Permission audit log
- Role-based access control

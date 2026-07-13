---
title: "Session Folders"
status: done
---

# Specification: Session Folders

## Overview

Session folders are managed via `useSessionFoldersStore.ts` with server-side persistence via `packages/web/server/lib/session-folders/routes.js`. The UI component `SessionFolderItem.tsx` renders folder nodes with drag-and-drop support.

## Architecture

```
SessionFolderItem (packages/ui/src/components/session/SessionFolderItem.tsx)
    +---> Folder CRUD (create, rename, delete)
    +---> Drag-and-drop (@dnd-kit)
    +---> Collapse/expand
    |
useSessionFoldersStore.ts (folder state, session-to-folder mapping)
    |
Server (packages/web/server/lib/session-folders/routes.js)
    Persists folder structure to local storage
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Persistence | Server-side local storage | Survives client refresh; shared across tabs |
| DnD | @dnd-kit sortable | Consistent with todo DnD; accessible |

## Out of Scope

- Folder templates or presets
- Folder-based permissions

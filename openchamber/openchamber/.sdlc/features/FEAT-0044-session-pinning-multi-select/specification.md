---
title: "Session Pinning & Multi-Select"
status: done
---

# Specification: Session Pinning & Multi-Select

## Overview

Pinning uses `useSessionPinnedStore.ts` with persistence. Multi-select uses `useSessionMultiSelectStore.ts` with `BulkActionBar.tsx` for actions.

## Architecture

```
SessionNodeItem (packages/ui/src/components/session/sidebar/)
    +---> Pin toggle
    +---> Checkbox for multi-select
    +---> Shift-click range selection
    |
BulkActionBar (packages/ui/src/components/session/sidebar/)
    +---> Archive, Delete, Move to Folder actions
    |
useSessionPinnedStore.ts (pinned session IDs, persisted)
useSessionMultiSelectStore.ts (selected session IDs, selection mode)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Pin persistence | Separate store with persistence | Pins must survive page reload |
| Selection | Shift-click + checkbox | Covers both keyboard and mouse workflows |

## Out of Scope

- Pin reordering
- Pin sharing across devices

---
title: "Command Palette"
status: draft
---

# Specification: Command Palette

## Overview

The command palette is implemented in `packages/ui/src/components/ui/CommandPalette.tsx` using the `cmdk` library. Fuzzy search is powered by `fuse.js`. It indexes sessions, files, branches, settings pages, and actions into a searchable collection.

## Architecture

```
CommandPalette (packages/ui/src/components/ui/CommandPalette.tsx)
    |
    +---> cmdk (palette UI with keyboard navigation)
    +---> fuse.js (fuzzy search over indexed items)
    |
    +---> Index sources:
          +---> Sessions (from globalSessions store)
          +---> Files (from fileStore / server search)
          +---> Branches (from gitStore)
          +---> Settings pages (static list)
          +---> Actions (registered commands)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Palette library | cmdk | Lightweight, accessible, well-maintained command palette component |
| Search | fuse.js | Best-in-class fuzzy search; handles typos and partial matches |
| Indexing | Client-side from existing stores | No additional server calls; data already in memory |

## Risks and Unknowns

1. Large projects (10k+ files) may cause search latency
2. Branch and session lists may be stale if not refreshed before palette open

## Out of Scope

- Custom user-defined commands
- Search across message content
- Recently used command history

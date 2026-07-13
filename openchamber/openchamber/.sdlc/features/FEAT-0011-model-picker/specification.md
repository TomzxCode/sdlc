---
title: "Model Picker"
status: done
---

# Specification: Model Picker

## Overview

The model picker lives in `packages/ui/src/components/model-picker/` and uses `ModelPickerList.tsx`. Favorites, recents, and hidden models are stored in `useUIStore.ts` fields. Model metadata is derived from provider state via `useModelLists.ts`.

## Architecture

```
ModelPickerList (packages/ui/src/components/model-picker/)
    |
    +---> Provider-grouped model list
    +---> Favorites section
    +---> Recents section
    +---> Search/filter (fuse.js)
    |
    +---> useUIStore (favoriteModels, recentModels, hiddenModels)
    +---> useModelLists (available models from provider state)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Persistence | useUIStore fields | Per-browser preferences; syncs across tabs via SSE |
| Search | Client-side filter | Fast; model list is small enough for in-memory search |
| Favorites cycling | Keyboard shortcut | Power-user workflow for rapid model switching |

## Out of Scope

- Model benchmarking or comparison UI
- Custom model registration (handled by provider settings)

---
title: "Diff Viewer"
status: draft
---

# Specification: Diff Viewer

## Overview

The diff viewer uses `@pierre/diffs` (Pierre) for rendering. The full-screen view (`DiffView.tsx`) combines a file tree sidebar with the diff content area. Inline diffs in chat messages use the same rendering components in a compact form.

## Architecture

```
DiffView (packages/ui/src/components/views/DiffView.tsx)
    |
    +---> File tree sidebar (changed files list)
    +---> PierreDiffViewer (packages/ui/src/components/views/PierreDiffViewer.tsx)
    |         |
    |         +---> @pierre/diffs (diff rendering engine)
    |         +---> Syntax highlighting (CodeMirror)
    |
    v
Inline diffs in chat (packages/ui/src/components/chat/message/)
    uses same Pierre rendering in compact mode
```

## Data Models

### DiffFile

| Field | Type | Constraints | Description |
|---|---|---|---|
| path | string | PK | File path |
| status | enum | not null | added, modified, deleted, renamed |
| additions | number | not null | Lines added |
| deletions | number | not null | Lines removed |
| hunks | DiffHunk[] | not null | Ordered diff sections |

### DiffHunk

| Field | Type | Constraints | Description |
|---|---|---|---|
| oldStart | number | not null | Start line in old file |
| newStart | number | not null | Start line in new file |
| oldLines | number | not null | Lines in old |
| newLines | number | not null | Lines in new |
| content | string | not null | Diff content |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Diff engine | @pierre/diffs (Pierre) | Fast, beautiful diff rendering with syntax highlighting built in |
| Layout | Side-by-side and stacked toggle | Users have strong preferences; supporting both maximizes usability |
| Lazy loading | Per-file diff expansion | Prevents loading 100+ file diffs upfront |

## Risks and Unknowns

1. Pierre library is in beta (1.1.0-beta.13); API stability may be a concern
2. Very large single-file diffs (10k+ lines) may still cause rendering lag

## Out of Scope

- Three-way merge diffs
- Diff editing / conflict resolution
- Word-level diff toggling (handled by Pierre internally)

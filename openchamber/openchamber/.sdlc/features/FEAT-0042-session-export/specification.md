---
title: "Session Export"
status: done
---

# Specification: Session Export

## Overview

Session export is implemented in `packages/ui/src/lib/exportSession.ts`. It iterates through session messages, formats them as Markdown with metadata, and triggers download via browser API or native save dialog.

## Architecture

```
exportSession.ts (packages/ui/src/lib/exportSession.ts)
    +---> Iterate messages and parts
    +---> Format as structured Markdown
    +---> Include sub-agent sessions as nested sections
    |
    v  Download
Browser: Blob download
Desktop: Native save dialog + file reveal
VS Code: Save via extension host
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Format | Markdown | Human-readable, version-control friendly, universal |
| Sub-agents | Nested sections | Preserves the hierarchical session structure |

## Out of Scope

- JSON or HTML export
- Batch export
- Export with attachments

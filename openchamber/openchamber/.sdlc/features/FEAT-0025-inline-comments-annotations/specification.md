---
title: "Inline Comments & Annotations"
status: draft
---

# Specification: Inline Comments & Annotations

## Overview

Inline comments are managed via `useInlineCommentDraftStore.ts` and rendered by components in `packages/ui/src/components/comments/`. CodeMirror integration uses `CodeMirrorCommentWidgets.tsx`, diff overlays use `PierreDiffCommentOverlays.tsx`, and the controller logic is in `useInlineCommentController.ts`.

## Architecture

```
InlineCommentCard / InlineCommentInput (packages/ui/src/components/comments/)
    |
    +---> CodeMirrorCommentWidgets (editor line comments)
    +---> PierreDiffCommentOverlays (diff-side annotations)
    +---> useInlineCommentController (lifecycle management)
    |
useInlineCommentDraftStore.ts (comment storage per session)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Editor integration | CodeMirror widgets | Native to the editor; precise line anchoring |
| Diff integration | Overlay on Pierre viewer | Pierre doesn't expose comment hooks; overlay approach works |

## Out of Scope

- Collaborative commenting (multi-user)
- Comment threads or replies

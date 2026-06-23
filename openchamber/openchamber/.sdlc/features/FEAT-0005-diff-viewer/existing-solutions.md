---
issue: ""
title: "Diff Viewer"
status: draft
---

# Existing Solutions: Diff Viewer

## Overview

OpenChamber's diff viewer is already fully implemented using `@pierre/diffs` (Pierre) as the rendering engine, backed by Shiki for syntax highlighting with web worker offloading. The full-screen DiffView combines a file tree sidebar with Pierre-based diff rendering, supporting side-by-side and stacked modes, file expansion/collapse, and inline comment overlays. The recommendation is to continue with `@pierre/diffs`, which is modern, fast, feature-rich, and already deeply integrated. No alternative library provides a compelling reason to migrate.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/components/views/DiffView.tsx` (1897 lines), `packages/ui/src/components/views/PierreDiffViewer.tsx` (751 lines), `packages/ui/src/components/chat/DiffPreview.tsx`, `packages/ui/src/components/chat/StreamingTextDiff.tsx`, `packages/ui/src/components/chat/message/parts/toolDiffUtils.ts`, `packages/ui/src/components/comments/PierreDiffCommentOverlays.tsx`, `packages/ui/src/contexts/DiffWorkerProvider.tsx`, `packages/ui/src/lib/diff/workerFactory.ts`, `packages/ui/src/lib/shiki/appThemeRegistry.ts`, `packages/ui/package.json` (@pierre/diffs 1.1.0-beta.13) |
| Open-source | Yes | @pierre/diffs, @git-diff-view/react, react-diff-view (otakustay), react-diff-viewer (downshift), react-virtualized-diff, react-version-compare (CrashBytes), CodeMirror @codemirror/merge |
| Commercial / SaaS | Yes | GitHub diff viewer, GitLab diff viewer, VS Code diff editor, Bitbucket diff viewer |
| Standards / protocols | Yes | Unified diff format, Git diff format, side-by-side vs unified diff mode |
| Reference material | Yes | @pierre/diffs documentation, @git-diff-view/react docs, GitHub diff style guide |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| @pierre/diffs (current) | Library | MIT | Active (beta 1.1.0) | FR-01 (side-by-side/stacked), FR-04 (syntax-highlighted diffs via Shiki), FR-05 (inline in chat), FR-06 (image diffs), FR-07 (inline comment annotations), FR-08 (mixed line endings), NFR-01 (virtualized), NFR-02 (lazy loading) | FR-02 (file tree is custom, in DiffView.tsx), FR-03 (expand/collapse is custom), FR-09 (copy/delete actions), FR-10 (two-parent diff) |
| internal DiffView + PierreDiffViewer | Internal | MIT | Ship-ready | FR-01 through FR-08, FR-10, NFR-01, NFR-02 | FR-09 (copy/delete actions not yet implemented) |
| @git-diff-view/react | Library | MIT | Active (46 versions) | FR-01 (split/unified), FR-04 (syntax highlighting via Shiki/lowlight), widget system, extend data | FR-06 (no image diff), FR-07 (no comment annotations), smaller ecosystem |
| react-diff-view (otakustay) | Library | BSD-2 | Stale (last update 2017) | FR-01 (split/unified), token system with refractor, decoration widgets | Outdated (ES5, refractor@3.x), no Shiki integration, no longer actively maintained |
| react-virtualized-diff (Zhang-JiahangH) | Library | MIT | Active (2026) | Virtualized rendering for large files, side-by-side/unified, collapsed unchanged blocks | No syntax highlighting, no comment overlays, limited to text comparison |
| Monaco Editor diff editor | Library | MIT | Mature | Full-featured diff editor, TypeScript-aware | 5MB bundle, poor mobile support, overkill for diff-only use case |

## Evaluation

### @pierre/diffs (current)

- **Strengths:** Fast diff rendering with syntax highlighting via Shiki. Supports both side-by-side and unified modes. Worker pool for offloaded computation (`DiffWorkerProvider.tsx`). Native support for annotations/overlays (used for inline comments in `PierreDiffCommentOverlays.tsx`). Supports file contents objects for original/modified comparison. Custom theme registration via Shiki API. Virtualized rendering via `VirtualizedFileDiff` for large files. Actively maintained in beta.
- **Weaknesses:** Beta version (1.1.0-beta.13). API may break on stable release. Smaller community than more established libraries.
- **Integration effort:** Already deeply integrated. Used in DiffView.tsx (full-screen), PierreDiffViewer.tsx (inline), ToolPart.tsx (chat tool output), ToolOutputDialog.tsx, and FilesView.tsx (diff file preview). Comment overlay integration already complete.
- **Cost:** MIT (free).
- **Risks:** Low-moderate. Beta stability is the main risk. The project pins `@pierre/diffs` to 1.1.0-beta.13. Monitor for stable release.

### @git-diff-view/react

- **Strengths:** GitHub-style UI. Split/unified modes with full syntax highlighting via Shiki. Web Worker and server-side rendering support. Widget system for custom line actions. Large feature set (line wrapping, extend data, themes). Framework-agnostic (React/Vue/Solid/Svelte).
- **Weaknesses:** No native image diff support (FR-06). No built-in annotation model for inline comments (FR-07) — would need custom overlay logic. No streaming diff support (used in StreamingTextDiff.tsx). Less focus on internal diff computation; expects pre-computed hunks.
- **Integration effort:** Medium to high. Would need to replace all Pierre imports across 10+ files, reimplement comment overlays, and adapt the file tree integration.
- **Cost:** MIT (free).
- **Risks:** Medium. Migration cost outweighs benefits given the existing Pierre integration is mature and feature-complete.

## Recommendation

**Direction:** Adopt

Continue with `@pierre/diffs` as the diff rendering engine. It is modern, integrates Shiki for best-in-class syntax highlighting, supports virtualized rendering for large files, and has native annotation support which enables the inline comment draft feature (FR-07). The remaining gaps (FR-09 copy/delete actions, FR-10 two-parent diff support) are application-level concerns built on top of Pierre, not library gaps. Monitor the Pierre project's path to stable and update the pinned version when 1.1.0 stable is released.

## Sources of Information

- @pierre/diffs: `npmjs.com/package/@pierre/diffs` — diff library with Shiki syntax highlighting, worker pool, annotations
- @git-diff-view/react: `github.com/MrWangJustToDo/git-diff-view` — GitHub-style diff view for React
- react-diff-view (otakustay): `github.com/otakustay/react-diff-view` — token-based diff viewer (older, stale)
- react-virtualized-diff: `github.com/Zhang-JiahangH/react-virtualized-diff` — virtualized diff for large files
- Existing `packages/ui/src/components/views/DiffView.tsx` — file tree sidebar + diff content area
- Existing `packages/ui/src/components/views/PierreDiffViewer.tsx` — Pierre wrapper with theme, worker pool, and comment overlay integration
- Existing `packages/ui/src/components/comments/PierreDiffCommentOverlays.tsx` — inline comment overlay on diffs

## Open Questions

1. When will `@pierre/diffs` reach a stable 1.1.0 release, and should we pin to a specific commit or continue with `1.1.0-beta.13`?
2. Should inline comment drafts on diffs (FR-07) be persisted server-side (via the existing comment store) or only exist as ephemeral UI state until sent?

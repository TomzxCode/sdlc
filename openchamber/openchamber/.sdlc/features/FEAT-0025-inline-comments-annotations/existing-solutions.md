---
issue: ""
title: "Inline Comments & Annotations"
status: draft
---

# Existing Solutions: Inline Comments & Annotations

## Overview

The codebase already has a complete inline comment system. A Zustand store (`useInlineCommentDraftStore.ts`) persists comments per session with local storage. Rendering components cover CodeMirror editor widgets (`CodeMirrorCommentWidgets.tsx`), Pierre diff overlays (`PierreDiffCommentOverlays.tsx`), and card/input UI (`InlineCommentCard.tsx`, `InlineCommentInput.tsx`). Formatting helpers (`inlineComments.ts`) support comment consumption. The recommended direction is to adopt the existing implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/stores/useInlineCommentDraftStore.ts`, `packages/ui/src/components/comments/`, `packages/ui/src/lib/messages/inlineComments.ts` |
| Open-source | Yes | CodeMirror decoration APIs, @pierre/diffs, Diff viewer annotation patterns |
| Commercial / SaaS | No | |
| Standards / protocols | No | |
| Reference material | Yes | CodeMirror WidgetType, Decoration API, @pierre/diffs API |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| useInlineCommentDraftStore (current) | Internal | MIT | Active | FR-04 persisted per session, FR-09 session-scoped, FR-08 create/edit/delete | None |
| CodeMirrorCommentWidgets.tsx | Internal | MIT | Active | FR-02 editor line comments, FR-07 | FR-06 diff viewer integration |
| PierreDiffCommentOverlays.tsx | Internal | MIT | Active | FR-01 diff-side annotations (original/modified) | Overlay approach (spec decision) |
| InlineCommentCard/Input | Internal | MIT | Active | FR-01/02/03 comment CRUD UI | None |
| useInlineCommentController.ts | Internal | MIT | Active | Comment lifecycle management | None |
| formatInlineComments.ts | Internal | MIT | Active | FR-05 comment consumption formatting | None |

## Evaluation

### useInlineCommentDraftStore.ts

- **Strengths:** Full Zustand store with persist middleware (localStorage). Types: `InlineCommentDraft` with `InlineCommentSource` (`'diff' | 'plan' | 'file' | 'preview-console' | 'preview-annotation'`). Actions: `addDraft`, `updateDraft`, `removeDraft`, `clearDrafts`, `consumeDrafts` (returns sorted drafts and clears them), `hasDrafts`, `getDraftCount`. Includes sanitization and schema migration. ID generation uses `icd-${timestamp}-${random}` prefix for uniqueness.
- **Weaknesses:** Consume operation is destructive (clears drafts after reading). No draft editing in-place (replace via updateDraft).
- **Integration effort:** Already implemented at `packages/ui/src/stores/useInlineCommentDraftStore.ts` (228 lines)
- **Cost:** Free (MIT)
- **Risks:** Low; well-structured store with input sanitization

### CodeMirrorCommentWidgets.tsx

- **Strengths:** Uses CodeMirror's `WidgetType` and `Decoration.widget` API for precise line anchoring. Consistent with the file editor's CodeMirror integration. Decorations update when document changes.
- **Weaknesses:** Relies on CodeMirror view lifecycle; must handle viewport changes and re-rendering. Widget DOM management needs care to avoid flicker.
- **Integration effort:** Already implemented at `packages/ui/src/components/comments/CodeMirrorCommentWidgets.tsx`
- **Cost:** Free
- **Risks:** Low; CodeMirror decoration API is stable

### PierreDiffCommentOverlays.tsx

- **Strengths:** Overlays on the `@pierre/diffs` viewer (`@pierre/diffs@1.1.0-beta.13` in `packages/ui/package.json:44`) without modifying Pierre internals. Supports both original and modified side annotations (FR-01). Gutter or inline rendering.
- **Weaknesses:** Overlay approach may have z-index/layering issues. Pierre is a beta release and may change its DOM structure.
- **Integration effort:** Already implemented at `packages/ui/src/components/comments/PierreDiffCommentOverlays.tsx`
- **Cost:** Free (MIT)
- **Risks:** Moderate - `@pierre/diffs` is beta and may have breaking changes. Overlays depend on Pierre's DOM structure.

### InlineCommentCard.tsx / InlineCommentInput.tsx

- **Strengths:** Comment display card shows file label, line range, code context, comment text, timestamps. Input has text area with submit/cancel. Create, edit, and delete actions (FR-08). No resolve/address state (per spec).
- **Weaknesses:** No rich text in comments (plain text only per spec).
- **Integration effort:** Already implemented at `packages/ui/src/components/comments/`
- **Cost:** Free
- **Risks:** Low

### formatInlineComments.ts

- **Strengths:** `formatInlineCommentDraft()` handles diff, plan, file, preview-console, and preview-annotation sources. `appendInlineComments()` appends formatted comments to chat input (FR-05). Markdown code block formatting for context.
- **Weaknesses:** Preview-annotation format is minimal (code + text without file label).
- **Integration effort:** Already implemented at `packages/ui/src/lib/messages/inlineComments.ts`
- **Cost:** Free
- **Risks:** Low

## Recommendation

**Direction:** Adopt

All requirements are already implemented:
- FR-01: Diff annotations via `PierreDiffCommentOverlays.tsx` (original and modified sides)
- FR-02: File editor comments via `CodeMirrorCommentWidgets.tsx`
- FR-03: Plan comments via `InlineCommentCard.tsx` (plan source type in store)
- FR-04: Persistence per session via `useInlineCommentDraftStore` with Zustand persist middleware (localStorage key: `openchamber-inline-comment-drafts`)
- FR-05: Comment consumption via `consumeDrafts` in store + `appendInlineComments` formatter
- FR-06: Pierre diff viewer overlays via `PierreDiffCommentOverlays.tsx`
- FR-07: CodeMirror widgets via `CodeMirrorCommentWidgets.tsx`
- FR-08: Create, edit, and delete actions only (no resolve/address) - confirmed in store and UI
- FR-09: Scoped to `sessionKey` - no cross-session sharing

No gaps found. The implementation follows the specification decisions (overlay for Pierre, CodeMirror widgets for editor, session-scoped store).

Minor consideration: The `@pierre/diffs` beta dependency may need monitoring for breaking changes. The overlay approach for diff comments should be tested with the latest Pierre version.

## Sources of Information

- CodeMirror Decoration + WidgetType examples: https://codemirror.net/examples/decoration/
- CodeMirror widget lifecycle: https://codemirror.net/docs/ref/#view.WidgetType
- Pierre Diffs: https://github.com/pierre-org/pierre-diffs (npm: `@pierre/diffs`)
- Zustand persist middleware: https://docs.pmnd.rs/zustand/integrations/persisting-store-data

## Open Questions

1. Does the `@pierre/diffs` beta release cadence risk breaking the overlay component?
2. Should inline comments support attachment of selection context from multiple files, or is one-file-at-a-time sufficient?
3. Should the inline comment store be integrated with the sync layer for real-time comment delivery across sessions (currently out of scope)?

---
issue: ""
title: "Plan View"
status: draft
---

# Existing Solutions: Plan View

## Overview

The plan view is partly implemented with `PlanView.tsx`, i18n message strings, and a specification referencing CodeMirror markdown mode. The existing CodeMirror dependency (`@codemirror/lang-markdown`) already provides markdown editing capabilities. The recommended direction is to build on the existing CodeMirror setup and complete the PlanView component.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/components/views/PlanView.tsx`, CodeMirror setup, i18n strings, feature flag `planModeEnabled` |
| Open-source | Yes | CodeMirror, react-markdown, remark/rehype ecosystem |
| Commercial / SaaS | No | No commercial plan editors considered |
| Standards / protocols | No | |
| Reference material | Yes | CodeMirror docs for markdown, decoration APIs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| CodeMirror with @codemirror/lang-markdown (current) | Library | MIT | Mature | FR-01, FR-08, NFR-01 | FR-02 needs preview renderer, FR-05 inline comments |
| react-markdown + remark-gfm | Library | MIT | Mature | FR-02 markdown preview rendering | Not an editor; used for chat already |
| PlanView.tsx (partial) | Internal | MIT | Draft | FR-01 editor scaffolding | Not yet feature-complete per requirements |
| Obsidian / Notable | Commercial | Proprietary | Mature | Full plan/note editor with markdown + preview | Not embeddable; external tools |
| Stackblitz / CodeSandbox | Commercial | Proprietary | Mature | Plan + code + preview | Overkill; external dependency |

## Evaluation

### CodeMirror with @codemirror/lang-markdown

- **Strengths:** Already in the monorepo with 20+ CodeMirror packages (`packages/ui/package.json:15-35`). Used in the file editor. `@codemirror/lang-markdown` provides syntax highlighting, folding, keybindings. Good for large documents (NFR-01). Can be extended with custom widgets for inline comments (FR-05).
- **Weaknesses:** No built-in preview toggle. Markdown rendering requires a separate library (react-markdown already used in chat).
- **Integration effort:** Low - CodeMirror already wired up in the project. PlanView.tsx just needs to use it.
- **Cost:** Free (MIT)
- **Risks:** Low

### react-markdown + remark-gfm

- **Strengths:** Already in the codebase (`packages/web/package.json:92-94`) for chat message rendering. Supports GFM tables, task lists, etc. Easy to use for FR-02 preview.
- **Weaknesses:** Not an editor. Must be paired with CodeMirror for the edit mode.
- **Integration effort:** Low - already imported in `packages/ui/src/components/chat/MarkdownRendererImpl.tsx:4`
- **Cost:** Free (MIT)
- **Risks:** Low

### PlanView.tsx (existing partial implementation)

- **Strengths:** Already scaffolded with the plan context panel architecture. i18n strings defined for 7+ locales covering save/load, improve/implement actions, copy, loading states. Feature flag `planModeEnabled` defined.
- **Weaknesses:** Not yet feature-complete per requirements. Needs to integrate CodeMirror editor, preview toggle, inline comments, save/load to project files, worktree creation.
- **Integration effort:** Completion work, not new effort
- **Cost:** Free (MIT)
- **Risks:** Low

## Recommendation

**Direction:** Build (on existing scaffolding)

The codebase already has all the building blocks:
- FR-01: CodeMirror with `@codemirror/lang-markdown` is already in the dependency tree and suitable for the editor
- FR-02: `react-markdown` is already used in the chat module for rendering; can be reused for the preview toggle
- FR-03: PlanView.tsx action bar already has "improve" and "implement" i18n strings; needs to wire to session input
- FR-04: Worktree creation from plan items reuses the existing worktree dialog infrastructure
- FR-05: Inline comments can reuse `useInlineCommentDraftStore` and the CodeMirror widget pattern from `CodeMirrorCommentWidgets.tsx`
- FR-06/FR-09: Save/load plan files uses the existing filesystem API endpoints
- FR-08: Plain markdown is the default; no template enforcement
- NFR-01: CodeMirror handles large documents efficiently

The plan view should be completed as a context panel overlay (`packages/ui/src/components/layout/ContextPanel.tsx`) per the specification. The plan mode feature flag should gate the UI entry point.

## Sources of Information

- CodeMirror markdown language: https://github.com/codemirror/lang-markdown
- CodeMirror decoration examples: https://codemirror.net/examples/decoration/
- react-markdown: https://github.com/remarkjs/react-markdown
- Existing PlanView.tsx at `packages/ui/src/components/views/PlanView.tsx`
- Existing i18n strings in `packages/ui/src/lib/i18n/messages/en.ts` under `planView.*` keys

## Open Questions

1. Should the plan view be accessible as a tab in the main layout or only as a context panel overlay?
2. Should plan files be saved in `.sdlc/features/` directory, project root, or a dedicated plan directory?
3. Is inline commenting on plan sections (FR-05) in scope for the initial implementation or a follow-up?
4. Should "send to session for improvement" create a new session or use the current one?

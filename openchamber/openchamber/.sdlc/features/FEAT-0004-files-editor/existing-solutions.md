---
issue: ""
title: "Files & Editor"
status: draft
---

# Existing Solutions: Files & Editor

## Overview

OpenChamber's file explorer and code editor are already substantially implemented using CodeMirror 6 for the text editor (with 15+ language modes, custom Flexoki theme, search, Go To Line), a custom file tree component with server-side `/api/fs/` endpoints, and integrated previews for markdown, JSON, and images. The recommendation is to continue with CodeMirror 6, which is the correct choice for this use case (lightweight, modular, mobile-friendly), and incrementally improve the file tree with virtualized rendering and search. No external file manager library should replace the custom implementation, which is tightly integrated with the OpenCode workspace model.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/components/views/FilesView.tsx` (3654 lines - file tree + editor + previews), `packages/ui/src/components/ui/CodeMirrorEditor.tsx` (CodeMirror wrapper), `packages/ui/src/lib/codemirror/` (languageByExtension, flexokiTheme), `packages/ui/src/stores/` (useFilesViewTabsStore, useFileSearchStore, fileStore), `packages/web/server/lib/fs/` (routes.js, search.js), `packages/ui/src/components/views/GoToLineDialog.tsx`, `packages/ui/src/components/views/PreviewToggleButton.tsx`, `package.json` (extensive @codemirror/* deps) |
| Open-source | Yes | CodeMirror 6, Monaco Editor, react-simple-code-editor, Sandpack (CodeSandbox), SVAR React File Manager, exploration (jaredLunde), vfs-kit |
| Commercial / SaaS | Yes | VS Code (Monaco-based), GitHub Codespaces, Replit, CodeSandbox, Cursor, Zed |
| Standards / protocols | Yes | LSP (Language Server Protocol), Tree-sitter, Lezer grammars, TextMate grammars |
| Reference material | Yes | CodeMirror 6 docs, Monaco Editor comparison guides, reactive-file-explorer primitives, CodeMirror from the Ground Up |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| CodeMirror 6 (current) | Library | MIT | Mature (7.5K stars, 5M/week) | FR-02 (syntax highlighting 15+ languages), FR-05 (Go To Line), FR-06 (markdown rendering delegated), FR-07 (JSON tree view), FR-08 (inline images), FR-09 (inline comment widgets), FR-13 (truncation), FR-14 (warning), NFR-01, NFR-02 | FR-01 (file tree is custom), FR-04 (file search is custom), FR-03 (CRUD operations use server API), FR-12 (diff preview) |
| Internal file tree + FS API (current) | Internal | MIT | Ship-ready | FR-01 (custom file tree with git status indicators, file type icons), FR-03 (CRUD via server API), FR-04 (client-side search with server-side FS search), FR-10 (clickable paths), FR-11 (pending navigation guard), FR-13, FR-14, FR-15 | FR-01 (no virtualization for large directories), FR-12 (diff preview not yet added) |
| Monaco Editor | Library | MIT | Mature (38K stars, 2M/week) | FR-02 (full IntelliSense, TS/JS LSP, 60+ languages), FR-05, FR-12 (built-in diff editor) | Bundle size (~5MB gzipped), poor mobile support, heavy initial load, overkill for OpenChamber's use case |
| Sandpack (CodeSandbox) | Library | MIT | Mature (4K stars) | FR-02 (CodeMirror-based editor), code execution in browser | Built for interactive playgrounds, not general-purpose file editing |
| SVAR React File Manager | Library | MIT | Active (3.8K/week) | FR-01 (file tree, list view, search, CRUD, split view) | Not a code editor, no integration with CodeMirror or git status |

## Evaluation

### CodeMirror 6 (current)

- **Strengths:** Modular and tree-shakeable (~50KB minimum, 300KB full). Extensions installed as needed (15+ languages already configured). Excellent mobile support with native platform selection. Near-instant initialization (~100ms). `@tanstack/react-virtual` for CodeMirror virtualization (NFR-02). Custom Flexoki theme integration. Comment widgets already built.
- **Weaknesses:** No built-in IntelliSense (must integrate LSP separately). No minimap. Language support requires separate packages.
- **Integration effort:** Already integrated. CodeMirrorEditor.tsx is a mature wrapper with compartments for dynamic config, keybinding support, search panel, cursor position tracking, and custom decoration plugins.
- **Cost:** MIT (free).
- **Risks:** Low. CodeMirror 6 is the correct choice for OpenChamber's use case (lightweight embedding, mobile support, customizability). The existing investment (65+ imports across the codebase) should not be abandoned.

### Monaco Editor

- **Strengths:** Full VS Code experience in the browser. Built-in TypeScript IntelliSense, go-to-definition, refactoring. 60+ languages out of the box. Built-in diff editor.
- **Weaknesses:** ~5MB gzipped bundle. Poor mobile touch optimization. Heavy initialization (1-3 seconds). Complex web worker configuration. SSR complications. Overkill for an AI chat companion tool where the user's primary editor is external.
- **Integration effort:** Very high. Would require replacing all CodeMirror integrations, rewriting the editor wrapper, and adding web worker configuration.
- **Cost:** MIT (free).
- **Risks:** Bundle size impact on PWA/mobile users. Worker setup complexity. The project has no need for the full VS Code IntelliSense features that Monaco provides.

## Recommendation

**Direction:** Adopt and extend

Continue with CodeMirror 6 as the editor engine and the custom file tree component. CodeMirror 6 is the right choice for OpenChamber's use case — a lightweight, mobile-friendly code viewer/editor embedded in an AI chat app. Key improvements:

- **FR-01 (file tree virtualization):** The custom file tree in FilesView.tsx currently renders all visible nodes. Adopt `react-window` or `@tanstack/react-virtual` (already a dependency) to virtualize the tree for large directories.
- **FR-04 (file tree search):** Already has `useFileSearchStore` and server-side `fs/search.js`. The search UI in the file tree should use Fuse.js (already a dependency) for client-side filtering with fuzzy matching.
- **FR-12 (diff preview in file tree):** Use the existing Pierre diff infrastructure to show inline diffs when git changes exist for a file.

## Sources of Information

- CodeMirror 6 docs: `codemirror.net/docs/` — modular editor with Lezer parsers
- CodeMirror vs Monaco vs Sandpack: `pkgpulse.com/guides/monaco-editor-vs-codemirror-6-vs-sandpack-in-browser-2026` — comprehensive comparison
- CodeMirror from the Ground Up: `codemirror.net/examples/` — extension system, facets, compartments
- exploration: `github.com/jaredLunde/exploration` — React file tree primitives (headless, virtualized)
- SVAR React File Manager: `svar.dev/react/filemanager/` — full file explorer component
- Existing `packages/ui/src/components/ui/CodeMirrorEditor.tsx` — mature CodeMirror wrapper with compartments, decoration, and view plugins
- Existing `packages/web/server/lib/fs/routes.js` — server-side FS endpoints

## Open Questions

1. Should the file tree adopt a headless library like `exploration` for virtualization and drag-and-drop, or continue with the custom implementation augmented by `@tanstack/react-virtual`?
2. Should file diff preview (FR-12) be inline in the tree or open in the existing DiffView?

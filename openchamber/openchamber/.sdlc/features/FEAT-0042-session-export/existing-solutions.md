---
issue: ""
title: "Session Export"
status: draft
---

# Existing Solutions: Session Export

## Overview

OpenChamber already has a complete session export implementation in `packages/ui/src/lib/exportSession.ts`. It covers structured Markdown export with timestamps, model info, role indicators, nested sub-agent sections, browser download via Blob URL, desktop native save dialog (via Electron IPC), VS Code save, and file reveal. The i18n keys for all export UI strings are already defined across all 8 locales. No external library is needed — the remaining work is UI refinement and cross-runtime testing.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/lib/exportSession.ts`, `packages/ui/src/lib/desktop.ts`, `packages/ui/src/components/session/sidebar/SessionNodeItem.tsx`, i18n messages for all locales |
| Open-source | Yes | marked, showdown, html-to-md, file-saver |
| Commercial / SaaS | No | Not applicable for local file export |
| Standards / protocols | No | Markdown is the de facto standard for structured text export |
| Reference material | No | |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| **Built-in exportSession.ts** | Internal | MIT | Production (v1.x) | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06 | None identified — all requirements met |
| **file-saver** | Library | MIT | Mature (npm) | Browser download | Not needed — built-in Blob/URL approach works; doesn't cover desktop native dialog |
| **marked** | Library | MIT | Mature | Markdown parsing/render | Not needed — we generate Markdown, not parse it |

## Evaluation

### Built-in exportSession.ts

- **Strengths:** Handles all FRs: `formatSessionAsMarkdown` generates structured Markdown with title, date, participant labels, timestamps, model/providers, text content, and recursive sub-agent nesting. `downloadAsMarkdown` uses Blob URL + anchor click for browser download. `saveAsMarkdownDesktop` delegates to Electron IPC for native save dialog with retry to VS Code backend. `revealExportedMarkdown` handles desktop and runtime-file reveal. `buildExportFilename` sanitizes titles to safe filenames with date suffix. Sub-agent export includes a confirmation dialog (i18n keys already exist). All export i18n strings are localized in 8 languages.
- **Weaknesses:** The `saveAsMarkdownDesktop` function has a fallback chain that could be clearer about failure modes across runtimes.
- **Integration effort:** Low — already wired in `SessionNodeItem.tsx` context menu via the "Export Markdown" menu item.
- **Cost:** MIT, free.
- **Risks:** No significant risks. The module is self-contained with no external dependencies for Markdown generation.

### file-saver

- **Strengths:** Well-known, handles cross-browser download quirks.
- **Weaknesses:** Solves a problem the current Blob URL approach already handles. Doesn't address desktop native dialog or reveal.
- **Integration effort:** Low, but unnecessary.
- **Risks:** Extra dependency with no benefit.

## Recommendation

**Direction:** Adopt (existing solution)

The `exportSession.ts` module already satisfies all functional requirements. The implementation approach — pure string generation for Markdown, Blob URL for web downloads, Electron IPC for desktop native dialogs — is correct and matches the cross-runtime architecture (web/desktop/VS Code). No new libraries are needed.

## Sources of Information

- `packages/ui/src/lib/exportSession.ts` — full export implementation with `formatSessionAsMarkdown`, `downloadAsMarkdown`, `saveAsMarkdownDesktop`, `revealExportedMarkdown`, `buildExportFilename`.
- `packages/ui/src/components/session/sidebar/SessionNodeItem.tsx:413` — context menu trigger for export.
- `packages/ui/src/lib/desktop.ts` — `saveDesktopMarkdownFile` and `revealDesktopPath` IPC wrappers.
- `packages/web/server/index.js` — server-side `/api/vscode/save-markdown` endpoint.
- All locale files under `packages/ui/src/lib/i18n/messages/` contain `sessions.sidebar.session.export.*` keys.

## Open Questions

1. Should batch export (multiple sessions at once) be supported? Not in current requirements but a natural extension.
2. Should export include full message parts (tool calls, images, code blocks with syntax highlighting) beyond just text parts? Current implementation only extracts text parts.

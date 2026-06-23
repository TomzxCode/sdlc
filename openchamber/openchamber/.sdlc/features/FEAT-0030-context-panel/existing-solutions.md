---
issue: ""
title: "Context Panel"
status: draft
---

# Existing Solutions: Context Panel

## Overview

A complete context panel implementation already exists in the codebase. `packages/ui/src/components/layout/ContextPanel.tsx` provides the resizable panel shell with tabs (files, diff, plan, browser), while `packages/ui/src/components/layout/ContextSidebarTab.tsx` (exported as `ContextPanelContent`) delivers the full token usage overview, message statistics, per-message token details, context breakdown by role, and raw message JSON inspector. The recommended direction is to document and refine the existing implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `ContextPanel`, `ContextSidebarTab`, `ContextPanelContent`, `token`, `cost`, `pricing`, `tokenBreakdown`, `extractTokenBreakdown`, `computeContextBreakdown` |
| Open-source | Yes | `cost-katana`, `opencode-token-tracker`, `codeburn`, `opencode-quota-sidebar`, `@assistant-ui/react` |
| Commercial / SaaS | Yes | Helicone, Langfuse, Datadog LLM cost, FutureAGI, Portkey |
| Standards / protocols | No | N/A |
| Reference material | Yes | OpenCode SDK message token types, models.dev pricing data |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal `ContextPanel` + `ContextSidebarTab` | Internal | MIT | Production | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07 | NFR-01 (performance under streaming) |
| `opencode-token-tracker` (OpenCode plugin) | Plugin | MIT | Active | FR-01 (partial), FR-07 | OpenCode TUI plugin, not web UI; toast-based, no raw JSON inspector |
| `codeburn` | CLI | MIT | Active | FR-01 (token visualization) | CLI/TUI only; external tool, not embeddable |
| `cost-katana` | Library | MIT | Active | FR-07 (cost tracking) | Proxy/SDK wrapper; requires server changes; no UI |
| `opencode-quota-sidebar` | Plugin | MIT | Active | FR-01 (quota sidebar) | OpenCode TUI sidebar plugin; unrelated to per-session context panel |

## Evaluation

### Existing internal ContextPanel + ContextSidebarTab

- **Strengths:** Full implementation across two components. `ContextPanel.tsx:1-2395` provides the resizable panel shell with: min/max width constraints (380-1400px), draggable resize handle, multi-tab support (files, diff, plan, browser), tab reordering via SortableTabsStrip, preview-browser with console, URL bar, and responsive behavior. `ContextSidebarTab.tsx:1-604` (exported as `ContextPanelContent`) delivers: token breakdown display showing input/output/reasoning/cache timestamps (FR-01), percentage usage bar with color coding (green -> warning at 80%) (FR-01), session statistics grid (message count, user/assistant counts, cost estimate) (FR-02), per-message raw JSON inspector with expandable/collapsible rows (FR-04), syntax-highlighted JSON via react-syntax-highlighter (FR-04), copy-to-clipboard for raw message JSON, context breakdown by role (user/assistant/tool/other) with segmented bar and percentage labels (FR-05). The `extractTokenBreakdown` function at `ContextSidebarTab.tsx:68-107` parses `tokens` from OpenCode SSE events. `computeContextBreakdown` at line 197 computes character-based breakdown by role with a 4:1 char-to-token approximation. `formatNumber`, `formatMoney`, `formatDateTime` utilities handle display formatting. Client-side cost via `totalAssistantCost` at line 336 with `resolveProviderAndModel` at line 258. The header-level context usage indicator (FR-06) appears in the chat header via the `context-usage` command palette entry. The `--oc-context-panel-width` CSS variable at `ContextPanel.tsx:2284` is used by inline comments for responsive width.
- **Weaknesses:** NFR-01 states the panel should not re-render on every streaming delta. The current implementation reads `sessionMessages` directly which could cause re-renders during streaming. Batching updates or memoization may be needed. Cost estimates are client-side per FR-07, using `(message.info as { cost?: unknown }).cost` from SSE events which may not cover all model pricing. The `computeContextBreakdown` char-to-token ratio of 4:1 is a rough approximation.
- **Integration effort:** Low. Already wired into `MainLayout.tsx` and toggled from the header `ContextPanel` button.
- **Cost:** Free (MIT, existing code).
- **Risks:** Re-render performance during high-frequency streaming (NFR-01). The panel already triggers on session changes and may need `React.memo` or store selector optimization.

### opencode-token-tracker (OpenCode plugin)

- **Strengths:** Real-time toast notifications for token usage. Budget controls. Session statistics. CLI query tool.
- **Weaknesses:** OpenCode TUI plugin, not web UI. Cannot be integrated into React components. No JSON inspector. No per-message breakdown.
- **Integration effort:** N/A (separate plugin ecosystem).
- **Cost:** Free (MIT).
- **Risks:** Not relevant (different runtime).

### codeburn

- **Strengths:** Beautiful TUI dashboard showing token usage across 25 AI coding tools. Per-task, per-model, per-provider breakdown.
- **Weaknesses:** CLI/TUI only. External tool reading session data from disk. Cannot be embedded in OpenChamber.
- **Integration effort:** N/A (external tool).
- **Cost:** Free (MIT).
- **Risks:** Not relevant.

## Recommendation

**Direction:** Adopt and extend (refine existing implementation)

The existing `ContextPanel` and `ContextSidebarTab` implementation satisfies all functional requirements (FR-01 through FR-08). The work needed:
- Verify NFR-01: ensure the panel uses stable selectors that do not cause re-render on every streaming delta. Consider extracting token display into a memoized child component that only reads from the last completed message's token data
- Review the cost estimation accuracy in `ContextSidebarTab.tsx:336-338` against model pricing data
- Ensure the header-level context usage indicator (FR-06) is wired and visible
- Confirm per-session cost scoping (FR-08) — the `viewModel` is already scoped to `currentSessionId`

No external libraries are needed. The implementation correctly sources token data from OpenCode SSE events per the constraint.

## Sources of Information

- `packages/ui/src/components/layout/ContextPanel.tsx:1-2395` — panel shell with tabs, resize, preview
- `packages/ui/src/components/layout/ContextSidebarTab.tsx:1-604` — token display, stats, JSON inspector
- `packages/ui/src/sync/session-ui-store.ts:593-611` — `AssistantTokens` type with reasoning/cache fields
- `packages/ui/src/components/layout/Header.tsx:1391-1443` — context panel toggle buttons
- `packages/ui/src/components/mini-chat/MiniChatLayout.tsx:163-184` — duplicate token extraction logic
- `packages/ui/src/components/layout/VSCodeLayout.tsx:598-643` — duplicate token extraction logic
- `packages/ui/src/stores/useUIStore.ts` — context panel state management
- `packages/ui/src/lib/i18n/messages/en.ts:851` — context panel i18n keys
- opencode-token-tracker: <https://github.com/tongsh6/opencode-token-tracker>
- codeburn: <https://github.com/getagentseal/codeburn>
- cost-katana: <https://www.npmjs.com/package/cost-katana>

## Open Questions

1. Should the total cost estimate include both input and output tokens, and is the cost field populated by the OpenCode SDK or an SSE event?
2. Is the `computeContextBreakdown` char-to-token ratio (4:1) accurate for the models users are most likely to use?
3. Should the context panel's JSON inspector respect the same theme syntax coloring as the code editor?
4. How should the context panel update when streaming is in progress without causing layout shifts?
5. Should the cost display vary by provider (OpenAI per-token, Anthropic per-character, etc.)?

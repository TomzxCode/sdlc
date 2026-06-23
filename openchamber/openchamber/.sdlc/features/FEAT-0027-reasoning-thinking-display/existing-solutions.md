---
issue: ""
title: "Reasoning / Thinking Display"
status: draft
---

# Existing Solutions: Reasoning / Thinking Display

## Overview

A full solution for rendering expandable/collapsible reasoning blocks in chat messages already exists in the codebase. `packages/ui/src/components/chat/message/parts/ReasoningPart.tsx` provides `ReasoningTimelineBlock`, `ReasoningPart`, and `MergedReasoningPart` with animated expand/collapse, summary preview, streaming-aware auto-expand, and the `cleanReasoningText` sanitizer. The recommended direction is to document and refine the existing implementation rather than adopting an external library.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `reasoning`, `thinking`, `cleanReasoningText`, `ReasoningPart`, `ReasoningTimelineBlock`, `MergedReasoningPart`, `groupReasoningBlocks` |
| Open-source | Yes | `@assistant-ui/react` reasoning component, `@llamaindex/chat-ui`, `llm-ui`, `assistant-ui` reasoning, Open WebUI reasoning patterns |
| Commercial / SaaS | No | N/A |
| Standards / protocols | Yes | OpenCode SDK `reasoning` part type (from `@opencode-ai/sdk/v2`) |
| Reference material | Yes | VSCode Copilot reasoning fold pattern, assistant-ui docs, Open WebUI `<details type="reasoning">` spec |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing in-codebase `ReasoningPart.tsx` | Internal | MIT | Production | FR-01, FR-02, FR-03, FR-07 | FR-04 (per-turn merged view done), FR-05 (user toggle not wired into settings yet), FR-06 |
| `@assistant-ui/react` Reasoning component | Library | MIT | Active | FR-01, FR-02, FR-03 | Not in project; heavyweight dependency; full chat framework |
| `llm-ui` | Library | MIT | Active | FR-01 (partial) | No collapsible reasoning block; focused on markdown streaming |
| Open WebUI reasoning pattern | Reference | MIT | N/A | FR-01, FR-04 | Documentation pattern only (`<details type="reasoning">`); no code to adopt |

## Evaluation

### Existing in-codebase ReasoningPart.tsx

- **Strengths:** Fully implemented with: animated expand/collapse via `motion` library (already in deps), summary generation (80 char preview with markdown stripping), streaming-aware auto-expand, merged per-turn view (`MergedReasoningPart`), keyboard navigation, `cleanReasoningText` sanitizer, `stripMarkdown` utility, i18n support across 8 languages. Tests exist in `ReasoningPart.test.tsx`. The `groupReasoningBlocks` flag in `useUIStore` controls merged vs per-part rendering. The `showReasoningTraces` setting exists in settings UI (`packages/ui/src/components/sections/openchamber/OpenChamberVisualSettings.tsx:1538`).
- **Weaknesses:** The user toggle for show/hide reasoning by default (FR-05) is visible in settings but may not be fully wired to the event pipeline. Keyboard navigation for reasoning mode in model selector (FR-06) is partially implemented in `ModelControls.tsx:112` but may need refinement.
- **Integration effort:** Low. The components are already wired into `MessageBody.tsx` and rendered at line 1594-1612. Refinement only.
- **Cost:** Free (MIT, existing code).
- **Risks:** Low. Already in production across all runtimes (web, Electron, VSCode).

### @assistant-ui/react Reasoning

- **Strengths:** Dedicated `ReasoningRoot`, `ReasoningTrigger`, `ReasoningContent`, `ReasoningText` primitives. Well-documented. Includes streaming state awareness.
- **Weaknesses:** Requires adopting the entire assistant-ui framework. Would conflict with the existing Zustand/OpenCode SDK architecture. Not compatible with the existing `Part`-based message model.
- **Integration effort:** Very high. Would require rewriting the message rendering layer.
- **Cost:** Free (MIT). However the assistant-ui styled theme requires shadcn/ui setup.
- **Risks:** Architectural incompatibility with the existing sync pipeline and `@opencode-ai/sdk` part types.

## Recommendation

**Direction:** Adopt and extend (refine existing implementation)

The existing code in `ReasoningPart.tsx` already satisfies FR-01, FR-02, FR-03, and FR-07. The work needed is:
- Verify FR-05 (user toggle for showing/hiding reasoning by default) is wired from `useUIStore` -> settings -> component behavior
- Verify FR-06 keyboard navigation for thinking mode in model selector (`ModelControls.tsx`)
- FR-04 (per-turn merged view) is already implemented via `MergedReasoningPart` and the `groupReasoningBlocks` store flag

No external library adoption is warranted given the production-ready internal implementation.

## Sources of Information

- `packages/ui/src/components/chat/message/parts/ReasoningPart.tsx:1-542` — full implementation
- `packages/ui/src/components/chat/message/parts/ReasoningPart.test.tsx:1-88` — existing tests
- `packages/ui/src/components/chat/ModelControls.tsx:112` — reasoning capability toggle in model selector
- `packages/ui/src/components/sections/openchamber/OpenChamberVisualSettings.tsx:1538` — show reasoning traces setting
- `packages/ui/src/sync/session-ui-store.ts:593` — `AssistantTokens` type with reasoning
- `packages/ui/src/stores/useUIStore.ts` — `groupReasoningBlocks` and `showReasoningTraces` state
- assistant-ui reasoning docs: <https://www.assistant-ui.com/docs/ui/reasoning>
- Open WebUI reasoning tag spec: <https://docs.openwebui.com/features/chat-conversations/chat-features/reasoning-models>

## Open Questions

1. Is `showReasoningTraces` currently persisted and respected across sessions, or does it reset on reload?
2. Does `groupReasoningBlocks` default to true or false, and does it match the VSCode Copilot merged pattern?
3. Should the reasoning toggle setting be per-session or global?

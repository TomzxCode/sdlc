---
issue: ""
title: "Model Picker"
status: draft
---

# Existing Solutions: Model Picker

## Overview

The codebase already has a mature model picker implementation in `packages/ui/src/components/model-picker/ModelPickerList.tsx` with provider grouping, favorites, recent models, hidden models, search, keyboard navigation, and drag-to-reorder. Model metadata is sourced from models.dev (an open-source database built by the same team behind OpenCode) via a server-side proxy, with fallback to OpenCode SDK provider data. The recommendation is to adopt the existing implementation with targeted enhancements rather than build from scratch or adopt an external library.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/components/model-picker/`, `packages/ui/src/stores/useUIStore.ts`, `packages/ui/src/stores/useConfigStore.ts`, `packages/web/server/lib/opencode/openchamber-routes.js` |
| Open-source | Yes | models.dev, OpenRouter API, RightModel.dev, RubyLLM model registry |
| Commercial / SaaS | Yes | OpenRouter model picker component |
| Standards / protocols | Yes | AI SDK model ID format, models.dev TOML schema |
| Reference material | Yes | Vercel AI SDK provider patterns, OpenCode documentation |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing ModelPickerList + useUIStore | Internal | MIT | Mature | FR-01 through FR-08 | FR-09 (model cost indicators from models.dev) |
| models.dev API | API / Database | MIT | Mature | FR-01, FR-08, FR-09 | Not a UI component; raw data source |
| OpenRouter Model Picker | Library | MIT | Active | FR-01, FR-05 | Tied to OpenRouter; no favorites/hide/recent |
| @llamaindex/chat-ui | Library | MIT | Active | FR-01 | Not a model picker; general chat components |
| RightModel.dev | Web tool | MIT | Active | FR-08, FR-09 | Web-only; not embeddable |

## Evaluation

### Existing ModelPickerList + useUIStore

- **Strengths:** Already integrated with Zustand stores, theme system, icon sprite, @dnd-kit drag-to-reorder, keyboard navigation, search/filter, provider logos, favorites, hidden models, recent models, per-session and per-agent persistence, collapsible provider groups. Already used in `ModelControls`, `ModelSelector`, and `ModelMultiSelect`.
- **Weaknesses:** Cost indicators and capability icons (FR-08) are not fully wired to models.dev metadata. The models.dev data flows through `useConfigStore` but model-level capability display is incomplete.
- **Integration effort:** Low. The picker is already the primary model selection surface. The main gap is surfacing per-model cost/capability metadata from the existing models.dev fetch pipeline.
- **Cost:** Free (MIT).
- **Risks:** Low. Already shipping in production.

### models.dev API

- **Strengths:** Built by the same team (Anomaly). Provides pricing, context limits, capabilities (tool calling, reasoning, structured output, modalities), and provider logos. AI SDK compatible model IDs. Community-contributed TOML definitions. Used internally by OpenCode.
- **Weaknesses:** Not always up to date for brand-new models (community-driven). Requires a fetch + cache layer.
- **Integration effort:** Low. Server-side proxy already exists at `/api/openchamber/models-metadata`. Client-side fetch and cache is already in `useConfigStore`.
- **Cost:** Free (MIT).
- **Risks:** None significant. Backup: OpenCode SDK provider data for unsupported providers (already implemented).

### OpenRouter Model Picker

- **Strengths:** Ready-made React component for model selection. Pulls live model catalog from OpenRouter.
- **Weaknesses:** Tied to OpenRouter as provider. No favorites, hidden models, or recent models support. Cannot customize provider grouping or display. Would require replacing the entire existing UX.
- **Integration effort:** High. Would need to replace the existing picker and lose all current features.
- **Cost:** Free (MIT).
- **Risks:** Vendor lock-in to OpenRouter. Users would see OpenRouter model IDs and pricing, not their actual provider pricing.

## Recommendation

**Direction:** Adopt

The existing model picker implementation already covers FR-01 through FR-08. The primary gap is FR-09 (model cost indicators and capability icons sourced from models.dev). The models.dev integration is already partially wired — the server-side proxy and client-side fetch are in place. The remaining work is to merge the models.dev metadata into the `ModelPickerEntry` type and display it in the picker rows (e.g., cost badges, capability icons).

No external library adoption is warranted. The existing implementation is more feature-complete than any open-source alternative for this use case.

## Sources of Information

- `packages/ui/src/components/model-picker/ModelPickerList.tsx`: The core picker component with all current features.
- `packages/ui/src/stores/useUIStore.ts:558-561`: Store types for favorites, hidden, and recent models.
- `packages/web/server/lib/opencode/openchamber-routes.js:272-282`: Server-side models.dev proxy endpoint.
- `packages/ui/src/stores/useConfigStore.ts:18-19`: Client-side models.dev URL and proxy URL constants.
- `models.dev`: Community-maintained, MIT-licensed AI model database at `https://models.dev/api.json`.
- `packages/ui/src/components/sections/agents/ModelSelector.tsx`: Uses ModelPickerList for agent model selection.

## Open Questions

1. Should model cost display be a toggle (show/hide) or always visible in the picker?
2. Should capability icons (tool calling, reasoning, vision) be shown as small badges, a compact icon row, or a tooltip on hover?

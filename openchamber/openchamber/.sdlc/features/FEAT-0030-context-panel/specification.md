---
title: "Context Panel"
status: done
---

# Specification: Context Panel

## Overview

The context panel is a multi-tab overlay in the main content area (`ContextPanel.tsx`). The context overview tab (`ContextPanelContent`) aggregates token and cost data from the session's messages. A compact context usage display in the header (`ContextUsageDisplay.tsx`) shows the current percentage at a glance.

## Architecture

```
ContextPanel (packages/ui/src/components/layout/ContextPanel.tsx)
    |
    +---> Context Overview tab
    |         +---> Token breakdown (input/output/reasoning/cache)
    |         +---> Usage percentage bar
    |         +---> Message statistics (count, cost, role breakdown)
    |         +---> Per-message token details
    |         +---> Raw message JSON inspector
    |
    +---> Other tabs: File Viewer, Diff, Plan, Preview, Browser

Header (packages/ui/src/components/layout/Header.tsx)
    +---> ContextUsageDisplay (compact percentage badge)
```

## Data Models

### ContextUsage

| Field | Type | Constraints | Description |
|---|---|---|---|
| inputTokens | number | not null | Total input tokens consumed |
| outputTokens | number | not null | Total output tokens generated |
| reasoningTokens | number | nullable | Reasoning tokens (o1/o3 models) |
| cacheTokens | number | nullable | Cached input tokens |
| maxTokens | number | not null | Context window limit |
| estimatedCost | number | nullable | Estimated cost in USD |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Location | Overlay panel (not sidebar) | Full width for detailed inspection; does not permanently consume sidebar space |
| Token source | SSE events from OpenCode | Live data without additional API calls |
| Cost calculation | Client-side from model pricing | No server-side cost tracking dependency |

## Risks and Unknowns

1. Model pricing data may become stale if providers change rates
2. Token counting accuracy depends on provider reporting

## Out of Scope

- Budget limits or spending caps
- Historical cost tracking across sessions
- Export of usage reports

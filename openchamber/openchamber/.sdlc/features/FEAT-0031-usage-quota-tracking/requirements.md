---
title: "Usage & Quota Tracking"
status: draft
---

# Requirements: Usage & Quota Tracking

## Overview

OpenChamber tracks AI provider usage metrics including rate limits, token consumption, quota balances, and pace indicators. Users can see how much of their provider quota has been consumed, view reset times in their local timezone, and monitor usage across multiple providers.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Cost-conscious developers | Monitor API spending and quota consumption |
| Free-tier users | Track rate limit proximity to avoid throttling |
| Teams | Aggregate usage visibility across providers |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display usage metrics per AI provider (tokens used, quota remaining). |
| FR-02 | Must | The system shall display rate limit status with progress bars. |
| FR-03 | Must | The system shall show pace indicators predicting when quota will be exhausted. |
| FR-04 | Must | The system shall display quota reset times in the user's local timezone. |
| FR-05 | Should | The system shall support usage tracking across multiple providers (OpenRouter, Wafer.ai, etc.). |
| FR-06 | Should | The system shall guard against non-finite quota percentages to prevent UI glitches. |
| FR-07 | May | The system shall support model family breakdowns within a provider. |
| FR-08 | Must | The system shall support quota tracking for the following providers: openai/codex, claude (anthropic), google, github-copilot, github-copilot-addon, kimi-for-coding, nano-gpt, openrouter, zai-coding-plan, zhipuai-coding-plan, minimax-coding-plan, minimax-cn-coding-plan, ollama-cloud, wafer. |
| FR-09 | Must | The system shall display current period usage data only, with no historical aggregation. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Missing or malformed quota data shall be handled gracefully without UI errors. |
| NFR-02 | Should | Performance | Usage data polling shall not interfere with streaming performance. |

## Constraints

- Quota data comes from provider-specific APIs via server-side quota modules
- Provider modules live in `packages/web/server/lib/quota/`
- Usage display uses progress bars, cards, and pace indicators
- Each provider fetches live snapshots

## Acceptance Criteria

- [ ] FR-01: Given a provider with usage data, the settings page shows tokens used and quota remaining
- [ ] FR-02: Given a provider with rate limits, progress bars show proximity to the limit
- [ ] FR-03: Given usage data over time, pace indicators predict exhaustion time
- [ ] FR-04: Given a quota reset time, it displays in the user's local timezone
- [ ] FR-05: Given multiple configured providers, usage is tracked per provider
- [ ] FR-06: Given non-finite quota percentages, the UI renders them gracefully without glitches
- [ ] FR-07: Given a provider with multiple models, per-model usage breakdowns are displayed
- [ ] FR-08: Given any of the 14 supported providers, quota data is tracked and displayed
- [ ] FR-09: Given usage data, only the current period is shown with no historical aggregation
- [ ] NFR-01: Given missing or malformed quota data, the UI handles it gracefully without errors
- [ ] NFR-02: Given active usage data polling, streaming performance is not degraded



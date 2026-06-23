---
issue: ""
title: "Usage & Quota Tracking"
status: draft
---

# Existing Solutions: Usage & Quota Tracking

## Overview

OpenChamber already has a complete server-side quota module (14 providers) and a Zustand-based UI store with progress bars, pace indicators, and per-provider usage views. The feature requirements map closely to this existing implementation, which was purpose-built for OpenCode's provider ecosystem. No external library provides the breadth of provider-specific APIs needed (Claude, Codex, Google, GitHub Copilot, Kimi, NanoGPT, OpenRouter, Z.AI, ZhipuAI, MiniMax, Ollama Cloud, Wafer). External tools like Delimiter, ai-sdk-rate-limiter, and llm-limits-tracker offer complementary monitoring but operate at a different layer (SDK instrumentation vs. server-side API polling) and don't cover OpenCode's specific provider set.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/quota/` (14 provider modules, routes, utils), `packages/ui/src/stores/useQuotaStore.ts`, `packages/ui/src/components/sections/usage/` (PaceIndicator, UsageCard, UsageProgressBar, UsagePage, UsageSidebar) |
| Open-source | Yes | npm search for quota/rate-limit tracking for AI providers |
| Commercial / SaaS | Yes | Delimiter.app (rate-limit monitoring SaaS) |
| Standards / protocols | No | Each provider has its own quota API, no standard format |
| Reference material | Yes | OpenCode's own `opencode-quota` plugin, @bytespell/model-provider-usage-limits, @metyatech/ai-quota, ai-sdk-rate-limiter, llm-limits-tracker |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber's existing quota module (internal) | Internal | MIT | Production (v1.11.7) | FR-01 through FR-09 | Must add model family breakdown (FR-07) |
| @metyatech/ai-quota | Library | MIT | Active (v1.x) | Claude, Gemini, Copilot, Codex quota | Only 4 providers, no UI components |
| @bytespell/model-provider-usage-limits | Library | MIT | Early (v0.x) | Anthropic, Copilot, OpenAI usage + pace tracking | 3 providers, no UI, tightly coupled to its router |
| ai-sdk-rate-limiter | Library | MIT | Active | Rate limiting + cost tracking for AI SDK calls | SDK-level middleware, doesn't poll provider quota APIs |
| Delimiter (delimiter.app) | SaaS | Proprietary | Active | Real-time rate limit monitoring via HTTP header interception | SaaS dependency, API keys sent to third-party, no provider billing poll |
| llm-limits-tracker | Library | MIT | Active (v0.x) | Local dashboard for Claude, GPT, Gemini, OpenRouter, Groq | Standalone dashboard, not embeddable, probes keys directly |
| overbit/opencode-quota | Library (plugin) | MIT | Active | OpenCode-specific quota plugin with TUI and /quota commands | Terminal-only (CLI plugin), no UI components |
| mil-orb/claude-gauge | Library (plugin) | MIT | Active | Claude Code status-line quota gauge | Claude Code only, statusline plugin |

## Evaluation

### OpenChamber's existing quota module (internal)

- **Strengths:** Already covers all 14 required providers. Server-side polling via Express routes. Zustand store with settings persistence. UI components (PaceIndicator, UsageCard, UsageProgressBar, UsageSidebar, UsagePage) already built. Graceful fallback on fetch failure. Auto-refresh with configurable interval.
- **Weaknesses:** FR-07 (model family breakdowns within a provider) not yet implemented. Pace indicator needs per-model consumption data that providers rarely expose.
- **Integration effort:** Low — already integrated and in production.
- **Cost:** None (MIT, in-house).
- **Risks:** Provider API changes could break individual provider modules; mitigated by the modular provider pattern.

### @metyatech/ai-quota

- **Strengths:** Covers Claude, Gemini, Copilot, Codex. Provides MCP server mode for agent self-awareness. JSON output for scripting.
- **Weaknesses:** Only 4 of the 14 required providers. No React UI components. CLI-focused. Requires provider-specific credential files.
- **Integration effort:** Medium — could be used as reference for provider patterns but doesn't reduce overall work.
- **Cost:** Free (MIT).
- **Risks:** Low adoption (niche), small community.

### Delimiter (SaaS)

- **Strengths:** Auto-detects all AI providers at the network layer via HTTP header interception. Real-time monitoring with health cards, usage bars, and timeline charts. Slack/Discord alerts at configurable thresholds.
- **Weaknesses:** SaaS dependency — API keys flow through Delimiter's proxy. Covers rate limits only, not quota balances (separate provider connection needed). Doesn't support OpenCode-specific providers (Kimi, NanoGPT, Z.AI, ZhipuAI, MiniMax, Ollama Cloud, Wafer).
- **Integration effort:** Low (2 lines of code) for basic SDK, but provider connections require per-provider OAuth setup.
- **Cost:** Unknown (proprietary SaaS; likely usage-based pricing).
- **Risks:** Third-party data access, vendor lock-in, doesn't cover the full provider set needed.

## Recommendation

**Direction:** Adopt and extend (build on existing internal module)

The existing quota infrastructure already meets FR-01 through FR-06, FR-08, and FR-09. The provider module pattern is proven across 14 providers. The gap is FR-07 (model family breakdowns), which requires extending individual providers to return per-model data where the provider API supports it. For reference patterns, study how @metyatech/ai-quota handles Google Gemini's per-model quotas and how @bytespell/model-provider-usage-limits computes pace deltas. The external libraries are useful reference implementations but none cover the full provider set, and migrating to them would lose the existing routing, UI, and settings infrastructure.

## Sources of Information

- @metyatech/ai-quota (`github.com/metyatech/ai-quota`): Shows how to fetch per-model Gemini quotas and exposes an MCP tool for agent self-awareness of remaining quota.
- @bytespell/model-provider-usage-limits (`github.com/bytespell-oss/model-provider-usage-limits`): Introduces `paceDelta` calculation — comparing actual usage vs. expected pace within a window — which is directly applicable to FR-03.
- ai-sdk-rate-limiter (`github.com/piyushgupta344/ai-sdk-rate-limiter`): Comprehensive sliding-window rate limiter with cost tracking and circuit breaker. Relevant for SDK-level enforcement but not quota display.
- Delimiter (`github.com/delimiterapp/delimiter`): Reference for UI patterns: health cards, progress bars, timeline charts for rate-limit monitoring.

## Open Questions

1. Should pace indicators (FR-03) estimate from historical usage patterns or from provider-reported window progress? The former requires aggregating our own data over time; the latter depends on provider API support.
2. Can per-provider model family breakdowns (FR-07) be derived from the OpenCode session token usage data (which the server already has access to) rather than from provider quota APIs?

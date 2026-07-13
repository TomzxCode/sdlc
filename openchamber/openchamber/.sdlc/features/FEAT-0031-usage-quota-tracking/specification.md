---
title: "Usage & Quota Tracking"
status: done
---

# Specification: Usage & Quota Tracking

## Overview

Quota tracking is split between server-side provider integrations (`packages/web/server/lib/quota/`) and client-side display components (`packages/ui/src/components/sections/usage/`). Each provider has a dedicated module that fetches quota data from the provider's API. The UI renders progress bars, pace indicators, and usage cards.

## Architecture

```
Usage Settings UI (packages/ui/src/components/sections/usage/)
    +---> UsagePage
    +---> UsageSidebar (provider navigation)
    +---> UsageCard (per-provider summary)
    +---> UsageProgressBar (rate limit visualization)
    +---> PaceIndicator (exhaustion prediction)
    |
    v  REST calls
Quota Provider Registry (packages/web/server/lib/quota/)
    +---> Provider-specific modules (OpenRouter, Wafer.ai, etc.)
    |
    v  HTTP
Provider APIs (OpenRouter, etc.)
```

## Data Models

### ProviderUsage

| Field | Type | Constraints | Description |
|---|---|---|---|
| provider | string | PK | Provider name |
| used | number | not null | Tokens or credits used |
| limit | number | not null | Total quota |
| resetAt | timestamp | nullable | When quota resets |
| percentage | number | not null | Usage as percentage |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Provider pattern | Registry with per-provider modules | Easy to add new providers without modifying core |
| Display | Progress bars + pace indicators | Visual and actionable; users can see at a glance |
| Defensive rendering | Guard non-finite values | Provider APIs can return inconsistent data; UI must not break |

## Risks and Unknowns

1. Provider APIs may change without notice
2. Some providers do not expose quota endpoints at all

## Out of Scope

- Billing or payment integration
- Usage alerts or notifications
- Historical usage charts

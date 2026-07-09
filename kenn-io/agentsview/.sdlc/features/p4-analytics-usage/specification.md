---
title: "Analytics & Cost Tracking"
status: draft
---

# Specification: Analytics & Cost Tracking

## Overview

Analytics queries are implemented as SQL aggregations over the sessions and messages tables. Cost tracking uses a model pricing catalog with LiteLLM integration for dynamic pricing and an offline fallback. Health signals are computed post-sync using heuristic rules on session content.

## Architecture

```
SQLite DB → Analytics Queries → REST API → Frontend Charts
                  ↓
           Pricing Catalog (LiteLLM + offline)
                  ↓
           Cost Calculator (cache-aware)
                  ↓
           Usage/Tracking API
```

## API Contracts

### GET /api/v1/analytics/summary
**Response:** Summary statistics (sessions, messages, tokens, costs)

### GET /api/v1/analytics/activity
**Query Parameters:** `since`, `until`, `granularity`, `agent`, `project`
**Response:** Activity time series

### GET /api/v1/analytics/heatmap
**Response:** Heatmap data for the web UI

### GET /api/v1/usage/summary
**Response:** Per-model cost breakdown, total spend, token counts

## Data Models

### Usage Stats

| Field | Type | Description |
|---|---|---|
| session_id | TEXT | Session identifier |
| agent | TEXT | Agent type |
| model | TEXT | Model name |
| input_tokens | INTEGER | Input token count |
| output_tokens | INTEGER | Output token count |
| cache_creation_tokens | INTEGER | Cache creation tokens |
| cache_read_tokens | INTEGER | Cache read tokens |
| cost_usd | REAL | Estimated cost in USD |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Pricing source | LiteLLM catalog + offline fallback | Covers most models; works offline |
| Cost calculation | Cache-aware (creation + read tokens) | Reflects actual billing for providers with prompt caching |
| Timezone | Configurable per-query | Supports global users and teams |
| Session classification | ML classifier in DB | Distinguishes automated vs human-driven sessions |

## Risks and Unknowns

1. LiteLLM API dependency for pricing updates
2. ML classifier accuracy varies by agent type

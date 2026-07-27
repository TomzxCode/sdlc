---
title: "Analytics & Cost Tracking"
status: done
---

# Test Plan: Analytics & Cost Tracking

## Scope

Tests cover activity heatmaps, token usage tracking, cost estimation, daily cost summaries, session health signals, session stats, timezone-aware bucketing, AI-generated insights, session classification, and velocity metrics.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Activity heatmap computed over time range | Session data + time range | Heatmap data points |
| TC-2 | Token usage tracked per session and model | Parsed usage events | Correct token counts |
| TC-3 | Cost estimated from pricing catalog | Token counts + model | Cost in USD |
| TC-4 | Daily cost summary with per-model breakdown | Multiple sessions with usage | Grouped cost by day and model |
| TC-5 | Session health signal computation | Session messages | Signal scores |
| TC-6 | Session stats with distribution metrics | Session data | Statistical distributions |
| TC-7 | Timezone-aware date bucketing | UTC timestamps + timezone | Bucketed by local date |
| TC-8 | Pricing match from LiteLLM catalog | Model name + usage | Matched pricing |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | Activity query integration | Sessions with activity data | Correct activity metrics |
| TC-10 | Usage rollup integration | Sessions with token data | Accurate cost rollups |

## Test Files

- `internal/activity/activity_test.go` - Activity aggregation tests
- `internal/activity/query_test.go` - Activity query tests
- `internal/activity/sessions_test.go` - Session activity tests
- `internal/activity/usage_test.go` - Usage activity tests
- `internal/db/usage_test.go` - Usage database queries
- `internal/db/activity_test.go` - Activity database queries
- `internal/db/activityreport_test.go` - Activity report tests
- `internal/db/analytics_test.go` - Analytics query tests
- `internal/db/pricing_test.go` - Pricing match tests
- `internal/db/stats_test.go` - Stats query tests
- `internal/db/trends_test.go` - Trends query tests
- `internal/db/usage_perf_test.go` - Usage performance tests
- `internal/pricing/litellm_test.go` - LiteLLM pricing tests
- `internal/server/activity_test.go` - HTTP activity handler tests
- `internal/server/activity_report_test.go` - Activity report handler tests
- `internal/server/analytics_test.go` - Analytics handler tests
- `internal/server/usage_test.go` - Usage handler tests
- `internal/service/usage_test.go` - Service layer usage tests

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-11 | No token data for session | Cost shows as unavailable |
| TC-12 | Model not in pricing catalog | Unpriced model flagged |
| TC-13 | Empty session data | Zero-filled results |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-9 |
| FR-2 | TC-2, TC-10 |
| FR-3 | TC-3, TC-8 |
| FR-4 | TC-4 |
| FR-5 | TC-5 |
| FR-6 | TC-6 |
| FR-7 | TC-7 |

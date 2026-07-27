---
title: "REST API & Web Frontend"
status: done
---

# Test Plan: REST API & Web Frontend

## Scope

Tests cover REST API endpoints, Svelte SPA rendering, session listing/filtering/pagination, session detail view, analytics dashboard, usage tracking, activity reports, full-text search UI, SSE live updates, keyboard navigation, starring/trash, message pinning, recent edits feed, and settings management.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Session list endpoint with cursor pagination | Filter params + cursor | Paginated session list |
| TC-2 | Session detail returns full message history | Session ID | Complete message tree |
| TC-3 | SSE stream sends live updates | Sync event | Event received by client |
| TC-4 | Frontend session list renders correctly | Session data array | Rendered list items |
| TC-5 | Frontend message content renders correctly | Message data | Rendered messages |
| TC-6 | Frontend analytics dashboard renders | Analytics data | Charts and metrics displayed |
| TC-7 | Frontend usage page renders | Usage data | Cost breakdown displayed |
| TC-8 | Keyboard navigation works | j/k keypresses | Selection moves |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | Frontend-backend full integration | Server running | SPA loads and queries API |
| TC-10 | E2E session browsing | Test data | Full browse flow works |
| TC-11 | E2E search flow | Indexed sessions | Search results displayed |

## Test Files

- `internal/server/sessions_test.go` - Session API handler tests
- `internal/server/session_mgmt_test.go` - Session management tests
- `internal/server/session_usage_test.go` - Session usage API tests
- `internal/server/session_stats_test.go` - Session stats API tests
- `internal/server/search_test.go` - Search API tests
- `internal/server/analytics_test.go` - Analytics API tests
- `internal/server/activity_test.go` - Activity API tests
- `internal/server/usage_test.go` - Usage API tests
- `internal/server/server_test.go` - Server lifecycle tests
- `internal/server/auth_test.go` - Auth middleware tests
- `internal/server/middleware_test.go` - Middleware tests
- `internal/server/export_test.go` - Export handler tests
- `internal/server/starred_test.go` - Starred session tests
- `internal/server/pins_test.go` - Pinned message tests
- `internal/server/spa_test.go` - SPA serving tests
- `internal/server/broadcaster_test.go` - SSE broadcaster tests
- `internal/server/huma_routes_sessions_test.go` - Session route tests
- `frontend/src/lib/api/client.test.ts` - API client tests
- `frontend/src/lib/api/runtime.test.ts` - Runtime tests
- `frontend/src/lib/stores/sessions.test.ts` - Session store tests
- `frontend/src/lib/stores/search.test.ts` - Search store tests
- `frontend/src/lib/stores/analytics.test.ts` - Analytics store tests
- `frontend/src/lib/stores/usage.test.ts` - Usage store tests
- `frontend/src/lib/stores/activity.test.ts` - Activity store tests
- `frontend/src/lib/components/sidebar/SessionList.test.ts` - Session list component
- `frontend/src/lib/components/content/MessageContent.test.ts` - Message content component
- `frontend/src/lib/components/analytics/AnalyticsPage.test.ts` - Analytics page component
- `frontend/src/lib/components/usage/UsagePage.test.ts` - Usage page component
- `frontend/e2e/session-list.spec.ts` - Session list e2e
- `frontend/e2e/usage.spec.ts` - Usage page e2e
- `frontend/e2e/navigation.spec.ts` - Navigation e2e

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1 |
| FR-2 | TC-9 |
| FR-3 | TC-1 |
| FR-4 | TC-2 |
| FR-5 | TC-6 |
| FR-6 | TC-7 |
| FR-8 | TC-11 |
| FR-9 | TC-3 |
| FR-10 | TC-8 |
| FR-11 | TC-1 |
| FR-12 | TC-2 |

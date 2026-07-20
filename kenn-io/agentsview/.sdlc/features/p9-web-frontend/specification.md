---
title: "REST API & Web Frontend"
status: done
---

# Specification: REST API & Web Frontend

## Overview

The REST API is registered in `internal/server/huma_route_groups.go` using the Huma v2 framework, which automatically generates an OpenAPI 3.1 schema. The frontend is a Svelte 5 SPA with runes-based reactivity, built with Vite+ and TypeScript. The SPA is embedded into the Go binary during build for single-binary deployment.

## Architecture

```
Browser → HTTP Server (Huma + Chi) → Service Backend → SQLite/PG/DuckDB
             ↓
        Embedded SPA (frontend/dist/)
             ↓
        SSE Broadcaster (live updates)
```

## Frontend Component Tree

```
App.svelte
├── ThreeColumnLayout
│   ├── AppHeader (search, nav)
│   ├── SessionList (sidebar)
│   │   └── SessionItem
│   ├── MessageList (content)
│   │   ├── MessageContent
│   │   ├── ToolBlock / CallGroup / ParallelGroup
│   │   ├── ThinkingBlock / CodeBlock / MermaidBlock
│   │   └── ActivityLane
│   └── SessionVitals (right panel)
├── AnalyticsPage
├── UsagePage
├── ActivityPage
├── TrendsPage
├── InsightsPage
├── PinnedPage
├── TrashPage
├── RecentEditsPage
└── SettingsPage
```

## API Contracts

### Core Routes (OpenAPI 3.1)

| Method | Path | Description |
|---|---|---|
| GET | /api/v1/sessions | List sessions |
| GET | /api/v1/sessions/{id} | Get session detail |
| GET | /api/v1/sessions/{id}/messages | List messages |
| GET | /api/v1/search | Full-text search |
| GET | /api/v1/analytics/summary | Analytics summary |
| GET | /api/v1/usage/summary | Usage summary |
| GET | /events | SSE events |

## Sequences

### SPA Load
```
1. Browser requests /
2. Server serves index.html with embedded SPA
3. SPA loads and calls GET /api/v1/sessions for initial data
4. SPA opens SSE connection to /events for live updates
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| API framework | Huma v2 | OpenAPI 3.1 native, code-first |
| Frontend framework | Svelte 5 (runes) | Lightweight, fast, reactive |
| Embedding | Build-time copy of frontend/dist | Single binary deployment |
| SSE | /events endpoint with Broadcaster | Real-time updates without polling |
| Routing | Client-side store-based router | SPA navigation without page reloads |
| i18n | Paraglide JS + inlang | Type-safe message catalogs |

## Risks and Unknowns

1. SPA bundle size growth over time
2. Browser compatibility with Svelte 5 runes

---
title: "REST API & Web Frontend"
status: done
---

# Requirements: REST API & Web Frontend

## Overview

The REST API and web frontend provide the primary user interface for agentsview. The API is built with the Huma framework (OpenAPI 3.1) and exposes endpoints for sessions, messages, search, analytics, usage, and administration. The frontend is a Svelte 5 SPA embedded in the Go binary, featuring session browsing, analytics dashboard, usage tracking, and settings.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Browse, search, and interact with session data through a web UI |
| API consumer | Integrate with agentsview via REST API |
| Developer | Build on top of agentsview's OpenAPI schema |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a REST API with OpenAPI 3.1 specification |
| FR-2 | Must | The system shall serve a Svelte 5 SPA embedded in the Go binary |
| FR-3 | Must | The system shall support session listing with rich filtering and cursor pagination |
| FR-4 | Must | The system shall support session detail view with full message history |
| FR-5 | Must | The system shall provide an analytics dashboard with charts and metrics |
| FR-6 | Must | The system shall provide a usage/cost tracking page |
| FR-7 | Must | The system shall provide an activity/concurrency report page |
| FR-8 | Must | The system shall provide a full-text search page |
| FR-9 | Must | The system shall provide SSE for live updates |
| FR-10 | Must | The system shall support keyboard navigation (j/k, Cmd+K search, ? shortcuts) |
| FR-11 | Must | The system shall support session starring and trash/restore |
| FR-12 | Must | The system shall support message pinning |
| FR-13 | Should | The system shall provide a recent edits feed showing files changed by agents |
| FR-14 | Should | The system shall support settings management via the web UI |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | API rejects requests with unrecognized Host headers (DNS rebinding protection) |
| NFR-2 | Must | Security | Server binds to 127.0.0.1 by default |
| NFR-3 | Should | Performance | Frontend bundle is embedded for single-binary deployment |

## Acceptance Criteria

- [ ] **FR-2**
    - **Given** the server is running
    - **When** a browser navigates to http://127.0.0.1:8080
    - **Then** the Svelte SPA is served and interactive
- [ ] **FR-10**
    - **Given** the session list is displayed
    - **When** j/k keys are pressed
    - **Then** the selection moves up/down in the list

## Open Questions

1. Should there be a mobile-responsive layout or is desktop-only sufficient?

---
title: "HTTP API Server"
status: draft
---

# Requirements: HTTP API Server

## Overview

The HTTP API Server is OpenCode's headless surface, letting any client (TUI, web, desktop, SDK, editor integrations) drive projects and sessions over HTTP.
It exposes multi-project, multi-session routes under a project-scoped namespace, plus config, provider, and agent resolution.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| SDK / editor authors | Stable, documented REST routes |
| Operators | Headless deployment on a known port; auth |
| Core team | Project-scoped routing; clean projection of messages and parts |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The server shall run headless on a configurable port (default 4096) via `serve`. |
| FR-02 | Must | The server shall support multiple projects and per-project sessions (`GET/POST /project`, `/project/:projectID/session...`). |
| FR-03 | Must | The server shall expose session lifecycle routes: create, init, abort, share/unshare, compact, revert/unrevert, delete. |
| FR-04 | Must | The server shall expose message routes that return `{ info, parts }` projections and accept new messages. |
| FR-05 | Must | The server shall expose permission resolution (`POST .../permission/:permissionID`) and file routes (`find/file`, `file`, `file/status`). |
| FR-06 | Should | The server shall resolve provider, config, and agent by directory query parameter. |
| FR-07 | Should | The server shall accept logs via `POST /log`. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Compatibility | The SDK shall be regenerable from the server routes via `./script/generate.ts`. |
| NFR-02 | Should | Security | Authenticated routes shall be enforceable for hosted/enterprise deployments. |

## Constraints

- Server routing is Hono-based and lives in `packages/server` and `packages/opencode/src/server`.
- Some directory-resolved routes (`/provider`, `/config`, `/project/:id/agent`, `/find/file`) are noted as awkward in the spec and may change.
- API/SDK changes require regenerating the SDK and related files.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** the server is started with `serve`
    - **When** no port is specified
    - **Then** it listens on port 4096
- [ ] **FR-02**
    - **Given** two initialized projects
    - **When** a client lists sessions per project
    - **Then** each project returns only its own sessions
- [ ] **FR-04**
    - **Given** a session with messages
    - **When** a client calls the message route
    - **Then** each item is returned as `{ info: Message, parts: Part[] }`
- [ ] **NFR-01**
    - **Given** a route change in `packages/opencode/src/server/server.ts`
    - **When** `./script/generate.ts` runs
    - **Then** the SDK and related files are regenerated to match

## Conflicts

None identified yet.

## Open Questions

1. Should the awkward directory-resolved routes be refactored into the project-scoped namespace?

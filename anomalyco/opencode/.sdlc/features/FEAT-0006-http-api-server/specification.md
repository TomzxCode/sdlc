---
title: "HTTP API Server"
status: done
---

# Specification: HTTP API Server

## Overview

A Hono-based server exposes project- and session-scoped REST routes over HTTP.
Routes project messages and parts, file access, permissions, and directory-resolved config/provider/agent lookups, and feeds SDK generation.

## Architecture

```
Client (TUI/Web/Desktop/SDK) ──HTTP──▶ Hono server (packages/server + opencode/src/server)
                                             │ routes: project, session, message,
                                             │ permission, file, provider, config, agent, log
                                             ▼
                                   Session Runtime + Storage (FEAT-0001)
```

## Data Models

The API projects server-side `Session`, `Message`, `Part`, and `File` shapes; it defines no new durable model.

## API Contracts

### GET /project -> Project[]
### POST /project/init -> Project
### GET /project/:projectID/session -> Session[]
### GET /project/:projectID/session/:sessionID -> Session
### POST /project/:projectID/session -> Session

| Field | Type | Required | Description |
|---|---|---|---|
| id | string | no | Optional session id |
| parentID | string | no | Optional parent session |
| directory | string | yes | Working directory |

### DELETE /project/:projectID/session/:sessionID
### POST /project/:projectID/session/:sessionID/init
### POST /project/:projectID/session/:sessionID/abort
### POST /project/:projectID/session/:sessionID/share
### DELETE /project/:projectID/session/:sessionID/share
### POST /project/:projectID/session/:sessionID/compact
### GET /project/:projectID/session/:sessionID/message -> { info: Message, parts: Part[] }[]
### GET /project/:projectID/session/:sessionID/message/:messageID -> { info: Message, parts: Part[] }
### POST /project/:projectID/session/:sessionID/message -> { info: Message, parts: Part[] }
### POST /project/:projectID/session/:sessionID/revert -> Session
### POST /project/:projectID/session/:sessionID/unrevert -> Session
### POST /project/:projectID/session/:sessionID/permission/:permissionID -> Session
### GET /project/:projectID/session/:sessionID/find/file -> string[]
### GET /project/:projectID/session/:sessionID/file -> { type: "raw" | "patch", content: string }
### GET /project/:projectID/session/:sessionID/file/status -> File[]
### POST /log
### GET /provider?directory=\<path\> -> Provider
### GET /config?directory=\<path\> -> Config
### GET /project/:projectID/agent?directory=\<path\> -> Agent
### GET /project/:projectID/find/file?directory=\<path\> -> File

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Malformed request body or path |
| 404 | NOT_FOUND | Project, session, or message not found |

## Sequences

### Submit a message

```
Client -> POST /project/:id/session/:sid/message
Server -> SessionV2.prompt (admit + wake)
Server -> 200 { info, parts }
Client -> poll/subscribe message route for streamed parts
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | Hono | Lightweight, typed routing with Effect integration |
| Projection | `{ info, parts }` per message | Uniform shape for streaming and history |
| SDK parity | Generated from routes via `script/generate.ts` | Keeps SDK and server in lockstep |

## Risks and Unknowns

1. Directory-resolved routes (`/provider`, `/config`, `/agent`, `/find/file`) are flagged as awkward and may move under the project namespace.
2. Hosted/enterprise auth on these routes needs explicit policy.

## Out of Scope

- Session runtime internals (see FEAT-0001).
- Generated SDK client (see FEAT-0008).

---
title: "Auth & Access Control"
status: draft
---

# Specification: Auth & Access Control

## Overview

Auth is mode-dependent. In `local_trusted` mode all local requests are implicit board; in `authenticated` mode the system uses session-based auth with user profiles, company memberships, and role-based access. The authorization engine enforces fine-grained action-on-resource gates. Agent API keys are hashed at rest and scoped to one company.

## Architecture

```
Request → authz middleware (assertBoard, assertCompanyAccess, assertAgent)
                │
                ├─ auth mode check (local_trusted vs authenticated)
                ├─ bearer token / session resolution
                ├─ company_id scoping
                └─ permission check (action on resource)
                │
                ▼
         Route handler (company-scoped context)
```

## Data Models

### auth / user

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | User ID |
| email | text | unique | User email |
| display_name | text | - | Display name |

### board_api_keys / agent_api_keys

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| key_hash | text | not null | Hashed key material |
| name | text | not null | Human label |
| last_used_at / revoked_at | timestamptz | null | Usage tracking |

### company_memberships

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id | uuid | FK, not null | Scoping |
| user_id | uuid | FK, not null | Member |
| role | text | not null | `owner \| admin \| member` |

### principal_permission_grants

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| principal_type / principal_id | - | - | Who gets the grant |
| permission | text | - | Action/resource pair |

## API Contracts

### POST /api/auth/login, POST /api/auth/logout, GET /api/auth/me

Session management.

### POST /companies/:companyId/invites, POST /invites/:inviteId/accept

Invite flow.

### POST /cli-auth/challenge, POST /cli-auth/respond

CLI authentication.

### POST /agents/:agentId/keys, POST /agents/:agentId/keys/:keyId/revoke

Agent API key management.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 401 | UNAUTHORIZED | Not authenticated |
| 403 | FORBIDDEN | Authenticated but not authorized for this action/resource |
| 404 | NOT_FOUND | Resource not found (company-scoped) |

## Sequences

### Authenticated request flow

```
Request → authz middleware → session cookie → resolve user → resolve company context → check permission → route handler or 403
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Auth modes | `local_trusted` + `authenticated` | Supports both single-user and multi-user deployments |
| Agent keys | Hashed at rest (bcrypt) | Standard practice for credential storage |
| Authz engine | Middleware-based action/resource gates | Consistent cross-cutting enforcement before route logic |
| Company scoping | Request-level `company_id` context | Prevents cross-company data access at framework level |

## Risks and Unknowns

1. Permission grant composition with role-based defaults has not been battle-tested in production.
2. Session management and token refresh semantics need hardening for production.

## Out of Scope

- Multi-board governance or role-based human permission granularity (Pro/Enterprise).
- OAuth2/OIDC federation for V1.
- SAML/SSO enterprise integration.

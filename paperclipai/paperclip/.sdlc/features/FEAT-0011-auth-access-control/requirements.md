---
title: "Auth & Access Control"
status: draft
---

# Requirements: Auth & Access Control

## Overview

Paperclip supports two deployment modes: `local_trusted` (implicit board, loopback) and `authenticated` (session-based with user profiles). Access control spans board-level management, company membership and roles, agent API keys (hashed at rest), principal permission grants, instance user roles, invite/join flows, CLI authentication, and a fine-grained authorization engine that gates actions on resources. The authorization layer is cross-cutting infrastructure used by every route handler.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Manage users, API keys, invites; configure deployment mode and instance settings |
| Human user | Authenticate, manage profile, accept invites, request company access |
| Agent | Authenticate via bearer API key for company-scoped operations |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support two deployment modes: `local_trusted` and `authenticated`. |
| FR-02 | Must | In `authenticated` mode, users shall authenticate with sessions and have user profiles. |
| FR-03 | Must | Agent API keys shall be hashed at rest with bcrypt or equivalent; plaintext shown once at creation. |
| FR-04 | Must | The system shall enforce company access boundaries: request-scoped `company_id` context checked on every protected route. |
| FR-05 | Must | The system shall support board API keys for programmatic board-level access. |
| FR-06 | Must | The system shall support CLI authentication challenges. |
| FR-07 | Must | The authorization middleware shall gate actions (create/read/update/delete/approve/etc.) on resources (company/agent/issue/etc.) per actor (board/user/agent). |
| FR-08 | Should | The system shall support instance user roles for multi-user deployments. |
| FR-09 | Should | The system shall support company membership management with roles and invites. |
| FR-10 | Should | The system shall support join requests for users requesting access to a company. |
| FR-11 | Should | The system shall support principal permission grants for fine-grained access beyond role-based defaults. |
| FR-12 | Should | The system shall support API key revocation and usage tracking (last_used_at). |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Agent API keys must not access other companies' data. |
| NFR-02 | Must | Security | Hashed keys must use a strong, salted algorithm (bcrypt). |
| NFR-03 | Must | Auditability | All user/access mutations (invite, role change, key create/revoke) write `activity_log`. |
| NFR-04 | Should | Performance | Auth middleware must complete in under 10ms p95. |

## Constraints

- `local_trusted` mode grants implicit board access without authentication.
- `authenticated` mode requires session-based auth with user resolution.
- Agent keys are scoped to exactly one company.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a `local_trusted` deployment
    - **When** any request is made from localhost
    - **Then** it is treated as board-level without explicit auth
- [ ] **FR-03**
    - **Given** a new agent API key creation
    - **When** the key is created
    - **Then** the hash is stored and the plaintext key is returned exactly once
- [ ] **FR-04**
    - **Given** an agent API key for company A
    - **When** a request targets company B's endpoint
    - **Then** the request is rejected with 403/404
- [ ] **FR-09**
    - **Given** a company owner
    - **When** they invite a user
    - **Then** the user receives an invitation and can accept to become a member
- [ ] **NFR-01**
    - **Given** the authorization middleware
    - **When** processing any API request
    - **Then** company boundaries are enforced before any business logic runs

## Conflicts

None identified yet.

## Open Questions

1. What is the full taxonomy of principal permission grants and how do they compose with role-based defaults?
2. How are instance user roles and company membership roles reconciled for cross-company board users?

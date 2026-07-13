---
title: "Environment Management"
status: done
---

# Specification: Environment Management

## Overview

Environments are company-scoped named configurations with key/value bindings. Values use the `${{ secrets.key }}` syntax for secret references, resolved at runtime by the secrets service. Environment leases grant agents temporary access. The resolver applies values in a defined overlay chain: project env → environment env → routine env → Paperclip runtime-owned keys.

## Architecture

```
Board → /api/companies/:companyId/environments (CRUD)
           │
           ▼
      environments table (company_id, name, env JSONB)
           │
           ▼
      environment_leases (agent_id, environment_id, lease_until)
           │
           ▼
      Runtime: heartbeat execution → resolve env overlay chain → inject into agent context
```

## Data Models

### environments

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id | uuid | FK, not null | Scoping |
| name | text | not null | Environment name (e.g. staging, production) |
| env | jsonb | not null, default `{}` | Key/value bindings with secret ref syntax |
| created_at | timestamptz | not null | Creation timestamp |
| updated_at | timestamptz | not null | Last update |

### environment_leases

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| environment_id | uuid | FK, not null | Leased environment |
| agent_id | uuid | FK, not null | Leasing agent |
| project_id | uuid | FK, null | Optional project scope |
| lease_start | timestamptz | not null | When lease starts |
| lease_until | timestamptz | not null | When lease expires |
| created_at | timestamptz | not null | Record creation |

## API Contracts

### GET/POST /companies/:companyId/environments

List and create environments.

### PATCH /companies/:companyId/environments/:envId

Update environment configuration.

### POST /companies/:companyId/environments/:envId/leases

Create an environment lease.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Invalid environment config |
| 403 | UNAUTHORIZED | Caller lacks company access |
| 404 | NOT_FOUND | Environment not found |

## Sequences

### Environment resolution at heartbeat

```
Heartbeat execution → resolve project env → resolve environment env (resolve secret refs via secrets service) → resolve routine env → apply Paperclip runtime keys → inject into agent context
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Secret refs | `${{ secrets.key }}` syntax, resolved at runtime | Secrets never stored in plaintext in environment config |
| Overlay order | Project → Environment → Routine → Runtime | Predictable precedence; most specific wins |

## Risks and Unknowns

1. Runtime resolution of secret references may add latency to heartbeat startup.
2. Lease expiry handling: what happens when a lease expires mid-execution?

## Out of Scope

- Environment variable inheritance between environments (e.g., production inherits from staging)
- Environment variable diffing or change tracking

---
title: "Secrets Management"
status: draft
---

# Specification: Secrets Management

## Overview

Secrets are company-scoped, versioned, and provider-backed. A pluggable provider architecture (local encrypted, AWS Secrets Manager, GCP, Vault) stores the material. Bindings attach secrets to agents/projects/routines via config paths. Inline secret references in JSON configs are resolved at runtime. Every access is audited via `secret_access_events`.

## Architecture

```
User → /api/secrets (CRUD + versions + bindings)
           │
           ▼
      company_secrets (name, key, provider, status)
           │
           ├── company_secret_versions (SHA256 fingerprint)
           ├── company_secret_bindings (target: agent/project, config path)
           ├── company_secret_provider_configs (vault config)
           └── secret_access_events (audit)
           │
           ▼
      Provider layer: local-encrypted | aws-secrets-manager | gcp | vault
           │
           ▼
      Runtime resolution: inline ${{ secrets.ref }} → resolved value → env injection
```

## Data Models

### company_secrets

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | Secret identifier |
| company_id | uuid | FK companies, not null | Scoping |
| name | text | not null | Human-readable name |
| key | text | not null | Machine key for references |
| provider | text | not null | Provider type |
| status | text | not null | `active \| deprecated \| destroyed` |
| version | int | not null, default 1 | Current version number |

### company_secret_versions

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| secret_id | uuid | FK, not null | Parent secret |
| version | int | not null | Monotonic version |
| sha256 | text | not null | Fingerprint of material |
| created_by / created_at | - | - | Attribution |

### company_secret_bindings

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| secret_key | text | not null | Reference key |
| target_type | enum | not null | `agent \| project \| routine` |
| target_id | uuid | FK, not null | Scoped target |
| config_path | text[] | not null | JSON path for resolution |

## API Contracts

### POST /companies/:companyId/secrets

**Request**: `{ name, key, provider, value }`

**Response (201)**: `{ id, name, key, provider, status, version }` — value NOT returned.

### GET/PATCH/DELETE /companies/:companyId/secrets/:secretId

Standard CRUD. GET never returns value.

### POST /companies/:companyId/secrets/:secretId/versions

Create new version of existing secret.

### GET /companies/:companyId/secrets/:secretId/bindings, POST /companies/:companyId/secrets/bindings

Binding management.

### GET /companies/:companyId/secrets/access-events

Audit log of secret accesses.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Missing provider type or invalid value |
| 403 | UNAUTHORIZED | Actor may not access this company's secrets |
| 404 | NOT_FOUND | Secret not found |
| 409 | CONFLICT | Duplicate secret key within company |

## Sequences

### Secret creation and binding

```
Board → POST /secrets (value) → store in provider vault → return metadata (no value)
Board → POST /bindings (secretKey, targetType, targetId, configPath) → binding row
Agent → runtime resolution → resolve bindings + inline refs → fetch from provider → env injection → ${{ secrets.ref }} replaced
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Provider architecture | Pluggable with registry | Supports local dev, AWS, GCP, Vault without hardcoding |
| Inline refs | `${{ secrets.key }}` syntax in JSONB configs | Usable in agent config, project env, routine env |
| Audit | Dedicated `secret_access_events` table | Immutable trail for compliance |
| Material storage | Provider vault only (not in business DB) | Material is the provider's concern; DB holds metadata only |

## Risks and Unknowns

1. Vault provider may not be available in all deployment modes; fallback behavior must be graceful.
2. Inline secret reference resolution ordering in nested env overlays (project env → routine env → runtime keys) needs clear documentation.

## Out of Scope

- Automatic secret rotation or expiry notification.
- Cross-company secret sharing.

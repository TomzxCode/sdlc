---
title: "Secrets, Settings & Provider Configuration"
status: done
---

# Specification: Secrets, Settings & Provider Configuration

## Overview

Secrets are stored encrypted at rest (AES-256-GCM) under scopes with access policies in `@fusion/core`; global/project settings merge with precedence; providers/models resolve instances with rotation/fallback; MCP servers are configured with secret references. All are surfaced via the Settings modal, CLI, and API routes.

## Architecture

```
Settings modal / CLI commands / API routes
   (register-secrets-routes, register-config-mcp-pi-settings-routes,
    register-custom-provider-routes, register-model-routes, register-provider-routes)
      │
      ▼
@fusion/core (secrets-store, secrets-crypto, master-key, secret-access-policy,
              secrets-sync, config/settings, settings-ops, mcp)
      │
      ▼
PostgreSQL / file-backed secrets + sync
```

## Data Models

### Secret

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK | Secret name |
| scope | enum | not null | Global / project / task scope |
| ciphertext | string | not null | AES-256-GCM encrypted value |
| accessPolicy | enum | not null | Who may read it |

### Settings

| Field | Type | Constraints | Description |
|---|---|---|---|
| key | string | PK | Setting key |
| value | json | — | Setting value |
| level | enum | — | Global / project / task |

## API Contracts

### POST /api/settings/mcp

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | yes | MCP server name |
| command | string | yes | Launch command |
| secretRefs | object | no | Secret references |
| enabled | bool | no | Enabled flag |

**Response (200 OK)**

- 200 with config; 400 INVALID_INPUT on validation failure

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Encryption at rest | AES-256-GCM under master key | Single encryption model documented in docs/secrets.md |
| Model hierarchy | global → project → task → lane | Deterministic precedence (docs/settings-reference.md) |
| Credential rotation | append-only rotation events | Never expose credentials in audit |
| MCP import/export | CLI + dashboard | Operator-friendly configuration |

## Risks and Unknowns

1. Secrets sync between nodes authentication parity is an open security review area.

## Out of Scope

- Agent execution (FEAT-p4) and command center (FEAT-p7) internals
---
title: "Org Chart & Agents"
status: done
---

# Specification: Org Chart & Agents

## Overview

Agents live in a company-scoped strict reporting tree. Each agent carries adapter/runtime configuration, a status state machine, a monthly budget, and one or more hashed API keys. Hiring may go through a board approval. Built-in adapters cover process, http, local CLI tools (claude/codex/gemini/opencode/pi/cursor), and the OpenClaw gateway; external adapters load via the plugin flow.

## Architecture

```
Board ──► /api/agents (CRUD, pause/resume/terminate, keys)
Agent  ──► /api/agents/:id/heartbeat/invoke  (via API key)
              │
              ▼
         agents table (company_id, reports_to, status, adapter_config, budget)
              │
              ▼
         agent_api_keys (hashed) + approvals(hire_agent)
```

## Data Models

### agents

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | Agent id |
| company_id | uuid | FK companies, not null | Scoping |
| name / role / title / icon | text | - | Identity |
| status | enum | not null | `active \| paused \| idle \| running \| error \| pending_approval \| terminated` |
| reports_to | uuid | FK agents, null | Manager (nullable root) |
| adapter_type | text | - | `process`, `http`, `claude_local`, `codex_local`, etc. |
| adapter_config | jsonb | not null | Adapter-specific config |
| runtime_config | jsonb | default `{}` | Runtime policy incl. `modelProfiles.cheap` |
| context_mode | enum | default `thin` | `thin \| fat` |
| budget_monthly_cents / spent_monthly_cents | int | not null | Budgets |
| permissions | jsonb | default `{}` | Permissions |
| last_heartbeat_at | timestamptz | null | Liveness |

### agent_api_keys

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| agent_id / company_id | uuid | FK, not null | Scoping |
| name | text | not null | Label |
| key_hash | text | not null | Hashed key (plaintext shown once) |
| last_used_at / revoked_at | timestamptz | null | Usage/revocation |

## API Contracts

### POST /companies/:companyId/agents, GET /agents/:agentId, PATCH /agents/:agentId

Agent CRUD.

### POST /agents/:agentId/pause | /resume | /terminate

Lifecycle transitions (terminate board-only).

### POST /agents/:agentId/keys, POST /agents/:agentId/heartbeat/invoke

Key management and heartbeat invocation.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 409 | CONFLICT | Invalid status transition or cycle in reports_to |
| 422 | RULE_VIOLATION | e.g. resuming a terminated agent |

## Sequences

### Hire via approval

```
Agent → approvals(hire_agent, pending) → Board approve → create agent row + optional key → activity_log
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Org graph | Strict tree (`reports_to`) | Simple, auditable delegation; no multi-manager ambiguity |
| Key storage | Hashed at rest | Plaintext shown once; safe at rest |

## Risks and Unknowns

1. Graceful-cancel-then-force-kill semantics during pause of an active run need careful adapter coordination.

## Out of Scope

- Multi-board governance or role-based human permission granularity.

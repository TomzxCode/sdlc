---
title: "Company Management & Multi-Tenancy"
status: done
---

# Specification: Company Management & Multi-Tenancy

## Overview

Companies are top-level isolated tenants. Each company row carries configuration, branding, budget, and issue-counter state. Company scoping is enforced by a `company_id` foreign key on every business table plus boundary checks in routes/services. Portability is provided by a markdown-first package contract rooted at `COMPANY.md` with `.paperclip.yaml` sidecar.

## Architecture

```
Board ──► /api/companies (CRUD + archive)
              │
              ▼
         companies table ──► company_id FK on agents, goals, projects,
              │               issues, cost_events, activity_log, secrets, ...
              ▼
         per-company isolation enforced in services/routes
```

## Data Models

### companies

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK, not null | Company identifier |
| name | text | not null | Company name |
| description | text | null | Optional description |
| status | enum | not null | `active \| paused \| archived` |
| pause_reason | text | null | Reason when paused |
| paused_at | timestamptz | null | When paused |
| issue_prefix | text | not null | Prefix for issue identifiers (e.g. `PAPA`) |
| issue_counter | int | not null | Monotonic per-company issue counter |
| budget_monthly_cents | int | not null, default 0 | Monthly budget |
| spent_monthly_cents | int | not null, default 0 | Month-to-date spend |
| attachment_max_bytes | int | not null | Per-company attachment size cap |
| require_board_approval_for_new_agents | boolean | not null, default false | Governance flag |
| brand_color / branding | - | null | Branding fields |

## API Contracts

### POST /companies

Creates a company. Returns the created company.

### GET /companies, GET /companies/:companyId, PATCH /companies/:companyId, PATCH /companies/:companyId/branding, POST /companies/:companyId/archive

Standard CRUD + branding + archive. All under `/api`. Board-only.

### Company import/export

Preview/apply endpoints for portable company packages (`companies.ts`, `company-import-paths.ts`, `company-portability.ts` service).

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Validation error |
| 403 | UNAUTHORIZED | Caller lacks company access |
| 404 | NOT_FOUND | Company not found |

## Sequences

### Archive a company

```
Board → PATCH/archive → companies(status=archived) → activity_log
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Tenancy model | Single-tenant deployment, multi-company data model | One deployment runs many isolated companies without multi-tenant infra |
| Issue identifiers | Per-company prefix + counter | Human-readable, collision-free within a company |

## Risks and Unknowns

1. Export/import secret resolution and collision handling semantics need precise documentation.

## Out of Scope

- Cloud-grade multi-tenant infra or centralized policy overlays (Pro/Enterprise).

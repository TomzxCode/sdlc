---
title: "Governance & Approvals"
status: draft
---

# Specification: Governance & Approvals

## Overview

Governance is enforced through the `approvals` table, execution policies, budget hard-stops, board override authority, and the scoped task-watchdog contract. Board approvals are transactional (no lost decisions). Watchdogs are a narrow, persisted-configuration-derived capacity confined to one watched issue subtree.

## Architecture

```
Board ──► /api/approvals (approve/reject/cancel)
Agent  ──► approvals(hire_agent | approve_ceo_strategy | request_board_approval)
              │
              ▼
         approvals table → activity_log
Watchdog ──► scoped mutations within watched subtree (comments, child issues, status,
             blockers, eligible request_confirmation) → activity (watchdog metadata)
```

## Data Models

### approvals

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id | uuid | FK, not null | Scoping |
| type | enum | - | `hire_agent \| approve_ceo_strategy \| budget_override_required \| request_board_approval` |
| requested_by_agent_id / requested_by_user_id | uuid | null | Requester |
| status | enum | - | `pending \| revision_requested \| approved \| rejected \| cancelled` |
| payload | jsonb | not null | Approval content |
| decision_note | text | null | Decision rationale |
| decided_by_user_id / decided_at | - | null | Decision attribution |

Supporting tables: `approval_comments`, `issue_approvals`, `issue_execution_decisions`, `issue_watchdogs`, `heartbeat_run_watchdog_decisions`, `issue_recovery_actions`.

## API Contracts

### GET/POST /companies/:companyId/approvals, POST /approvals/:approvalId/approve | /reject

Approval listing, creation, and decisions.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 403 | UNAUTHORIZED | Non-board actor attempting board-only decision |
| 409 | CONFLICT | Decision on an already-terminal approval |

## Sequences

### Hire approval

```
Agent → approvals(hire_agent, pending) → Board approve (transactional) → create agent + optional key → activity_log
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Approval writes | Transactional | No lost approval decisions (reliability target) |
| Watchdog scope | Persisted-config-derived, subtree-scoped | Safety: prompts cannot expand authority |

## Risks and Unknowns

1. Ensuring watchdog capability discovery comes only from wake metadata/denials (no probe issues) requires careful server enforcement and tests.

## Out of Scope

- Multi-board governance or RBAC granularity for humans.

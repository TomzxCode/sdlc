---
title: "Task System (Issues)"
status: draft
---

# Specification: Task System (Issues)

## Overview

Issues are company-scoped tasks with a strict status state machine, single-assignee ownership, and atomic checkout. Rich collaboration (comments, documents, work products, attachments, labels, blockers, thread interactions) is layered on top. Execution locks and checkout/execution-run fields prevent double-work. A non-terminal liveness rule keeps work from silently stalling.

## Architecture

```
Agent/Board ──► /api/issues (CRUD, checkout, release, force-release)
                    │
                    ▼
               issues (status, assignee, checkout/execution locks, parent_id, goal_id)
                    ├── issue_comments
                    ├── issue_documents ← documents / document_revisions
                    ├── issue_attachments ← assets
                    ├── issue_work_products
                    ├── issue_relations (blockers)
                    ├── issue_thread_interactions / issue_approvals
                    └── activity_log (every mutation)
```

## Data Models

### issues (core fields)

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id | uuid | FK, not null | Scoping |
| project_id / goal_id / parent_id | uuid | FK, null | Traceability + hierarchy |
| title / description | text | - | Content |
| status | enum | not null | `backlog \| todo \| in_progress \| in_review \| done \| blocked \| cancelled` |
| priority | enum | - | `critical \| high \| medium \| low` |
| assignee_agent_id | uuid | FK, null | Single assignee |
| checkout_run_id / execution_run_id / execution_locked_at | - | null | Atomic checkout/execution locks |
| work_mode | text | default `standard` | `standard \| ask \| planning` |
| issue_number / identifier | - | - | Per-company human id |

## API Contracts

### POST /issues/:issueId/checkout

Atomic checkout. Request: `{ agentId, expectedStatuses }`. Single guarded SQL update; `409` on conflict.

### POST /issues/:issueId/release | /issues/:issueId/admin/force-release

Release locks; force-release is board-only and writes `issue.admin_force_release` activity.

### Documents, comments, attachments

`GET/PUT /issues/:issueId/documents/:key` (+lock/unlock/revisions), `POST/GET /issues/:issueId/comments`, `POST /companies/:companyId/issues/:issueId/attachments`, `GET /attachments/:attachmentId/content`, `DELETE /attachments/:attachmentId`.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 409 | CONFLICT | Checkout conflict or invalid transition |
| 422 | RULE_VIOLATION | Semantic rule violation (e.g. in_progress without assignee) |

## Sequences

### Atomic checkout

```
Agent → checkout(expectedStatuses) → UPDATE issues SET status=in_progress, assignee, locks WHERE id AND status IN(?) AND (assignee IS NULL OR assignee=agent) → rowcount 0 ? 409 : ok
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Checkout | Single guarded SQL update | Race-free without app-level locks |
| Communication | Tasks + comments only | No separate chat system (V1 decision) |

## Risks and Unknowns

1. Non-terminal liveness enforcement touches scheduler, watchdogs, and recovery actions; semantics are detailed in `doc/execution-semantics.md`.

## Out of Scope

- Project/issue-level privacy ACLs (Pro/Enterprise).

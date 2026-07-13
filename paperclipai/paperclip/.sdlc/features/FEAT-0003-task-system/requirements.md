---
title: "Task System (Issues)"
status: done
---

# Requirements: Task System (Issues)

## Overview

Issues are the core task entity and the primary unit of work. Each issue traces to a company goal chain, has a single assignee, supports parent/child hierarchy, and uses atomic checkout to guarantee no double-work. Issues carry comments, documents, work products, attachments, labels, blocker relations, thread interactions, inbox/read state, and execution locks. Work modes (`standard`, `ask`, `planning`) control what execution is allowed.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Create/assign/force-reassign/cancel tasks; view kanban and audit trail |
| Agent | Atomically check out assigned tasks, execute, comment, attach artifacts, delegate children |
| CEO agent | Decompose approved plans into child issues |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support issue lifecycle with status `backlog \| todo \| in_progress \| in_review \| done \| blocked \| cancelled` and the defined transitions. |
| FR-02 | Must | The system shall enforce single-assignee ownership and require an assignee before `in_progress`. |
| FR-03 | Must | The system shall provide atomic checkout that sets assignee, status `in_progress`, and execution locks via a single guarded SQL update, returning `409` on concurrent claims. |
| FR-04 | Must | The system shall enforce that every task traces to a company goal chain via `goal_id`, `parent_id`, or project-goal linkage. |
| FR-05 | Must | The system shall support issue comments authored by agents or users. |
| FR-06 | Must | The system shall support attachments (upload allowlist, inline vs download serving, range requests for video) and link them to issues/comments. |
| FR-07 | Should | The system shall support documents (markdown, append-only revisions) linked to issues by workflow key, with board lock/unlock. |
| FR-08 | Should | The system shall support work products (artifact-backed and workspace-file references), labels, first-class blockers (`issue_relations`), and thread interactions (`request_confirmation`, `ask_user_questions`, `suggest_tasks`). |
| FR-09 | Should | The system shall enforce the non-terminal liveness rule: agent-owned non-terminal issues must have a live, waiting, or explicit recovery path. |
| FR-10 | May | The system shall support work modes `standard`, `ask`, and `planning`. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Correctness | Checkout must be race-free under concurrent claims. |
| NFR-02 | Must | Auditability | All issue mutations write `activity_log`. |
| NFR-03 | Should | Performance | Standard issue CRUD p95 < 250 ms at 1k tasks/company. |

## Constraints

- Terminal states are `done` and `cancelled`.
- `in_progress` requires an assignee and sets `started_at`; `done`/`cancelled` set completion timestamps.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-03**
    - **Given** two concurrent checkout requests for the same `todo` issue
    - **When** both execute
    - **Then** exactly one succeeds and the other gets `409` with current owner/status
- [ ] **FR-06**
    - **Given** a video attachment
    - **When** a browser requests a byte range
    - **Then** the server responds `206` with `Content-Range` and `Accept-Ranges: bytes`
- [ ] **NFR-01**
    - **Given** the checkout race regression test
    - **When** run
    - **Then** it passes (release-gate item)

## Conflicts

None identified yet.

## Open Questions

1. Exact scope of the non-terminal liveness recovery actions and when issue-backed recovery is used vs source-scoped actions (see `doc/execution-semantics.md`).

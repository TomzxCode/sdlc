---
title: "Company Management & Multi-Tenancy"
status: draft
---

# Requirements: Company Management & Multi-Tenancy

## Overview

The company is the first-order business entity in Paperclip.
Every other business record (agents, goals, projects, issues, costs, activity) is scoped to exactly one company, and a single deployment can run many companies with complete data isolation.
This feature covers the company lifecycle, per-company configuration, multi-company data boundaries, and company portability (export/import of entire organizations).

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Create/list/get/update/archive companies; switch between them; import/export orgs |
| Agent | Operates strictly within its own company; must never see another company's data |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating a company with a name, description, status, and issue prefix/counter. |
| FR-02 | Must | The system shall enforce that every business record belongs to exactly one company and that company boundaries are checked on every fetch/mutation. |
| FR-03 | Must | The system shall support listing, getting, updating, and archiving companies. |
| FR-04 | Must | The system shall maintain company status as `active \| paused \| archived` with pause reason and paused-at tracking. |
| FR-05 | Should | The system shall support per-company branding (brand color, logo) and feedback-sharing consent fields. |
| FR-06 | Should | The system shall support exporting and importing entire companies (agents, skills, projects, routines, issues) with secret scrubbing and collision handling. |
| FR-07 | Should | The system shall support per-company attachment size limits (`attachment_max_bytes`). |
| FR-08 | May | The system shall support per-company board-approval requirement flag for new agents (`require_board_approval_for_new_agents`). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Agent API keys must not access other companies' data; cross-company reads/writes must be rejected. |
| NFR-02 | Must | Auditability | Every company mutation must write an `activity_log` entry attributed to an actor. |
| NFR-03 | Should | Performance | Company CRUD must meet the p95 < 250 ms latency target at 1k tasks/company. |

## Constraints

- Single-tenant deployment with a multi-company data model (one deployment, many isolated companies).
- Board has full read/write across all companies in the deployment.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** a board operator
    - **When** they create a company with required fields
    - **Then** a company row exists with status `active`, a generated issue prefix, and a zeroed issue counter
- [ ] **FR-02**
    - **Given** two companies A and B and an agent key scoped to A
    - **When** the agent attempts to read or mutate a B-scoped entity
    - **Then** the request is rejected with `403`/`404` and no B data is returned
- [ ] **FR-04**
    - **Given** an active company
    - **When** it is paused
    - **Then** `status=paused`, `paused_at` is set, and a pause reason is recorded
- [ ] **FR-06**
    - **Given** an exported company package
    - **When** it is imported into a fresh deployment
    - **Then** agents, skills, projects, routines, and issues are recreated with secrets scrubbed and id collisions handled
- [ ] **NFR-01**
    - **Given** an agent API key for company A
    - **When** it calls any endpoint scoped to company B
    - **Then** the request is denied before any company B data is exposed

## Conflicts

None identified yet.

## Open Questions

1. What is the exact set of entities included in company export/import, and how are secret references resolved on import?

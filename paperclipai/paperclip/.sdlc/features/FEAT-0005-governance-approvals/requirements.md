---
title: "Governance & Approvals"
status: draft
---

# Requirements: Governance & Approvals

## Overview

Governance ensures nothing ships without board sign-off and that the board can intervene anywhere. It covers board approval workflows for hires and CEO strategy, execution policies with review/approval stages, decision tracking, budget hard-stops, agent pause/resume/terminate, full audit logging, and the scoped task-watchdog capacity for watched issue subtrees.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Approve/reject hires and CEO strategy; override any decision; pause/resume/terminate agents |
| CEO agent | Proposes strategy that must be approved before delegated execution |
| Watchdog agent | Restore live task paths within a watched subtree (scoped, not board authority) |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support approval types `hire_agent`, `approve_ceo_strategy`, `budget_override_required`, `request_board_approval` with status `pending \| revision_requested \| approved \| rejected \| cancelled`. |
| FR-02 | Must | The system shall block CEO-created delegated work from active execution states until the CEO strategy is approved. |
| FR-03 | Must | The board shall be able to pause/resume/terminate any agent, reassign or cancel any task, edit budgets, and approve/reject/cancel pending approvals at any time. |
| FR-04 | Must | Every governance mutation shall write an auditable `activity_log` entry. |
| FR-05 | Should | The system shall support execution policies with review/approval stages and decision tracking. |
| FR-06 | Should | The system shall support a scoped task watchdog that may only restore live task paths inside one watched subtree, may resolve eligible `request_confirmation` plan confirmations, and is explicitly denied board/governance/secret/cross-company authority. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Watchdogs must not resolve board approvals, force-release locks, cancel active runs, or cross company boundaries. |
| NFR-02 | Must | Auditability | Watchdog mutations must record watchdog id, source issue, run id, and stop fingerprint. |

## Constraints

- Watchdog authority is derived from persisted configuration and run context; custom instructions/prompt text cannot expand it.
- The watched subtree excludes `task_watchdog`-origin issues and their descendants.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-02**
    - **Given** a CEO that drafted delegated tasks
    - **When** strategy has not been approved
    - **Then** those tasks cannot transition to active execution states
- [ ] **NFR-01**
    - **Given** a task watchdog run
    - **When** it attempts to approve a hire/budget approval or touch a company outside the watched subtree
    - **Then** the action is denied and no probe issue/comment is created

## Conflicts

None identified yet.

## Open Questions

1. Which interaction families beyond eligible `request_confirmation` plan confirmations will watchdogs resolve in future iterations?

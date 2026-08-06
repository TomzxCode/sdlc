---
title: "Missions, Goals, Research & Evals"
status: done
---

# Requirements: Missions, Goals, Research & Evals

## Overview

A product-hierarchy layer (missions → milestones → features) drives task work, optionally fueled by goals anchors, research runs, and evals. Missions break into milestones and features, research produces cited findings, goals anchor objectives, and evolutions score task outcomes.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Program/PM | Defines missions, milestones, features, goals/KRs |
| Researcher | Runs research and exports findings |
| Evaluator | Scores task outcomes with evidence |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall model the hierarchy mission → milestone → feature and track their progress |
| FR-2 | Must | The system shall sync missions, features, and their state on the board and drive them via autopilot/execution loops |
| FR-3 | Must | The system shall manage goals, objectives, and key results with citation extraction and anchoring |
| FR-4 | Must | The system shall run research/broadly-scoped research (research store, orchestrator, step-runner, providers) and manage findings |
| FR-5 | Should | The system shall score task/feature outcomes via evals with evidence persistence |
| FR-6 | Should | The system shall expose missions, goals, research, and evals in dashboard views (MissionManager, GoalsView, ResearchView) |
| FR-7 | Should | The system shall integrate missions and research with task execution |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Consistency | Run-audit events from missions/research must hold ids/counts/outcomes-only metadata (never prose) |
| NFR-2 | Must | Correctness | Feature IDs for milestones must be converted/anchored to board tasks deterministically |
| NFR-3 | Should | Performance | Research steps must not block unrelated task lane work |

## Constraints

- Research/experiment sessions use `research_*` for cited search/synthesis and `experiment_session_*` for upstream parity
- Mission completion gates are governed by a documented contract (`docs/missions-completion-contract.md`)

## Acceptance Criteria

- [ ] **FR-1, FR-2**
    - **Given** a mission with milestones/features and project context
    - **When** the mission autopilot/execution loop runs
    - **Then** attached board tasks and features progress per the mission plan and sync state
- [ ] **FR-3**
    - **Given** goals and objectives
    - **When** citation extraction runs
    - **Then** goals are anchored to evidence
- [ ] **FR-4**
    - **Given** a research request
    - **When** research runs
    - **Then** a research run is persisted with findings
- [ ] **FR-5**
    - **Given** a task to score
    - **When** an eval runs
    - **Then** a scored outcome is persisted with evidence and the intended reason + acceptance

## Conflicts

None identified yet.

## Open Questions

1. How are `evaluations` and `insights` integrated routers wired (primary surface for each) — a concrete focus area identified at sync, awaiting mapping.
2. The exact KPIs/KRs that anchor goal refinement are not fully instrumented.
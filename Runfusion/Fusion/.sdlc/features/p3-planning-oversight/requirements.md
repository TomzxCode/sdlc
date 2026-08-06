---
title: "Planning Mode & Planner Oversight"
status: done
---

# Requirements: Planning Mode & Planner Oversight

## Overview

A dedicated planning flow (Planning Mode chat, Plan Review, specification editor) plus an automated planner overseer let operators shape a task before execution and keep human control over high-stakes actions. The overseer runs across oversight levels (`off`/`observe`/`steer`/`autonomous`) with human confirmation gates on merge, PR, and destructive actions, and records an Intervention Timeline in Task Detail.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Shapes plans, approves/rejects Plan Review, watches and steers planner work |
| Planner lane | Produces the plan and plan artifacts |
| Oversight automation | Monitors planner work and withholds/recommends actions |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a Planning Mode chat and Plan Review node that produce and review a plan for a task |
| FR-2 | Must | The system shall persist plan approval state and plan artifacts (plan-md writeback) |
| FR-3 | Must | The system shall run a planner overseer across `off`/`observe`/`steer`/`autonomous` levels with per-task overrides |
| FR-4 | Must | The system shall gate merge/PR and destructive actions behind a human confirmation where oversight level requires it |
| FR-5 | Must | The system shall record planner interventions and events, surfacing them as an Intervention Timeline in Task Detail |
| FR-6 | Should | The system shall withhold oversight actions for user-paused or auto-merge-off tasks (deduped event) |
| FR-7 | Should | The system shall recover planner handoffs and continuation across runs |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Correctness | The planner role must not be treated as a board column |
| NFR-2 | Must | Reliability | Plan Review state must survive engine restart (handoff recovery) |
| NFR-3 | Should | Usability | Oversight settings must be visible and togglable in Settings + Task Detail |

## Constraints

- Plan Review is owned by a workflow-graph node; do not reintroduce an in-session review authority
- Being user-paused or auto-merge-off must withhold full oversight action

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a task in planning
    - **When** Planning Mode is used
    - **Then** a plan is drafted and reviewable at the Plan Review node
- [ ] **FR-3**
    - **Given** a configured oversight level
    - **When** the planner produces work
    - **Then** the overseer acts per the level and per-task override
- [ ] **FR-4**
    - **Given** a merge/PR or destructive action with human confirmation required
    - **When** the action is attempted
    - **Then** it is held until a human confirms
- [ ] **FR-5**
    - **Given** interventions or events
    - **When** Task Detail is opened
    - **Then** the Intervention Timeline shows them
- [ ] **NFR-1**
    - **Given** planner state
    - **When** rendered
    - **Then** the planner role is not represented as a board column

## Conflicts

None identified yet.

## Open Questions

1. Which destructive actions are governed by default vs. opt-in confirmation?
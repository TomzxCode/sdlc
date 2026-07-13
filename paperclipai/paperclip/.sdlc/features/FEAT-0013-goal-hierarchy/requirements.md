---
title: "Goal Hierarchy"
status: done
---

# Requirements: Goal Hierarchy

## Overview

Goals provide the company-wide alignment hierarchy that ties every task back to business mission.
Each goal is a node in a tree (company root goal, team goals, agent goals) with a level, status, and optional owner agent.
Goals are the first step in the Paperclip workflow: a board operator defines the company mission as a root goal and decomposes it down the org tree, giving every task a traceable purpose.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Create, edit, and restructure goal hierarchy; link goals to projects and issues |
| Agent | Work within goal-aligned tasks; see goal context in heartbeat invocations |
| CEO agent | Propose strategy that maps to goals (requires board approval) |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support CRUD of company-scoped goals with title, description, level (`company | team | task`), and status (`planned | active | completed | cancelled`). |
| FR-02 | Must | The system shall support a goal hierarchy via `parent_id` (nullable root) that forms a tree, with all goals scoped to the same company. |
| FR-03 | Must | The system shall track goal ownership via `owner_agent_id`. |
| FR-04 | Must | Goals shall link to projects and issues: issues carry `goal_id`, projects carry `goal_id`, and the goal chain is traceable from task to company root. |
| FR-05 | Should | The system shall support listing goals by company with ordering. |
| FR-06 | Should | The system shall create a default root company goal on company creation. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Auditability | All goal mutations must write `activity_log` entries. |
| NFR-02 | Should | Performance | Goal CRUD must meet the p95 < 250 ms latency target. |

## Constraints

- Goals are company-scoped; cross-company goal references are not supported.
- A goal hierarchy is expected to be shallow (company root, team, task levels).

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a company
    - **When** a board operator creates a goal with title, level, and status
    - **Then** a goal row exists scoped to that company
- [ ] **FR-02**
    - **Given** a root goal
    - **When** a child goal is created with `parent_id` pointing to the root
    - **Then** the goal tree is correctly navigable from root to leaf
- [ ] **FR-04**
    - **Given** a goal
    - **When** an issue or project is created with that `goal_id`
    - **Then** the goal chain is traceable from the issue to the company root goal
- [ ] **NFR-01**
    - **Given** any goal mutation (create, update, delete)
    - **When** the mutation completes
    - **Then** an `activity_log` entry is written

## Conflicts

None identified yet.

## Open Questions

1. Should goal deletion cascade to child goals (soft delete with orphan marking)?
2. What is the exact default root goal creation behavior on company creation?

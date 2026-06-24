---
title: "Projects"
status: draft
---

# Requirements: Projects

## Overview

Projects are company-scoped groupings that organize work around a specific initiative.
Each project carries a name, description, status, lead agent, target date, environment config, and execution workspace policy.
Projects link to goals for strategic alignment and support workspaces with runtime services for agent execution.
Projects are a core organizational entity visible throughout the board UI and agent API.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Create and manage projects, assign lead agents, set targets, configure environments and workspaces |
| Agent | Work within project context; access project env, workspace, and runtime services |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support CRUD of company-scoped projects with name, description, status, lead agent, and target date. |
| FR-02 | Must | Projects shall support status lifecycle (`backlog | active | paused | completed | archived`). |
| FR-03 | Must | Projects shall link to a goal via `goal_id` for strategic alignment. |
| FR-04 | Must | The system shall support project workspaces (named working directories with repo URL, CWD, runtime config, and metadata). |
| FR-05 | Must | The system shall support project execution workspace policy (how execution worktrees are created for issues within the project). |
| FR-06 | Should | The system shall support project memberships tracking which users/agents have joined a project (for sidebar visibility). |
| FR-07 | Should | The system shall support project runtime services (dev servers, preview URLs) with desired state management. |
| FR-08 | Should | The system shall support project env configuration with secret ref resolution (project-level env overlay). |
| FR-09 | Should | The system shall track project budget summaries (aggregate spend across project issues and agents). |
| FR-10 | May | The system shall support plugin-managed projects (plugins can declare and manage project-level resources). |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Auditability | All project mutations must write `activity_log` entries. |
| NFR-02 | Must | Security | Project env and secrets must be scoped to the project's company. |
| NFR-03 | Should | Performance | Project CRUD and workspace operations must meet latency targets. |

## Constraints

- Projects are company-scoped; cross-company project access is not permitted.
- A project links to exactly one goal (optional).
- Project workspace runtime services are provider-dependent and may not be available in all deployment modes.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a company
    - **When** a project is created with name, status, and lead agent
    - **Then** a project row exists scoped to the company
- [ ] **FR-04**
    - **Given** a project
    - **When** a project workspace is created with repo URL and CWD
    - **Then** the workspace is available for agent execution
- [ ] **FR-07**
    - **Given** a project workspace
    - **When** runtime services are configured with desired state
    - **Then** services are started/stopped to match the desired state
- [ ] **NFR-01**
    - **Given** any project mutation
    - **When** the mutation completes
    - **Then** an `activity_log` entry is written

## Conflicts

None identified yet.

## Open Questions

1. How do project env overlays compose with agent env and routine env at runtime?
2. What is the exact relationship between project workspaces and execution workspaces (git worktrees)?
3. Are plugin-managed projects fully supported in V1 or deferred?

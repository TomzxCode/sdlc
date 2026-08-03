---
title: "Agent Manager"
status: done
---

# Requirements: Agent Manager

## Overview

The Agent Manager is a dedicated view for organizing agent groups and launching multi-run sessions from them. Users browse agent groups in a sidebar, inspect a group's detail (the agents it contains), and start a multi-run for a selected group from the manager, in addition to the composer-level multi-run launcher.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users (developers) | Curate named groups of models/agents and launch parallel runs from them |
| Power users | Reuse consistent agent lineups across projects |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall list agent groups in a sidebar within the Agent Manager. |
| FR-2 | Must | The system shall show the detail of a selected group, including the agents it contains. |
| FR-3 | Must | The system shall launch a multi-run for a selected group from the Agent Manager. |
| FR-4 | Must | The system shall surface connection and configuration state (server connection status, config initialized) in the manager. |
| FR-5 | Should | The system shall support creating and editing agent groups. |
| FR-6 | Should | The system shall show an empty state when no agent groups exist. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Should | Usability | Agent group workflows shall be usable on desktop, web, and VS Code runtimes. |

## Constraints

- Reuses the agent-groups store (`useAgentGroupsStore`) and the multi-run store (`useMultiRunStore`)
- Multi-run launches reuse the existing multi-run session machinery with isolated worktrees

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the Agent Manager is open
    - **When** the user has agent groups
    - **Then** the groups appear in the sidebar
- [ ] **FR-2**
    - **Given** a group selected in the sidebar
    - **When** the detail pane renders
    - **Then** it lists the group's agents
- [ ] **FR-3**
    - **Given** a selected group
    - **When** the user starts a multi-run
    - **Then** sessions launch for the group's agents
- [ ] **FR-5**
    - **Given** the Agent Manager
    - **When** the user creates or edits a group
    - **Then** the change persists to the agents-groups store
- [ ] **FR-6**
    - **Given** no agent groups
    - **When** the Agent Manager opens
    - **Then** an empty state guides the user to create a group

## Conflicts

None identified yet.

## Open Questions

1. Should agent groups be shareable across projects or stay per-installation?

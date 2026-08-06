---
title: "Swarm Multi-Agent Coordination"
status: done
---

# Requirements: Swarm Multi-Agent Coordination

## Overview

Swarm coordination lets jcode delegate work across multiple agent instances. A coordinator agent builds a plan DAG of tasks, spawns worker agents (visible, headless, inline, or auto spawn modes), and communicates with them over typed comm channels (direct messages, broadcasts, and plan updates). Members report progress and completion back so the coordinator can revise the plan. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Parallel, coordinated multi-agent work on complex tasks with visible progress |
| Maintainer | Reliable task graph execution, persisted swarm state, and debuggable comm flows |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let a coordinator agent delegate tasks to worker agents within a session. |
| FR-2 | Must | The system shall maintain a plan DAG of tasks (up to a bounded number of plan items) that the coordinator can revise as work completes. |
| FR-3 | Must | The system shall support multiple spawn modes for workers: visible, headless, inline, and auto. |
| FR-4 | Must | The system shall provide typed comm channels for messages between the coordinator and members, including direct messages and broadcasts. |
| FR-5 | Must | The system shall surface swarm status and plan progress to the UI (swarm status, plan, todo items). |
| FR-6 | Must | The system shall persist swarm state so it survives reloads. |
| FR-7 | Should | The system shall validate member reports (including a tldr rule and completion-report marker) before accepting them. |
| FR-8 | May | The system shall support an inline gallery of swarm members in the UI. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Swarm state must be durable across server reloads and restarts. |
| NFR-2 | Should | Performance | Comm messages must flow without blocking the main agent turn loop. |
| NFR-3 | Should | Usability | The user shall be able to see each member's status and the overall plan at a glance. |

## Constraints

- The plan DAG is bounded (`MAX_PLAN_ITEMS = 1024`).
- Swarm behavior is configured under the `[agents]` config section (spawn mode, swarm model).

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** an active session with swarm enabled
    - **When** the coordinator emits a task delegation
    - **Then** a worker agent runs the task and reports back
- [ ] **FR-2**
    - **Given** a multi-task swarm
    - **When** tasks complete
    - **Then** the plan DAG updates and remains bounded
- [ ] **FR-3**
    - **Given** the configured spawn mode
    - **When** a worker spawns
    - **Then** it runs visible, headless, inline, or auto as configured
- [ ] **FR-4**
    - **Given** active swarm members
    - **When** a member sends a message
    - **Then** the message is delivered to the addressed member(s) over the comm channel
- [ ] **FR-5**
    - **Given** an active swarm
    - **When** the user views the session
    - **Then** member status and plan progress are visible
- [ ] **FR-6**
    - **Given** an in-flight swarm
    - **When** the server reloads
    - **Then** the swarm resumes with its state intact
- [ ] **FR-7**
    - **Given** a member completion report
    - **When** it lacks the required tldr or marker
    - **Then** the report is rejected or flagged for the coordinator
- [ ] **FR-8**
    - **Given** an active swarm in the TUI
    - **When** the inline gallery is enabled
    - **Then** members are shown inline in the transcript
- [ ] **NFR-1**
    - **Given** persisted swarm state
    - **When** a reload occurs
    - **Then** no task or member is lost
- [ ] **NFR-2**
    - **Given** high-volume comm traffic
    - **When** the main turn loop is running
    - **Then** the turn loop continues without being blocked by comm delivery
- [ ] **NFR-3**
    - **Given** a running swarm
    - **When** the UI renders the swarm panel
    - **Then** member statuses and plan state are shown clearly

## Conflicts

None identified yet.

## Open Questions

1. What is the default worker limit and how are tasks balanced across members? Config exposes a swarm model and spawn mode but the scheduling heuristics are inferred from code.

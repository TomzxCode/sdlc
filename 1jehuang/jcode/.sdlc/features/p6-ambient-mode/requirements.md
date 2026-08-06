---
title: "Ambient Mode"
status: done
---

# Requirements: Ambient Mode

## Overview

Ambient mode is a proactive, OpenClaw-style background agent that works while the user does. A scheduler runs work cycles against configured directives (garden/scout style tasks), executes background tasks, and persists its state. A safety system gates ambient actions, and overnight processing handles long-running consolidation. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | A background assistant that makes progress without interrupting the main session |
| Maintainer | Safe, configurable, observable ambient behavior with strong permissioning |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall run a background ambient scheduler on the server that executes work cycles. |
| FR-2 | Must | The system shall execute directives (ambient instructions) and run tasks such as garden/scout activities. |
| FR-3 | Must | The system shall persist ambient state (status, log, directives) so it survives reloads. |
| FR-4 | Must | The system shall gate ambient actions through a safety and permissions system. |
| FR-5 | Must | The system shall expose ambient status and control via the CLI (`jcode ambient status`, `trigger`, `stop`, `log`). |
| FR-6 | Should | The system shall support overnight processing for long-running consolidation jobs. |
| FR-7 | Should | The system shall render ambient status in the TUI (e.g. via a side panel / badge). |
| FR-8 | May | The system shall trigger ambient activity on configurable schedules. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Safety | Ambient actions shall be subject to the same permission/safety gates as interactive actions. |
| NFR-2 | Should | Performance | Ambient work shall not starve interactive turns on the same server. |
| NFR-3 | Should | Reliability | Ambient state must be durable across restarts. |

## Constraints

- Ambient behavior is configured under the `[ambient]` config section.
- Ambient runs inside the same server process (not a separate daemon).

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** ambient mode enabled
    - **When** the scheduler runs
    - **Then** a work cycle executes on schedule
- [ ] **FR-2**
    - **Given** configured directives
    - **When** a work cycle runs
    - **Then** the directive's tasks execute
- [ ] **FR-3**
    - **Given** an active ambient session
    - **When** the server reloads
    - **Then** ambient state and status are restored
- [ ] **FR-4**
    - **Given** an ambient action requiring permission
    - **When** the action is attempted
    - **Then** it is gated by the safety system before executing
- [ ] **FR-5**
    - **Given** ambient mode running
    - **When** the user runs `jcode ambient status` or `jcode ambient log`
    - **Then** status and recent activity are shown
- [ ] **FR-6**
    - **Given** overnight enabled
    - **When** the overnight window arrives
    - **Then** consolidation jobs run
- [ ] **FR-7**
    - **Given** an active ambient session
    - **When** the TUI renders
    - **Then** ambient status is visible
- [ ] **FR-8**
    - **Given** a configured schedule
    - **When** the trigger time arrives
    - **Then** ambient activity starts
- [ ] **NFR-1**
    - **Given** an ambient task that would run a risky command
    - **When** the command is executed
    - **Then** it passes through the same risk/permission gates as interactive commands
- [ ] **NFR-2**
    - **Given** simultaneous interactive and ambient work
    - **When** both are active
    - **Then** interactive turns are not starved
- [ ] **NFR-3**
    - **Given** a restart
    - **When** ambient is enabled
    - **Then** persisted ambient state is recovered

## Conflicts

None identified yet.

## Open Questions

1. What is the default work-cycle cadence and task budget for ambient mode? Config exposes knobs; defaults are inferred from code.

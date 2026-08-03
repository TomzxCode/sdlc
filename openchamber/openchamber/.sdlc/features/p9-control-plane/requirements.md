---
title: "Control Plane and Agent Tool"
status: done
---

# Requirements: Control Plane and Agent Tool

## Overview

The control plane exposes a typed, fixed action contract for orchestrating a running OpenChamber instance: project, model, session, and scheduled-task operations. It is shared by two adapters: the `openchamber control` CLI command (an authenticated HTTP adapter) and the managed `openchamber` OpenCode custom tool (a native-tool adapter injected only when OpenChamber launches and owns the OpenCode process). Both delegate to the same service, so behavior has one owner.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operators / power users | Script and drive OpenChamber from the CLI |
| Agents | Call an `openchamber` tool to start, wait for, and inspect sessions |
| Automation / CI | Drive multi-turn goal-mode sessions and scheduled tasks programmatically |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall expose a fixed action allowlist covering project, model, session, and scheduled-task operations. |
| FR-2 | Must | The system shall share one control service between the CLI and the agent tool. |
| FR-3 | Must | The system shall support dispatching a session with optional worktree, branch, and goal-mode settings. |
| FR-4 | Must | The system shall support waiting for a session with a timeout, never treating an initial idle response as completion. |
| FR-5 | Must | The system shall support sending messages to and forking sessions. |
| FR-6 | Must | The system shall support session status and message listing from official directory-scoped OpenCode APIs. |
| FR-7 | Must | The system shall support scheduled-task status, list, and toggle operations. |
| FR-8 | Must | The system shall expose a session-directory fallback to the managed tool's current session, with explicit scope taking precedence. |
| FR-9 | Must | The system shall mark CLI-only actions (e.g. `schedule.status`) as not agent-exposed. |
| FR-10 | Must | The system shall authenticate the CLI adapter and use a separate ephemeral loopback credential for the agent tool. |
| FR-11 | Should | The system shall propagate request cancellation and preserve partial-result details for directory status lookups. |
| FR-12 | Should | The system shall expose the agent tool only while `agentControlToolEnabled` is not `false` and only when OpenChamber owns the OpenCode process. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The agent tool's per-child token and callback URL are random and added only to the managed OpenCode child environment. |
| NFR-2 | Must | Reliability | Timeout and cancellation are failures, never authoritative idle results. |
| NFR-3 | Must | Correctness | One failed directory status lookup produces `unknown` for only that directory and does not erase other results. |
| NFR-4 | Should | Usability | Usage errors name the missing or conflicting input so callers can correct requests without an upfront manual. |

## Constraints

- Destructive session/worktree deletion and project-path registration are excluded from the action contract
- The CLI adapter and the agent tool may not call or spawn each other
- Session status and messages come from official directory-scoped OpenCode APIs; message output includes only ordered `text` parts

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the control service
    - **When** an action outside the allowlist is requested
    - **Then** it is rejected
- [ ] **FR-2**
    - **Given** the CLI and the agent tool
    - **When** both perform the same action
    - **Then** behavior is identical because both delegate to one service
- [ ] **FR-4**
    - **Given** a freshly dispatched session with no activity
    - **When** wait is requested
    - **Then** it does not treat the initial idle response as completion
- [ ] **FR-5**
    - **Given** a session
    - **When** a message is sent or the session is forked
    - **Then** the action executes and reuses the last user-message model selection
- [ ] **FR-8**
    - **Given** an explicit projectId or directory scope
    - **When** the action resolves its target
    - **Then** explicit scope wins over the managed tool's current-session directory fallback
- [ ] **FR-12**
    - **Given** `agentControlToolEnabled: false`
    - **When** OpenChamber launches a managed OpenCode process
    - **Then** the `openchamber` tool is not injected
- [ ] **NFR-3**
    - **Given** multiple directories with one failing lookup
    - **When** status is requested
    - **Then** the failing directory reports `unknown` and the others return normally

## Conflicts

None identified yet.

## Open Questions

1. Should the action allowlist grow to cover permissions or file operations in a future release?

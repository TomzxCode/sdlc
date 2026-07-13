---
title: "Workspaces & Runtime"
status: done
---

# Requirements: Workspaces & Runtime

## Overview

Workspaces give agents the right working directory and runtime context. Project workspaces hold shared project state; execution workspaces are isolated git worktrees (often operator branches) where an agent runs. Runtime services (dev servers, preview URLs) and workspace operations (commands, diffs, uploads) support the execution. Environments and leases bind secret-aware env to execution targets.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Manage project workspaces, environments, runtime services |
| Agent | Check out an execution workspace, run commands, publish diffs |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support project workspaces and isolated execution workspaces (git worktrees). |
| FR-02 | Must | The system shall support workspace operations (commands, diffs, large uploads, git publishing). |
| FR-03 | Must | The system shall resolve execution workspace per issue (preference + settings fields on issues). |
| FR-04 | Should | The system shall support runtime services (dev servers, preview URLs) and their lifecycle. |
| FR-05 | Should | The system shall support environments with secret-aware env bindings and leases. |
| FR-06 | Should | The system shall base fresh worktrees on `origin/master` and refresh unstarted reuses. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Should | Security | Workspace command authorization must scope commands to the workspace and agent. |
| NFR-02 | Should | Reliability | Large workspace uploads and git publishing must succeed without truncation. |

## Constraints

- Workspace runtime services are optional and provider-dependent (e.g. Daytona sandbox leases).

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** an issue with an execution workspace preference
    - **When** the agent checks out
    - **Then** an isolated execution workspace is resolved/created for the run

## Conflicts

None identified yet.

## Open Questions

1. Which sandbox providers are supported and how are leases reused (e.g. Daytona)?

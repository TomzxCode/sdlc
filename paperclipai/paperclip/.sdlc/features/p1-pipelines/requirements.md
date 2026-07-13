---
title: "Pipelines"
status: done
---

# Requirements: Pipelines

## Overview

Pipelines provide structured, stage-based workflows for tracking work items (cases) through defined lifecycle stages (working, review, done, cancelled) with configurable transitions, automated execution agents, and full event audit trails. Cases carry structured fields, workspace references, parent/child hierarchy, issue links, and lease-based ownership. The pipeline system integrates with agents for automated stage transitions and with the heartbeat execution system for automation runs.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Define pipelines with stages and transitions; view and manage cases; configure automation agents |
| Agent | Claim cases, execute automation workflows, suggest/perform stage transitions |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating pipelines with a key, name, description, project association, and transition enforcement flag. |
| FR-02 | Must | The system shall support pipeline stages with kind (working, review, done, cancelled), config, and position ordering. |
| FR-03 | Must | The system shall support pipeline transitions defining allowed moves between stages. |
| FR-04 | Must | The system shall support creating cases within a pipeline with title, summary, structured fields, and stage assignment. |
| FR-05 | Must | The system shall support case lifecycle with lease-based ownership for agent claiming and releasing. |
| FR-06 | Must | The system shall record full event history for each case (ingested, transitioned, claimed, reviewed, automated actions, blockers, issues linked). |
| FR-07 | Must | The system shall support case workspace references linking cases to execution workspaces. |
| FR-08 | Should | The system shall support pipeline automation with retry plans, agent assignment, and heartbeat-run integration. |
| FR-09 | Should | The system shall support case-to-issue linking for tracking work products. |
| FR-10 | Should | The system shall support case parent/child hierarchy with version tracking. |
| FR-11 | Should | The system shall support pipeline settings in a dedicated UI page. |
| FR-12 | May | The system shall support transition suggestion with agent-provided rationale and confidence scoring. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | All pipeline operations must be company-scoped and enforce company access checks. |
| NFR-02 | Should | Observability | Case events must provide a complete audit trail of all state changes. |

## Constraints

- Pipeline keys must be unique within a company.
- Stage kinds are constrained to working, review, done, cancelled.
- Every case belongs to exactly one pipeline and one stage.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** A board operator
    - **When** They create a pipeline with key, name, and project
    - **Then** The pipeline is persisted and accessible via the API
- [ ] **FR-02**
    - **Given** A pipeline exists
    - **When** Stages are added with kinds and positions
    - **Then** Stages are ordered and kind-validated
- [ ] **FR-03**
    - **Given** A pipeline has stages
    - **When** Transitions are defined between them
    - **Then** Only allowed transitions are permitted
- [ ] **FR-04**
    - **Given** A pipeline exists
    - **When** A case is created with title and fields
    - **Then** The case is placed in the initial stage
- [ ] **FR-05**
    - **Given** A case exists
    - **When** An agent claims it
    - **Then** A lease with expiry is created; concurrent claims are prevented
- [ ] **FR-06**
    - **Given** A case undergoes state changes
    - **When** Events occur (transition, claim, review)
    - **Then** Events are recorded with actor, type, and payload
- [ ] **NFR-01**
    - **Given** A pipeline belongs to company A
    - **When** An agent from company B accesses it
    - **Then** Access is denied

## Conflicts

None identified yet.

## Open Questions

1. How does pipeline automation interact with the existing heartbeat execution and routine scheduling systems?
2. Are pipeline cases expected to generate issues automatically, or is issue linking manual?

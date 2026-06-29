---
title: "Environment Management"
status: draft
---

# Requirements: Environment Management

## Overview

Environments are named configuration contexts (e.g., staging, production) that hold key/value bindings with secret reference resolution. They are scoped to a company and can be leased to agents for execution context. Environment variables are resolved in a defined overlay order: project env → environment env → routine env → Paperclip runtime-owned keys.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Create, configure, and manage environments; assign environments to projects |
| Agent | Receive resolved environment variables at runtime |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support named environments scoped to a company (e.g., staging, production). |
| FR-02 | Must | Environments shall hold key/value pairs and support secret reference syntax (`${{ secrets.key }}`). |
| FR-03 | Must | The system shall support environment leases that grant an agent access to an environment for a period of time. |
| FR-04 | Should | The system shall expose an environment selection flow for agents requesting execution context. |
| FR-05 | Should | The system shall resolve environment variables at execution time in the defined overlay order. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Secret references within environment values must be resolved at runtime, not stored in plaintext in the environment definition. |
| NFR-02 | Should | Audibility | Environment access and lease creation should be logged in the activity log. |

## Constraints

- Environments are optional; agents can run without an environment lease.
- Environment values are resolved at heartbeat time, not stored as plaintext.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** a company
    - **When** an environment is created with name and key/value pairs
    - **Then** the environment is stored and scoped to the company
- [ ] **FR-03**
    - **Given** an environment and an agent
    - **When** a lease is created
    - **Then** the agent can resolve the environment variables at runtime
- [ ] **NFR-01**
    - **Given** an environment with a secret reference value
    - **When** the environment definition is read
    - **Then** the secret reference syntax is stored, not the resolved secret value

## Conflicts

None identified yet.

## Open Questions

1. What is the exact lease duration policy and renewal mechanism?
2. Can multiple agents share the same environment lease?

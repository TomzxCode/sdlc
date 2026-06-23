---
title: "Org Chart & Agents"
status: draft
---

# Requirements: Org Chart & Agents

## Overview

Agents are the AI employees of a company. They have roles, titles, reporting lines, capabilities, budgets, permissions, and adapter configuration. Agents form a strict reporting tree (`reports_to` nullable root) with no multi-manager reporting and no cycles. This feature covers agent lifecycle, org structure, adapter/API-key configuration, pause/resume/terminate, and the board approval flow for hiring.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Hire (directly or via approval), configure, pause/resume/terminate agents; view org chart |
| CEO agent | Proposes strategy; delegates work down the tree after board approval |
| Agent | Has an identity, reporting manager, budget, and an adapter that receives heartbeats |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating an agent scoped to a company with name, role, title, adapter type/config, and `reports_to`. |
| FR-02 | Must | The system shall enforce a strict tree org graph: `reports_to` nullable root, agent and manager in the same company, and no cycles. |
| FR-03 | Must | The system shall manage agent status (`active \| paused \| idle \| running \| error \| pending_approval \| terminated`) with the defined transition rules. |
| FR-04 | Must | The system shall reject resuming a `terminated` agent. |
| FR-05 | Must | The system shall create agent API keys hashed at rest, showing plaintext once at creation, with revocation. |
| FR-06 | Must | The system shall support pause/resume/terminate actions (board-only for terminate). |
| FR-07 | Should | The system shall support a hire-agent approval flow requested by an agent and decided by the board. |
| FR-08 | Should | The system shall support per-agent runtime config, context mode (`thin \| fat`), permissions JSONB, and optional cheap-model profile lane. |
| FR-09 | Should | The system shall track `last_heartbeat_at` and budget spent per agent. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Only hashed API keys are stored; plaintext is shown once at creation. |
| NFR-02 | Must | Auditability | All agent mutations (hire, pause, resume, terminate, key ops) write `activity_log`. |

## Constraints

- `terminated` is irreversible.
- Agent and manager must be in the same company.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-02**
    - **Given** an existing reporting tree
    - **When** a cycle-creating `reports_to` is attempted
    - **Then** the update is rejected with a `422`/`409` and the tree remains acyclic
- [ ] **FR-03**
    - **Given** an agent in `running`
    - **When** it is paused mid-run
    - **Then** the run is gracefully cancelled then force-killed and status becomes `paused`
- [ ] **FR-05**
    - **Given** a new API key request
    - **When** the key is created
    - **Then** only the hash is persisted and the plaintext is returned exactly once
- [ ] **NFR-01**
    - **Given** the `agent_api_keys` table
    - **When** inspected
    - **Then** no row contains recoverable plaintext key material

## Conflicts

None identified yet.

## Open Questions

1. What adapter types are fully supported in V1 and which are plugin-only?

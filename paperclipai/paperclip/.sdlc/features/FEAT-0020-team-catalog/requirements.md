---
title: "Team Catalog"
status: draft
---

# Requirements: Team Catalog

## Overview

The team catalog provides pre-built team templates with agent roles, skills, and configurations that can be installed into a company. It accelerates onboarding by letting operators deploy a fully-configured team (CEO, engineers, support agents, etc.) with a few clicks instead of manually creating each agent and assigning skills.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Browse, preview, and install team templates into their company |
| New company operator | Rapidly bootstrap a company from a template |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall expose a catalog of pre-built team templates. |
| FR-02 | Must | Each team template shall define agent roles, titles, reporting relationships, adapter configs, and skills. |
| FR-03 | Must | The system shall support installing a team template into a company, creating all defined agents. |
| FR-04 | Should | The system shall support team template discovery with search and filtering. |
| FR-05 | Should | The system shall report installation results (agents created, errors encountered). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Should | Usability | Template installation should complete within a few seconds. |

## Constraints

- Team templates are read-only catalogs; modifications must be done after installation.
- Installation respects company governance settings (e.g., `require_board_approval_for_new_agents`).

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-01**
    - **Given** the team catalog endpoint
    - **When** requested
    - **Then** a list of available templates is returned
- [ ] **FR-03**
    - **Given** a selected team template and a target company
    - **When** installation is requested
    - **Then** all defined agents are created in the company with correct roles and reporting structure

## Conflicts

None identified yet.

## Open Questions

1. Who maintains and publishes the team templates (Paperclip core vs. community)?
2. Are team templates versioned?

---
title: "Company Skills"
status: draft
---

# Requirements: Company Skills

## Overview

Skills are reusable, versioned bundles of agent capabilities that can be installed into a company and assigned to agents. The system includes a skills catalog for browsing available skills, per-company skill installation with version pinning, and team/agent skill assignments. Skills may include prompts, tools, MCP configurations, and other capability definitions. Operator-authored custom skills are also supported alongside catalog skills.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Browse catalog, install/pin skills to company, assign skills to agents/teams, manage custom skills |
| Agent | Consume assigned skills at runtime via heartbeat context |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support a skills catalog listing available skills with name, description, version, and metadata. |
| FR-02 | Must | The system shall support installing a skill into a company with version pinning. |
| FR-03 | Must | The system shall support assigning installed skills to individual agents or teams. |
| FR-04 | Must | The system shall include default skill bundles for common agent capabilities. |
| FR-05 | Should | The system shall support operator-authored custom skills alongside catalog skills. |
| FR-06 | Should | The system shall support skill versioning and upgrades within a company. |
| FR-07 | Should | The system shall support a teams catalog for pre-configured agent team templates. |
| FR-08 | Should | The system shall resolve skill selections at heartbeat runtime, injecting only assigned skills. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Should | Security | Custom skills must be validated before installation to prevent malicious content. |
| NFR-02 | Should | Performance | Skill resolution at heartbeat time must not add more than 200ms overhead. |

## Constraints

- Skills are company-scoped: each company has its own installed skill set.
- Default skills ship with the product; custom skills are operator-created.
- Team catalog entries may reference multiple skills and agents.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a board operator
    - **When** they view the skills catalog
    - **Then** available skills are listed with name, description, and version
- [ ] **FR-02**
    - **Given** a company
    - **When** a skill is installed
    - **Then** the skill is available for assignment within that company
- [ ] **FR-03**
    - **Given** an installed skill
    - **When** it is assigned to an agent
    - **Then** the agent receives that skill's capabilities at next heartbeat

## Conflicts

None identified yet.

## Open Questions

1. What is the exact skill definition format (prompts, tools, MCP, or a combination)?
2. How do skill version upgrades handle backward compatibility?
3. What is the team catalog's relationship to the org chart (are teams static templates or dynamic groupings)?

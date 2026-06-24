---
title: "Company Skills"
status: draft
---

# Specification: Company Skills

## Overview

Skills are versioned capability bundles. A central catalog lists available skills; companies install them with version pinning and assign them to agents or teams. At heartbeat runtime, the skill selection service resolves the set of skills active for the agent and injects them into the invocation context. The teams catalog provides pre-configured agent templates that bundle skills and agent configurations together.

## Architecture

```
Catalog ──► GET /api/catalog/skills (public skill definitions)
                │
Company ──► POST /api/companies/:companyId/skills (install + pin version)
                │
                ▼
           company_skills (skill_id, company_id, version)
                │
                ▼
           agent skill assignments (agent_skills / runtime_skill_selections)
                │
                ▼
           Heartbeat runtime → skill resolution → inject into context
```

## Data Models

### company_skills

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| company_id | uuid | FK, not null | Scoping |
| skill_id | text | not null | Catalog skill identifier |
| version | text | not null | Pinned version |
| config | jsonb | null | Per-install configuration |

### runtime_skill_selections

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | - |
| agent_id | uuid | FK, not null | Target agent |
| skill_id | text | not null | Skill reference |
| enabled | boolean | not null | Active/inactive |

## API Contracts

### GET /api/companies/:companyId/skills-catalog

Browse available skills.

### POST /api/companies/:companyId/skills

Install a skill for the company.

### POST /api/companies/:companyId/skills-catalog/install-from-catalog

Install from catalog directly.

### GET/DELETE /api/companies/:companyId/skills/:skillId

Manage installed skills.

### GET /api/catalog/teams, POST /api/companies/:companyId/teams-catalog

Teams catalog management.

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | Invalid skill reference or version |
| 404 | NOT_FOUND | Skill not found in catalog |

## Sequences

### Skill installation and assignment

```
Board → browse catalog → install skill (pin version) → company_skills row
Board → assign skill to agent → runtime_skill_selections row
Agent heartbeat → resolve agent's enabled skills → inject into invocation context → agent executes with skill capabilities
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Skill resolution | Runtime selection join at heartbeat | Skills are evaluated per invocation; no agent-side state |
| Version pinning | Company-specific version per skill | Companies upgrade on their own schedule |
| Catalog source | Built-in default skills + operator custom | Supports both out-of-box and tailored capability sets |

## Risks and Unknowns

1. Skill definition format is evolving; backward compatibility during catalog updates must be managed.
2. Custom skill validation is critical for security but the validation rules are not fully defined.
3. The relationship between the teams catalog and the org chart `/reports_to` tree needs documentation.

## Out of Scope

- Public skill marketplace or community contributions (ClipHub).
- Skill dependency resolution (skills requiring other skills).

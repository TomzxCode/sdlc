---
title: "Team Catalog"
status: done
---

# Specification: Team Catalog

## Overview

Team templates are JSON/YAML definitions of agent org trees with role assignments, adapter configs, and skill links. The catalog endpoint returns available templates. Installation creates agents in the target company by iterating the template definition and calling the agent creation service for each entry.

## Architecture

```
Board → GET /api/teams-catalog (list templates)
Board → POST /api/companies/:companyId/teams-catalog/install/:templateId (install)
           │
           ▼
      teams-catalog service → iterate template agents → create agents via agent service
           │
           ▼
      agents created in company (org tree, configs, skills)
```

## Data Models

No dedicated DB tables for team templates. Templates may be loaded from files or fetched from a remote catalog source. Installation results are returned inline.

## API Contracts

### GET /teams-catalog

List available team templates.

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| templates | array | Template objects with id, name, description, agent count |

### POST /companies/:companyId/teams-catalog/install/:templateId

Install a team template into a company.

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| created | int | Number of agents created |
| errors | array | List of errors encountered |

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 403 | UNAUTHORIZED | Caller lacks company access |
| 404 | NOT_FOUND | Template not found |

## Sequences

### Template installation

```
Board → select template → POST install → validate template → for each agent definition: createAgent() → report results
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Template source | Loaded from files/packages | Simple V1; no remote catalog sync needed |
| Installation | Sequential agent creation | Simpler than batch; errors are scoped per agent |

## Risks and Unknowns

1. Installation may fail partway through if some agents fail to create; cleanup/rollback semantics needed.
2. Skill references in templates may reference skills that do not exist in the target company.

## Out of Scope

- User-customizable team templates (modify template before install)
- Community template marketplace (ClipHub) — deferred

---
title: "Skills Catalog"
status: done
---

# Specification: Skills Catalog

## Overview

The skills catalog system is split between server-side discovery/installation logic (`packages/web/server/lib/skills-catalog/`) and client-side UI (`packages/ui/src/components/sections/skills/`, `packages/ui/src/stores/useSkillsCatalogStore.ts`, `useSkillsStore.ts`). The server fetches remote catalogs and manages local skill files; the UI provides browsing, search, and management.

## Architecture

```
Skills Settings UI (packages/ui/src/components/sections/skills/)
    |
    v  REST calls
Express Server (packages/web/server/lib/skills-catalog/)
    |
    +---> Remote catalog fetch (HTTP)
    +---> Local skill file management (.opencode/skills/)
    +---> OpenCode skill sync
```

## Data Models

### Skill

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Skill identifier |
| name | string | not null | Display name |
| description | string | not null | What the skill does |
| source | string | not null | Catalog source URL |
| version | string | nullable | Skill version |
| installed | boolean | not null | Whether installed locally |
| enabled | boolean | not null | Whether active |

### SkillSource

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Source identifier |
| name | string | not null | Display name |
| url | string | not null | Catalog URL |
| type | enum | not null | builtin, custom |

## API Contracts

### GET /api/skills/catalog

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| skills | Skill[] | Available skills from all sources |

### POST /api/skills/install

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| skillId | string | yes | Skill to install |

### POST /api/skills/uninstall

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| skillId | string | yes | Skill to uninstall |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | File-based in .opencode/skills/ | Consistent with OpenCode's convention; no database needed |
| Catalog fetch | Server-side HTTP with caching | Avoids CORS issues; server can cache and validate |
| UI | Settings section under Skills | Follows existing settings UI patterns |

## Risks and Unknowns

1. Remote catalog availability may be intermittent
2. Skill schema compatibility between OpenCode versions

## Out of Scope

- Skill authoring UI
- Private skill registries with authentication
- Skill dependency resolution

---
title: "Custom Slash Commands"
status: draft
---

# Specification: Custom Slash Commands

## Overview

Custom commands are managed via `useCommandsStore.ts` with a settings page at `sections/commands/`. The chat input autocomplete (`CommandAutocomplete.tsx`) merges custom commands with built-in commands and skills.

## Architecture

```
Commands Settings (packages/ui/src/components/sections/commands/)
    +---> CommandsPage (CRUD UI)
    +---> CommandsSidebar (command list)
    +---> AgentSelector (per-command agent assignment)
    |
    v  Store
useCommandsStore.ts (command definitions, scope management)
    |
    v  Merged in autocomplete
CommandAutocomplete.tsx (built-in + custom + skills)
```

## Data Models

### CustomCommand

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Command identifier |
| name | string | not null | Slash command name (without /) |
| description | string | not null | What the command does |
| template | string | not null | Prompt template text |
| agent | string | nullable | Target agent |
| model | string | nullable | Target model |
| scope | enum | not null | user, project |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Scope | User and project level | User commands work everywhere; project commands are workspace-specific |
| Storage | OpenCode config via store | Commands are part of the agent configuration ecosystem |

## Out of Scope

- Command marketplace
- Nested or chained commands
- Conditional logic in templates

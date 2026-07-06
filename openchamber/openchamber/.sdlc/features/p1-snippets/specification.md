---
title: "Snippets (Code Snippet Management)"
status: draft
---

# Specification: Snippets

## Overview

Snippets are markdown files stored in the OpenCode config directory (`~/.config/opencode/snippets/` or `~/.config/opencode/snippet/`) and project-level `.opencode/snippets/` directories. The server provides CRUD operations via the OpenCode API, and the UI provides a settings page and chat autocomplete integration.

## Architecture

```
User types "/" in chat input
    |
    v
SnippetAutocomplete.tsx reads snippets from useSnippetsStore
    |
    v  HTTP request
Express Server → opencode/snippets.js (CRUD on snippet files)
    |
    v  File system
~/.config/opencode/snippets/*.md  and  .opencode/snippets/*.md
```

## Data Models

### Snippet

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK, pattern: `^[a-z0-9][a-z0-9_-]{0,79}$` | Unique snippet identifier |
| content | string | not null | Markdown snippet body |
| aliases | string[] | optional | Alternative trigger names |
| description | string | optional | Human-readable description |
| scope | string | `global` or `project` | Where the snippet is available |

## API Contracts

Snippet operations are exposed through the OpenCode config API. The server routes live in `packages/web/server/lib/opencode/snippets.js`.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage format | Markdown files on disk | Simple, version-controllable, no database needed |
| Snippet scope | Global + project directories | Users own global snippets; teams share project snippets via git |

## Risks and Unknowns

1. Snippet expansion in autocomplete may conflict with other `/` commands (skills, slash commands). The system uses a hashtag-based detection in text expansion, but autocomplete priority needs careful handling.

## Out of Scope

- Snippet sharing/catalog (beyond file-based project sharing)
- Dynamic template variables (e.g., `{{selection}}`)

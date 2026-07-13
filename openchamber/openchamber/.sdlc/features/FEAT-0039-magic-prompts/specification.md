---
title: "Magic Prompts"
status: done
---

# Specification: Magic Prompts

## Overview

Magic prompts are defined server-side in `packages/web/server/lib/magic-prompts/` and managed client-side via `useMagicPromptsStore.ts` with settings at `sections/magic-prompts/`. Templates use placeholders that are filled with context (diff, issue body, etc.) at generation time.

## Architecture

```
MagicPromptsPage / MagicPromptsSidebar (packages/ui/src/components/sections/magic-prompts/)
    +---> Prompt list by group (Git, GitHub, Planning, Session)
    +---> Edit instruction template
    +---> Show/hide toggle
    |
useMagicPromptsStore.ts (prompt definitions, user overrides)
    |
Server (packages/web/server/lib/magic-prompts/)
    +---> 31 built-in prompt definitions
    +---> Template rendering with context injection
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | Server-side definitions, client-side overrides | Built-in prompts ship with the app; user customizations persist locally |
| Grouping | By functional area (Git, GitHub, Planning, Session) | Matches user mental model for when to use each prompt |

## Out of Scope

- User-created prompt templates (use Custom Slash Commands instead)
- Prompt marketplace

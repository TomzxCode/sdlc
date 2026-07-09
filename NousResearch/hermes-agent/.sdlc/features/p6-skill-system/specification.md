---
title: "Skill System"
status: draft
---

# Specification: Skill System

## Overview

Skills are loaded from two parallel surface directories: skills/ (built-in, loadable by default) and optional-skills/ (shipped but inactive, installed via hermes skills install). Agent-created skills live under ~/.hermes/skills/. The curator monitors usage and auto-archives stale skills.

## Architecture

```
Skill loading:
    ├── skills/ (built-in, ~18 categories)
    ├── optional-skills/ (optional, ~20 categories)
    ├── ~/.hermes/skills/ (agent-created)
    │   └── .archive/ (curator-archived)
    └── Skills Hub (community distribution via tools/skills_hub.py)

Skill lifecycle:
    Agent creates skill → active → ...usage tracked...
        └── stale? → curator archives (never deletes)
        └── pinned? → curator exempt

Skill injection:
    skill_commands.py scans skills/ → generates user message injected at session start
    └── NOT system prompt (preserves prompt caching)
```

## Data Models

### SKILL.md Frontmatter

| Field | Type | Description |
|---|---|---|
| name | string | Skill name |
| description | string | ≤60 characters, one sentence, ends with period |
| version | string | Semantic version |
| author | string | Human contributor first |
| license | string | License identifier |
| platforms | list | OS-gating list (macos, linux, windows) |
| metadata.hermes.tags | list | Search tags |
| metadata.hermes.category | string | Category name |
| metadata.hermes.related_skills | list | Cross-references |

### Skill Usage (sidecar JSON)

| Field | Type | Description |
|---|---|---|
| use_count | int | How many times the skill was invoked |
| view_count | int | How many times the skill was viewed |
| patch_count | int | How many times the skill was edited |
| last_activity_at | ISO date | Most recent activity |
| state | string | active / stale / archived |
| pinned | bool | Exempt from auto-transitions |

## API Contracts

No API contracts. Skills interact with the agent through the system prompt injection mechanism and the skill_tool's skill_manager_tool() functions.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Injection method | User message, not system prompt | Preserves prompt caching — system prompt is byte-stable per conversation |
| Skill loading | Slash command scans skills/ at session start | Adds a user message with skill instructions, not a system prompt modification |
| Curator | Background process with LLM review | Automates skill lifecycle management without user intervention |
| Archives | Near for safe recovery | Never deletes skills — moves to .archive/ for restoration |

## Risks and Unknowns

1. Large numbers of loaded skills could dilute model attention
2. Agent-created skills may have variable quality — the curator's LLM review pass attempts to address this
3. Skill = user message pattern means skills are subject to the model's context window, not the system prompt cache

## Out of Scope

- Skill marketplace or community hub (the Skills Hub is a basic distribution mechanism)
- Automated skill testing or validation
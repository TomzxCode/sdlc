---
title: "Custom Slash Commands"
status: done
---

# Requirements: Custom Slash Commands

## Overview

Users can define custom slash commands with name, description, agent, model, template, and scope. These appear in chat input autocomplete alongside built-in commands and skills. Commands have user or project scope with full CRUD management via a settings page.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Power users | Create reusable prompt shortcuts for common workflows |
| Teams | Share project-scoped commands for consistent agent behavior |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall allow creating custom slash commands with name, description, template, agent, and model. |
| FR-02 | Must | The system shall support user-level and project-level command scope. |
| FR-03 | Must | The system shall show custom commands in chat input autocomplete. |
| FR-04 | Must | The system shall support editing and deleting custom commands. |
| FR-05 | Should | The system shall support slash command message ID preservation for undo/redo. |
| FR-06 | Should | The system shall treat commands as plain markdown templates without variable interpolation or context injection. |
| FR-07 | May | The system shall not provide a command marketplace or sharing mechanism. |

## Acceptance Criteria

- [ ] FR-01: Given the commands settings page, the user creates a new command with a template
- [ ] FR-02: Given a project-scoped command, it only appears in that project's autocomplete
- [ ] FR-03: Given custom commands, typing `/` in chat shows them alongside built-in commands
- [ ] FR-04: Given an existing custom command, the user can edit its name, description, template, agent, or model; the user can also delete it
- [ ] FR-05: Given a slash command message, the original command text carries a message ID for undo/redo tracking
- [ ] FR-06: Given a custom command template, it is rendered as plain markdown with no variable substitution
- [ ] FR-07: Given the commands UI, no marketplace, sharing, or download option is available

## Constraints

- Commands are stored in `.opencode/commands/` or `~/.config/opencode/commands/`

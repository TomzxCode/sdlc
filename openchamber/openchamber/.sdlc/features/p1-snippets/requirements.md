---
title: "Snippets (Code Snippet Management)"
status: draft
---

# Requirements: Snippets

## Overview

A snippet management system that lets users create, edit, and auto-expand reusable text templates in the chat input. Snippets can be global (shared across all projects) or project-scoped, support aliases for quick expansion, and are stored as markdown files in the OpenCode config directory or project `.opencode/snippets/` directory.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Speed up repetitive chat inputs with autocomplete-expandable snippets |
| Teams | Share project-specific snippets via `.opencode/snippets/` in version control |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating, reading, updating, and deleting snippets with a name, content, optional aliases, and optional description. |
| FR-02 | Must | The system shall support two snippet scopes: global (shared across all projects) and project (scoped to a directory). |
| FR-03 | Must | The system shall expand snippet references in chat input (e.g., `/snippet-name`) with the snippet content via autocomplete. |
| FR-04 | Must | The system shall store snippets as markdown files in the OpenCode config directory (`~/.config/opencode/snippets/`) and project `.opencode/snippets/` directories. |
| FR-05 | Should | The system shall support snippet aliases for multiple trigger words. |
| FR-06 | Should | The system shall provide a settings page for managing snippets with a list, editor, and preview. |
| FR-07 | Should | The system shall load snippets from both global and project directories on startup and cache them with a TTL. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Snippet expansion shall complete within 100ms for typical snippet sizes. |
| NFR-02 | Should | Usability | The snippet autocomplete shall appear within 200ms of typing a `/` trigger in the chat input. |

## Acceptance Criteria

- [ ] FR-01: Given a user creates a snippet with name and content, the snippet is stored and retrievable.
- [ ] FR-01: Given an existing snippet, the user can update its content and aliases.
- [ ] FR-01: Given an existing snippet, the user can delete it.
- [ ] FR-02: Given a global snippet, it is available in all projects.
- [ ] FR-02: Given a project snippet, it is only available when the project directory matches.
- [ ] FR-03: Given a chat input with `/snippet-name`, the system expands it to the snippet content.
- [ ] FR-06: Given the settings page, the user can view, create, edit, and delete snippets.

## Open Questions

1. Should snippets support dynamic variables (e.g., `{{selection}}`) for inserting selected text?


---
title: "Multi-Platform CLI"
status: done
---

# Requirements: Multi-Platform CLI

## Overview

The HermesCLI class provides an interactive terminal experience with Rich-styled banners, prompt_toolkit input with autocomplete, a kawaii animated spinner, a data-driven skin/theme system, and a central slash command registry supporting ~70 commands across five categories. The CLI is the primary user-facing surface and also serves as the embedding target for the web dashboard via PTY bridge.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Power users | A rich, visually appealing interactive CLI with autocomplete, theming, and fast slash commands |
| Developers | Easy-to-add slash commands via the COMMAND_REGISTRY with automatic cross-surface dispatch |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The CLI shall support slash commands for session management (/new, /undo, /branch, /compress, /snapshot) |
| FR-2 | Must | The CLI shall support configuration commands (/model, /skin, /reasoning, /voice, /fast, /yolo) |
| FR-3 | Must | The CLI shall support tools and skills management commands (/tools, /skills, /cron, /learn, /plugins, /kanban, /curator, /blueprint) |
| FR-4 | Must | The CLI shall support info commands (/help, /usage, /insights, /debug, /version) |
| FR-5 | Must | The CLI shall support a skin/theme system with built-in skins and user-customizable YAML skins |
| FR-6 | Must | The CLI shall provide Rich-styled banners and a kawaii animated spinner during API calls |
| FR-7 | Must | The CLI shall support prompt_toolkit input with slash-command autocomplete |
| FR-8 | Must | The CLI shall support history across sessions |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Slash command dispatch shall complete in under 100ms |
| NFR-2 | Must | Compatibility | The CLI shall work in tmux, screen, iTerm2, and standard terminals |

## Constraints

- The skin engine must be pure data — no code changes needed to add a skin
- Skin customization includes banner colors, spinner faces/verbs/wings, tool prefixes, per-tool emojis, and branding text

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the CLI is running
    - **When** the user types /new
    - **Then** a new session is created and the conversation restarts
- [ ] **FR-5**
    - **Given** the CLI is running
    - **When** the user types /skin ares
    - **Then** the banner colors and spinner change to the ares theme
- [ ] **FR-7**
    - **Given** the CLI is running
    - **When** the user types /
    - **Then** a dropdown of available slash commands appears

## Conflicts

None identified yet.

## Open Questions

1. Should the classic prompt_toolkit CLI eventually be deprecated in favor of the TUI?
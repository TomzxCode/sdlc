---
title: "Multi-Platform CLI"
status: done
---

# Specification: Multi-Platform CLI

## Overview

The CLI is built on prompt_toolkit for input with autocompletion and Rich for output rendering. Commands are defined centrally in the COMMAND_REGISTRY in hermes_cli/commands.py, which all downstream consumers (CLI dispatch, gateway dispatch, Telegram menu, Slack mapping, autocomplete) derive from automatically.

## Architecture

```
prompt_toolkit REPL
     │
     ├── text input ──→ process_text()
     │                      │
     │               ┌────┴────────┐
     │               │ Text input  │→ AIAgent.chat()
     │               │             │
     │               │ Slash cmd   │→ process_command()
     │               └─────────────┘
     │                      │
     │               resolve_command(name)
     │                      │
     │               matched CommandDef
     │                      │
     │               handler method
     │
     └── autocomplete ──→ SlashCommandCompleter
                                  │
                           queries COMMAND_REGISTRY
```

## Data Models

### CommandDef

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK, not null | Canonical command name without slash |
| description | string | not null | Human-readable description |
| category | string | Session/Configuration/Tools & Skills/Info/Exit | Display category for help |
| aliases | tuple | optional | Alternative names |
| args_hint | string | optional | Argument placeholder shown in help |
| cli_only | bool | default false | Only available in interactive CLI |
| gateway_only | bool | default false | Only available in messaging platforms |
| gateway_config_gate | string | optional | Config dotpath that gates availability in gateway |

### SkinConfig

| Field | Type | Description |
|---|---|---|
| name | string | Skin identifier |
| colors | dict | Banner border, title, accent, dim, text; response border |
| spinner | dict | Waiting faces, thinking faces, thinking verbs, optional wings |
| branding | dict | Agent name, welcome message, response label, prompt symbol |
| tool_prefix | string | Prefix character for tool output |
| tool_emojis | dict | Per-tool emoji mapping |

## API Contracts

No external API contracts. The CLI communicates with AIAgent through direct method calls.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Skin engine | Pure data (YAML + defaults) | No code changes needed for new skins; users can create custom skins |
| Command registry | Centralized list | One definition drives CLI, gateway, autocomplete, help, Telegram BotCommands, and Slack mapping |
| Input framework | prompt_toolkit | Supports cross-platform input, autocomplete, history, Vi mode |
| Output rendering | Rich | Supports styled output, tables, panels, progress display |

## Risks and Unknowns

1. The classic CLI has grown to ~16k LOC — god-file refactoring is needed but risky for an active codebase
2. prompt_toolkit's patch_stdout conflicts with ANSI escape codes used by the spinner

## Out of Scope

- The TUI (ui-tui/) is a separate surface, not part of the classic CLI
- GUI elements beyond terminal rendering
---
title: "Command-Line Interface"
status: draft
---

# Specification: Command-Line Interface

## Overview

The CLI is built using yargs for command parsing with nested subcommands. The entry point is `openclaw.mjs` which bootstraps the runtime and dispatches to command handlers. Each command is a module under `src/cli/` that registers its subcommand with yargs.

## Architecture

```
openclaw.mjs (entry point)
     │
     ▼
src/cli/
  ├── program.ts          → yargs setup and command registration
  ├── gateway-cli.ts      → gateway start/stop commands
  ├── plugins-cli.ts      → plugin management commands
  ├── config-cli.ts       → config CRUD commands
  ├── channels-cli.ts     → channel commands
  ├── models-cli.ts       → model/provider commands
  ├── secrets-cli.ts      → credential management
  ├── onboard (wizard)    → interactive setup
  └── ...
```

## Data Models

### CLICommand

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | PK | Command name (e.g., `plugins install`) |
| description | string | not null | Help text |
| handler | function | not null | Command implementation |
| options | yargs.Options | nullable | Command flags and arguments |

## Sequences

### Plugin Install Flow

```
User → CLI: openclaw plugins install @openclaw/plugin-telegram
CLI → Plugin Registry: resolve package
CLI → npm: install package
CLI → Config: update openclaw.json
CLI → User: confirmation message
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Command parsing | yargs | Mature, feature-rich, TypeScript-friendly |
| Entry point | Single `openclaw.mjs` | Simple PATH setup, standard npm bin pattern |
| Dynamic import | Lazy command loading | Fast startup for simple commands |
| Interactive flow | Inquirer-based prompts | Consistent user experience for wizards |

## Risks and Unknowns

1. Windows compatibility may require additional path handling and shell integration
2. TUI mode adds complexity and may have cross-terminal compatibility issues
3. Onboarding wizard must remain up-to-date with config schema changes

## Out of Scope

- Native binary distribution (requires Node.js runtime)
- GUI installer
- Remote CLI over SSH

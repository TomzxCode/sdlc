---
title: "Config System"
status: done
---

# Specification: Config System

## Overview

The Config System discovers `opencode.json`/`opencode.jsonc` files from multiple search paths, parses them with JSONC support, validates values against typed schemas, and merges them into a unified settings object. Each config domain is exposed as a typed namespace for consumption by its subsystem.

## Architecture

```
Global config (~/.config/opencode/opencode.json)
    │
Ancestor config (search up from project root)
    │
Project config (.opencode/opencode.json, opencode.json)
    │
    ▼
Config Discovery → Parsing (JSONC) → Validation → Merge → Typed Namespaces
                                                              │
                     ┌────────────────────────────────────────┼──────────────────────────┐
                     ▼                ▼                ▼                ▼
               ConfigAgent     ConfigProvider     ConfigPlugin     ConfigTool
               ConfigMCP       ConfigPermission  ConfigWatcher    ConfigFormatter
               ConfigLSP       ConfigSnapshot    ConfigTUI        ConfigMarkdown
                                                              │
                                                     Hot-reload watcher
```

## Data Models

### ConfigSource

| Field | Type | Constraints | Description |
|---|---|---|---|
| path | text | PK | File path of the config source |
| priority | integer | not null | Merge priority (higher wins) |
| parsed | json | not null | Parsed configuration content |

### ConfigNamespace (per domain)

Each domain (agent, provider, plugin, etc.) defines its schema as an Effect Schema and exposes a typed namespace object with a self-export pattern at the top of its module file (e.g. `export * as ConfigAgent from "./agent"`).

## API Contracts

Config resolution is internal (not an HTTP endpoint). The primary interface is the `ConfigService` Effect service:

### ConfigService.resolve()

**Signature:** `Effect<Config, ConfigError>`

Returns the merged, validated configuration for the current project directory.

### ConfigService.watch()

**Signature:** `Stream<Config, ConfigError>`

Returns a stream of configuration snapshots that emits when files change.

## Sequences

### Config resolution on server start

```
Server start → ConfigDiscovery.search(directory)
                   │
                   ├── Read global config (if exists)
                   ├── Walk ancestors (if opencode.json or .opencode/ found)
                   ├── Read project-local config
                   └── Merge all sources by priority
                   │
                   ▼
              ConfigService.resolve() → typed namespaces
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Config format | JSONC | Familiar to JS/TS developers; supports comments and trailing commas |
| Merge strategy | Deep merge by priority | Predictable override behavior |
| Namespace pattern | Self-export at top of file | Clear ownership; matches existing project conventions |
| Validation | Effect Schema at boundaries | Type-safe validation with descriptive errors |
| Cache behavior | Cached, invalidated on file change | Performance; hot-reload for development |

## Risks and Unknowns

1. Legacy V1 config keys must be supported during the migration period, adding complexity to the schema.
2. Plugin-contributed config namespaces are registered dynamically and may conflict with built-in names.
3. Config file changes during active sessions require careful race-condition handling.

## Out of Scope

- Runtime mutable settings (those are session or project state, not config).
- UI-based config editor (the TUI and web app may provide one but it is not part of the config system itself).

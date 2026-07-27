---
title: "Config System"
status: done
---

# Requirements: Config System

## Overview

The Config System manages OpenCode's structured configuration through discovery, parsing, validation, and resolution of `opencode.json`/`opencode.jsonc` files.
Configuration is sourced from global, ancestor, and project-local `.opencode/` directories and merged into a unified settings object consumed by every subsystem: agents, providers, tools, plugins, permissions, MCP, watchers, formatters, LSP, snapshots, sharing, and the terminal UI.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Simple, discoverable configuration via `opencode.json` with sensible defaults |
| Plugin authors | Stable config schema for registering plugin-specific settings |
| Core team | Centralized validation and resolution; legacy-to-V2 migration path |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall discover `opencode.json`/`opencode.jsonc` from global config directories, ancestor directories, and `.opencode/` directories. |
| FR-02 | Must | The system shall parse configuration files with JSONC support (comments and trailing commas). |
| FR-03 | Must | The system shall merge configurations from multiple sources with project-local settings taking highest precedence. |
| FR-04 | Must | The system shall expose typed namespaces for each config domain: agent, provider, tool, plugin, mcp, permission, watcher, formatter, lsp, snapshot, sharing, tui, markdown, compaction, experimental. |
| FR-05 | Must | The system shall validate configuration values against their expected types and report clear validation errors. |
| FR-06 | Must | The system shall support environment variable interpolation in configuration values. |
| FR-07 | Should | The system shall watch configuration files for changes and hot-reload when they are modified. |
| FR-08 | Should | The system shall provide a migration path from legacy V1 config keys to V2 equivalents. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Config parsing errors must not crash the server; invalid settings shall fall back to defaults. |
| NFR-02 | Must | Performance | Config resolution shall be cached and invalidated only when watched files change. |
| NFR-03 | Should | Usability | Config validation errors shall include file path, line number, and suggested fix. |

## Constraints

- Config files use JSONC format (JSON with comments and trailing commas).
- The `opencode.json` schema is versioned and may evolve across releases.
- Plugins register their config namespace via the plugin SDK's schema declaration.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** an opencode.json exists in the project root
    - **When** the config system resolves settings
    - **Then** it includes settings from global, ancestor, and project files merged appropriately
- [ ] **FR-03**
    - **Given** conflicting settings in global and project-local config
    - **When** the config system resolves a value
    - **Then** the project-local value takes precedence
- [ ] **FR-04**
    - **Given** a request for agent configuration
    - **When** ConfigAgent namespace is accessed
    - **Then** typed agent settings are returned
- [ ] **NFR-01**
    - **Given** a malformed opencode.json file
    - **When** the config system parses it
    - **Then** a validation error is returned without crashing the process

## Conflicts

None identified yet.

## Open Questions

1. Should the config system support YAML or TOML as alternative formats?
2. How should schema evolution be communicated to users when config keys change between versions?

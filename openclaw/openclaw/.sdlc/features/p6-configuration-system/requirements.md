---
title: "Configuration System"
status: done
---

# Requirements: Configuration System

## Overview

The Configuration System manages the `openclaw.json` configuration file, environment variables, schema validation, merge-patch logic, and configuration reload. It provides the single source of truth for all gateway, agent, channel, plugin, provider, and tool settings.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Understandable, well-documented configuration with sensible defaults |
| Operators | Reliable config reload, validation, and migration paths |
| Plugin developers | Clear config schema contracts for plugin configuration |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall load configuration from `openclaw.json` at startup |
| FR-2 | Must | The system shall validate configuration against a JSON schema (zod) |
| FR-3 | Must | The system shall support environment variable substitution in config values |
| FR-4 | Must | The system shall support hot-reload of configuration changes without restart |
| FR-5 | Must | The system shall support merge-patch updates to configuration |
| FR-6 | Must | The system shall provide migration from legacy configuration formats via `openclaw doctor --fix` |
| FR-7 | Must | The system shall support multiple methods of auth configuration (env vars, config file, credentials file) |
| FR-8 | Should | The system shall support configuration includes and inheritance |
| FR-9 | Should | The system shall redact secrets from configuration snapshots and logs |
| FR-10 | May | The system shall support runtime config overrides via CLI flags |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Secrets (API keys, tokens) must be redacted in logs and error output |
| NFR-2 | Must | Compatibility | Config schema validation shall provide clear error messages for deprecated keys |

## Constraints

- Config is stored as a single JSON file (`openclaw.json`) by default
- Runtime code reads only the current canonical schema; no silent compat for old shapes
- All migrations go through `openclaw doctor --fix`

## Acceptance Criteria

- [ ] **FR-1**: Given a valid `openclaw.json`, when the gateway starts, then the config is loaded and applied
- [ ] **FR-2**: Given an invalid `openclaw.json`, when the gateway starts, then a clear validation error is shown
- [ ] **FR-4**: Given a running gateway, when `openclaw.json` is modified, then the gateway detects the change and reloads
- [ ] **FR-6**: Given a legacy config file, when `openclaw doctor --fix` runs, then the config is migrated to the current schema
- [ ] **NFR-1**: Given a config snapshot, when it is logged, then all API keys and tokens are redacted

## Conflicts

None identified yet.

## Open Questions

1. Should there be a config schema generation tool for plugin developers?
2. How should conflicting config sources (env vs file vs CLI) be resolved?

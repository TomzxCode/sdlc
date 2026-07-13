---
title: "Plugin SDK and Extension System"
status: done
---

# Requirements: Plugin SDK and Extension System

## Overview

The Plugin SDK provides the tools, contracts, and APIs for building extensions to OpenClaw. The extension system manages plugin discovery, installation, lifecycle, configuration, and import boundaries. This enables community-contributed channels, model providers, tools, and other capabilities.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Plugin developers | Well-documented SDK, clear contracts, easy testing |
| Maintainers | Stable API surface, backward compatibility, security boundaries |
| End users | Access to a rich ecosystem of community plugins via ClawHub |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The SDK shall provide TypeScript types and interfaces for building channel, provider, and tool plugins |
| FR-2 | Must | The system shall support installing plugins from npm packages |
| FR-3 | Must | The system shall manage plugin lifecycle (install, activate, deactivate, uninstall, update) |
| FR-4 | Must | The system shall enforce import boundaries so plugins cannot import core internals |
| FR-5 | Must | The system shall support plugin configuration via `openclaw.json` |
| FR-6 | Must | The system shall provide a plugin registry with discovery and search |
| FR-7 | Should | The system shall support ClawHub marketplace for community plugin discovery |
| FR-8 | Should | The system shall provide plugin testing utilities in the SDK |
| FR-9 | May | The system shall support plugin permissions and capability gating |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Plugin import boundary enforcement shall prevent plugins from accessing core modules outside the SDK |
| NFR-2 | Must | Compatibility | The SDK public API shall maintain backward compatibility within a major version |

## Constraints

- Plugins must not import from core `src/` directories; only `@openclaw/plugin-sdk` is allowed
- Bundled plugins ship with core; external plugins are installed from npm
- Plugin code must be compatible with the facade-runtime pattern

## Acceptance Criteria

- [ ] **FR-1**: Given a plugin project, when the developer imports from `@openclaw/plugin-sdk`, then all required types are available
- [ ] **FR-4**: Given a plugin that imports from `src/gateway`, when the import boundary check runs, then it fails
- [ ] **FR-5**: Given a plugin with config schema, when the user sets config in `openclaw.json`, then the plugin reads it correctly
- [ ] **NFR-1**: Given a plugin import from `src/config`, when the boundary enforcement is active, then the import is blocked

## Conflicts

None identified yet.

## Open Questions

1. What is the plugin API stability guarantee (semver policy)?
2. Should there be a plugin sandbox for untrusted third-party plugins?

---
title: "Plugins & Extension Ecosystem"
status: done
---

# Requirements: Plugins & Extension Ecosystem

## Overview

A plugin SDK and management system lets third-party plugins extend the dashboard and engine. First-party "pi extensions" route Fusion's agent commands into different coding-agent CLIs (Claude CLI, Droid CLI, Llama.cpp), and plugins (e.g. reports, even-realities-glasses) plug into the runtime via manifests, lifecycle hooks, routes, and tools.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Discovers, installs, enables, configures, updates, uninstalls plugins |
| Plugin author | Builds plugins using the SDK/manifest/hooks/routes/tools |
| Operator | Manages plugin permission and interop, and the pi extension fleet |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall discover, install, enable, configure, update, and uninstall plugins from a plugin manager |
| FR-2 | Must | The system shall run plugins via a plugin runner with skill-body delivery and lifecycle hooks |
| FR-3 | Must | The system shall expose plugin authoring surfaces (manifest, SDK, routes, tools, dashboard UI/runtime contributions) |
| FR-4 | Must | The system shall route agent commands into coding-agent CLIs via first-party pi extensions (Claude CLI, Droid CLI, Llama.cpp) |
| FR-5 | Should | The system shall validate plugin interop and version pinning (pi versions pinned) |
| FR-6 | Should | The system shall expose plugin/extension management in dashboard (PluginManager, PiExtensionsManager) and CLI |
| FR-7 | Should | The system shall document authoring guidance and support MCP discovery isolation for in-process runtime plugins |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Plugins must not be force-installed without user action and must run under the plugin runner's permissions |
| NFR-2 | Must | Maintainability | Plugin interop drift must be checked at lint time |
| NFR-3 | Should | Performance | MCP discovery for in-process plugins must be isolated per plugin |

## Constraints

- Plugin SDK and runtime are part of the monorepo; `plugins/*` are bundled
- Authoring guidance lives in `docs/PLUGIN_AUTHORING.md`

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a plugin catalog entry
    - **When** the user installs/enables it
    - **Then** the plugin is installed, enabled, and configurable from the manager
- [ ] **FR-2**
    - **Given** an active plugin
    - **When** the plugin runner runs
    - **Then** lifecycle hooks and skill bodies are delivered per the contract
- [ ] **FR-4**
    - **Given** the `fn` CLI with a pi extension
    - **When** a command is issued
    - **Then** it routes into the target coding-agent CLI
- [ ] **NFR-2**
    - **Given** the workspace
    - **When** lint runs
    - **Then** plugin interop drift checks pass

## Conflicts

None identified yet.

## Open Questions

1. Which plugins are bundled first-party vs. external (reports, even-realities) is per-plugin; confirm the canonical list.
---
title: "Plugins (OpenCode Plugin Management)"
status: draft
---

# Requirements: Plugins

## Overview

A plugin management system for OpenCode plugins that extend agent behavior. Users can browse, install, configure, and remove OpenCode plugins from npm packages or local file paths. The system supports user-scoped and project-scoped plugins with JSON configuration options.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Extend agent capabilities with community or custom plugins |
| Teams | Share project-specific plugin configurations |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support adding plugins by npm package spec or local file path. |
| FR-02 | Must | The system shall support two plugin scopes: user (global) and project (per-directory). |
| FR-03 | Must | The system shall support enabling, disabling, and removing plugins. |
| FR-04 | Must | The system shall support plugin configuration options as JSON. |
| FR-05 | Should | The system shall display a plugin registry with available plugins and install counts. |
| FR-06 | Should | The system shall support importing plugin configurations from JSON snippets. |
| FR-07 | Should | The system shall refresh agent/plugin state after plugin changes without full restart. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Plugin installation from npm shall use the configured package manager with standard security checks. |
| NFR-02 | Should | Usability | The plugin settings page shall show plugin status (enabled/disabled/error) at a glance. |

## Acceptance Criteria

- [ ] FR-01: Given an npm package spec, the system installs and registers the plugin.
- [ ] FR-01: Given a local file path, the system registers the plugin from that file.
- [ ] FR-02: Given a user-scoped plugin, it is available across all projects.
- [ ] FR-02: Given a project-scoped plugin, it is only available in that project.
- [ ] FR-03: Given an installed plugin, the user can enable, disable, or remove it.
- [ ] FR-06: Given a JSON configuration snippet, the system imports and applies it.

## Open Questions

1. Should there be a curated plugin registry with verified plugins?

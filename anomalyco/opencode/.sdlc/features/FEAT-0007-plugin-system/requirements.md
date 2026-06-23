---
title: "Plugin System"
status: draft
---

# Requirements: Plugin System

## Overview

The Plugin System lets packages extend OpenCode through the `@opencode-ai/plugin` SDK with namespaced hooks and a direct runtime registry.
Plugins can contribute provider integrations, PTY environment overlays, tools, context sources, and TUI behavior, and the runtime awaits plugin readiness before serving sessions.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Plugin authors | Stable SDK, namespaced hooks, clear lifecycle |
| End users | Installable plugins that load reliably |
| Core team | Direct runtime registry; readiness guarantees; Location scoping |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a plugin SDK (`@opencode-ai/plugin`) exposing a namespaced hook API. |
| FR-02 | Must | The system shall register plugins through a direct runtime registry and await plugin readiness before proceeding. |
| FR-03 | Must | The system shall allow plugins to contribute provider integrations (e.g. OpenAI, xAI, Azure, Cloudflare, DigitalOcean, Snowflake Cortex, GitHub Copilot). |
| FR-04 | Must | The system shall allow plugins to supply a PTY environment overlay observed per Location. |
| FR-05 | Should | The system shall support plugin loading and installation flows. |
| FR-06 | Should | The system shall allow plugin-defined Context Sources via the System Context Registry. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Sessions shall not start until required plugins report readiness. |
| NFR-02 | Should | Extensibility | Plugin-defined context registration and hot-reload shall use the same scoped registry seam. |

## Constraints

- Built-in and instruction context producers register through the System Context Registry with stable contribution keys.
- Plugin-defined context registration and hot-reload lifecycle remain a follow-up built on the same scoped registry seam.
- The PTY environment is a server concern; standalone servers use an empty adapter.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** a plugin authored against `@opencode-ai/plugin`
    - **When** it is loaded
    - **Then** its hooks are registered under a stable namespace
- [ ] **FR-02**
    - **Given** plugins are installed
    - **When** the server starts
    - **Then** it awaits plugin readiness before serving sessions
- [ ] **FR-04**
    - **Given** a PTY environment plugin is active for a Location
    - **When** a PTY is created
    - **Then** the host overlay is applied with the resolved working directory

## Conflicts

None identified yet.

## Open Questions

1. When will plugin-defined Context Source hot-reload be implemented on the scoped registry seam?
2. Should legacy `experimental.chat.system.transform` be ported to a plugin hook or replaced by plugin-defined Context Sources?

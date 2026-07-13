---
title: "Plugin System"
status: done
---

# Requirements: Plugin System

## Overview

The plugin system lets operators extend Paperclip without forking it. Plugins are instance-wide, out-of-process workers with capability-gated host services, job scheduling, tool exposure, UI contributions, webhooks, and isolated database namespaces. The local/self-hosted early plugin runtime is in scope for V1; the cloud marketplace and packaged public distribution remain out of scope. External adapter plugins are loaded through this same flow with zero hardcoded adapter imports in the loader.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Install/configure plugins, manage state and jobs, view logs |
| Plugin author | Build external plugins (SDK + scaffolder) and external adapters |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support installing and configuring instance-wide plugins. |
| FR-02 | Must | The plugin loader shall have zero hardcoded adapter imports and load external adapters purely dynamically. |
| FR-03 | Must | The system shall expose capability-gated host services to plugins (tools, jobs, webhooks, UI contributions). |
| FR-04 | Must | `createServerAdapter()` shall include all optional adapter fields (especially `detectModel`). |
| FR-05 | Should | The system shall support plugin database namespaces with migrations. |
| FR-06 | Should | The system shall support plugin jobs, logs, webhooks, and managed resources. |
| FR-07 | Should | External adapter plugins shall be installable via the Adapter Plugin manager and `~/.paperclip/adapter-plugins.json` (including `file:` entries for local dev). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Plugin capabilities must be gated; a plugin must not exceed its granted capabilities. |
| NFR-02 | Should | Maintainability | Built-in UI parsers for adapters must be removed when fully externalized to avoid shadowing plugin parsers. |

## Constraints

- Cloud-grade plugin marketplace/distribution is out of scope for V1.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-02**
    - **Given** the plugin loader
    - **When** inspected
    - **Then** there are no hardcoded adapter imports; all adapters load dynamically
- [ ] **NFR-01**
    - **Given** a plugin attempting a capability it was not granted
    - **When** the call is made
    - **Then** it is denied

## Conflicts

None identified yet.

## Open Questions

1. What is the full capability taxonomy granted to plugins, and how are new capabilities added safely?

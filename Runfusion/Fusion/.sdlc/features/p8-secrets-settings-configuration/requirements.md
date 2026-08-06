---
title: "Secrets, Settings & Provider Configuration"
status: done
---

# Requirements: Secrets, Settings & Provider Configuration

## Overview

Fusion ships an encrypted secrets store with per-secret access policies, a global/project settings system with sync, model/provider credential management, and MCP server configuration. These surfaces are exposed through the Settings modal, CLI commands, and API routes, and constrain how agents access credentials and models.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Manages settings, secrets, providers, MCP servers, and model selection |
| Agents | Resolve provider/model and secret references during execution |
| Security | Enforces access policies on secret scopes |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall store secrets encrypted at rest with AES-256-GCM under scopes with access policies |
| FR-2 | Must | The system shall manage global and project settings with sync and precedence resolution |
| FR-3 | Must | The system shall manage provider/model credentials with instance rotation and fallback resolution |
| FR-4 | Must | The system shall configure and validate MCP servers, including secret references and CLI/dashboard import/export |
| FR-5 | Must | The system shall expose secrets/settings/mcp/provider operations via CLI, dashboard API, and Settings modal |
| FR-6 | Should | The system shall resolve the model-selection hierarchy (global→project→task→lane) per settings reference |
| FR-7 | Should | The system shall record credential rotation in the run-audit with append-only ids/counts/outcomes metadata |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Credential material must never be persisted in run-audit or logs |
| NFR-2 | Must | Security | Secrets must be masked/redacted in settings UI and CLI output |
| NFR-3 | Must | Reliability | Settings sync must reconcile across nodes/projects without clobbering |
| NFR-4 | Should | Usability | The onboarding wizard should guide provider setup with a quick-start list |

## Constraints

- Secrets master-key handling and scopes are documented in `docs/secrets.md` and `docs/architecture.md`
- Model resolution precedence is defined in `docs/settings-reference.md`

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a secret with a scope
    - **When** stored
    - **Then** it is encrypted at rest and only readable per its access policy
- [ ] **FR-2**
    - **Given** global and project settings
    - **When** read
    - **Then** precedence is resolved per the settings reference
- [ ] **FR-3**
    - **Given** multiple provider instances
    - **When** rotation/fallback applies
    - **Then** instances rotate with append-only run-audit records
- [ ] **FR-4**
    - **Given** an MCP server config
    - **When** validated
    - **Then** invalid configs are rejected with clear errors
- [ ] **NFR-1**
    - **Given** credential rotation
    - **When** audit records are written
    - **Then** no secret material appears in the audit

## Conflicts

None identified yet.

## Open Questions

1. How does secrets sync between nodes authenticate (auth parity review exists in docs)?
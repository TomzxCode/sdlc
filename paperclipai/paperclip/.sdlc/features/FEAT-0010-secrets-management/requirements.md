---
title: "Secrets Management"
status: draft
---

# Requirements: Secrets Management

## Overview

Paperclip manages secrets (API keys, tokens, credentials) centrally rather than storing them in plaintext in agent configs or project files. Secrets are versioned, bound to agents and projects via config paths, backed by pluggable provider vaults (local encrypted, AWS Secrets Manager, GCP, Vault), and every access is audited. The system supports inline env secret references in agent/project/routine configs and resolves them at runtime against the appropriate binding target.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Configure secret providers, create/rotate/revoke secrets, bind secrets to agents/projects, view access audit log |
| Agent | Consume secrets at runtime via env injection; never see plaintext in configs |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating, reading, updating, and deleting company-scoped secrets with a name, key, provider, and status. |
| FR-02 | Must | The system shall support versioned secrets with SHA256 fingerprinting of secret material. |
| FR-03 | Must | The system shall support binding secrets to agents, projects, and other targets via config paths with JSON schema-defined secret references. |
| FR-04 | Must | Every secret resolution and access attempt shall be recorded as a `secret_access_event` for auditability. |
| FR-05 | Must | The system shall support a pluggable provider architecture: local encrypted storage (default), AWS Secrets Manager, GCP, and HashiCorp Vault. |
| FR-06 | Must | Secret values shall never be returned in API responses after creation; only metadata and status are readable. |
| FR-07 | Should | The system shall support inline secret reference syntax (`${{ secrets.my-secret-key }}`) in agent configs, project env, and routine env. |
| FR-08 | Should | The system shall resolve secret references against the routine binding target when used in routine env (routine-owned secrets). |
| FR-09 | Should | The system shall support bulk secret binding operations and env overlay resolution for execution contexts. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Secret material must be encrypted at rest in the provider vault. |
| NFR-02 | Must | Auditability | Every secret read event must log who accessed which secret key at what time, attributed to an agent or user. |
| NFR-03 | Must | Security | Plaintext secrets must never be persisted in logs, activity entries, or run context snapshots. |
| NFR-04 | Should | Performance | Secret resolution at invocation time must not add more than 500ms overhead. |

## Constraints

- Provider config is instance-wide (not per-company for V1).
- Inline secret references use a specific syntax and are distinct from direct secret bindings.
- Secrets are company-scoped: agent/project/routine within company A cannot access company B's secrets.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a board operator with a company
    - **When** they create a secret with name, key, and provider
    - **Then** the secret row exists with status `active` and metadata is returned
    - **And** the secret value itself is never returned in any API response
- [ ] **FR-02**
    - **Given** an existing active secret
    - **When** a new version is created
    - **Then** a `company_secret_versions` row exists with SHA256 fingerprint
- [ ] **FR-04**
    - **Given** any secret access
    - **When** the value is resolved
    - **Then** a `secret_access_event` is recorded with actor, secret key, and timestamp
- [ ] **FR-06**
    - **Given** a secret API response payload
    - **When** inspected
    - **Then** no field contains the plaintext secret value
- [ ] **NFR-01**
    - **Given** the provider storage
    - **When** inspected at the storage layer
    - **Then** secret material is encrypted
- [ ] **NFR-03**
    - **Given** server logs after a secret resolution
    - **When** inspected
    - **Then** no plaintext secret values are present

## Conflicts

None identified yet.

## Open Questions

1. What is the full list of supported secret providers for V1 beyond local encrypted and AWS Secrets Manager?
2. How are secret references resolved when multiple bindings overlap for the same config path (priority/precedence order)?

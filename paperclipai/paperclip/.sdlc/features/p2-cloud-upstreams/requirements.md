---
title: "Cloud Upstreams"
status: done
---

# Requirements: Cloud Upstreams

## Overview

Cloud Upstreams enable cross-instance synchronization of Paperclip companies. A local or self-hosted Paperclip instance can connect to a cloud Paperclip instance (or another peer instance) to export and sync company data including agents, skills, projects, routines, and issues. The system manages connection lifecycle, authentication via OAuth, encrypted credential storage, idempotent transfer runs with conflict detection, and reconciliation of synced runs on server startup.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Connect local instance to cloud; manage sync runs; view transfer history and conflicts |
| Cloud operator | Receive and integrate synced company data from local instances |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support initiating an OAuth-based connection to a remote Paperclip instance. |
| FR-02 | Must | The system shall store connection credentials encrypted at rest. |
| FR-03 | Must | The system shall support listing configured cloud upstream connections per company. |
| FR-04 | Must | The system shall support executing transfer runs that export local company data and sync to the remote. |
| FR-05 | Must | The system shall track run status, progress, warnings, and conflicts for each transfer run. |
| FR-06 | Must | The system shall support dry-run mode for previewing transfer effects without applying them. |
| FR-07 | Must | The system shall reconcile incomplete or interrupted runs on server startup. |
| FR-08 | Should | The system shall support viewing run reports with detailed transfer summaries. |
| FR-09 | Should | The system shall gate cloud upstream functionality behind an experimental feature flag. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Connection credentials must be encrypted at rest using instance-scoped sealing keys. |
| NFR-02 | Must | Security | Transfers must use authenticated channels with token-based authorization scoped to the connecting instance. |
| NFR-03 | Should | Reliability | Transfer runs must be idempotent to support safe retry after interruption. |

## Constraints

- Cloud upstreams are gated behind the `enableCloudSync` experimental feature flag.
- Transfer runs use idempotency keys to prevent duplicate application.
- Connection tokens have configurable expiry and scope.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** A board operator
    - **When** They initiate a connect flow with a remote URL
    - **Then** An OAuth authorization request is created with a redirect URI
- [ ] **FR-02**
    - **Given** An OAuth connection is completed successfully
    - **When** The access token is stored
    - **Then** It is encrypted with the instance's sealing key
- [ ] **FR-03**
    - **Given** Company A has configured upstream connections
    - **When** The operator lists connections
    - **Then** Only connections for company A are returned
- [ ] **FR-07**
    - **Given** An upstream run was interrupted during the previous server session
    - **When** The server starts
    - **Then** The run is reconciled to a terminal state
- [ ] **NFR-01**
    - **Given** An upstream connection stores credential material
    - **When** It is read from the database
    - **Then** Private keys and tokens are encrypted

## Conflicts

None identified yet.

## Open Questions

1. Should cloud upstreams support bidirectional sync, or is it export-only from local to cloud?
2. How are conflicts resolved when both sides have modified the same entity?

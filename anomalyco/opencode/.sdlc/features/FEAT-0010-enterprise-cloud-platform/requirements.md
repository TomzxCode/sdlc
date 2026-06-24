---
title: "Enterprise & Cloud Platform"
status: draft
---

# Requirements: Enterprise & Cloud Platform

## Overview

The Enterprise & Cloud Platform provides SST-deployed backend infrastructure for managing OpenCode at scale.
It includes a console application for cloud service management, a stats/analytics dashboard, an enterprise self-hosted web app with team and project management, and the supporting infrastructure (monitoring, identity, secrets, data lake).
This feature enables organizations to run OpenCode as a managed or self-hosted service.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Enterprise operators | Self-hosted deployment with team management and access control |
| Cloud users | Console-based management of cloud resources |
| Core team | Unified SST infrastructure for all managed services |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a console application for managing cloud-deployed OpenCode instances (SST). |
| FR-02 | Must | The system shall provide a stats/analytics dashboard for usage telemetry and reporting. |
| FR-03 | Must | The system shall provide an enterprise web app supporting team management, projects, and self-hosting on Cloudflare or custom servers. |
| FR-04 | Must | The system shall deploy infrastructure via SST with defined stages: app, console, enterprise, lake, monitoring, stats, identity. |
| FR-05 | Should | The system shall include monitoring infrastructure with OpenTelemetry and Sentry integrations. |
| FR-06 | Should | The system shall support identity/auth flows via OpenAuth for enterprise deployments. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Scalability | Infrastructure shall be defined as code (SST) and deployable to multiple environments. |
| NFR-02 | Should | Security | Enterprise deployments shall support authenticated routes and team-scoped access control. |

## Constraints

- Infrastructure lives under `infra/` and is defined with SST (`sst.config.ts`).
- Console lives in `packages/console/` (with app, core, function, mail, resource, support sub-workspaces).
- Stats lives in `packages/stats/` (with app, core, server sub-workspaces).
- Enterprise app lives in `packages/enterprise/`.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** SST infrastructure is deployed
    - **When** the console app is accessed
    - **Then** it shows managed OpenCode instances and their status
- [ ] **FR-03**
    - **Given** an enterprise deployment
    - **When** an admin creates a team and invites members
    - **Then** team members can access shared project sessions
- [ ] **FR-04**
    - **Given** the SST config
    - **When** `sst deploy` runs
    - **Then** all defined stages (app, console, enterprise, lake, monitoring, stats, identity) are deployed

## Conflicts

None identified yet.

## Open Questions

1. What is the pricing/licensing model for enterprise self-hosting vs cloud-managed?
2. Should enterprise auth integrate with external identity providers (SAML, OIDC)?

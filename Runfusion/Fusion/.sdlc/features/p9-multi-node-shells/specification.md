---
title: "Multi-Node Operator Surfaces & Shells"
status: done
---

# Specification: Multi-Node Operator Surfaces & Shells

## Overview

Projects and nodes are managed through `@fusion/core` (project, node, mesh, central modules) and dashboard route registrars; nodes coordinate over a shared PostgreSQL backend with claims/leases and membership. Native shells wrap the dashboard SPA via a shared `window.fusionShell` bridge; the `fn` CLI drives serve/daemon/dashboard/project/node/mesh.

## Architecture

```
Desktop (Electron) / Mobile (Capacitor) ── window.fusionShell bridge
   │
Dashboard SPA + shells (shell-host)
   │
   ▼
Dashboard API (register-project-routes, register-node-routes, register-mesh-routes,
               register-discovery-routes, register-settings-sync-*,
               register-docker-*)
   │
   ▼
@fusion/core (project-*, mesh/, central/)  ──►  PostgreSQL (shared backend)
   │
   ▼
engine (project-engine, scheduler node-unreachable audit, fanout lanes)
```

## Data Models

### Node

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Node id |
| url | string | not null | Node endpoint |
| status | enum | not null | online/offline |
| claims/leases | json | — | Current claims |

## API Contracts

### POST /api/projects

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | yes | Project name |
| nodeUrl | string | no | Optional node URL |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| project | object | Created project |

## Sequences

### Node onboarding

```
register → discover → onboard (QR/manual/tokenized link) → mesh membership
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Shared backend | single PostgreSQL + claims/leases | Retired multi-leader mesh replication |
| Shell bridge | `window.fusionShell` + shell-host | Normalizes host type across shells |
| Native shells out of typecheck | desktop/mobile excluded | Packaging-focused packages |

## Risks and Unknowns

1. Multi-leader mesh replication is retired; active topology is shared-Postgres with claims/leases (see docs/shared-mesh-protocol.md).

## Out of Scope

- Fleet execution scheduling internals (FEAT-p4)
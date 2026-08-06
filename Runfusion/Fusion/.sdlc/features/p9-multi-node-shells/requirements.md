---
title: "Multi-Node Operator Surfaces & Shells"
status: done
---

# Requirements: Multi-Node Operator Surfaces & Shells

## Overview

Fusion runs as a fleet across machines. Operators manage multiple projects and nodes (cluster/mesh sharing a PostgreSQL backend), plus native desktop (Electron) and mobile (Capacitor) shells and the `fn` CLI with its TUI. Every surface drives and observes the same board.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Manages projects, nodes, mesh membership, and remote access |
| Mobile/desktop users | Runs Fusion on phones and native apps via a shared shell bridge |
| CLI users | Drives Fusion from the terminal and TUI |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let operators create/manage projects and nodes with registration and onboarding |
| FR-2 | Must | The system shall coordinate nodes via a shared mesh/cluster protocol over a shared PostgreSQL backend |
| FR-3 | Must | The system shall ship desktop (Electron) and mobile (Capacitor) shells that wrap the dashboard SPA via a shared shell bridge |
| FR-4 | Must | The system shall expose CLI commands and TUI for serve, daemon, dashboard, project, node, and mesh |
| FR-5 | Should | The system shall support remote access with tokenized login and QR/manual setup |
| FR-6 | Should | The system shall stream node/project scoped events over the shared `/api/events` bus |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Claims/leases and membership must survive node unreachability (scheduler node-unreachable audit) |
| NFR-2 | Must | Security | Node auth and remote access must not expose the dashboard without tokens |
| NFR-3 | Should | Availability | Unreachable nodes must degrade gracefully in the UI |

## Constraints

- Desktop/mobile are excluded from the workspace typecheck (packages `@fusion/desktop`, `@fusion/mobile`)
- Port 4040 is reserved for the dashboard; shells must use the configured token flow

## Acceptance Criteria

- [ ] **FR-1, FR-2**
    - **Given** a registered node/project
    - **When** the mesh runs
    - **Then** nodes claim/lease work over the shared backend and report membership
- [ ] **FR-3**
    - **Given** a native shell
    - **When** it connects
    - **Then** it drives the dashboard SPA through the shared `window.fusionShell` bridge
- [ ] **FR-4**
    - **Given** the `fn` CLI
    - **When** `serve`, `daemon`, `dashboard`, `project`, `node`, or `mesh` runs
    - **Then** the corresponding surface operates correctly
- [ ] **NFR-1**
    - **Given** an unreachable node
    - **When** scheduling runs
    - **Then** claims are audited and work is not lost

## Conflicts

None identified yet.

## Open Questions

1. Retired multi-leader mesh replication is documented as "shared mesh protocol"; confirm whether the active topology is single-leader-shared-Postgres or multi-node writes.
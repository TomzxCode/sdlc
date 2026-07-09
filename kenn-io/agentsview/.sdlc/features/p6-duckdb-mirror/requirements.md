---
title: "DuckDB Mirror"
status: draft
---

# Requirements: DuckDB Mirror

## Overview

The DuckDB mirror pushes session data from the local SQLite archive to a DuckDB database file, enabling portable analytics and read-only local serving. It also supports the Quack remote protocol for network access to DuckDB, allowing remote querying of the session mirror.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Portable analytics file for data analysis |
| Power user | Remote access to session data via Quack protocol |
| Analyst | SQL-based querying of session data using DuckDB |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall push session data from SQLite to DuckDB |
| FR-2 | Must | The system shall support incremental push with fingerprint-based change detection |
| FR-3 | Must | The system shall serve the web UI read-only from DuckDB |
| FR-4 | Must | The system shall expose the DuckDB mirror over the Quack remote protocol |
| FR-5 | Must | The system shall support dual DuckDB drivers (CGO and pure Go) |
| FR-6 | Should | The system shall support project filtering |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Quack server binds to loopback by default and requires a token |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** local SQLite has session data
    - **When** `agentsview duckdb push` is run
    - **Then** session data is replicated to DuckDB
- [ ] **FR-4**
    - **Given** the Quack server is running
    - **When** a remote client connects with a valid token
    - **Then** the client can query the DuckDB mirror

## Open Questions

None.

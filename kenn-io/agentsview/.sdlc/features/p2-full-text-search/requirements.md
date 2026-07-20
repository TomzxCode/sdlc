---
title: "Full-Text Search"
status: done
---

# Requirements: Full-Text Search

## Overview

The full-text search feature indexes all session message content using SQLite FTS5 and provides fast text-based search across all sessions. It supports multiple query modes (AND, exact phrase, prefix), filtering by agent, project, date, and source scope, and returns ranked results with snippet highlights.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Quickly find past sessions by searching for specific terms, code snippets, or error messages |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall index all message content using SQLite FTS5 |
| FR-2 | Must | The system shall support AND-mode search (all terms must match) |
| FR-3 | Must | The system shall support exact phrase matching with double quotes |
| FR-4 | Must | The system shall support prefix matching (trailing wildcard) |
| FR-5 | Must | The system shall return ranked results with snippet highlights |
| FR-6 | Must | The system shall support filtering by agent, project, date range, machine, and git branch |
| FR-7 | Must | The system shall support cursor-based pagination |
| FR-8 | Should | The system shall support regex-based content search as an alternative mode |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Search results should return in under 500ms for typical queries |
| NFR-2 | Should | Scalability | Index should handle millions of messages |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** messages are synced
    - **When** a search query is submitted
    - **Then** results include matching messages with snippet highlights

## Open Questions

None.

---
title: "Recall System"
status: done
---

# Requirements: Recall System

## Overview

The recall system extracts reusable facts from session history, ranks them by relevance, and assembles context for AI agent prompts. It distills key information such as technical decisions, project conventions, environment setup, and solution patterns from past sessions into structured recall entries that can be queried and surfaced.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Reuse past learnings and avoid repeating solved problems |
| AI agent user | Provide context to AI coding assistants from session history |
| Power user | Manually curate and review recall entries |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall extract structured recall entries from session messages |
| FR-2 | Must | The system shall rank recall entries by relevance to a given query |
| FR-3 | Must | The system shall assemble recall entries into a formatted context block |
| FR-4 | Must | The system shall support querying recall entries via the API |
| FR-5 | Should | The system shall support evidence tracking linking recall entries to source messages |
| FR-6 | Should | The system shall support distillation configurations for extraction |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Recall queries should complete in under 1 second |

## Acceptance Criteria

- **FR-1**
  - Given session messages exist
  - When recall extraction is run
  - Then structured recall entries are created with source evidence
- **FR-2**
  - Given a query string
  - When recall ranking is performed
  - Then results are ordered by relevance score

## Open Questions

1. What is the optimal number of recall entries to include in context assembly?

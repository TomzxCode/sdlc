---
title: "Semantic Search"
status: draft
---

# Requirements: Semantic Search

## Overview

The semantic search feature provides meaning-based search across session content using vector embeddings. An opt-in feature, it indexes session messages via an OpenAI-compatible embeddings endpoint, stores vectors in a separate sqlite-vec database, and supports pure semantic and hybrid (RRF-merged) search modes.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Find sessions by meaning rather than exact text match |
| Power user | Configure custom embedding endpoints (model, dimensions, provider) |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall support building an embedding index from session message content |
| FR-2 | Must | The system shall support multiple embedding generations (different models/dimensions) |
| FR-3 | Must | The system shall support activating and retiring generations |
| FR-4 | Must | The system shall support pure semantic search (query → vector → similarity) |
| FR-5 | Must | The system shall support hybrid search (RRF merge of FTS5 + semantic results) |
| FR-6 | Must | The system shall support configurable embedding endpoints, API keys, and models |
| FR-7 | Should | The system shall support incremental index updates (only new/changed content) |
| FR-8 | Should | The system shall provide a background scheduler for automatic index builds |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Embedding build should batch requests with configurable concurrency |
| NFR-2 | Should | Isolation | Semantic search is opt-in and does not affect core sync or FTS5 search |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** messages are synced
    - **When** an embeddings build is triggered
    - **Then** a vector index is created for all messages
- [ ] **FR-4**
    - **Given** an active embedding generation
    - **When** a semantic search query is submitted
    - **Then** results ranked by cosine similarity are returned

## Open Questions

1. What are the recommended default embedding providers and models?

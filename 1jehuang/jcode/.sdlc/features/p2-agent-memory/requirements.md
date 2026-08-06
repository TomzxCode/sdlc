---
title: "Agent Memory System"
status: done
---

# Requirements: Agent Memory System

## Overview

The agent memory system gives jcode a persistent, searchable memory across sessions. Memories are extracted from sessions, stored in a memory graph, embedded locally with an ONNX MiniLM model, and re-injected into prompts on later turns. A rerank and consolidation pipeline keeps recall relevant and merges memories over time. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | The agent remembers project context across sessions and finds relevant past work without manual prompts |
| Maintainer | Low-footprint local embedding, tunable recall quality, and auditable memory behavior |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall extract memories from session content for later recall. |
| FR-2 | Must | The system shall compute local text embeddings for memories using a bundled ONNX MiniLM model so no external embedding API is required. |
| FR-3 | Must | The system shall store memories in a persistent memory graph and expose memory operations through the CLI (`jcode memory list`, `search`, `export`, `import`, `stats`). |
| FR-4 | Must | The system shall support both keyword and semantic search over memories. |
| FR-5 | Must | The system shall inject relevant memories into the agent prompt on session turns. |
| FR-6 | Should | The system shall rerank candidate memories (configurable cadence and votes) to keep recall precise. |
| FR-7 | Should | The system shall consolidate and merge related memories over time, including overnight consolidation. |
| FR-8 | May | The system shall expose a memory sidecar agent for autonomous memory maintenance. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Local embedding inference shall not stall the server; the embedding stack is pinned to optimized profiles. |
| NFR-2 | Must | Privacy | Memory embeddings and extraction shall run locally without sending session content to third parties. |
| NFR-3 | Should | Performance | Session search shall scale to multi-megabyte session files (SIMD-backed matching). |
| NFR-4 | Should | Reliability | Memory storage must be durable across restarts. |

## Constraints

- Embeddings must work out of the box in default builds (the `embeddings` feature is on by default).
- A `local` embedding backend is required; an `openai` backend is optional.

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** a completed session
    - **When** memory extraction runs
    - **Then** candidate memories are persisted to the memory store
- [ ] **FR-2**
    - **Given** a memory to embed
    - **When** the local embedding backend is selected
    - **Then** a numeric embedding is produced without any network call
- [ ] **FR-3**
    - **Given** stored memories
    - **When** the user runs `jcode memory list` and `jcode memory stats`
    - **Then** the memories and their counts are shown
- [ ] **FR-4**
    - **Given** stored memories
    - **When** the user searches by keyword or by semantic similarity
    - **Then** relevant memories are returned in ranking order
- [ ] **FR-5**
    - **Given** an active session
    - **When** a turn begins
    - **Then** relevant memories are injected into the prompt
- [ ] **FR-6**
    - **Given** candidate memories for a turn
    - **When** reranking is enabled and due
    - **Then** the injected set is reordered by rerank score
- [ ] **FR-7**
    - **Given** accumulated memories
    - **When** consolidation (including overnight) runs
    - **Then** related memories are merged and redundant ones are removed
- [ ] **FR-8**
    - **Given** the memory sidecar enabled
    - **When** the sidecar agent runs
    - **Then** it performs autonomous memory maintenance within its configured budget
- [ ] **NFR-1**
    - **Given** an active server
    - **When** embedding inference runs
    - **Then** the agent loop does not stall waiting on the embedding model
- [ ] **NFR-2**
    - **Given** memory extraction and embedding
    - **When** observed on the network
    - **Then** no session content leaves the machine via the memory subsystem
- [ ] **NFR-3**
    - **Given** a large session file
    - **When** session search runs
    - **Then** results return quickly using SIMD-optimized matching
- [ ] **NFR-4**
    - **Given** a server restart
    - **When** memory commands run afterwards
    - **Then** previously stored memories are still present

## Conflicts

None identified yet.

## Open Questions

1. What is the exact recall budget per turn (how many memories are injected and at what token cost)? The tuning knobs exist in config but the defaults are inferred from code.

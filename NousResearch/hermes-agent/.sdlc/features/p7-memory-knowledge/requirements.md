---
title: "Memory and Cross-Session Knowledge"
status: done
---

# Requirements: Memory and Cross-Session Knowledge

## Overview

Hermes maintains persistent knowledge across sessions through two systems: pluggable memory providers (Honcho, Mem0, Supermemory, Byterover, Hindsight, Holographic, OpenViking, RetainDB) and the learning graph (for extracting and persisting skill-like procedures from user interactions). The session store (SQLite with FTS5) provides full-text search across past conversations.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Users | The agent remembers relevant context across sessions — preferences, ongoing projects, facts learned |
| Developers | Pluggable backends mean users can choose their preferred memory storage (local, cloud, 3rd-party) |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall persist conversation history in SQLite with FTS5 full-text search |
| FR-2 | Must | The system shall support pluggable memory providers via the MemoryProvider ABC |
| FR-3 | Must | Memory providers shall sync turn data via sync_turn(turn_messages) after each conversational turn |
| FR-4 | Must | The system shall support query-based memory prefetch (prefetch(query)) during session start |
| FR-5 | Should | The system shall support learning graph extraction — converting user interactions into reusable skills |
| FR-6 | Should | The learning system shall extract procedures from conversations, directories, URLs, notes, and chat history |
| FR-7 | Should | The system shall support session search across all past conversations with summarization |
| FR-8 | Should | The system shall automatically generate session titles via LLM |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Session search should return results in under 2 seconds |
| NFR-2 | Must | Privacy | Memory provider choice should be user-configurable (local vs cloud) |

## Constraints

- No new in-tree memory providers (policy) — new providers must ship as standalone plugin repos
- Cron sessions pass skip_memory=True by default — memory providers intentionally do not run during cron

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a conversation has completed
    - **When** the user sends a new message in a different session
    - **Then** the agent can find the previous conversation via session search
- [ ] **FR-2**
    - **Given** the user has configured a memory provider
    - **When** a conversation turn completes
    - **Then** sync_turn() is called with the turn messages
- [ ] **FR-5**
    - **Given** the user has completed a multi-step operation
    - **When** the learning graph processes the session
    - **Then** a skill can be extracted and saved

## Conflicts

None identified yet.

## Open Questions

1. Should there be a built-in (zero-dependency) memory provider option?
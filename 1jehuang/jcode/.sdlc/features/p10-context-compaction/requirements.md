---
title: "Context Compaction"
status: done
---

# Requirements: Context Compaction

## Overview

Context compaction keeps long sessions usable by compressing the accumulated context (and provider KV cache) when it grows too large. jcode supports reactive, proactive, and semantic compaction strategies, all configurable under the `[compaction]` config section. This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Long-running sessions that stay fast and stay within provider context limits |
| Maintainer | Predictable compaction behavior that preserves important context |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall compact a session's context when it approaches the provider context window limit. |
| FR-2 | Must | The system shall support multiple compaction strategies: reactive (on threshold), proactive (before it is needed), and semantic. |
| FR-3 | Must | The system shall preserve a summary of the compacted context so later turns retain continuity. |
| FR-4 | Must | The system shall record compaction state on the session so resume reflects the compacted context. |
| FR-5 | Should | The system shall keep a cache-relevant hash of messages so KV-cache prefix changes are detected after compaction. |
| FR-6 | Should | The system shall allow strategy configuration per the `[compaction]` section (reactive/proactive/semantic). |
| FR-7 | May | The system shall support context-window resolution invariants across providers (respecting per-provider limits). |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Compaction must never lose the ability to resume the session. |
| NFR-2 | Should | Performance | Compaction must be cheap enough to run mid-turn without disrupting the user. |
| NFR-3 | Should | Availability | Sessions at the context limit must be able to continue rather than fail. |

## Constraints

- Compaction interacts with the KV cache; hashes must stay stable for unchanged prefixes.
- Context window limits differ per provider.

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** a session near its context limit
    - **When** a new turn starts
    - **Then** the context is compacted and the turn continues
- [ ] **FR-2**
    - **Given** each configured strategy
    - **When** the strategy condition is met
    - **Then** compaction runs accordingly
- [ ] **FR-3**
    - **Given** a compacted session
    - **When** a later turn runs
    - **Then** it receives a summary of the compacted context
- [ ] **FR-4**
    - **Given** a compacted session
    - **When** the session is resumed
    - **Then** the compacted state is reflected
- [ ] **FR-5**
    - **Given** compaction of a session
    - **When** cache-relevant hashes are computed
    - **Then** the prefix change is detected for KV-cache correctness
- [ ] **FR-6**
    - **Given** a `[compaction]` config with a strategy
    - **When** jcode runs
    - **Then** the configured strategy is used
- [ ] **FR-7**
    - **Given** a provider with a known context window
    - **When** the context window is resolved
    - **Then** the resolved limit respects provider invariants
- [ ] **NFR-1**
    - **Given** a compacted session
    - **When** the session is reopened
    - **Then** it resumes without data loss
- [ ] **NFR-2**
    - **Given** compaction running
    - **When** the user continues interacting
    - **Then** the disruption is minimal
- [ ] **NFR-3**
    - **Given** a session at the limit
    - **When** the user continues
    - **Then** the session continues rather than failing on context overflow

## Conflicts

None identified yet.

## Open Questions

1. What is the exact compaction trigger threshold and how much context is retained? The logic is inferred from `compaction.rs` and the compaction core crate.

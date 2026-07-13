---
title: "Session Persistence and Branching"
status: done
---

# Requirements: Session Persistence and Branching

## Overview

Sessions make pi's conversations durable, resumable, and branchable.
`SessionManager` persists tree-structured JSONL logs (messages, model/thinking changes, compaction summaries, branch summaries); users can resume, fork, clone, and navigate session trees; compaction reclaims context lossily while preserving the original log.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Resume past work, branch explorations without losing history, manage context length |
| Extension authors | Session lifecycle hooks (compact, fork, switch, tree) to observe and augment |
| Maintainers | A stable, migratable on-disk format with clear versioning |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall persist sessions as JSONL with tree-structured entries (`id`/`parentId` per entry) under a versioned format. |
| FR-02 | Must | The system shall support session entry types: messages, thinking-level changes, model changes, compaction summaries, branch summaries, labels, custom messages, and session info. |
| FR-03 | Must | The system shall support resume (`-r`, `-c`, `--session`, `/resume`), new (`/new`), fork (`/fork`, `--fork`), clone (`/clone`), and tree navigation (`/tree`). |
| FR-04 | Must | The system shall support branching where forking from a previous user message creates a new session file and the original log is preserved. |
| FR-05 | Must | The system shall support compaction (manual via `/compact [prompt]` or automatic on threshold/overflow) that summarizes older messages while keeping recent ones. |
| FR-06 | Must | The system shall preserve the original JSONL file through compaction (compaction is lossy but non-destructive to the source log). |
| FR-07 | Must | The system shall hot-swap the runtime when switching sessions or cwds, tearing down and recreating cwd-bound services. |
| FR-08 | Must | The system shall emit session lifecycle hooks (`session_before_compact/compact`, `session_before_fork/fork`, `session_before_switch/switch`, `session_before_tree/tree`) extensions can observe. |
| FR-09 | Should | The system shall provide compaction post-token estimates and branch summarization. |
| FR-10 | Should | The system shall support session export to HTML. |
| FR-11 | Should | The system shall migrate older session format versions to the current version on load. |
| FR-12 | May | The system shall support session labels and bookmarks for navigation. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | The original session JSONL shall never be destructively modified by compaction or branching. |
| NFR-02 | Must | Compatibility | The format version shall be explicit (`CURRENT_SESSION_VERSION`) with documented migration steps. |
| NFR-03 | Should | Performance | Session append and read operations shall remain efficient for large session files. |
| NFR-04 | Should | Observability | Compaction events shall carry reason and retry metadata for extension consumers. |

## Constraints

- Sessions are local JSONL files; no server-side session store.
- `progress.md` and `state.yml` (workflow state) are never committed; session JSONL is user data.
- Compaction is lossy by design.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** a session with multiple turns and a branch
    - **When** serialized to disk
    - **Then** the JSONL contains tree-structured entries each with `id` and `parentId` forming a valid tree.
- [ ] **FR-05**
    - **Given** a session exceeding the compaction threshold
    - **When** compaction runs
    - **Then** older messages are summarized, recent messages are retained, and a compaction summary entry is appended.
- [ ] **FR-06**
    - **Given** a session that has been compacted
    - **When** inspecting the JSONL file
    - **Then** the original message entries remain present alongside the compaction summary.
- [ ] **FR-07**
    - **Given** an interactive session
    - **When** the user runs `/tree` and switches branches
    - **Then** the runtime tears down cwd-bound services and recreates them for the target branch without leaking state.
- [ ] **NFR-01**
    - **Given** any compaction or fork operation
    - **When** it completes
    - **Then** the source session JSONL file is byte-for-byte unchanged except for appended entries.

## Conflicts

None identified yet.

## Open Questions

1. Is there a plan to support remote/session-sync, or will sessions remain strictly local files?
2. What is the policy for pruning or archiving very large session files over time?

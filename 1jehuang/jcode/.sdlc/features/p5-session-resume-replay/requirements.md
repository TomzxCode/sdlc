---
title: "Session Persistence, Resume and Replay"
status: done
---

# Requirements: Session Persistence, Resume and Replay

## Overview

Sessions are jcode's durable unit of work. Every session is persisted to disk (a snapshot JSON plus an append-only JSONL journal), so sessions survive crashes, reloads, and reboots. Users can resume sessions by memorable short name, replay past sessions in the TUI, export them, and even resume sessions started in other tools (Claude Code, Codex, Pi, OpenCode, Cursor). This feature was reverse-engineered from the existing codebase during an SDLC sync; it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Never lose a session; resume context across restarts and terminals |
| Maintainer | Crash-safe persistence, reliable reload recovery, and clean replay/export |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall persist each session as a snapshot file plus an append-only journal of messages and events. |
| FR-2 | Must | The system shall resume a session by id or memorable short name (`--resume`, session picker). |
| FR-3 | Must | The system shall record session status (active, closed, crashed, reloaded, compacted, rate-limited, error) and survive server reloads and restarts. |
| FR-4 | Must | The system shall import sessions from external tools (Claude Code, Codex, Pi, OpenCode, Cursor) as resume targets. |
| FR-5 | Must | The system shall capture an environment snapshot (git state, provider, model) per session. |
| FR-6 | Should | The system shall support TUI replay of a session, including swarm status and plan events, with export options. |
| FR-7 | Should | The system shall support a restart snapshot to resume sessions after a reboot. |
| FR-8 | Should | The system shall record crash and reload recovery so interrupted sessions can be restored. |
| FR-9 | May | The system shall support session search across persisted sessions. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Journal appends shall be crash-safe; a partial journal must not corrupt the session. |
| NFR-2 | Must | Performance | Session files can grow large; persistence and search must not degrade the agent loop. |
| NFR-3 | Should | Usability | Resuming should feel instant via memorable names and a picker. |

## Constraints

- Storage layout: `~/.jcode/sessions/<id>.json` snapshot plus `<id>.journal.jsonl`.
- Imported sessions keep their provenance (ResumeTarget enum).

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**
    - **Given** an active session
    - **When** a message is exchanged
    - **Then** it is appended to the journal and reflected in the snapshot
- [ ] **FR-2**
    - **Given** a persisted session
    - **When** the user resumes by name or id
    - **Then** the conversation and context are restored
- [ ] **FR-3**
    - **Given** a server reload mid-session
    - **When** the server restarts
    - **Then** the session status is recorded and the session is recoverable
- [ ] **FR-4**
    - **Given** an external tool session (e.g. Codex)
    - **When** the user resumes it
    - **Then** it imports and continues in jcode
- [ ] **FR-5**
    - **Given** a new session
    - **When** it is created
    - **Then** the environment snapshot (git, provider, model) is captured
- [ ] **FR-6**
    - **Given** a persisted session
    - **When** the user runs `jcode replay --export`
    - **Then** the session replays and exports correctly
- [ ] **FR-7**
    - **Given** saved sessions
    - **When** a reboot occurs and restart restore runs
    - **Then** sessions resume from the restart snapshot
- [ ] **FR-8**
    - **Given** a crashed session
    - **When** recovery runs
    - **Then** the session is restored with its crash status recorded
- [ ] **FR-9**
    - **Given** persisted sessions
    - **When** the user searches
    - **Then** matching sessions are returned
- [ ] **NFR-1**
    - **Given** an interrupted journal write
    - **When** the session is reopened
    - **Then** the journal is repaired or rejected without corrupting the snapshot
- [ ] **NFR-2**
    - **Given** a large session
    - **When** it is loaded or searched
    - **Then** the agent loop remains responsive
- [ ] **NFR-3**
    - **Given** memorable session names
    - **When** the user types the name
    - **Then** the session resumes immediately

## Conflicts

None identified yet.

## Open Questions

1. What is the exact journal compaction/truncation policy for very long sessions? Compaction interacts with this feature and the exact boundary is inferred from code.

---
title: "Session Sync & Management"
status: draft
---

# Requirements: Session Sync & Management

## Overview

The sync engine discovers session files from all configured AI coding agent directories on disk, parses them using agent-specific parsers, sanitizes the extracted data, and writes it into the SQLite database. It provides incremental and full resync modes, a file watcher for live updates, and supports remote sync from other machines via SSH and S3-compatible storage.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Sessions are automatically discovered and indexed without manual intervention |
| Operator | Can trigger resyncs and monitor sync status |
| Developer | Extensible provider system for adding new agent parsers |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall discover session files from all configured agent directories on startup |
| FR-2 | Must | The system shall parse session files using agent-specific parsers to extract messages, tool calls, and usage data |
| FR-3 | Must | The system shall sanitize parsed data (clamp tokens, blank timestamps, coerce roles, strip control characters) |
| FR-4 | Must | The system shall write parsed sessions to SQLite in batches of 100 with 8 parallel workers |
| FR-5 | Must | The system shall support incremental sync (only changed files) and full resync |
| FR-6 | Must | The system shall provide a file watcher using fsnotify with configurable debounce |
| FR-7 | Must | The system shall run a periodic full scan every 15 minutes |
| FR-8 | Must | The system shall track failed/unparseable files by path and mtime via a skip cache |
| FR-9 | Should | The system shall support syncing sessions from remote machines via SSH |
| FR-10 | Should | The system shall support S3-compatible object storage as a session source |
| FR-11 | Should | The system shall emit SSE notifications after each write pass for live UI updates |
| FR-12 | Should | The system shall auto-start the daemon on demand for commands that need fresh data |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Sync should process at least 100 sessions per second |
| NFR-2 | Must | Reliability | Failed parses must not crash the sync engine; errors are tracked and skipped |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** agent session files exist on disk
    - **When** the server starts
    - **Then** all session files are discovered and queued for parsing
- [ ] **FR-2**
    - **Given** a session file for a supported agent
    - **When** the sync engine processes it
    - **Then** messages, tool calls, and usage data are extracted
- [ ] **FR-5**
    - **Given** a previously synced session file is modified
    - **When** the file watcher detects the change
    - **Then** only that session is re-parsed and updated
- [ ] **FR-6**
    - **Given** the server is running
    - **When** a new session file is created
    - **Then** it is detected and synced within the debounce window

## Open Questions

1. What are the performance characteristics of S3-based session discovery at scale?

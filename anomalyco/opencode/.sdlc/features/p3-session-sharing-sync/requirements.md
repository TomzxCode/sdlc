---
title: "Session Sharing & Sync"
status: done
---

# Requirements: Session Sharing & Sync

## Overview

OpenCode lets users create public links to their conversations so they can collaborate or get help, and keeps those sessions synchronized to a share host.
Sharing is backed by a git-based file snapshot system that tracks project state per session so shared conversations can include file diffs and be replayed elsewhere.
An `import` command reconstructs a session locally from a share URL.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Public share links for conversations, privacy control via sharing modes |
| Teammates / reviewers | Read shared conversations without local setup |
| Operators / enterprise | Self-hosted share endpoint behind their own URL |
| Session runtime owners | Durable event log that can be replayed on another device |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall create a public share for a session, returning a unique URL. |
| FR-02 | Must | The system shall persist share metadata (id, url, secret) locally keyed by session. |
| FR-03 | Must | The system shall sync session changes (session info, messages, parts, file diffs, models) to the share host as they occur. |
| FR-04 | Must | The system shall coalesce rapid change events into a single delayed sync per session. |
| FR-05 | Must | The system shall support manual, auto, and disabled sharing modes controlled by configuration. |
| FR-06 | Must | The system shall route share requests to an enterprise URL when an active account/org is present, otherwise to the default share host. |
| FR-07 | Must | The system shall remove a share (locally and on the host) on unshare. |
| FR-08 | Should | The system shall track file snapshots via git to compute per-session file diffs. |
| FR-09 | Should | The system shall support restoring and reverting files from a snapshot. |
| FR-10 | Should | The system shall import a session from a share URL into the local worktree. |
| FR-11 | Should | The system shall record sync events with a sequence id so other devices can replay them. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Shared conversations are publicly accessible to anyone with the link; share must be disableable. |
| NFR-02 | Must | Performance | Sync flushes shall be debounced so bursts of events produce a bounded number of requests. |
| NFR-03 | Must | Availability | Sync failures shall be logged and not crash the server; they may be retried on the next event. |
| NFR-04 | Should | Performance | Snapshot storage shall seed the git object database from the source repo to avoid re-hashing large trees. |

## Constraints

- Sharing can be disabled entirely via `OPENCODE_DISABLE_SHARE` or configuration.
- The share API surface is `/api/share` (legacy) and `/api/shares` (console/enterprise).
- Sync events use total ordering via a simple incrementing sequence id; only one device writes.
- Sync events must remain backwards compatible with the existing `Bus` event abstraction.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** an unshared session
    - **When** the user runs the share command
    - **Then** a unique public URL is returned and the session is uploaded
- [ ] **FR-03**
    - **Given** a shared session receiving a new message or file diff
    - **When** the change event fires
    - **Then** the change is queued and flushed to the share host
- [ ] **FR-04**
    - **Given** two rapid diff events for the same session
    - **When** both are published within the debounce window
    - **Then** exactly one sync request is sent containing the latest data
- [ ] **FR-07**
    - **Given** a shared session
    - **When** the user unshares
    - **Then** the share is deleted locally and on the host
- [ ] **FR-08**
    - **Given** a git worktree with a tracked snapshot
    - **When** files change
    - **Then** the snapshot diff lists the changed files
- [ ] **NFR-01**
    - **Given** sharing configured as disabled
    - **When** the user attempts to share
    - **Then** the operation is rejected

## Conflicts

None identified yet.

## Open Questions

1. Should sync events support multi-writer sessions in the future, and what ordering model would that need?
2. How long should shared conversations remain hosted before they are pruned?

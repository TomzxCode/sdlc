---
title: "Session Persistence, Resume and Replay"
status: done
---

# Specification: Session Persistence, Resume and Replay

## Overview

Session persistence lives in `crates/jcode-base/src/session/` (persistence, journal, render, crash) with shared models in `crates/jcode-session-types`. External-session import is implemented in `crates/jcode-import-core`. Replay and video export live in the TUI layer (`jcode-tui/src/video_export.rs`), reachable via `jcode replay`. This document was reverse-engineered from the existing codebase during an SDLC sync.

## Architecture

```
jcode server (app-core)
   │ writes
   ▼
~/.jcode/sessions/<id>.json          (snapshot)
~/.jcode/sessions/<id>.journal.jsonl (append-only journal)
   │
   ├── session/ (persistence, journal, render, crash)
   ├── import-core (ResumeTarget: jcode/claude-code/codex/pi/opencode/cursor)
   └── TUI video_export (jcode replay --video/--export)
```

## Data Models

### StoredMessage (`jcode-session-types`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK | Message id. |
| role | enum | not null | User or Assistant. |
| content | list | not null | Content blocks of the message. |
| token_usage | object | nullable | Token accounting. |
| timestamp | timestamp | not null | When the message was stored. |

### SessionJournalMeta

Captures parent id, title, status, compaction state, provider session id, model, reasoning effort, working dir, last pid, timestamps, and flags (canary, debug, saved).

### StoredReplayEvent

Kinds: `display_message`, `swarm_status`, `swarm_plan`; appended to the journal for replay.

## API Contracts

### CLI: `jcode replay [session]`

Flags: `--swarm`, `--export`, `--video`, `--auto-edit`, `--timeline`, `--speed`, `--fps`.

### CLI: `jcode session rename`

Rename a session's title (stored in journal meta).

## Sequences

### Resume a session

```
jcode --resume <name|id> → connect to server → load journal → replay events
→ client state rebuilt → stream continues from where it left off
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Snapshot + append journal | `<id>.json` + `<id>.journal.jsonl` | Crash-safe appends; snapshot for fast load. |
| Journal replay events | `StoredReplayEvent` | Reconstructs UI state and swarm plans on resume. |
| Import from external tools | `ResumeTarget` enum + `jcode-import-core` | Users migrate context from other agents. |
| Memorable short names | whimsical names (e.g. `fox`) | Fast resume by name (NFR-3). |

## Risks and Unknowns

1. Very long journals interact with compaction; the truncation policy is inferred from code.
2. Import fidelity depends on external tool formats, which change upstream.

## Out of Scope

- Cloud-backed session sync (a separate Jade cloud integration).
- Editing/deleting persisted history beyond rename and standard lifecycle.

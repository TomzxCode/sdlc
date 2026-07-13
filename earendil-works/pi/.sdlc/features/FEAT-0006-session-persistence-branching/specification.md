---
title: "Session Persistence and Branching"
status: done
---

# Specification: Session Persistence and Branching

## Overview

Sessions are JSONL files with a tree-structured entry stream.
`SessionManager` owns append/read/migration; `AgentSessionRuntime` hot-swaps the active session and its cwd-bound services on fork/switch/tree navigation; compaction runs in `AgentSession` with hooks for extensions.

## Architecture

```
AgentSession
  prompt loop appends entries ------+
  compaction summarizes             |
  branch summarization              |
        |                           v
        |                  +-------------------+
        +----------------->|   SessionManager  |
                           | JSONL append/read |
                           | tree traversal    |
                           | migration (v1->N) |
                           +---------+---------+
                                     | hot-swap
                                     v
                        +------------------------+
                        | AgentSessionRuntime    |
                        | owns active session +  |
                        | cwd-bound services     |
                        | fork()/switch()/       |
                        | navigate()             |
                        +------------------------+
```

## Data Models

### Session JSONL entry (union, tree-structured)

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | required | Unique entry id |
| parentId | string | nullable | Parent entry id (null = root) |
| type | enum | required | message, thinkingChange, modelChange, compaction, branchSummary, label, custom, sessionInfo |
| ... | varies | per type | Type-specific payload |

### SessionHeader

| Field | Type | Description |
|---|---|---|
| version | number | Format version (`CURRENT_SESSION_VERSION`) |
| sessionId | string | Stable session identifier |
| cwd | string | Working directory at creation |

### Compaction summary entry

| Field | Type | Description |
|---|---|---|
| reason | enum | `manual`, `threshold`, `overflow`, `retry` |
| willRetry | boolean | Whether compaction will retry |
| summary | string | Summarized older context |
| cutPoint | string | Entry id where cut occurred |

## API Contracts

### SessionManager.append(entry) / read()

Append appends a JSONL line; read loads and indexes the tree for traversal, listing, and migration.

### Runtime: fork() / switch(id) / navigate(direction)

Each tears down the current runtime, emits the corresponding `session_before_*` event, and recreates services bound to the target session/cwd.

### /compact [prompt]

Triggers compaction: emits `session_before_compact`, summarizes older messages, retains recent ones, appends a compaction summary, emits `session_compact`.

## Sequences

### Compaction flow

```
threshold exceeded OR /compact
  -> session_before_compact event (extensions may modify/inject)
  -> findCutPoint (token estimation)
  -> summarize messages before cut
  -> keep recent messages
  -> append compaction summary entry to JSONL
  -> post-token estimate
  -> session_compact event (with reason, willRetry)
  -> if willRetry: agent.continue()
```

### Branching flow

```
/fork <message-id>
  -> session_before_fork event
  -> create new session file from entries up to message-id
  -> runtime.switch() to new session
  -> session_fork event
(original session file unchanged)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Format | JSONL, tree-structured | Append-only, diff/stream friendly, supports branching |
| Compaction | Lossy, non-destructive | Reclaims context while preserving source history |
| Migration | Explicit version + on-load migration | Supports evolving format without breaking old sessions |
| Hot-swap | Runtime recreation | Clean state across sessions/cwds |
| Hook surface | `session_before_*`/`session_*` pairs | Extensions observe and augment lifecycle |

## Risks and Unknowns

1. Large session files (multi-MB) affect resume and read performance; pruning policy is undefined.
2. Migration logic must handle every prior version; a missed step corrupts old sessions.
3. Compaction quality (what gets summarized) directly affects agent performance and is hard to evaluate automatically.

## Out of Scope

- The interactive TUI rendering of sessions (FEAT-0004).
- The agent loop and tool execution (FEAT-0002).
- Extension API internals beyond session hooks (FEAT-0005).

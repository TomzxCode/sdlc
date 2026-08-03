---
title: "Kanban Multi-Agent Work Queue"
status: done
---

# Specification: Kanban Multi-Agent Work Queue

## Overview

Kanban is implemented as three cooperating layers: a CLI parser and SQLite-backed store (`hermes_cli/kanban.py`), a `kanban_*` toolset for agent workers (`tools/kanban_tools.py`), and a long-lived dispatcher embedded in the gateway (or run standalone via `hermes kanban daemon`). Boards live in a directory tree where each board has its own SQLite database, workspaces directory, and (when run standalone) dispatcher.

## Architecture

```
User / orchestrator agent
    │  kanban_create / kanban_link / kanban_comment ...
    v
kanban_* tools (tools/kanban_tools.py)        hermes kanban CLI (hermes_cli/kanban.py)
    │                                                 │
    └───────────────►  SQLite board store (per-board DB)
                              │
                              v
                     Dispatcher (embedded in gateway, default)
                     │  - reclaim stale claims (60s tick)
                     │  - promote ready tasks
                     │  - atomically claim + spawn assigned profile
                     │  - auto-block after failure_limit
                     │
                     └──► Worker agent (spawned, HERMES_KANBAN_BOARD pinned)
                              │  kanban_heartbeat / kanban_complete / kanban_comment
                              v
                     Board DB (claim released, run history appended)
```

## Data Models

### Board

| Field | Type | Constraints | Description |
|---|---|---|---|
| slug | text | immutable | Directory name; identifier for the board |
| name | string | — | Human-readable display name (renamable) |
| db_path | path | per-board | SQLite database path under the board directory |
| workspaces | path | per-board | Worker workspace directory for the board |
| dispatcher | process | optional | Standalone dispatcher process when not gateway-embedded |

### Task

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | uuid | PK | Task identifier |
| title | text | not null | Task title |
| description | text | — | Free-form task body |
| status | enum | todo/in_progress/blocked/done/archived | Card status; blocked is explicit and skips brief running-to-blocked transition |
| priority | int | default 0 | Priority tiebreaker |
| assignee | string | nullable | Assigned profile |
| tenant | string | nullable | Tenant namespace within a board |
| dedup_key | text | unique | Idempotent create key (no duplicate task created on re-submission) |
| created_by | string | — | Creator/anchor profile |
| failure_count | int | default 0 | Consecutive non-success attempts |

## API Contracts

The model-facing contract is the `kanban_*` toolset:

| Tool | Purpose |
|---|---|
| kanban_show | Show a task with comments and events |
| kanban_complete | Mark a task done |
| kanban_block | Block a task |
| kanban_heartbeat | Report worker liveness (extends the claim) |
| kanban_comment | Append a comment |
| kanban_create | Create a task (idempotent via dedup key) |
| kanban_link | Add a parent->child dependency |
| kanban_attach / kanban_attach_url | Attach a file/URL to a task |
| kanban_attachments | List a task's attachments |

Profiles that explicitly enable the `kanban` toolset outside a dispatcher-spawned task also get `kanban_list` and `kanban_unblock` for board routing.

## Sequences

### Dispatch tick (default 60s)
```
Dispatcher tick
    → reclaim stale claims (SIGTERM then SIGKILL runaway workers)
    → promote ready tasks (respect dependency links)
    → atomically claim a task
    → spawn the assigned profile (HERMES_KANBAN_BOARD pinned)
    → worker heartbeats keep the claim alive
    → worker completes → run history recorded → next promotion
```

### Idempotent create (automation / webhooks)
```
kanban_create(dedup_key="K")
    → existing task with key K? → return its id (no duplicate)
    → otherwise create a new task with key K
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | SQLite per board | Durable, zero-dependency, survives restarts |
| Board as hard boundary | HERMES_KANBAN_BOARD env pinned on workers | Prevents cross-board visibility without per-task ACLs |
| Dispatcher location | Embedded in gateway by default | No extra process to run; `hermes kanban daemon --force` for standalone |
| Failure handling | Auto-block after failure_limit | Prevents unbounded retry spin loops |
| Tenant isolation | Workspace-path + memory-key namespacing | One specialist fleet can serve multiple businesses on one board |
| Runaway workers | SIGTERM then SIGKILL on reclaim | Guarantees abandoned tasks are freed in bounded time |

## Risks and Unknowns

1. Single-host dispatcher limits multi-machine collaboration (out of scope for now)
2. Auto-block heuristics may block a task a human could complete manually — operators can unblock
3. Attachment storage lives in the board directory, so hard-deleting a board removes attachments

## Out of Scope

- Cross-machine / distributed boards
- Task dependency DAG execution (links exist, but the dispatcher promotes ready tasks; complex DAG scheduling is future work)
- Fine-grained per-user ACLs beyond the board/tenant isolation model

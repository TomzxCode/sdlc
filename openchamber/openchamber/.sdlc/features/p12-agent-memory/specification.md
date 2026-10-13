---
title: "Agent Memory"
status: done
---

# Specification: Agent Memory

## Overview

Agent memory is owned by `packages/web/server/lib/agent-memory/`, with `runtime.js` owning the JSON-file store, `actions.js` owning the `memory.*` tool dispatch, `routes.js` owning the panel HTTP surface, `project-resolution.js` mapping session directories to projects, `threat-patterns.js` flagging prompt-injection text, and `feature-flag.js` gating the build.
The UI speaks to it only through `packages/ui/src/lib/agentMemoryApi.ts`, and the session index in `session-knowledge/runtime.js` carries entry titles plus save guidance into sessions where memory is on.

## Architecture

```
Managed OpenCode `openchamber_memory` tool ──memory.*──> actions.js ──┐
                                                                      v
Memory panel ──HTTP /api/agent-memory*──> routes.js ──> runtime.js (memory.json per scope)
                                                                      ^
Session index (titles only + save guidance) ──readAll──> runtime.js ──┘
Project scope resolution: session directory ──> project-resolution.js ──> project id
Injection screening on write and read: threat-patterns.js
Build gate: feature-flag.js (OPENCHAMBER_MEMORY_ENABLE); runtime gate: agentMemoryToolEnabled
```

## Data Models

### Memory entry

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK, non-empty | Generated identifier, stable across corrections |
| title | string | Required, max 60 chars | Short label; also the lookup key for reads by title |
| body | string | Required, max 2000 chars | Full text, rejected over the limit rather than truncated |
| type | enum | `fact`, `preference`, `reference`; defaults to `fact` | What kind of knowledge the entry holds |
| createdAt | number | Unix ms, non-negative | Set once at creation |
| updatedAt | number | Unix ms, non-negative | Bumped on replacement and correction; drives panel new/changed badges |
| flagged | boolean | Optional, set when a threat pattern matches | Withheld from sessions, shown in the panel |
| sessionId | string | Optional | Session the entry was learned in, when recorded |

### Memory file

| Field | Type | Constraints | Description |
|---|---|---|---|
| version | number | Currently 1 | Store format version |
| entries | array | Max 60 global, 200 project | Sorted by `updatedAt` descending on read |

## API Contracts

| Method | Path | Description |
|---|---|---|
| GET | /api/agent-memory?scope=global | Read the global store |
| GET | /api/agent-memory?scope=project&projectId=... | Read one project store; missing projectId is a 400 |
| GET | /api/agent-memory/all?projectId=... | Read both scopes at once for the panel; per-scope failure flags included |
| PATCH | /api/agent-memory/:memoryId?scope=... | Correct title, body, or type in place; unknown id is a 404 |
| DELETE | /api/agent-memory/:memoryId?scope=... | Delete the entry in scope; unknown id is a 404 |

All routes sit behind the enabled gate, which answers disabled-flagged 404 when memory is off and 503 when the setting cannot be read.
Validation failures answer 400, and there is intentionally no create route because creation belongs to the agent tool.

### Tool actions (`openchamber_memory`)

| Action | Input | Output |
|---|---|---|
| memory.list | Optional scope (`both` default) | Summaries (`memoryId`, title, type, scope), no bodies, plus unavailability flags |
| memory.read | `memoryId` or title, optional scope | Full entry with body; project preferred when unscoped |
| memory.save | scope, title, body, optional type and sessionId | Saved summary plus `replaced` flag and injection warning when flagged |
| memory.delete | scope, `memoryId` | Deletion confirmation |

## Sequences

### Remember flow

```
1. Agent calls memory.save with scope, title, body, and optional type.
2. actions.js rejects the call when memory is off and resolves project scope from the session directory.
3. runtime.js validates title and body, screens for threat patterns, and checks for a superseded entry.
4. A restatement updates the existing entry in place and reports replaced: true.
5. A new entry is prepended under a per-scope write lock and persisted atomically.
6. onMemoryChanged announces the write so an open panel refreshes.
```

### Recall flow

```
1. Session index build calls readAll and embeds titles only, grouped as About the user and About this project.
2. Flagged entries are excluded from what the session is told.
3. Agent reads a promising title once via memory.read by title or memoryId.
4. The full body then stays in context and is not re-read on later turns.
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Dark shipping | Build flag plus settings toggle, both default off | Test against real work without appearing to users who never asked for it |
| Two scopes, two files | Global under user config root, project beside the bounded project folder | A wrong global fact shapes every project, so global stays small and separate |
| Restatements replace | Exact title match, else 0.75 token overlap with stop-word filtering and a 4-token minimum | Prevents near-duplicate drift while making silent merges of distinct memories unlikely |
| Reject over-limit bodies | 400 usage error naming the limit and actual length | A silent slice would confirm a body that was never stored |
| Missing versus malformed | Missing file reads as empty; corrupt file throws | An agent told it has no memories would rewrite everything it thought it lost |
| Project from directory | Session directory resolved through configured projects then git primary worktree | Worktree sessions share one project memory instead of filing into invisible stores |
| Pattern screening, not deletion | Flagged entries stored, withheld from sessions, shown to the user | Only the user can judge the attempt, and silent drops would hide it |

## Risks and Unknowns

1. Threat patterns raise the floor only against blunt injections; subtle prompt smuggling still passes.
2. The UI title clamp (120) exceeds the server clamp (60), so the editor can accept titles the server trims.
3. The tool persists in the managed child until it restarts, so the runtime gate must keep refusing calls made between switch-off and restart.

## Out of Scope

- User notes, which remain a separate surface the user writes and pins
- Any create route on the HTTP surface
- Cross-project search or merging of project stores
- Classifier-based injection detection

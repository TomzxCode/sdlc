---
title: "Multi-Agent / Multi-Run Sessions"
status: done
---

# Specification: Multi-Agent / Multi-Run Sessions

## Overview

Multi-run creates multiple OpenCode sessions in parallel, each targeting an isolated Git worktree. The Agent Manager UI in `packages/ui/src/components/multirun/` displays each agent's progress. A fusion view combines results for comparison.

## Architecture

```
User prompt (multi-agent enabled)
    |
    v
MultiRunStore (packages/ui/src/stores/useMultiRunStore.ts)
    |
    v  POST /api/sessions (x N)
Express Server creates N sessions with worktrees
    |
    v
N parallel OpenCode SSE streams
    |
    v  Event pipeline (coalesced per session)
N independent Zustand session states
    |
    v
Agent Manager UI (packages/ui/src/components/multirun/)
```

## Data Models

### MultiRunConfig

| Field | Type | Constraints | Description |
|---|---|---|---|
| agentCount | number | 1-10 | Number of parallel agents |
| isolation | boolean | not null | Whether to use worktree isolation |
| modelLimits | object | nullable | Per-agent model/cost constraints |
| prompt | string | not null | Shared prompt for all agents |

### MultiRunResult

| Field | Type | Constraints | Description |
|---|---|---|---|
| sessionId | string | FK | Per-agent session ID |
| worktreePath | string | nullable | Isolated worktree path |
| status | enum | not null | running, completed, failed |
| fusionData | object | nullable | Merged result for fusion view |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Isolation | Git worktrees (primary), directory copies (fallback) | Worktrees are lightweight and share .git objects; no full clone needed |
| UI component | Dedicated multirun/ section | Separate from single-session chat to avoid state confusion |
| State | Per-session Zustand stores with multi-run orchestration | Reuses existing session infrastructure |

## Risks and Unknowns

1. Worktree creation may fail on repos with sparse checkout or unusual .git layouts
2. Fusion of results from different agents may produce conflicting code changes

## Out of Scope

- Automatic selection of best result
- Cross-agent communication or coordination

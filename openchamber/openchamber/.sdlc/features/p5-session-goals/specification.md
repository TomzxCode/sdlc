---
title: "Session Goals (Autonomous Multi-Turn Execution)"
status: done
---

# Specification: Session Goals

## Overview

Session goals enable autonomous multi-turn execution driven by the web server backend. The objective is stored in `session.metadata.openchamber.goal` and persists across restarts. The loop runs on the server so it survives UI disconnects and browser tabs closing.

## Architecture

```
User sets goal via UI
    |
    v
useSessionGoalArmStore (arms next message as goal start)
    |
    v
Session sends prompt with goal metadata
    |
    v
Server: packages/web/server/lib/session-goal/runtime.js
    |   - Monitors session status for idle/activity
    |   - Sends auto-continuations via prompt_async
    |   - Tracks turns, tokens, and audit results
    |
    v
Server: packages/web/server/lib/session-goal/audit.js (independent small model call)
    |   - Evaluates each turn for completeness
    |   - Generates progress note (<= 280 chars)
    |   - Produces verdict: pass / fail (blocked)
    |
    v
Goal status updated in metadata
    |
    v
UI goal strip (Goal strip component) reflects status
```

## Data Model

### Goal payload (`metadata.openchamber.goal`)

| Field | Type | Description |
|---|---|---|
| id | string | Opaque per-logical-goal identifier; stale-write guard |
| objective | string | Inline user text (fallback), <= 5000 chars |
| objectiveFile | boolean | True if objective text lives in a server-side file |
| status | string | active / paused / blocked / budgetLimited / complete |
| tokenBudget | number (optional) | Positive integer budget |
| tokensUsed | number | tokensCommitted + current segment snapshot |
| tokensBaseline | number | Segment start snapshot |
| tokensCommitted | number | Closed segments total |
| turnsUsed | number | Auto-continuations sent |
| blockedStreak | number | Consecutive blocked audit verdicts |
| auditFailStreak | number | Consecutive failed/unavailable audit calls |
| note | string | Latest audit progress note, <= 280 chars |
| statusReason | string | Why settled; 'resumed' is UI kickoff signal |
| evaluationProviderID | string | Provider used by latest successful audit |
| evaluationModelID | string | Model used by latest successful audit |
| lastAccountedMessageID | string | Incremental accounting cursor |
| createdAt, updatedAt | ISO timestamp | Creation and last update timestamps |

## Key Flows

### Goal creation
1. User arms the goal via the composer target button or fork dialog
2. The goal arm store tracks the armed state and optional objective override
3. On send, the prompt is tagged with goal metadata
4. The server runtime reads the goal from session metadata and starts the loop

### Auto-continuation loop
1. After the main response completes, the runtime detects the goal is still active
2. An audit call evaluates the latest turn
3. If audit passes and goal not complete, the runtime sends `prompt_async` with the objective
4. Token and turn accounting are updated
5. Loop repeats until goal is complete, blocked, or budget exhausted

### Session compaction handling
1. The runtime listens for `session.compacted` events
2. After compaction, goal metadata is preserved and the next auto-continuation uses compacted context

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Goal storage | Session metadata | Survives restarts without separate storage |
| Audit model | Small model config | Reuses existing provider config, minimal extra cost |
| Turn limit | 50 (configurable) | Prevents infinite loops while allowing complex tasks |
| Blocked detection | 3 consecutive audit failures | Balances false positives against wasted compute |
| Token tracking | Per-segment with cumulative total | Budget enforcement without complex accounting |
| UI updates | SSE events from runtime | Real-time progress without polling |

## Risks and Unknowns

1. Audit quality depends on the configured small model; weak models may produce unreliable verdicts
2. Token budget accuracy depends on provider reporting and may vary
3. Very long goals may require periodic compaction which adds latency
4. The audit progress note is limited to 280 chars, which may be insufficient for complex progress descriptions

## Out of Scope

- Goal templates with predefined objectives
- Multi-session goals (single session per goal)
- Goal sharing between users
- Automatic goal recommendation based on session content

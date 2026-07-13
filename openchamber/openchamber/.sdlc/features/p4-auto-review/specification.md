---
title: "Auto Review (Automated Agent Review Loop)"
status: done
---

# Specification: Auto Review

## Overview

Auto Review orchestrates a back-and-forth loop between two agents. The original agent completes work in a session; the user triggers review, which creates a linked review session. A reviewer agent examines the original session's output, generates findings, and passes them back. The original agent revises. The loop repeats until the reviewer finds no remaining issues or the max iteration count is reached.

## Architecture

```
User triggers auto review on session A
    |
    v
reviewFlow.ts startReviewFlow()
    |
    +-- Creates review session B (linked via metadata)
    +-- Sets phase to "waiting_for_reviewer"
    |
    v
Reviewer agent processes session A's output
    |
    +-- Generates findings in session B
    +-- Sets phase to "waiting_for_implementer"
    |
    v
Original agent receives findings and revises session A
    |
    +-- New findings? → back to reviewer
    +-- "FINAL_REVIEW_STATUS: no_remaining_findings" → done
```

## Data Models

### AutoReviewRun

| Field | Type | Constraints | Description |
|---|---|---|---|
| originalSessionID | string | PK | Original session being reviewed |
| reviewSessionID | string | not null | Review session for findings |
| directory | string | not null | Project directory |
| runtimeKey | string | not null | Runtime identifier for bridging |
| status | string | `running`, `completed`, `stopped`, `error` | Review loop status |
| phase | string | `waiting_for_reviewer`, `waiting_for_implementer` | Current loop phase |
| iteration | number | not null | Current iteration count |
| maxIterations | number | default 15 | Maximum loop iterations |

## API Contracts

The review flow is client-side orchestrated via `packages/ui/src/lib/reviewFlow.ts` using the OpenCode SDK's message sending and metadata patching. No dedicated server routes.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Orchestration | Client-side (browser/desktop) | Leverages existing session-actions and OpenCode SDK; no server changes needed |
| Session linking | Session metadata (`openchamber.reviewSessionID`, `openchamber.originalSessionID`) | Avoids separate tracking infrastructure |
| Completion signal | Final message content marker | Simple string detection, no structured output parsing |
| Polling | 300-400ms interval for handoff detection | Balance of responsiveness and resource usage |

## Risks and Unknowns

1. Very long review loops could create many messages. The iteration cap prevents infinite loops.
2. The final marker detection relies on the AI including the exact string "FINAL_REVIEW_STATUS: no_remaining_findings", which may not be reliable across all models.

## Out of Scope

- Automated trigger on session completion (requires user intent)
- Visual diff of review changes
- Custom reviewer agent configuration

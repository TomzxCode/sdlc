---
title: "Timeline / Undo / Redo"
status: done
---

# Specification: Timeline / Undo / Redo

## Overview

The timeline system uses `TimelineDialog.tsx` for the full-history view, `useTimelineStaging.ts` for deferred rendering, `useChatTimelineController.ts` for timeline logic, and `useChatTurnNavigation.ts` for keyboard-driven turn navigation.

## Architecture

```
TimelineDialog (packages/ui/src/components/chat/TimelineDialog.tsx)
    +---> Full message list with search
    +---> Revert / Fork actions per message
    +---> useTimelineStaging (deferred rendering)
    |
useChatTimelineController (turn-based undo/redo logic)
useChatTurnNavigation (keyboard arrow key navigation)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Rendering | Deferred staging | Large timelines (100+ messages) need virtualization to avoid DOM bloat |
| Navigation | Turn-based, not message-based | Users think in turns (user+assistant pairs), not individual messages |
| History | Server-side via OpenCode | Message branching is an OpenCode concept; UI sends revert/fork commands |

## Out of Scope

- Visual diff between branches
- Merge between branches

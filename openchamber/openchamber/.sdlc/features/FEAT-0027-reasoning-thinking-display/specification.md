---
title: "Reasoning / Thinking Display"
status: draft
---

# Specification: Reasoning / Thinking Display

## Overview

Reasoning display uses `ReasoningPart.tsx` and `JustificationBlock.tsx` in the chat message parts. Collapsed state shows a header with animated typing indicator; expanded state shows full reasoning text.

## Architecture

```
ReasoningPart (packages/ui/src/components/chat/message/parts/ReasoningPart.tsx)
    +---> Collapsed: summary preview header with typing animation
    +---> Expanded: full reasoning text
    |
JustificationBlock.tsx (justification-specific rendering)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Animation | CSS transitions | Smooth expand/collapse without JS animation overhead |
| Merged view | Per-turn (not per-message-part) | Reduces visual noise; reasoning spans multiple parts |

## Out of Scope

- Reasoning editing
- Reasoning comparison between turns

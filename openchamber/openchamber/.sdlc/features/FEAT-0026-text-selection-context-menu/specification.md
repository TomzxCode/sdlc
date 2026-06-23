---
title: "Text Selection Context Menu"
status: draft
---

# Specification: Text Selection Context Menu

## Overview

The text selection menu is implemented in `TextSelectionMenu.tsx` within the chat message components. It detects text selection via the Selection API, computes position, and renders a floating action bar.

## Architecture

```
TextSelectionMenu (packages/ui/src/components/chat/message/TextSelectionMenu.tsx)
    +---> Selection API detection
    +---> Position computation (near selection)
    +---> Action buttons: Copy, Add to Notes, Ask AI, Add as Todo
    |
    v  Actions
Clipboard API, ProjectNotesTodoPanel, ChatInput
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Detection | Selection API (not mouseup) | Works for both mouse and touch selection |
| Positioning | Near selection, clamped to viewport | Follows user's visual focus |

## Out of Scope

- Custom action configuration
- Selection across multiple message bubbles

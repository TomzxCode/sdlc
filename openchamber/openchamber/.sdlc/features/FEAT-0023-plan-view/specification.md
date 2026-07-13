---
title: "Plan View"
status: done
---

# Specification: Plan View

## Overview

The plan view (`PlanView.tsx`) is a markdown editor using CodeMirror that opens in the context panel. It provides write/preview toggle, inline comments, and actions to send the plan to the current session or create a worktree from it.

## Architecture

```
PlanView (packages/ui/src/components/views/PlanView.tsx)
    |
    +---> CodeMirror editor (markdown mode)
    +---> Preview toggle (rendered markdown)
    +---> Action bar: Send to session, Create worktree, Save
    |
    v
Context Panel overlay (packages/ui/src/components/layout/ContextPanel.tsx)
```

## Sequences

### Send plan to session for implementation

```
User writes plan in PlanView -> Clicks "Implement"
    |
    v
Plan markdown injected as a prompt in the current chat session
    |
    v
Agent processes the plan and begins implementation
```

### Create worktree from plan

```
User clicks "Create worktree" -> NewWorktreeDialog opens
    |
    v
User configures branch name -> Worktree created
    |
    v
New session started in worktree with plan context attached
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Editor | CodeMirror with markdown mode | Consistent with file editor; syntax highlighting and keybindings |
| Location | Context panel overlay | Keeps plan visible alongside chat without splitting the main view |
| Persistence | Optional file save | Plans are primarily session-scoped; file save is for sharing |

## Risks and Unknowns

1. Plan mode adoption is unknown; the feature flag may be permanent or removed

## Out of Scope

- Plan version history
- Plan comparison between sessions
- Automatic plan generation from requirements

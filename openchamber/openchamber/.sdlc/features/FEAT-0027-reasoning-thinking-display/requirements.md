---
title: "Reasoning / Thinking Display"
status: done
---

# Requirements: Reasoning / Thinking Display

## Overview

Expandable/collapsible rendering of AI reasoning/thinking and justification blocks in chat messages. Shows a summary preview when collapsed with animated expand/collapse. Supports per-turn merged view and user-toggleable display preference.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Users of extended thinking models (o1, o3) | Inspect AI reasoning chains |
| Power users | Toggle reasoning visibility for cleaner or more transparent view |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall render reasoning/thinking blocks as expandable sections in chat messages. |
| FR-02 | Must | The system shall show a summary preview when collapsed. |
| FR-03 | Must | The system shall support smooth animated expand/collapse transitions. |
| FR-04 | Should | The system shall merge reasoning blocks into a per-turn view. |
| FR-05 | Should | The system shall support a user toggle for showing/hiding reasoning by default. |
| FR-06 | Should | The system shall support keyboard navigation for thinking mode in model selector. |
| FR-07 | Must | The system shall render reasoning blocks in full without truncation, applying sanitization only. |

## Acceptance Criteria

- [ ] FR-01: Given a response with reasoning, it renders as a collapsible block
- [ ] FR-02: Given a collapsed reasoning block, a summary preview is visible
- [ ] FR-03: Given expand/collapse, the animation is smooth without layout shift
- [ ] FR-04: Given multiple reasoning blocks in a turn, they are merged into a single per-turn view
- [ ] FR-05: Given the chat settings, the user can toggle reasoning visibility
- [ ] FR-06: Given the model selector, the user can navigate thinking mode options using keyboard
- [ ] FR-07: Given a reasoning block, the full text is rendered without truncation after sanitization

## Constraints

- The cleanReasoningText function sanitizes reasoning text but does not truncate

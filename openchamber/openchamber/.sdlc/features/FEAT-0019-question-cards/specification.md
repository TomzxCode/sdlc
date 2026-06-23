---
title: "Question Cards"
status: draft
---

# Specification: Question Cards

## Overview

Question cards are implemented in `QuestionCard.tsx` with serialization via `questionSerializers.ts`. The AI sends structured question payloads via the OpenCode SDK, and the UI renders them as interactive cards.

## Architecture

```
QuestionCard (packages/ui/src/components/chat/QuestionCard.tsx)
    +---> Text input
    +---> Radio (single choice)
    +---> Checkbox (multi choice)
    +---> Copy as Markdown / JSON
    |
questionSerializers.ts (format conversion)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Rendering | Typed by question type | Different input types require different UI controls |
| Export | Markdown and JSON | Markdown for human sharing; JSON for programmatic use |

## Out of Scope

- Conditional question branching
- File upload question type

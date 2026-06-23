---
title: "AI-Generated Commits & PR Descriptions"
status: draft
---

# Specification: AI-Generated Commits & PR Descriptions

## Overview

AI generation uses structured output from OpenCode sessions. The git view components (`AIHighlightsBox.tsx`, `CommitInput.tsx`, `PullRequestSection.tsx`) parse the JSON result via `generatedJsonResult.ts` and render it with `GeneratedJsonResultCard.tsx`.

## Architecture

```
Git View - CommitInput (packages/ui/src/components/views/git/)
    +---> "Generate" button triggers AI via OpenCode session
    +---> Structured JSON output parsed by generatedJsonResult.ts
    +---> GeneratedJsonResultCard renders subject + highlights
    +---> One-click insert into commit input
    |
Git View - PullRequestSection
    +---> "Generate" button triggers AI from branch diff
    +---> Result card with title + body
    +---> One-click insert into PR form
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Generation | OpenCode session (structured output) | Reuses existing AI infrastructure; consistent with agent behavior |
| Parsing | JSON structured output | Clean separation of subject/body/highlights |

## Out of Scope

- Custom generation templates (handled by Magic Prompts)
- Commit message linting

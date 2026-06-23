---
issue: ""
title: "Question Cards"
status: draft
---

# Existing Solutions: Question Cards

## Overview

OpenChamber has a fully implemented QuestionCard component supporting all required input types (radio buttons for single-choice, checkboxes for multi-choice, custom text input, file paths via textarea), copy-as-Markdown and copy-as-JSON export, inline response submission, multi-question tab navigation, and pending-question preservation across session switches. SSE event handling for question.asked/replied/rejected and toast notifications are already in place. The requirements are fully covered by the existing implementation; no new work is needed.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | packages/ui/src/components/chat/QuestionCard.tsx; questionSerializers.ts; questionSerializers.test.ts; types/question.ts; sync-context.tsx (SSE handling); lib/i18n messages |
| Open-source | Yes | npm for survey/form builder components that could render AI questions |
| Commercial / SaaS | No | Not applicable |
| Standards / protocols | No | OpenCode SDK defines the question protocol |
| Reference material | Yes | react-minimal-survey-builder, form-engine-react, SurveyJS |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal implementation | Internal | MIT | Mature | All FRs | None identified |
| react-minimal-survey-builder | Library | MIT | Early (0.4.x) | FR-01, FR-04, FR-06 | FR-02, FR-03, FR-05; architecture mismatch, no OpenCode integration |
| @question-forms/react | Library | MIT | Active | FR-01, FR-04, FR-06 | Same — schema-driven form builder, not AI question protocol |
| form-engine-react | Library | MIT | Early (1.0.x) | FR-01, FR-04 | Same — generic form builder |

## Evaluation

### Existing Internal Implementation

- **Strengths:** Complete QuestionCard with radio/checkbox/text/textarea/file path inputs, multi-tab navigation for multi-question requests, custom "Other" text field, copy-as-Markdown and copy-as-JSON via pure serializers (unit-tested), inline submit/dismiss, pending-question persistence in sync store across session switches, SSE event pipeline integration (question.asked/replied/rejected), toast notifications for background questions, recommended option highlighting, sub-agent source labeling, i18n translations across all supported locales
- **Weaknesses:** No deferred rendering for hundreds of questions (unlikely use case for AI questions). File path questions use plain text input rather than a file browser dialog.
- **Integration effort:** No integration needed — already fully integrated
- **Cost:** Already maintained
- **Risks:** None — code is production-used

### External survey/form builders

- **Strengths:** Rich schema-driven question definitions, drag-and-drop builders, custom renderers
- **Weaknesses:** Built for human-authored surveys, not AI-generated QuestionRequest protocol. No OpenCode SSE event handling, no session-aware state management, no copy-as-JSON/Markdown export. Heavy dependencies.
- **Integration effort:** Very high — would require a protocol adapter layer
- **Cost:** Free
- **Risks:** Unnecessary complexity for the use case

## Recommendation

**Direction:** Build (existing implementation covers all requirements)

No adoption needed. The existing QuestionCard, questionSerializers, SSE event handlers, and session store already meet every functional requirement. The only potential enhancement is replacing the plain textarea for file path questions with a proper file browser, which is a future UI polish rather than a requirements gap.

## Sources of Information

- `packages/ui/src/components/chat/QuestionCard.tsx`: Full QuestionCard implementation with all input types
- `packages/ui/src/components/chat/questionSerializers.ts`: Pure functions for Markdown and JSON export (unit-tested)
- `packages/ui/src/components/chat/__tests__/questionSerializers.test.ts`: Tests for serializers
- `packages/ui/src/types/question.ts`: QuestionRequest type definitions
- `packages/ui/src/sync/sync-context.tsx`: Lines 1210-1236 — SSE event handling for question.asked/replied/rejected
- `packages/ui/src/sync/session-ui-store.ts`: Question state in sync store
- `packages/ui/src/sync/session-actions.ts`: respondToQuestion and rejectQuestion functions

## Open Questions

1. Should file path questions be enhanced with a proper file browser dialog, or is the textarea sufficient?
2. Does the QuestionCard need deferred rendering (virtualization) for edge cases with 50+ questions in one request?

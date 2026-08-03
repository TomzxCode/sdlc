---
title: "Inline Comments & Annotations"
status: done
---

# Test Plan: Inline Comments & Annotations

## Scope

Tests cover the inline-comment draft store used by the inline comment controller.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Inline comment draft store manages drafts across files/sessions | Draft create/update/discard actions | Draft state transitions correctly |

## Test Files

- `packages/ui/src/stores/useInlineCommentDraftStore.terminal.test.ts`

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR (draft annotation state) | TC-1 |

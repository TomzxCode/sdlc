---
title: "Text Selection Context Menu"
status: done
---

# Test Plan: Text Selection Context Menu

## Scope

Tests cover the markdown conversion of selected text used by the text-selection context menu actions.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Selected text converts to markdown for context-menu actions | Raw selected text | Correct markdown representation |

## Test Files

- `packages/ui/src/components/chat/message/selectionMarkdown.test.ts`

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR (copy/explain/refactor/fix actions on selection) | TC-1 |

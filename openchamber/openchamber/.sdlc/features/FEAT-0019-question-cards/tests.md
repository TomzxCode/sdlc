---
title: "Question Cards"
status: done
---

# Test Plan: Question Cards

## Scope

Tests cover question card serialization and the textarea sizing behavior of the question input.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Question serialization round-trips structured questions | Question object | Correct serialized form |
| TC-2 | Question textarea sizing adapts to content | Textarea content | Appropriate height |

## Test Files

- `packages/ui/src/components/chat/__tests__/questionSerializers.test.ts`
- `packages/ui/src/components/chat/__tests__/questionTextareaSizing.test.ts`

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR (structured question serialization) | TC-1 |
| FR (question input UX) | TC-2 |

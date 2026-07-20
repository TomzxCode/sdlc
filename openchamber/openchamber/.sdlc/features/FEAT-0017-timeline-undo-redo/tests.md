---
title: "Timeline / Undo / Redo"
status: done
---

# Test Plan: Timeline / Undo / Redo

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Chat timeline controller handles undo/redo | Undo/redo events | Timeline state updates correctly |
| TC-2 | Raw message preview renders correctly | Message data | Preview shows expected content |

## Test Files

- `packages/ui/src/components/chat/hooks/useChatTimelineController.test.ts`
- `packages/ui/src/components/layout/__tests__/rawMessagePreview.test.ts`

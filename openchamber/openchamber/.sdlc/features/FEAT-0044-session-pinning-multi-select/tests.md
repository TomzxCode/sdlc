---
title: "Session Pinning & Multi-Select"
status: done
---

# Test Plan: Session Pinning & Multi-Select

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Sidebar persistence saves pinned state | Pin/unpin events | Pinned sessions persist across reloads |
| TC-2 | Context obligatory messages handle multi-session context | Multiple sessions selected | Correct context is aggregated |

## Test Files

- `packages/ui/src/components/session/sidebar/hooks/useSidebarPersistence.test.ts`
- `packages/ui/src/lib/contextObligatoryMessages.test.ts`

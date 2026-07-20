---
title: "Auto Review (Automated Agent Review Loop)"
status: done
---

# Test Plan: Auto Review (Automated Agent Review Loop)

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | hasFinalReviewMarker detects review markers | Session messages | Correctly identifies final review marker |
| TC-2 | stripFinalReviewMarker removes markers | Message with marker | Marker is removed from content |
| TC-3 | claimAutoReviewForward handles dedup | Concurrent claims | Only one claim succeeds per forward |

## Test Files

- `packages/ui/src/lib/reviewFlow.test.ts`

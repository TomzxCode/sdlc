---
title: "Chat & Session Management"
status: done
---

# Test Plan: Chat & Session Management

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Event reducer transforms raw SSE events | Raw event payload | Store-friendly patches |
| TC-2 | Event pipeline reconnects after disconnect | WebSocket close event | Exponential backoff, successful reconnect |
| TC-3 | Session UI store manages session list | Session list events | Correctly sorted and limited sessions |
| TC-4 | Input store queues messages | Multiple rapid submissions | FIFO ordering, dequeue after ack |
| TC-5 | Question serializers render correctly | Question card event | Properly rendered UI components |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-10 | Full send-and-receive message flow | Active session, user types message | Message visible in timeline, response streams |
| TC-11 | Session switch resync | Two open sessions, user switches | UI shows correct session, scroll restored |
| TC-12 | Event pipeline handles permanent errors | Server returns 4xx | Jump to long backoff, no infinite retry |

## Test Files

- `packages/ui/src/sync/__tests__/event-reducer.test.js`
- `packages/ui/src/sync/__tests__/event-pipeline.test.js`
- `packages/ui/src/sync/__tests__/event-pipeline-permanent-error.test.js`
- `packages/ui/src/sync/__tests__/event-pipeline-resume.test.js`
- `packages/ui/src/sync/__tests__/session-switch-resync.test.ts`
- `packages/ui/src/sync/session-ui-store.test.js`
- `packages/ui/src/sync/input-store.test.ts`
- `packages/ui/src/sync/session-message-records.test.ts`
- `packages/ui/src/sync/__tests__/session-event-freshness.test.ts`
- `packages/ui/src/sync/__tests__/materialization.test.ts`
- `packages/ui/src/sync/__tests__/eviction.test.ts`
- `packages/ui/src/components/chat/__tests__/questionSerializers.test.ts`
- `packages/ui/src/components/chat/__tests__/baseDisplayMessagesDedup.test.ts`
- `packages/ui/src/components/chat/__tests__/attachmentCitations.test.ts`
- `packages/ui/src/sync/__tests__/sync-context-session-events.test.ts`

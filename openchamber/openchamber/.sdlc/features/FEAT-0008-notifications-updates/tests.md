---
title: "Notifications & Updates"
status: done
---

# Test Plan: Notifications & Updates

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Notification emitter works | Event notification | Correctly emitted notification |
| TC-2 | APNs runtime handles push tokens | APNs token | Correct registration/deregistration |

## Test Files

- `packages/web/server/lib/notifications/emitter-runtime.test.js`
- `packages/web/server/lib/notifications/template-runtime.test.js`
- `packages/web/server/lib/notifications/apns-runtime.test.js`
- `packages/web/server/lib/notifications/message.test.js`
- `packages/web/server/lib/notifications/push-runtime.test.js`
- `packages/web/src/api/notifications.test.ts`
- `packages/ui/src/sync/permission-toast.test.ts`
- `packages/ui/src/components/update/__tests__/openCodeUpdateDedup.test.ts`
- `packages/web/server/lib/package-manager.test.js`

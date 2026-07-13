---
title: "Onboarding & Auth"
status: done
---

# Test Plan: Onboarding & Auth

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Auth gate validates session | Request with session token | Correct allow/deny |

## Test Files

- `packages/ui/src/components/auth/SessionAuthGate.test.ts`
- `packages/ui/src/components/auth/SessionAuthGate.behavior.test.tsx`
- `packages/web/server/lib/ui-auth/ui-auth.test.js`

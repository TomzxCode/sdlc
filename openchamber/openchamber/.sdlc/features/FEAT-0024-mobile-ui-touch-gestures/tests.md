---
title: "Mobile UI & Touch Gestures"
status: done
---

# Test Plan: Mobile UI & Touch Gestures

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | QR scan parsing works | QR code data | Correct connection URL |
| TC-2 | Mobile connections state | Connection config | Correct save/load/delete |

## Test Files

- `packages/ui/src/apps/mobileQrScan.test.ts`
- `packages/ui/src/apps/mobileConnections.test.ts`

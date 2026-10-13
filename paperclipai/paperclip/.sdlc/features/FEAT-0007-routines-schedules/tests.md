---
title: "Routines & Schedules"
status: done
session_link: "reverse-engineered during 2026-10-13 sync; no live session"
---

# Test Plan: Routines & Schedules

## Scope

Covers routine CRUD with cron/webhook/API triggers, run execution creating tracked issues and waking agents, concurrency/catch-up policy, revisions, secret-aware env overlay, and run tracking.
Out of scope: external calendar integrations beyond cron/webhook/API.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Routine service behavior (`server/src/__tests__/routines-service.test.ts`) | Routine definitions and triggers | Routines stored, triggered, and tracked per contract |
| TC-2 | Cron formatter caching (`server/src/services/routines-formatter-cache.test.ts`) | Sparse monthly cron in a timezone | Correct next tick computed |
| TC-3 | Routine run telemetry (`server/src/__tests__/routine-run-telemetry.test.ts`) | Routine run events | Telemetry recorded for executions |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Routines routes (`server/src/__tests__/routines-routes.test.ts`) | Authenticated company context | CRUD and trigger config endpoints behave per contract |
| TC-5 | Routine secrets E2E (`server/src/__tests__/qa-routine-secrets-e2e.test.ts`) | Routine with secret-aware env | Secret refs resolve against routine binding target without agent bindings |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-6 | Routine execution flow (`server/src/__tests__/routines-e2e.test.ts`) | Trigger fires on a cron routine | Tracked issue created, agent woken, run and activity recorded |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-7 | Overlapping executions | Configured concurrency and catch-up policy applied |

## Test Infrastructure

- Vitest suite under `server/src/__tests__/` and `server/src/services/`.
- Cron fixtures with fixed timestamps and timezones.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1, TC-4 |
| FR-02 | TC-6 |
| FR-03 | TC-7 |
| FR-04 | TC-1 |
| FR-05 | TC-5 |
| FR-06 | TC-1, TC-3 |

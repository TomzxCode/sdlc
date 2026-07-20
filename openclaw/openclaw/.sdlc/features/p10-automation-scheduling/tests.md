---
title: "Automation and Scheduling"
status: done
---

# Test Plan: Automation and Scheduling

## Scope

Unit and integration tests for cron scheduling, webhook receiver, and flow engine. Tests cover delivery, scheduling, isolated-agent execution, failure handling, and webhook HTTP handling.

## Unit Tests

| ID | Description | Source |
|---|---|---|
| TC-1 | Cron schedule parsing | src/cron/parse.test.ts, src/cron/schedule.test.ts |
| TC-2 | Cron delivery planning | src/cron/delivery-plan.test.ts |
| TC-3 | Cron delivery execution | src/cron/delivery.test.ts |
| TC-4 | Retry hint computation | src/cron/retry-hint.test.ts |
| TC-5 | Pacing logic | src/cron/pacing.test.ts |
| TC-6 | Schedule identity normalization | src/cron/schedule-identity.test.ts |
| TC-7 | Active job management | src/cron/active-jobs.test.ts |
| TC-8 | Webhook HTTP handling | extensions/webhooks/src/http.test.ts |
| TC-9 | Webhook config | extensions/webhooks/src/config.test.ts |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-10 | Cron service job execution | src/cron/service.jobs.test.ts | Jobs fire at correct times |
| TC-11 | Cron service declarative jobs | src/cron/service.declarative-jobs.test.ts | Declarative jobs registered |
| TC-12 | Cron failure alerts | src/cron/service.failure-alert.test.ts | Alerts on job failure |
| TC-13 | Cron isolated agent runs | src/cron/isolated-agent.*.test.ts | Isolated sessions start correctly |
| TC-14 | Cron delivery failure notification | src/cron/delivery.failure-notify.test.ts | Notifications sent on failure |
| TC-15 | Flow engine doctor checks | src/flows/doctor-core-checks.test.ts | Doctor checks run and report |
| TC-16 | Webhook index | extensions/webhooks/index.test.ts | Webhook processes requests |
| TC-17 | Heartbeat policy | src/cron/heartbeat-policy.test.ts | Heartbeat jobs fire correctly |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-20 | Duplicate timer scheduling prevented | src/cron/service.prevents-duplicate-timers.test.ts |
| TC-21 | Job removal during execution | src/cron/service.removal-postcommit.test.ts |
| TC-22 | Invalid main job from store | src/cron/service.store-load-invalid-main-job.test.ts |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (cron scheduling) | TC-1, TC-6, TC-10, TC-11 |
| FR-2 (persistence) | TC-10, TC-17 |
| FR-3 (webhooks) | TC-8, TC-9, TC-16 |
| FR-4 (flows) | TC-15 |
| FR-6 (isolated sessions) | TC-13 |
| FR-7 (failure handling) | TC-4, TC-12, TC-14 |
| FR-9 (no duplicates) | TC-20 |


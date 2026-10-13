---
title: "Budget & Cost Control"
status: done
session_link: "reverse-engineered during 2026-10-13 sync; no live session"
---

# Test Plan: Budget & Cost Control

## Scope

Covers cost event ingestion and validation, read-time spend rollups, monthly UTC budgets, 80% soft alerts, and 100% hard-stop auto-pause with checkout/invocation blocking.
Out of scope: revenue/expense accounting beyond model/token costs, materialized rollups.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Cost event validation rejects negative tokens/cost (`server/src/__tests__/costs-service.test.ts`) | Cost event with negative tokens or costCents | 400 INVALID_INPUT rejection |
| TC-2 | Budget service enforces hard limit (`server/src/__tests__/budgets-service.test.ts`) | Spend crossing 100% of monthly budget | Agent paused, invocations blocked, high-priority activity emitted |
| TC-3 | Cost data quality checks (`server/src/__tests__/cost-data-quality.test.ts`) | Ingested cost rows | Quality invariants hold |
| TC-4 | Anthropic receipt pricing (`server/src/services/anthropic-pricing.test.ts`) | Complete usage counters | Conservative priced estimate with rate-card provenance |
| TC-5 | AI connection usage probes (`server/src/services/ai-connection-usage.test.ts`) | Provider rate-limit windows | Percentages preserved, model restrictions separated |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-6 | Cost data quality routes (`server/src/__tests__/cost-data-quality-routes.test.ts`) | Authenticated company context | Quality endpoints return expected payloads |
| TC-7 | Heartbeat cost accounting (`server/src/__tests__/heartbeat-cost-accounting.test.ts`) | Runs with cost receipts | Spend attributed to runs correctly |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| — | No dedicated E2E file found for budget hard-stop | — | — |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-8 | Concurrent ingestion near threshold | Single pause transition, no double-spend or missed pause |
| TC-9 | Budget-paused agent checkout attempt | Checkout rejected |

## Test Infrastructure

- Vitest suite under `server/src/__tests__/` and `server/src/services/`.
- Company/agent fixtures with monthly UTC budget windows.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-1 |
| FR-03 | TC-2 |
| FR-04 | TC-2, TC-9 |
| FR-05 | TC-3, TC-6, TC-7 |
| FR-06 | TC-2 |
| FR-07 | TC-2 |
| FR-08 | TC-6 |

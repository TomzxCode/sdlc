---
title: "Observability"
status: done
---

# Test Plan: Observability

## Scope

Tests covering the observer-hook contract events and correlation, payload sanitization, fail-open behavior, the `/v1/metrics` gateway export, and the Langfuse / NeMo Relay plugin consumers and shared-metrics scripts.

## Test Files

- tests/plugins/test_langfuse_plugin.py — Langfuse plugin trace delivery against the observer contract
- tests/plugins/test_nemo_relay_plugin.py — NeMo Relay plugin trace + shared-metrics delivery
- tests/scripts/test_smoke_nemo_relay_shared_metrics.py — Shared-metrics path smoke test

## Unit Tests

- Observer hook callback registration and invocation for each lifecycle event
- Correlation ID propagation across event types
- Payload sanitization before hook delivery

## Integration Tests

- Langfuse plugin consuming real lifecycle events from an agent turn
- NeMo Relay plugin consuming the contract and the shared-metrics path
- Gateway `/v1/metrics` endpoint emitting runtime gauges

## End-to-End Tests

- A full agent turn with API request + tool call produces a joinable trace through the Langfuse consumer

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| EC-1 | Observer callback raises | Error logged; agent continues unchanged (fail-open) |
| EC-2 | Payload contains secret/token | Value removed before hook delivery |
| EC-3 | New observer field added | Callbacks accepting `**kwargs` remain compatible |
| EC-4 | Metrics endpoint scraped with no platforms | Gateway + cron gauges present; platform gauges show down/absent, not error |
| EC-5 | /v1/metrics requested without auth (when enabled) | 401 returned |

## Test Infrastructure

- Fake agent/turn fixtures emitting observer events
- Temp HERMES_HOME isolation
- Mock Langfuse / NeMo Relay backends (no live network)

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (lifecycle events) | test_langfuse_plugin.py, test_nemo_relay_plugin.py |
| FR-2 (correlation IDs) | test_langfuse_plugin.py |
| FR-3 (sanitization) | test_langfuse_plugin.py, test_nemo_relay_plugin.py |
| FR-4 (fail-open) | test_langfuse_plugin.py |
| FR-5 (/v1/metrics) | test_smoke_nemo_relay_shared_metrics.py |
| FR-6 (Langfuse plugin) | test_langfuse_plugin.py |
| FR-7 (NeMo Relay plugin) | test_nemo_relay_plugin.py |
| FR-9 (shared metrics scripts) | test_smoke_nemo_relay_shared_metrics.py |
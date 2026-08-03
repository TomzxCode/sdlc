---
title: "Observability"
status: done
---

# Specification: Observability

## Overview

Observability is delivered through three cooperating mechanisms: (1) the observer-hook contract, which plugins use to reconstruct execution; (2) a Prometheus-format `/v1/metrics` HTTP export for gateway runtime health; and (3) the Langfuse and NeMo Relay plugins plus shared-metrics scripts that consume both. The contract is backend-neutral and versioned, so any vendor can integrate without core changes.

## Architecture

```
Agent / Gateway runtime
    │  emits lifecycle events (session, LLM, API, tool, approval, subagent)
    v
Observer hook contract (docs/observability/README.md)
    │  correlation IDs · sanitized payloads · timing/status/error · hermes.observer.v1
    │
    ├──► plugins/observability/langfuse/  (traces)
    ├──► plugins/observability/nemo_relay/ (traces + shared metrics)
    │
Gateway runtime health
    │  /v1/metrics (Prometheus text format)
    v
scripts/observability/ (OpenTelemetry-style capture collectors, health export probe)
```

## Data Models

### Observer lifecycle events

| Event | Scope | Key fields |
|---|---|---|
| session_start / session_end | session | session_id, platform, profile |
| turn_llm | turn | turn_id, model, tokens, latency |
| pre_api_request / post_api_request / api_request_error | api_request | api_request_id, provider, status, duration |
| pre_tool_call / post_tool_call | tool | tool_name, status, result, duration |
| approval | — | action, decision |
| subagent | — | subagent_id, goal, status |

Every event carries correlation IDs (session/turn/task/api_request), a timestamp, status, timing, and sanitized payload. Callbacks accept `**kwargs` so new fields are additive and backward-compatible.

### Gateway metrics (/v1/metrics)

| Metric | Type | Description |
|---|---|---|
| gateway up/degraded | gauge | Gateway runtime state |
| platform up/degraded | gauge | Per-platform adapter health |
| cron scheduler | gauge | Scheduler heartbeat / job state |

## API Contracts

### GET /v1/metrics

**Response (200 OK):** Prometheus text format (content-type `text/plain`). Body lists gateway gauges, per-platform up/degraded gauges, and cron scheduler gauges.

**Error Responses:** 401 when the metrics endpoint requires auth; otherwise standard HTTP errors.

## Sequences

### Plugin trace flow
```
Agent turn
    → pre_api_request hook (api_request_id generated)
    → post_api_request hook (status, duration, sanitized body)
    → pre_tool_call / post_tool_call hooks
    → Langfuse / NeMo Relay plugin serializes to its backend
    → correlation ids join all events into one trace
```

### Gateway metrics scrape
```
Prometheus (or operator)
    → GET /v1/metrics
    → gateway emits runtime gauges
    → platform adapters report up/degraded
    → cron scheduler reports heartbeat
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Hook registration | `ctx.register_hook(event, callback)` in `register(ctx)` | Reuses the existing plugin surface, no new core mechanism |
| Backend-neutrality | Contract, not bindings | Any vendor integrates; no vendor baked into core |
| Sanitization | Before hooks fire | Secrets never leave the process |
| Fail-open | Exceptions caught and logged | A broken observer plugin cannot break the agent |
| Correlation | session/turn/task/api_request ids | Cross-event joins for trace reconstruction |
| Metrics export | Prometheus text format on /v1/metrics | Standard scrape protocol, zero dependency |

## Risks and Unknowns

1. Payload sanitization must keep up with new sensitive fields (secrets, tokens, PII)
2. OpenTelemetry-style collectors are scripts, not a maintained core integration — coverage may lag
3. `/v1/metrics` authentication posture (who may scrape) is deployment-dependent

## Out of Scope

- A built-in metrics database or dashboard UI (Langfuse/NeMo Relay/collectors fill this role)
- Behavior-changing instrumentation (observers report, they do not modify)
- Any single-vendor binding in the core tree

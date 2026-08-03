---
title: "Observability"
status: done
---

# Requirements: Observability

## Overview

Hermes provides a backend-neutral observability layer that lets plugins reconstruct agent execution without changing runtime behavior. A documented observer-hook contract (`docs/observability/`) exposes stable lifecycle events with correlation IDs, sanitized payloads, timing, status, and error fields. Consumers include the Langfuse and NeMo Relay plugins, plus a Prometheus-format `/v1/metrics` export for gateway runtime health and a first-party NeMo Relay shared-metrics path that requires no plugin.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operators | Monitor gateway health, platform up/down state, cron scheduler health, and agent execution traces |
| Plugin developers | Build trace/metric/audit/replay/export integrations (Langfuse, OpenTelemetry-style collectors, NeMo Relay) |
| Core maintainers | Keep observability backend-neutral so no single vendor is baked into the core |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall expose observer hooks covering session, turn-scoped LLM, request-scoped API (pre/post/error), tool lifecycle, approval, and subagent lifecycle events |
| FR-2 | Must | Hook callbacks shall receive correlation IDs (session/turn/task/api_request) so events can be joined across a request |
| FR-3 | Must | Hook payloads shall be sanitized before delivery to remove sensitive data |
| FR-4 | Must | Hooks shall be fail-open: a failing callback must not change runtime behavior or crash the agent |
| FR-5 | Must | The gateway shall export a Prometheus-format `/v1/metrics` endpoint with gateway, platform, and cron scheduler gauges |
| FR-6 | Must | The Langfuse plugin shall consume the observer contract to deliver traces |
| FR-7 | Must | The NeMo Relay plugin shall consume the observer contract and shared-metrics path |
| FR-8 | Should | The telemetry schema shall be versioned (`hermes.observer.v1`) for forward compatibility |
| FR-9 | Should | Scripts/collectors under scripts/observability/ shall support OpenTelemetry-style capture |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Safety | Observability must be read-only: it must not replace provider requests, tool arguments, or execution callbacks |
| NFR-2 | Must | Reliability | Observer callbacks must never block the agent's hot path (fail-open, no exceptions propagate) |
| NFR-3 | Must | Privacy | Payloads must be sanitized so secrets and personal data are not exported |
| NFR-4 | Should | Compatibility | Adding observer fields must remain backward-compatible (callbacks accept `**kwargs`) |

## Constraints

- Observer hooks are read-only and must not alter planner, provider, memory, tool, approval, CLI, gateway, or execution semantics
- Behavior-changing wrappers are outside the observer contract
- Payload sanitization happens before hooks fire

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** an agent turn with tool calls and an API request
    - **When** the observer contract is active
    - **Then** session, LLM, API, and tool lifecycle events are emitted with status and timing
- [ ] **FR-2**
    - **Given** events from one agent turn
    - **When** events are inspected
    - **Then** they share a correlation id (turn/task/api_request) that joins them
- [ ] **FR-3**
    - **Given** a tool call that includes a secret value
    - **When** the pre/post tool hook fires
    - **Then** the payload contains no secret value
- [ ] **FR-4**
    - **Given** a plugin callback that raises
    - **When** the hook fires
    - **Then** the error is logged and the agent continues unchanged
- [ ] **FR-5**
    - **Given** a running gateway
    - **When** `/v1/metrics` is scraped
    - **Then** gateway, platform, and cron scheduler gauges are present

## Conflicts

None identified yet.

## Open Questions

1. Should the first-party shared-metrics path be gated behind an opt-in config key, or is it acceptable as always-on for gateway operators?

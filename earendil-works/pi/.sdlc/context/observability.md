# Observability

<!--
This file inventories the project's existing observability infrastructure: metrics,
logging, tracing, and alerting.
There is no deployed monitoring stack in this repository.
The only observability infrastructure is the in-code tracing contracts in packages/telemetry.
Service-level targets do not exist because service-levels.md is absent.
Update this file when the monitoring stack changes.
-->

## Monitoring pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | None | Not configured |
| Logging | None | Not configured |
| Tracing | pi-telemetry contracts only, no backend or exporter | In-code contracts only |
| Profiling | None | Not configured |

## Instrumentation libraries

| Library | Pillar | Configuration |
|---|---|---|
| @earendil-works/pi-telemetry | Tracing (contracts) | TelemetryContext.startSpan callback contract with TelemetrySpan addEvent, setAttributes, and setStatus; NOOP_TELEMETRY_CONTEXT plus InMemoryTelemetryContext reference adapter; typed span, event, and attribute schema utilities with testing conformance suite; no sampler, no exporter, and no backend binding |

## Log aggregation

- No log aggregation destination is configured.
- No structured logging library was found in packages/*/src.
- No retention, sampling, or filtering policy exists.

## Tracing

- No trace backend is configured.
- No sampling strategy is defined.
- No propagation format (W3C Trace Context, B3, or other) is configured.
- No exporter or global current-span state exists in pi-telemetry by design.
- Span emission is limited to explicit TelemetryContext passing in code plus process-local in-memory capture for tests and diagnostics.

## Alerting

- No alert rules are defined.
- No alert routing or on-call target exists.

| Alert | Source | Routing | Severity |
|---|---|---|---|
| None | None | None | None |

## Dashboards

- No dashboards exist.

| Dashboard | Location | Purpose |
|---|---|---|
| None | None | None |

## SLO reference

- No service-level objectives, indicators, or error budgets exist.
- service-levels.md is absent from .sdlc/context/.
- Feature-level observability plans have no SLO targets to reference.

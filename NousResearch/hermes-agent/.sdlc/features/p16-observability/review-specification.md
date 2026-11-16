---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: specification

## Sync drift: 2026-11-16

The following specification details contradict the current code. Each item is new and not recorded in an earlier sync drift section.

- The Architecture diagram points to `docs/observability/README.md`, `plugins/observability/langfuse/`, and `plugins/observability/nemo_relay/`. None of these paths exist. The contract docs are at `website/docs/developer-guide/observer-hooks.md`, Langfuse is an external catalog plugin, and NeMo Relay shared metrics are a first-party path in `hermes_cli/observability/`.
- The Architecture, API Contracts, and Technical Decisions sections describe `GET /v1/metrics` as a gateway-served Prometheus text endpoint. The API Contracts section claims a 200 `text/plain` body and 401 when auth is required, and the Technical Decisions table says "Prometheus text format on /v1/metrics, zero dependency". The code pushes OTLP protobuf metrics to a remote collector instead. `agent/monitoring/gateway_health_export.py:207-227` uses an `OTLPMetricExporter` and a `MeterProvider`, and `agent/monitoring/otlp_exporter.py:99` lists `/v1/metrics` as an OTLP signal suffix. No gateway HTTP route serves `/v1/metrics`, and no Prometheus text response or 401 scrape path exists. `scripts/observability/gateway_health_export_probe.py:83-88` only checks that the exporter POSTed to a remote collector.
- The "Observer lifecycle events" table lists event names `session_start/session_end`, `turn_llm`, `approval`, and `subagent`. The implemented hooks use `on_session_start`/`on_session_end`, `pre_llm_call`/`post_llm_call`, `pre_approval_request`/`post_approval_response`, and `subagent_start`/`subagent_stop` (`website/docs/developer-guide/observer-hooks.md:96-248`). There is no `turn_llm` hook.

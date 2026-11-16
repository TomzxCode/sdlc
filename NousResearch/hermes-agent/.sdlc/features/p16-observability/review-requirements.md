---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: requirements

## Sync drift: 2026-11-16

The following requirements contradict the current code. Each item is new and not recorded in an earlier sync drift section.

- FR-5 and the Overview claim the gateway exports a Prometheus-format `/v1/metrics` HTTP endpoint with gateway, platform, and cron gauges. The code does not serve a scrapeable Prometheus text endpoint. `agent/monitoring/gateway_health_export.py:207-227` builds an OTLP `MeterProvider` with an `OTLPMetricExporter`, and `agent/monitoring/otlp_exporter.py:99` treats `/v1/metrics` as a remote OTLP signal path. No gateway HTTP route handles `/v1/metrics`, and no Prometheus `text/plain` response or 401-gated scrape exists. The exported metrics are OTLP gauges such as `hermes.gateway.up`, `hermes.platform.up`, `hermes.platform.degraded`, and `hermes.cron.scheduler.*` (`gateway_health_export.py:48-53`).
- The Overview and FR-6 name a Langfuse plugin under `plugins/observability/` that consumes the observer contract. No `plugins/observability/` directory exists. Langfuse left core and is now an external catalog plugin installed with `hermes plugins install langfuse` (`hermes_cli/left_core_migration.py:266`, `plugin-catalog/langfuse.yaml`, `website/docs/user-guide/features/built-in-plugins.md:144`).
- FR-7 names a NeMo Relay plugin that consumes the observer contract and the shared-metrics path. NeMo Relay shared metrics are implemented as a first-party path in `hermes_cli/observability/` (`shared_metrics_contract.py`, `relay_shared_metrics.py`), not as an observer plugin.
- The Overview says the observer contract is documented at `docs/observability/`. That path does not exist. The contract is documented at `website/docs/developer-guide/observer-hooks.md`.
- NFR-1 says observability must not replace provider requests, tool arguments, or execution callbacks. The implemented plugin hook contract includes behavior-affecting hooks that do replace them: `pre_tool_call` can block or modify args, `pre_llm_call` can block or inject context, and `transform_tool_result` and `transform_llm_output` replace outputs (`website/docs/developer-guide/observer-hooks.md:60-68`). The requirements treat these wrappers as outside the contract, but NFR-1 is written as an absolute.

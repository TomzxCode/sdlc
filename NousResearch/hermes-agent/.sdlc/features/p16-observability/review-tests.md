---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: tests

## Sync drift: 2026-11-16

The following test plan details contradict the current code. Each item is new and not recorded in an earlier sync drift section.

- The Test Files section lists `tests/plugins/test_langfuse_plugin.py` and `tests/plugins/test_nemo_relay_plugin.py`. Neither file exists. Langfuse is an external catalog plugin, and NeMo Relay coverage lives in `tests/monitoring/` and `tests/scripts/`, not in a `tests/plugins/` pair.
- The Coverage Matrix maps FR-5 (`/v1/metrics`) to `tests/scripts/test_smoke_nemo_relay_shared_metrics.py`. That file tests NeMo Relay shared-metrics contract expectations, not gateway `/v1/metrics` gauges. The `/v1/metrics` export path is exercised in `tests/monitoring/test_gateway_health_export.py`, which asserts the OTLP request path, not a Prometheus scrape.

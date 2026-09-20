<!-- session_link: manual creation from codebase signals, 2026-09-20 -->
# Observability

<!--
This file inventories the project's existing observability infrastructure: metrics,
logging, tracing, and alerting.
Service-level targets (SLOs, SLIs, error budgets) live in service-levels.md.
Update this file when the monitoring stack changes.
-->

## Monitoring Pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | OTLP gateway health export (`agent/monitoring/gateway_health_export.py`) plus NeMo Relay shared-metrics (`hermes_cli/observability/`) | In use (both opt-in, disabled by default) |
| Logging | stdlib `logging` via `hermes_logging.py` plus `hermes logs` CLI (`hermes_cli/logs.py`) | In use |
| Tracing | Backend-neutral plugin observer hooks plus opt-in Langfuse plugin plus OTLP trace export | In use (all tracing egress is opt-in) |
| Profiling | None | Not configured |

## Instrumentation Libraries

| Library | Pillar | Configuration |
|---|---|---|
| `opentelemetry-sdk==1.39.1`, `opentelemetry-exporter-otlp-proto-http==1.39.1` | Metrics, logs, traces | Optional `hermes-agent[otlp]` extra, lazy-installed via `tools/lazy_deps.py` feature `export.otlp`, endpoint `monitoring.export.otlp.endpoint`, signals `/v1/traces`, `/v1/metrics`, `/v1/logs` |
| stdlib `logging` | Logging | `RedactingFormatter` from `agent/redact.py`, async `QueueListener` queue, per-thread `session_tag`, noisy third-party loggers pinned to WARNING |
| NeMo Relay (`nemo-relay>=0.8.3,<0.9`, `agent/relay_runtime.py`) | Metrics | Bounded shared-metrics Relay subscriber (`hermes.nemo_relay.shared_metrics`), opt-in send consent, local SQLite store |
| `langfuse` SDK (lazy `pip install langfuse`, unpinned) | Tracing | Opt-in bundled plugin `observability/langfuse`, requires `HERMES_LANGFUSE_PUBLIC_KEY` and `HERMES_LANGFUSE_SECRET_KEY` |

## Log Aggregation

Logs are local files under `$HERMES_HOME/logs/` (profile-aware via `get_hermes_home()`), with no central aggregator shipped.
`agent.log` carries INFO and above at 5 MiB rotation with 3 backups.
`errors.log` carries WARNING and above at 2 MiB rotation with 2 backups.
`gateway.log` carries gateway-component records in gateway mode and `gui.log` carries dashboard and TUI-gateway records.
`hermes logs` views and filters these files by name, level, session ID, component prefix, and relative time.
Rotation sizes, backup counts, and level come from `config.yaml` `logging.*` with the above as defaults.
Multiplexed processes route each record to its owning profile home via `_ProfileRoutingFileHandler`.
Windows uses `concurrent-log-handler` for cross-process rotation locking while POSIX uses stdlib `RotatingFileHandler`.

## Tracing

Trace producers are backend-neutral plugin observer hooks (`pre_llm_call`, `post_llm_call`, `pre_tool_call`, `post_tool_call`, `on_stream_start`, `on_stream_delta`, `on_stream_end`, `on_session_start`, `on_session_end`, `on_session_finalize`, `subagent_start`, `subagent_stop`).
Stream observers run per-consumer on bounded daemon-worker queues that drop the oldest event when full.
The bundled `plugins/observability/langfuse` plugin traces conversations, LLM calls, tool usage, and subagents to Cloud or self-hosted Langfuse.
The OTLP exporter (`agent/monitoring/otlp_exporter.py`) maps gateway monitoring events to OTel spans, metrics, and logs with redaction before egress.
There is no in-repo trace-propagation format or sampler configuration beyond the OTLP exporter's bounded resource attributes.
No `structlog`, `prometheus-client`, or `sentry-sdk` is used in production code.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| No in-repo alert rules ship | Not applicable | Operator-owned OTLP collector | Not applicable |

There is no in-repo alerting, so this is a self-hosted concern for operators.
Operators consume `hermes.gateway.*`, `hermes.platform.*`, and `hermes.cron.*` gauges from `gateway_health_export` in their own collector.
The gateway loop watchdog hard-exits wedged processes so systemd or launchd revives them, which is supervision rather than alerting.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| No in-repo dashboards ship | Not applicable | Operators build views on their OTLP collector; local inspection uses `hermes logs` and gateway status |

Smoke coverage lives in `scripts/observability/` (`otel_capture_collector.py` plus `gateway_health_export_probe.py` asserting `/v1/metrics` traffic).
Shared-metrics local history lives in `~/.hermes/telemetry/shared_metrics/metrics.sqlite3` with 30-day retention.

## SLO Reference

There is no `service-levels.md` yet, so no SLOs, SLIs, or error budgets are referenced here.

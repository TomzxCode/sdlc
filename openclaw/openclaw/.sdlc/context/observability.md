# Observability

<!--
This file inventories the existing observability infrastructure for OpenClaw: metrics, logging, tracing, and alerting.
It gives feature work a starting point without grepping the codebase each time.
Service-level targets are not defined yet; see SLO Reference below.
Update this file when the monitoring stack changes.
-->

## Monitoring Pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | diagnostics-prometheus plugin (pull) plus diagnostics-otel OTLP/HTTP export (push) | In use (both are opt-in plugins) |
| Logging | tslog-based structured logger with JSONL rolling files, plus diagnostics-otel stdout JSONL sink | In use |
| Tracing | diagnostics-otel OTLP/HTTP trace export to any OTLP backend | In use (opt-in plugin) |
| Profiling | On-demand diagnostic snapshots (CPU, heap, GC, memory) in src/logging | In use (on-demand only, no continuous profiler) |

## Instrumentation Libraries

| Library | Pillar | Configuration |
|---|---|---|
| tslog (via src/logging/logger.ts) | Logging | Console plus JSONL file transport, level from logging.level with OPENCLAW log-level env override, secret redaction on every record |
| In-process diagnostic event bus (src/infra/diagnostic-events.ts, openclaw/plugin-sdk/diagnostic-runtime) | Metrics, traces, logs | Gateway and bundled plugins emit structured diagnostic events, exporters subscribe only when diagnostics and the plugin are enabled |
| @opentelemetry SDK 2.11.0 plus OTLP proto exporters (@openclaw/diagnostics-otel) | Tracing, metrics, logs | OTLP/HTTP protobuf push to diagnostics.otel.endpoint (example http://otel-collector:4318), per-signal endpoint overrides, protocol http/protobuf only, traces default on with metrics and opt-in logs |
| diagnostics-prometheus in-process store (@openclaw/diagnostics-prometheus) | Metrics | Prometheus text exposition at GET /api/diagnostics/prometheus on the Gateway HTTP port, gateway auth with operator.read scope, 2048 series cap with openclaw_prometheus_series_dropped_total overflow counter |
| sentry-sdk or equivalent error tracker | Errors | Not configured (no sentry, datadog, or similar references in package.json or src) |

## Log Aggregation

| Aspect | Value |
|---|---|
| Destination | Local rolling JSONL files only, no central ELK, Loki, or CloudWatch aggregator is shipped |
| File location | /tmp/openclaw/openclaw-YYYY-MM-DD.log by default, profile variants use openclaw-profile-YYYY-MM-DD.log, with OS-tmpdir fallback when the directory is unsafe |
| Retention and rotation | Active file rotates at logging.maxFileBytes (default 100 MB), up to five numbered archives are kept |
| Structured format | One JSON object per line, subsystem file logs omit call-site metadata below error level unless diagnostics are enabled with a consumer subscribed |
| Sampling and filtering | No sampling, secret redaction applies to messages, fields, and error stacks, verbose-only details require logging.level debug or trace |
| Tailing surfaces | Gateway logs.tail API, openclaw logs --follow CLI, and the Control UI Logs tab all tail the same file |
| Container pipeline option | diagnostics-otel logsExporter stdout or both mirrors log records as stdout JSONL for platform log shippers |
| Operator bundles | docs/gateway/diagnostics.md describes the separate operator support-bundle export (diagnostic-support-bundle.ts, diagnostic-stability-bundle.ts) for redacted troubleshooting archives |

## Tracing

| Aspect | Value |
|---|---|
| Backend | Any OTLP/HTTP backend (Grafana Tempo, Datadog, Honeycomb, New Relic, or a local collector), no backend is bundled |
| Export format | OTLP/HTTP protobuf only, other protocols disable the affected signal with a plugin warning |
| Sampling | diagnostics.otel.sampleRate drives a TraceIdRatioBasedSampler, otherwise OTEL_TRACES_SAMPLER and OTEL_TRACES_SAMPLER_ARG apply |
| Propagation | W3C tracecontext plus baggage by default, OTEL_PROPAGATORS can select b3, b3multi, or jaeger (deprecated), or none to disable |
| Provider header | Provider calls receive a W3C traceparent header from the live model-call span when the transport accepts custom headers |
| Emitting services | Gateway processes export at startup when configured, one-shot openclaw agent runs export via src/plugins/one-shot-diagnostics.ts (OTel only, Prometheus stays gateway-only) |
| Span coverage | Model calls, Gateway RPC, message flow, sessions, queues, exec, harness lifecycle, tool execution, event-loop windows, and exporter health, with exact names in docs/gateway/opentelemetry |
| Privacy | Session, chat, message, run, call, tool-call, and trace IDs are dropped from OTLP attributes, log bodies and GenAI content export only when diagnostics.otel.captureContent is true |
| Flush behavior | Metrics use a periodic exporting reader (diagnostics.otel.flushIntervalMs or OTEL_METRIC_EXPORT_INTERVAL), one-shot CLI runs drain 5 seconds and force-flush 10 seconds before exit |
| Verification | pnpm qa:otel:smoke runs the in-process OTLP receiver smoke (test/e2e/qa-lab/runtime/qa-otel-smoke-runtime.ts), pnpm qa:otel:smoke repeats against a real otel/opentelemetry-collector:0.159.0 Docker container |

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| None shipped | Not configured | Operator-owned backend rules | Not configured |

- No Prometheus rules, CloudWatch alarms, or PagerDuty routes are defined in this repository.
- Exporter health facts (extensions/diagnostics-otel/src/service-exporter-health.ts) and openclaw doctor checks (src/flows/bundled-health-checks.ts, src/flows/doctor-lint-flow.ts) surface failures in logs and CLI output instead of paging.
- Operators build alerts in their own Prometheus or OTLP backend from the metric catalog in docs/gateway/prometheus.md and docs/gateway/opentelemetry/model-calls-and-metrics.md.
- Smoke coverage for the export path is pnpm qa:observability:smoke (OTel plus Prometheus) and pnpm qa:observability:collector-smoke (Docker collector plus Prometheus).

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| None shipped | Not configured, build from docs/gateway/opentelemetry/model-calls-and-metrics.md and docs/gateway/prometheus.md | Latency, error rate, throughput, model usage, queue and session health |

- No Grafana JSON or hosted dashboard URLs exist in the repository.
- Histogram bucket layouts are frozen for dashboard stability (agent durations through one hour, context tokens through two million, Prometheus duration, token, byte, and ratio buckets in extensions/diagnostics-prometheus/src/service.ts).

## SLO Reference

- Service-level objectives, indicators, and error budgets are not defined in this repository.
- .sdlc/context/service-levels.md does not exist, so there is nothing to reference yet.
- Feature-level observability plans should reuse the existing metric, span, and log catalog above and record any new SLO proposal alongside the feature.

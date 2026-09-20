# Observability

## Monitoring pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | Honeycomb triggers over completion and LLM error events (see alerting) | In use |
| Logging | Effect Logger to local file, optional OTLP log export | In use |
| Tracing | OpenTelemetry OTLP HTTP export via Effect NodeSdk | In use (opt in by endpoint) |
| Profiling | No profiler integration was found | Not configured |
| Errors | Sentry in web app and desktop shell | In use |

## Instrumentation libraries

| Library | Pillar | Configuration |
|---|---|---|
| `@effect/opentelemetry` plus `@opentelemetry/api`, `@opentelemetry/context-async-hooks`, `@opentelemetry/exporter-trace-otlp-http`, `@opentelemetry/sdk-trace-base` (and `sdk-trace-node` in `packages/opencode`) | Tracing | `packages/core/src/observability/otlp.ts`, active only when an OTLP endpoint flag is set |
| Effect `Logger` with structured formatter in `packages/core/src/observability/logging.ts` | Logging | File logger to `opencode.log`, stderr gated by env, OTLP log export gated by endpoint |
| `@sentry/solid` in `packages/app` and `packages/desktop` | Errors | Initialized in `packages/app/src/entry.tsx` when `VITE_SENTRY_DSN` is set |

## Log aggregation

- Structured logs use Effect Logger with a custom logfmt style formatter (`key=value` pairs).
- Each line includes timestamp, level, run id, message fields, cause, spans, and annotations.
- Default destination is a local append file at the global log path (`opencode.log`).
- Stderr output is added only when `OPENCODE_PRINT_LOGS` equals `1`.
- Minimum level comes from `OPENCODE_LOG_LEVEL` (`DEBUG`, `INFO`, `WARN`, `ERROR`) and defaults to `INFO`.
- When an OTLP endpoint is configured, logs are also exported via `OtlpLogger` to `{endpoint}/v1/logs`.
- No central log aggregation backend or retention policy was conclusively determined from the repo.

## Tracing

- Backend is any OTLP HTTP receiver configured through `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Headers come from `OTEL_EXPORTER_OTLP_HEADERS` as comma separated `key=value` pairs.
- Resource reports service name `opencode` with service version from the installation version.
- Resource attributes include `deployment.environment.name`, `opencode.client`, `opencode.run`, `service.instance.id`, plus parsed `OTEL_RESOURCE_ATTRIBUTES`.
- Span export uses `BatchSpanProcessor` with `OTLPTraceExporter` to `{endpoint}/v1/traces`.
- Setup registers `AsyncLocalStorageContextManager` as the global context manager so AI SDK spans parent correctly.
- Tracing layers are empty when no endpoint is set, so local runs emit no remote spans.
- LLM calls in `packages/opencode/src/session/llm.ts` attach tracing only when `experimental.openTelemetry` is enabled.
- The LLM path resolves the optional `OtelTracer` service and wraps `startSpan` to add a `session.id` attribute.
- Agent generation in `packages/opencode/src/agent/agent.ts` forwards the same experimental OpenTelemetry tracer option.
- Named Effect spans cover operations such as `Session.updateMessage`, `Session.updatePart`, `Tool.execute`, and `GlobalHttpApi.health`.
- Sampling strategy and propagation format were not conclusively determined from the repo.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| Increased model HTTP errors Go | Honeycomb trigger in `infra/monitoring.ts` | Discord webhook recipient | Note: severity is not labeled in code |
| Increased model HTTP errors Zen | Honeycomb trigger in `infra/monitoring.ts` | Discord webhook recipient | Note: severity is not labeled in code |
| Low model TPS Go | Honeycomb trigger in `infra/monitoring.ts` | Discord webhook recipient | Note: severity is not labeled in code |
| Low model TPS Zen | Honeycomb trigger in `infra/monitoring.ts` | Discord webhook recipient | Note: severity is not labeled in code |
| Increased provider HTTP errors | Honeycomb trigger in `infra/monitoring.ts` | Discord webhook recipient | Note: severity is not labeled in code |
| Increased free tier requests | Honeycomb trigger in `infra/monitoring.ts` | Discord webhook recipient | Note: severity is not labeled in code |

- Alert rules are defined in `infra/monitoring.ts` using the Honeycomb provider.
- Notifications route through a `DiscordAlerts` webhook recipient posting to `https://{domain}/honeycomb/webhook`.
- All triggers are disabled when the SST stage is not production.
- Model error triggers fire when the failed share of completions reaches 0.7 with at least 150 events in a 15 minute window.
- Failed model status excludes 401 and usage limit 429s for `GoUsageLimitError` and `FreeUsageLimitError`.
- Low TPS triggers fire when P50 output tokens per second is at or below 10 with at least 100 completions in a 30 minute window.
- Provider error triggers compare `llm.error` events against successful completions with a 0.7 threshold.
- Free tier trigger watches hourly completion counts with a day ago percentage baseline.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| Honeycomb query datasets backing the triggers | Honeycomb account backing `infra/monitoring.ts` | Model error ratio, provider error ratio, output throughput, free tier volume |

- Dashboard URLs and ownership were not conclusively determined from the repo.

## Health endpoints

- `GET /global/health` exists in the instance HTTP API and returns healthy status plus server version.
- No `/ready` or `/ping` endpoint was found.
- No dedicated readiness versus liveness split was found.

## Error tracking

- Sentry covers the web frontend and desktop shell through `@sentry/solid`.
- `packages/app/src/entry.tsx` initializes Sentry only when `VITE_SENTRY_DSN` is present.
- Sentry environment defaults to `VITE_SENTRY_ENVIRONMENT` or Vite mode, and release defaults to the web package version.
- The web scope tags events with platform `web`.
- `packages/app/src/app.tsx` reports caught errors with `Sentry.captureException`.
- `packages/app/src/pages/error.tsx` reports page errors behind a `Sentry.isEnabled` guard.
- No server side Sentry DSN was found in the checked core and server paths.

## Product analytics

- No third party product analytics SDK was found (no Amplitude, Mixpanel, PostHog, or Segment dependency).
- Usage statistics use the first party `packages/stats` service (`app`, `core`, `server`).
- Direct telemetry questions at the stats service.
- An event taxonomy was not inventoried here and should not be assumed.

## SLO reference

- There is no `.sdlc/context/service-levels.md` yet, so SLOs are not formally defined.
- Treat the Honeycomb trigger thresholds in `infra/monitoring.ts` as operational alerts, not as agreed SLOs.

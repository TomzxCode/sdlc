<!-- session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA -->
# Observability

This file inventories the observability setup in this checkout.
It covers logging, tracing, error tracking, metrics instrumentation, health probing, alerting, and dashboards.
Update it when the monitoring stack changes.

## Monitoring pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | Effect Metrics counters in core, no metrics exporter or backend configured | Instrumented in process |
| Logging | Effect Logger with local file output and optional OTLP log export | In use |
| Tracing | Effect spans exported through OpenTelemetry OTLP HTTP | In use, opt in by endpoint |
| Profiling | No profiler integration found | Not configured |
| Errors | Sentry in the web app and desktop renderer | In use when a DSN is configured |

## Instrumentation libraries

| Library | Pillar | Configuration |
|---|---|---|
| Effect Logger in `packages/util/src/observability/logging.ts` | Logging | Logfmt file logger with hourly compaction, stderr gated by `OPENCODE_PRINT_LOGS`, minimum level from `OPENCODE_LOG_LEVEL` |
| `OtlpLogger` from `effect/observability`, wired in `packages/util/src/observability.ts` | Logging | Exports to `{endpoint}/v1/logs` when an OTLP endpoint is configured |
| `@effect/opentelemetry`, `@opentelemetry/api`, `@opentelemetry/context-async-hooks`, `@opentelemetry/exporter-trace-otlp-http`, `@opentelemetry/sdk-trace-base` | Tracing | NodeSdk layer in `packages/util/src/observability/otlp.ts` uses `BatchSpanProcessor` and `OTLPTraceExporter` with endpoint and headers from environment variables |
| `@opentelemetry/api-logs`, `@opentelemetry/sdk-logs`, `@opentelemetry/sdk-metrics`, `@opentelemetry/sdk-trace-node`, `@opentelemetry/resources` | Tracing, metrics | Declared in `packages/util/package.json`; no direct imports in the util source in this checkout |
| Effect `Metric` | Metrics | `opencode_session_websocket_events_total` counter in `packages/core/src/session/model-transport.ts`; no reader or exporter configured |
| `@sentry/solid` in `packages/app` and `packages/desktop` | Errors | Initialized in the web entry and desktop renderer startup when `VITE_SENTRY_DSN` is set |
| `@sentry/vite-plugin` in `packages/app` | Errors, build | Uploads source maps when `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, and `SENTRY_PROJECT` are set, then deletes uploaded maps |

## Log aggregation

- Structured logs use Effect Logger with a logfmt style formatter in `packages/util/src/observability/logging.ts`.
- Each line includes timestamp, level, run id, message fields, cause, spans, and annotations.
- The default destination is `Global.Path.log/opencode-local.log` for the local channel and `Global.Path.log/opencode.log` for other channels.
- Log files are append only and shared across processes.
- Logs are compacted in place every hour once they pass 50 MiB, keeping roughly 25 MiB rounded forward to a line boundary.
- Stderr output is added only when `OPENCODE_PRINT_LOGS` is `1`, which `--print-logs` sets in `packages/cli/src/framework/runtime.ts`.
- Minimum level comes from `OPENCODE_LOG_LEVEL` (`DEBUG`, `INFO`, `WARN`, `ERROR`) and defaults to `INFO`.
- When an OTLP endpoint is configured, logs are also exported via `OtlpLogger` to `{endpoint}/v1/logs`.
- `Observability.layer` falls back to local-only logging if OTLP setup fails.
- No central log aggregation backend or retention policy is defined in this checkout.
- An external OTLP receiver would own retention if one were configured.

## Tracing

- Backend is any OTLP HTTP receiver configured through `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Headers come from `OTEL_EXPORTER_OTLP_HEADERS` as comma separated `key=value` pairs.
- Resource reports service name `opencode`, service version from the app options, and attributes `deployment.environment.name`, `opencode.client`, `opencode.run`, `service.instance.id`, plus parsed `OTEL_RESOURCE_ATTRIBUTES`.
- The CLI passes `OPENCODE_VERSION`, `OPENCODE_CLIENT`, and `OPENCODE_CHANNEL` into those options in `packages/cli/src/index.ts`.
- Span export uses `BatchSpanProcessor` with `OTLPTraceExporter` to `{endpoint}/v1/traces`.
- Setup registers `AsyncLocalStorageContextManager` as the global context manager so AI SDK spans parent correctly.
- Tracing layers are empty when no endpoint is set, so local runs emit no remote spans.
- Named Effect spans cover operations such as `SessionModelTransport.connect`, `SessionModelTransport.send`, `Plugin.load`, and session state updates.
- The server drops the parent span when building request handlers so each request starts its own trace, see `packages/server/src/request-tracing.ts`.
- Sampling strategy, propagation format, and a hosted trace backend are not configured in this checkout.

## Alerting

- No alert rules, alert sources, routing rules, or on-call configuration were found in this checkout.
- Older context referenced `infra/monitoring.ts`, but there is no `infra/` directory here, so those trigger details are not verifiable.
- CI workflows under `.github/workflows/` build, test, and release the project; they do not define monitoring alerts.
- `packages/data/core/src/honeycomb-backfill.ts` prints Honeycomb query definitions and imports downloaded CSV results into the first party stats database.
- Those queries are reporting inputs, not alerts.

## Dashboards

- No operational dashboard definitions or dashboard URLs were found in this checkout.
- `packages/data/app` and `services/data` render first party usage statistics from the stats database.
- They are product reporting surfaces, not operations dashboards.

## Health endpoints

- No dedicated `/health`, `/ready`, or `/ping` endpoint was found in `packages/server/src` or `packages/protocol/src`.
- The server reports startup state as `starting`, `ready`, `stopping`, or `failed` in `packages/server/src/service-status.ts` and gates API traffic until it is ready.
- Clients probe `GET /api/info` for server health, see `packages/app/src/runtime/server/health-machine.ts`.
- `/openapi.json` serves the HTTP contract.
- There is no separate readiness versus liveness split.

## Error tracking

- Sentry covers the web frontend and desktop renderer through `@sentry/solid`.
- `packages/app/src/entry.tsx` initializes Sentry when `VITE_SENTRY_DSN` is set.
- Web environment defaults to `VITE_SENTRY_ENVIRONMENT` or Vite mode, and release defaults to `web@<package version>`.
- The web scope tags events with platform `web` and filters out Breadcrumbs, plus GlobalHandlers on the production channel.
- `packages/app/src/app.tsx` reports caught errors with `Sentry.captureException`.
- `packages/app/src/shell/errors/error.tsx` checks `Sentry.isEnabled` and offers user error reporting through `captureException`.
- `packages/desktop/src/renderer/startup/sentry.ts` initializes Sentry for the renderer with platform tag `desktop` and release `desktop@<version>`, and `index.tsx` calls it without awaiting.
- `.github/workflows/release.yml` supplies `VITE_SENTRY_DSN` and release metadata for desktop builds.
- No server side Sentry DSN or server SDK was found in the checked paths.

## Product analytics

- No third party product analytics SDK was found, with no Amplitude, Mixpanel, PostHog, or Segment dependency.
- No `telemetry.md` is maintained because this checkout defines no analytics platform or event taxonomy.
- Usage statistics use the first party `packages/data` and `services/data` services.
- Do not infer a product event taxonomy from the logging or OTLP setup.

## SLO reference

- `.sdlc/context/service-levels.md` does not exist in this checkout, so no SLOs, SLIs, error budgets, or SLAs are defined in the SDLC context.
- Honeycomb queries in `packages/data/core/src/honeycomb-backfill.ts` are reporting inputs, not service level targets.
- Feature observability plans should state their own indicators and targets until a service levels file is added.

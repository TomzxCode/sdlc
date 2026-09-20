# Observability

## Monitoring Pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | None in repo | Not configured |
| Logging | pino plus pino-http to stdout, no external aggregator | In use |
| Tracing | OpenTelemetry OTLP traces, endpoint-gated | In use (opt-in) |
| Profiling | None in repo | Not configured |
| Error monitoring | Sentry for server and browser, DSN-gated | In use (opt-in) |

## Instrumentation Libraries

| Library | Pillar | Configuration |
|---|---|---|
| pino, pino-http | Logging | JSON in production, pretty-print in development, level via `PAPERCLIP_LOG_LEVEL` (`server/src/middleware/logger.ts:21-41`) |
| @opentelemetry/api | Tracing | Normal server dependency, no-op interface until an SDK registers (`server/package.json:55`) |
| @opentelemetry/sdk-node, auto-instrumentations-node, resources, semantic-conventions, one OTLP exporter | Tracing | Optional peer dependencies at exact pinned versions, dynamically imported only when `OTEL_EXPORTER_OTLP_ENDPOINT` is set (`server/package.json:129-138`, `server/src/instrumentation.ts:304-306`) |
| @sentry/node | Errors | Optional peer dependency pinned to `10.71.0`, loaded only when a backend DSN resolves (`server/package.json:137`, `doc/observability.md:234-244`) |
| @sentry/browser | Errors | UI dev dependency pinned to `10.71.0`, lazy chunk fetched only after an authenticated session returns a DSN (`ui/package.json:77`, `doc/observability.md:261-266`) |

## Log Aggregation

- Server logs go to stdout via pino, as JSON in production and human-readable pretty-print in development.
- HTTP request logs come from pino-http with per-request ids and redacted URLs, query strings, and secret-bearing fields.
- Log level is set with `PAPERCLIP_LOG_LEVEL` and defaults to info in production and debug otherwise.
- Error responses carry a sanitized error context with secrets redacted and private webhook payloads fully omitted.
- Aggregation status is Not configured beyond local stdout logs, with no external aggregator or central retention policy found in the repo.

## Tracing

- Tracing is strictly opt-in and exports traces only, never metrics or logs.
- Setting `OTEL_EXPORTER_OTLP_ENDPOINT` activates the NodeSDK with auto-instrumentation for HTTP, Express, PG, and similar integrations.
- Auto-instrumentations for `fs`, `dns`, and `net` stay disabled because they are too chatty for this workload.
- The export protocol is selected with `OTEL_EXPORTER_OTLP_PROTOCOL` (`grpc` default, `http/protobuf`, `http/json`), each backed by its own exporter peer package.
- Service identity is `OTEL_SERVICE_NAME` (default `paperclip`) plus a `service.version` resolved from the build stamp, then git, then `OTEL_SERVICE_VERSION`, then `"unknown"`.
- Missing or version-mismatched peer packages log one diagnostic and continue without tracing, so observability never breaks control flow.
- Plugin provider spans are parented through hand-minted W3C `traceparent` strings passed on the per-call invocation channel.
- Native Runner task runs emit one foldable trace (schema version 2) rooted at `task.run`, covering preparation, session startup, agent turns, and settlement.
- Sandbox startup spans use the closed `paperclip.sandbox.startup.` attribute prefix with a fixed allowlist and `ok`, `skipped`, or `failed` outcomes (`packages/adapter-utils/src/acpx-engine/startup-timing.ts:48-124`).
- Duplex transport spans (`sandbox.duplex.channel_open`, `sandbox.duplex.request`) bind through an injected recorder whose default is a no-op (`packages/adapter-utils/src/duplex-observability.ts:21-24`, `server/src/services/duplex-observability-recorder.ts:1-23`).
- Sampling note: no explicit sampler is configured in `server/src/instrumentation.ts`, so the effective sampling behavior was not determined from the repo.
- Propagation note: cross-process parenting uses explicit W3C `traceparent` strings, while in-process propagation relies on auto-instrumentation defaults not enumerated from the repo.

## Error monitoring

- Sentry is opt-in per component via `SENTRY_DSN_BACKEND` for the server and `SENTRY_DSN_FRONTEND` for the browser, with legacy `SENTRY_DSN` as fallback for both.
- Server events carry no request data at all (no URL, method, headers, cookies, query, or body) under the shipped configuration.
- Browser events carry no page URL, referrer, user agent, or breadcrumbs, and `sendDefaultPii` is false with `tracesSampleRate` at 0 on both runtimes.
- Failed Sentry imports or init fall through to one diagnostic log line and keep the process running without error monitoring.
- The full capture set is the canonical contract in `doc/observability.md:371-450`, not repeated here.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| None defined in repo | Not configured | Not configured | Not configured |

- No Prometheus rules, CloudWatch alarms, or other alert definitions exist in the repo.
- Sentry-side rate limits and quota alerts are an operator responsibility and are not shipped in the repo.
- Status: Not configured.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| None defined in repo | Not configured | Not configured |

- Status: Not configured.

## SLO Reference

- No `service-levels.md` exists under `.sdlc/context/`, so feature-level observability plans have no local SLO reference yet.

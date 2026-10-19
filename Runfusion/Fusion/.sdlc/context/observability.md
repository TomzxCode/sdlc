# Observability

This file inventories the project's existing observability infrastructure: metrics, logging, tracing, and alerting.
Update it when the monitoring stack changes.

## Monitoring Pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | Usage and credit rows (`usage_events`), chat token accounting (`chat_token_usage`), reliability indicators (`GET /api/health/reliability`), project health (`central.project_health`), Prometheus-text scrape endpoint (`GET /metrics`, RUFU-081), opt-in OTLP/HTTP JSON metrics export (`FUSION_OTEL_METRICS_ENDPOINT`, off by default) | In use (in-app and SQL surfaces plus in-house Prometheus-text and OTLP export; no third-party metrics SDK) |
| Logging | Structured in-app loggers in `@fusion/engine` (`packages/engine/src/logger.ts`) and `@fusion/core` (`packages/core/src/process/logger.ts`), plus diagnostic conventions in `docs/diagnostics.md` | In use |
| Tracing | None (no distributed tracing backend and no trace context propagation) | Not configured |
| Profiling | None | Not configured |
| Run audit | Append-only `run_audit_events` rows for engine and task lifecycle (`docs/run-audit.md`) | In use |
| Activity stream | Durable per-agent activity rows (`agent_activity_events`), read through `GET /api/agent-activity` and live SSE frames (`docs/agent-activity-contract.md`) | In use |
| External signals | Inbound signal connectors (webhook, GitHub, GitLab, Sentry, Datadog, PagerDuty) into the Command Center over signed webhooks | In use (ingest only) |
| Provider health | Daemon-owned provider usage probe that resumes rate-limited providers (`packages/dashboard/src/provider-health-monitor.ts`) | In use |

## Instrumentation Libraries

| Library | Pillar | Configuration |
|---|---|---|
| `@fusion/engine` `createLogger` | Logging | Prefix-scoped structured logger with control-character severity markers and `info`/`warn`/`error` levels (`packages/engine/src/logger.ts`) |
| `@fusion/core` `createLogger` | Logging | Mirrors the engine logger; the dashboard server logs through this one (`packages/core/src/process/logger.ts`) |
| Dashboard `RuntimeLogger` | Logging | Scoped logger with a `child()` sub-scope and a replaceable sink, wrapping the core logger (`packages/dashboard/src/runtime-logger.ts`) |
| Log severity manifest | Logging | Pinned demotions and a no-bare-console rule that fail CI on an accidental severity reversion (`packages/engine/src/__tests__/log-severity-manifest.ts`) |
| Run-audit event rows | Audit | Append-only `project.run_audit_events` with ids, timestamps, and outcomes-only metadata; never prose or secrets (`packages/core/src/run-audit/emit-bounded-run-audit.ts`, `packages/engine/src/run-audit/run-audit-catalogue.ts`) |
| `/api/health/reliability` metrics | Metrics | Reliability indicator aggregation over run-audit and activity rows (`packages/dashboard/src/reliability-metrics.ts`) |
| Signal connectors | External ingest | Signed webhook receivers for webhook, GitHub, GitLab, Sentry, Datadog, and PagerDuty (`packages/dashboard/src/routes/register-signal-routes.ts`, `docs/signals-connectors.md`) |
| `/metrics` sampler and serializer | Metrics | In-house Prometheus-text serializer with runtime and domain samplers and no third-party client library; the public `GET /metrics` route is served synchronously from a pre-read snapshot (`packages/dashboard/src/metrics/`, mounted in `packages/dashboard/src/server.ts`) |
| OTLP metrics exporter | Metrics | Opt-in minimal OTLP/HTTP JSON POST of Command Center analytics to a collector, off by default and requiring `https:` in production, with no `@opentelemetry/*` SDK dependency (`packages/dashboard/src/otel-exporter.ts`, mapping in `packages/core/src/process/otel-metrics.ts`) |
| `agent_activity_events` | Activity | Inspectable per-agent activity event stream with cursor and retention contract (`docs/agent-activity-contract.md`) |
| Notification dispatcher and providers | Outbound alerting | Dispatcher, provider interface, and payload types in `packages/core/src/notification/`; ntfy and webhook providers, the notification service, the OAuth expiry monitor, and task-wedge notifications in `packages/engine/src/notification/` |
| Provider health monitor | Health | Probes metered provider usage windows and resumes rate-limited providers with exponential backoff (`packages/dashboard/src/provider-health-monitor.ts`) |

## Log Aggregation

- Engine and core subsystems log through `createLogger`, which prefixes each line with a subsystem tag and writes to stderr so stdout stays clean for command and test output.
- A control-character severity marker (`info`, `warn`, `error`) lets the dashboard TUI console-capture preserve severity even when info lines travel over `console.error`.
- A `debug()` level carries steady-state chatter and is off by default.
- Set `FUSION_DEBUG` to a subsystem prefix, a comma-separated list, or `1`/`all`/`*` to enable debug output, and the variable is re-read on every call.
- `docs/diagnostics.md` records the severity rules and the current list of debug-gated classes.
- There is no central log aggregation backend.
- Logs land on the local node that runs the engine.
- The dashboard surfaces operational state (usage, health, reliability, signals) from the store rather than from shipped logs.
- Per-task agent logs are newline-delimited JSON at `<rootDir>/.fusion/tasks/{ID}/agent-log.jsonl` (`docs/storage.md`).

## Tracing

- No distributed tracing backend, sampling strategy, or propagation format is configured.
- No OpenTelemetry or B3 trace context is used.
- The OTLP exporter sends metrics only, never traces.
- Durable run identification flows through run ids carried in run-audit and agent-activity rows.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| Task ready for review | `in-review` notification event | Notification dispatcher to ntfy and webhook providers | Informational |
| Task merged | `merged` notification event | Notification dispatcher to ntfy and webhook providers | Informational |
| Task failed | `failed` notification event | Notification dispatcher to ntfy and webhook providers | High |
| Task terminal wedge | `task-wedged` (`packages/engine/src/notification/task-wedge-notification.ts`) | Notification dispatcher plus a mailbox message to the operator | High |
| Plan or merge policy approval needed | `awaiting-approval` | Notification dispatcher to ntfy and webhook providers | High |
| Human review needed | `awaiting-user-review` | Notification dispatcher to ntfy and webhook providers | High |
| Planning awaiting input | `planning-awaiting-input` | Notification dispatcher to ntfy and webhook providers | High |
| CLI agent awaiting input | `cli-agent-awaiting-input` | Notification dispatcher to ntfy and webhook providers | High |
| Pipeline gridlock | `gridlock` (engine gridlock detector) | ntfy notifier only (`packages/engine/src/util/notifier.ts`) | High |
| Board stall not recovered | `board-stall-unrecovered` (engine self-healing) | ntfy notifier only (`packages/engine/src/util/notifier.ts`) | High |
| Database corruption detected | `db-corruption-detected` (engine self-healing) | Notification dispatcher to ntfy and webhook providers | High |
| Fallback model used | `fallback-used` (engine reviewer) | ntfy notifier only (`packages/engine/src/util/notifier.ts`) | High |
| Token budget reached | `token-budget` | Notification dispatcher to ntfy and webhook providers | High |
| OAuth expiry, relogin needed | `oauth-token-expired` (`packages/engine/src/notification/oauth-expiry-monitor.ts`) | In-app banner plus the notification dispatcher | High |
| Agent, room, and agent-to-agent messages | `message:agent-to-user`, `message:agent-to-agent`, `message:room` | Notification dispatcher to ntfy and webhook providers | Configurable per event |
| External incident or error signal | Command Center signal connectors (webhook, GitHub, GitLab, Sentry, Datadog, PagerDuty) | Command Center Signals inbox and the `incidents` table | Configurable per signal |
| Reliability degradation | `GET /api/health/reliability` indicators | Command Center reliability section | Warning |
| Provider rate limit | Provider health monitor (`packages/dashboard/src/provider-health-monitor.ts`) | Provider park plus a background recovery probe | Warning |

Alert rules live inside the engine's notification dispatcher and provider stack (`packages/core/src/notification/`, `packages/engine/src/notification/`).
The ntfy and webhook event allowlists are project settings (`ntfyEvents`, `webhookEvents` in `packages/core/src/config/settings-schema.ts`).
External alerting is pulled into Fusion over signal connectors rather than pushed out to on-call.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| Command Center | Dashboard (lazy-loaded `CommandCenter` view) | Operator mission control with overview, tokens, tools, activity, agent activity, productivity, review artifacts, team, workflows, ecosystem, GitHub, GitLab, signals, system, plugins, nodes, reliability, and mission-control sections |
| Task board | Dashboard board and list views | Per-task state, lifecycle history, and activity |
| Activity log | `ActivityLogModal` (`GET /api/activity`) | Newest-first project events with a type filter |
| Agent log viewer | `AgentLogViewer` | Per-task agent transcript from `agent-log.jsonl` |
| Usage | Command Center tokens and overview sections | Token and cost accounting from `usage_events` and `chat_token_usage` |

## SLO Reference

Fusion does not define formal SLOs, SLIs, or error budgets.
`.sdlc/context/service-levels.md` does not exist and is not planned.
Reliability indicators are collected through `GET /api/health/reliability` and surfaced in the Command Center, but no numeric SLO targets or error budgets are recorded yet.

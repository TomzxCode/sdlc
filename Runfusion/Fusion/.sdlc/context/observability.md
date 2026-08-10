# Observability

This file inventories the project's existing observability infrastructure: metrics, logging, tracing, and alerting.

## Monitoring Pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | Usage/credits tracking rows (`usage_events`), chat token accounting (`chat_token_usage`), reliability metrics (`/api/health/reliability`), project health (`central.project_health`) | In use (in-app/SQL, no external metrics backend) |
| Logging | Structured in-app logger in `@fusion/engine` (`logger.ts`), diagnostic logging conventions (`docs/diagnostics.md`) | In use |
| Tracing | None (no distributed tracing backend) | Not configured |
| Profiling | None | Not configured |
| Run audit | Append-only `run_audit_events` rows for engine/task lifecycle, plus `agent_activity_events` | In use |
| External signals | Inbound signal connectors (Sentry/Datadog/PagerDuty/webhooks) into the Command Center via HMAC-signed webhooks | In use (ingest only) |

## Instrumentation Libraries

| Library | Pillar | Configuration |
|---|---|---|
| `@fusion/engine` `createLogger` | Logging | Prefix-scoped structured logger; control-character severity markers; `info`/`warn`/`error` levels (`packages/engine/src/logger.ts`) |
| run-audit event rows | Audit | Append-only `project.run_audit_events` with ids/timestamps/outcomes-only metadata; never prose or secrets |
| `/api/health/reliability` metrics | Metrics | Reliability indicator aggregation (`packages/dashboard/src/reliability-metrics.ts`) |
| Signal connectors | External ingest | HMAC-signed webhook receivers for Sentry/Datadog/PagerDuty/webhooks; see `docs/signals-connectors.md` |
| `agent_activity_events` | Activity | Inspectable per-agent activity event stream with cursor/retention contract (`docs/agent-activity-contract.md`) |
| Notification providers | Outbound alerting | Webhook and ntfy providers (`packages/core/src/notification/`), OAuth expiry monitors, task-wedge notifications, remote/webhook alerting to Command Center |

## Log Aggregation

Logs are emitted by the engine through `createLogger` with structured, prefix-scoped lines and diagnostic conventions in `docs/diagnostics.md`. There is no central log aggregation backend; logs land on the local node that runs the engine, and the dashboard Command Center surfaces operational state (usage, health, reliability, signals) from the store rather than from raw log shipping. Per-task `agent-log.jsonl` storage and retention semantics are documented in `docs/storage.md`.

## Tracing

No distributed tracing backend, sampling strategy, or propagation format is configured. Durable-engine run identification flows through run ids carried in run-audit and agent-activity rows, but there is no OpenTelemetry/B3 trace context in use.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| OAuth expiry / relogin needed | OAuth expiry monitor (`oauth-expiry-monitor.ts`) | in-app banner + notification dispatcher | Warning |
| Task terminal wedge | task-wedge notification (`task-wedge-notification.ts`) | notification dispatcher | Warning |
| External incident/error signal | Command Center signal connectors (Sentry/Datadog/PagerDuty/webhooks) | Command Center inbox/incidents surface | Configurable per signal |
| Reliability degradation | `/api/health/reliability` indicators | dashboard reliability surface | Warning |

Alert rules live inside the engine's notification dispatcher and provider stack (`packages/core/src/notification/`, `packages/engine/src/notification/`). External alerting is pulled into Fusion via signal connectors rather than pushed out to on-call.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| Command Center | Dashboard (lazy-loaded `CommandCenter` view) | Operator mission control: usage/credits, health, reliability, active agents, signals, incidents |
| Task board | Dashboard board/list views | Per-task state, lifecycle history, activity |
| Usage | Dashboard usage surface | Token/cost accounting from `usage_events` and `chat_token_usage` |

## SLO Reference

Fusion does not define formal SLOs/SLIs/error budgets in `service-levels.md` (absent). Reliability indicators are collected via `/api/health/reliability` and surfaced in the dashboard, but no numeric SLO targets or error budgets are recorded yet.
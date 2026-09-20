# Observability

<!--
This file inventories the project's existing observability infrastructure: metrics,
logging, tracing, and alerting.
It gives create-observability, audit-observability, and
audit-reliability the context they need without grepping the codebase each time.
Service-level targets (SLOs, SLIs, error budgets) live in service-levels.md.
Update this file when the monitoring stack changes.
-->

## Monitoring Pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | No metrics backend (no Prometheus, Datadog, or CloudWatch) | Not configured |
| Logging | pino + pino-pretty to stderr in server and daemon | In use |
| Tracing | No trace backend or propagation | Not configured |
| Profiling | No profiler or continuous profiling | Not configured |
| Health probes | `GET /api/health` (build provenance) + `GET /api/health/db` (DB liveness) | In use |
| Deploy verification | `deploy.yml` / `deploy-prod.yml` smoke step asserting served `sha` matches pushed commit | In use |

## Instrumentation Libraries

| Library | Pillar | Configuration |
|---|---|---|
| pino (`^10.3.1`, direct in both packages) | Logging | Level from `LOOPANY_LOG_LEVEL` (default `info`), writes to stderr, ignores `pid,hostname` |
| pino-pretty (`^13.1.3`, direct in both packages) | Logging | Synchronous destination stream (no worker thread) so one-shot CLI logs flush before exit, `SYS:HH:MM:ss` timestamps, colorized |
| @opentelemetry/api | Tracing | Transitive dependency only (via lockfile), no project instrumentation configured |
| sentry-sdk / datadog / prometheus-client | Errors / Metrics | Not present in any package manifest |

## Log Aggregation

No centralized log aggregation is configured.
Both server (`packages/server/src/logger.ts`) and daemon (`packages/daemon/src/logger.ts`) log via pino to stderr (fd 2) to keep stdout clean for CLI protocol output.
Container stdout/stderr is captured by the Fly runtime logs by default, with no retention, sampling, or structured shipper configured in-repo.

## Tracing

No tracing backend is configured.
No sampler, exporter, or propagation format (W3C Trace Context, B3) is wired into server or daemon code.
Run-level visibility comes from persisted run rows, the daemon poll progress heartbeat (`{runId, step, label}`), and slimmed transcript steps, not from distributed traces.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| Exec run failure | `gateway/index.ts` finalize via `notify.ts` `shouldNotifyFailure` | Loop's channel (Telegram / Slack / Feishu push) | Warning |
| Still-broken reminder | Consecutive-failure streak (`store.execFailureStreak`), every 5th failure | Loop's channel (Telegram / Slack / Feishu push) | Warning |
| Autopause circuit breaker | `LOOPANY_FAILURE_AUTOPAUSE_STREAK` (default 10) consecutive exec failures, loop auto-paused | Loop's channel, subsumes the failure alert (silent under `notify:never`) | Critical |
| Deferred run waiting | Sweep stamps one `deferredMessage` per deferred exec run, only for genuinely offline machines | Loop's channel (Telegram / Slack / Feishu push) | Info |
| Goal reached / completion | `loopany finish` on a closed loop | Loop's channel unless `notify:never` | Info |
| Wedged DB pool | `GET /api/health/db` 503 + Fly `http_service` check going critical + in-process `server/dbWatchdog.ts` exiting on sustained wedge | Fly de-routes the machine, `restart.policy = on-failure` brings up a fresh pool | Critical |
| Deploy did not take | `deploy.yml` / `deploy-prod.yml` smoke step comparing `/api/health` `sha` to pushed commit | Failing workflow run (CI signal, no push notification) | Critical |

Alert rules for run outcomes live in `packages/server/src/gateway/notify.ts` (pure message builders plus `CHANNELS` senders for telegram, slack, and feishu).
Failure anti-spam is streak-based and derived from persisted run rows, so it survives deploys with no in-memory counter.
`notify:never` silences all pushes, while `skipped` (superseded/deferred) runs never count toward the failure streak.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| Team dashboard | Web UI (`DashboardView`, per-team `/t/$teamId`) | Loop cards, status strips, recent runs per loop (product surface, not ops) |
| Loop detail page | Web UI (`/loops/$loopId`) | Per-loop runs list with live progress line, files panel, edit composer |
| Run detail page | Web UI (`/loops/$loopId/runs/$runId`) | Live activity card while running, transcript, artifacts, run diff |
| Cross-loop timeline | Web UI (`/timeline`, `t.$teamId_.timeline`) | Lanes of run points plus cron-projected future fires |
| Notifications modal | Web UI (`NotificationsModal` / `ChannelAddForm`) | Channel binding plus live test ping (alerting configuration surface) |

No ops dashboards (Grafana, Datadog, CloudWatch) exist.

## SLO Reference

There is no `service-levels.md` in this project yet, so no SLOs, SLIs, or error budgets are defined.
The closest load-bearing targets are operational conventions: `/api/health/db` must answer within 5s, the daemon poll heartbeat runs on a ~3s cadence (20s long-poll hold when idle), and the autopause circuit breaker trips at 10 consecutive exec failures by default.
Reference this file when creating feature-level observability plans until `service-levels.md` exists.

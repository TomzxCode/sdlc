# Observability

## Monitoring pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | Telemetry pipeline: `jcode-telemetry-core` to `/v1/event` and `/v2/usage`, `telemetry-worker` to D1 plus Analytics Engine firehose datasets | In use |
| Logging | File logs under `~/.jcode/logs` via `jcode-logging` | In use |
| Tracing | None | Not configured |
| Profiling | None (the stall watchdog records a one-off resource snapshot on a suspected hang) | Not configured |

## Instrumentation libraries

| Library | Pillar | Configuration |
|---|---|---|
| `jcode-logging` | Logging | Date-stamped file output under `~/.jcode/logs` with 7-day pruning and task-scoped context |
| `jcode-telemetry-core` | Metrics and usage | In-memory background queue to `/v1/event` for activity events; durable on-disk outbox with retries to `/v2/usage` for `usage_report` |

## Log aggregation

- Application logs are written to date-stamped files (`jcode-YYYY-MM-DD.log`) under `~/.jcode/logs`, pruned after 7 days. `JCODE_HOME` redirects the directory.
- Application diagnostics go through `crate::logging`; `println!` and `eprintln!` remain for CLI output and for logger self-failure fallbacks.
- Log context is resolved task-first: a per-task map keyed by the Tokio task id takes precedence over the thread-local slot, capped at 1024 entries.
- Debug-level logs stay disabled unless the `JCODE_TRACE` environment variable is set.
- No central log aggregation system is configured.

## Tracing

- No distributed tracing backend is configured.
- Services do not emit traces in a standard propagation format.
- Sampling strategy is undefined because tracing is absent.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| Telemetry store health | `GET https://telemetry.jcode.sh/v1/health` (database size, soft limit, last emergency prune) | No routing | Not configured |
| Server stall | Stall watchdog in `jcode-logging` (RSS, thread count, open-fd count, per-thread wait channel after 90s without a beat) | Log only | Not configured |

- No runtime alerting rules are configured.
- CI budget checks act as quality gates and not as runtime alerts.
- No on-call routing exists for monitoring signals.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| dau | `telemetry-worker/dau.sql` | Daily active usage reporting |
| users | `telemetry-worker/users.sql` | User population reporting |
| conversion | `telemetry-worker/conversion.sql` | Website to installer to first-run conversion funnel |
| health | `telemetry-worker/health.sql` | Telemetry store health and lifecycle row reporting |
| geo | `telemetry-worker/geo.sql` | Geographic distribution reporting |
| token-value | `telemetry-worker/token-value.sql` | Estimated list-price value of model usage |
| token-value-daily | `telemetry-worker/token-value-daily.sql` | Daily token value time series |
| model-usage | `telemetry-worker/model-usage.sql` | Per-model usage rollup |
| concurrency | `telemetry-worker/concurrency.sql` | Observed runtime Agent session peaks with trust tiers |
| desktop-fleet | `telemetry-worker/desktop-fleet.sql` | Share of active Desktop installs on the newest version |
| prompt-users | `telemetry-worker/prompt-users.sql` | Users who actually submitted a prompt |
| opt-outs | `telemetry-worker/opt-outs.sql` | Opt-out counts by source |
| discovery | `telemetry-worker/discovery.sql` | Sponsored discovery funnel by phase, outcome, and category |

- Dashboards are SQL queries against telemetry-worker D1 data, registered as npm scripts in `telemetry-worker/package.json`.
- `telemetry-worker/schema.sql` is the canonical D1 schema and `repair-daily-active.sql` is a one-off backfill script, not dashboards.
- Usage events are queued in `jcode-telemetry-core` and flushed to the telemetry event endpoint.
- Event taxonomy and privacy rules are documented in `TELEMETRY.md`.
- No Grafana or hosted dashboard service is configured.

## SLO reference

- No `service-levels.md` file is present in `.sdlc/context`.
- Feature-level observability plans have no service-level targets to reference yet.

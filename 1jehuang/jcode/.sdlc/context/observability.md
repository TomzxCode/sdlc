# Observability

## Monitoring pillars

| Pillar | System | Status |
|---|---|---|
| Metrics | Telemetry D1 pipeline (`jcode-telemetry-core` plus `telemetry-worker`) | In use |
| Logging | File logs under `~/.jcode/logs` via `jcode-logging` | In use |
| Tracing | None | Not configured |
| Profiling | None | Not configured |

## Instrumentation libraries

| Library | Pillar | Configuration |
|---|---|---|
| `jcode-logging` | Logging | File output under `~/.jcode/logs` with rotation and thread-local context |
| `jcode-telemetry-core` | Metrics and usage | Queued background flush to the telemetry event endpoint |

## Log aggregation

- Application logs are written to local files under `~/.jcode/logs` with automatic rotation.
- Production code paths log through `crate::logging` instead of standard output or standard error.
- Thread-local context records server, session, provider, and model for each log entry.
- Debug-level logs stay disabled unless the `JCODE_TRACE` environment variable is set.
- Retention policy for local log files is unspecified in the codebase.
- No central log aggregation system is configured.

## Tracing

- No distributed tracing backend is configured.
- Services do not emit traces in a standard propagation format.
- Sampling strategy is undefined because tracing is absent.

## Alerting

| Alert | Source | Routing | Severity |
|---|---|---|---|
| No runtime alerts | No source | No routing | Not configured |

- No runtime alerting rules are configured.
- CI budget checks act as quality gates and not as runtime alerts.
- No on-call routing exists for monitoring signals.

## Dashboards

| Dashboard | Location | Purpose |
|---|---|---|
| dau | `telemetry-worker/dau.sql` | Daily active usage reporting |
| conversion | `telemetry-worker/conversion.sql` | Install conversion funnel reporting |
| health | `telemetry-worker/health.sql` | Telemetry store size and health reporting |
| users | `telemetry-worker/users.sql` | User population reporting |
| token-value | `telemetry-worker/token-value.sql` | Token usage value reporting |
| geo | `telemetry-worker/geo.sql` | Geographic distribution reporting |

- Dashboards are SQL queries against telemetry-worker D1 data.
- Usage events are queued in `jcode-telemetry-core` and flushed to the telemetry event endpoint.
- Event taxonomy and privacy rules are documented in `TELEMETRY.md`.
- No Grafana or hosted dashboard service is configured.

## SLO reference

- No `service-levels.md` file is present in `.sdlc/context`.
- Feature-level observability plans have no service-level targets to reference yet.

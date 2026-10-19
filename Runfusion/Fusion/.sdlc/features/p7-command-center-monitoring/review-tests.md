---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Named test files that do not exist:

- Key Test Files lists `packages/dashboard/src/routes/__tests__/register-signal-routes*.test.ts`. No file in that directory matches the glob. The signal route suite lives one directory up at `packages/dashboard/src/__tests__/register-signal-routes.test.ts`, and it is the only file that covers TC-1, TC-5, and TC-8.
- Key Test Files lists `packages/dashboard/app/__tests__/usage-*.test`. No file in `packages/dashboard/app/__tests__/` matches that pattern. The usage coverage sits in `packages/dashboard/app/hooks/__tests__/useUsageData.test.ts`, `packages/dashboard/app/components/__tests__/UsageIndicator.test.tsx`, and `packages/dashboard/src/__tests__/usage.test.ts`.

Stale test expectations:

- TC-1 expects "202 for valid, 401/400 otherwise". The route answers 201 for a created task, 200 for a non-actionable, deduplicated, or recovery-only delivery, and adds 413 for an oversized body and 429 for a rate-limited source (`packages/dashboard/src/routes/register-signal-routes.ts:283`, `:293` to `:347`). The existing suite already asserts 201 and 400 (`packages/dashboard/src/__tests__/register-signal-routes.test.ts:223` and `:346`).

Test cases with no named coverage:

- TC-3 "Monitor route health | system snapshot | Health payload rendered" has no test. No test file exercises `packages/dashboard/src/routes/monitor-routes.ts`. The nearest coverage is the store at `packages/dashboard/src/__tests__/monitor-store.pg.test.ts` and the trait at `packages/core/src/__tests__/postgres/monitor-trait-storm-guard.pg.test.ts`, and neither touches the routes.
- TC-6 "Usage route from live store | executed tasks | Usage data served" is covered only by files Key Test Files does not name: `packages/core/src/__tests__/postgres/command-center-analytics.pg.test.ts:84` and `packages/core/src/__tests__/postgres/command-center-remaining-analytics.pg.test.ts:98`.

Coverage matrix gaps:

- The Coverage Matrix has no row for FR-5, FR-6, NFR-2, or NFR-3, so four stated requirements are unverified by the plan.
- FR-4 maps only to TC-7, which covers the resume diagnostics registrar. Nothing in the plan covers the monitor routes, the reliability metrics, the system telemetry endpoint, or the health surfaces FR-4 names.

Significant test areas the plan does not cover:

- The core Command Center analytics aggregators are absent. `packages/core/src/__tests__/postgres/command-center-analytics.pg.test.ts` and `packages/core/src/__tests__/postgres/command-center-remaining-analytics.pg.test.ts` cover the token, tool, activity, productivity, team, workflow, GitHub, GitLab, signals, and live-snapshot aggregators, and `packages/dashboard/src/__tests__/command-center-analytics-column-flags.test.ts` covers the column-flag wiring that feeds them.
- The signal provider adapters are absent. `packages/dashboard/src/__tests__/signal-source.test.ts` and `packages/dashboard/src/__tests__/github-signal-source.test.ts` cover the normalization, field caps, replay window, and link-safety rules that the connectors depend on.
- The provider health monitor is absent: `packages/dashboard/src/__tests__/provider-health-monitor.test.ts` covers the probe, the backoff, and the capacity check.
- The reliability surface is absent: `packages/dashboard/src/__tests__/reliability-metrics.test.ts`, `packages/dashboard/src/__tests__/reliability-lanes-resolved.test.ts`, and `packages/dashboard/app/components/__tests__/ReliabilityView.test.tsx` cover the in-review flow, duration percentiles, and merge-attempt distribution.
- The Prometheus surface is absent: `packages/dashboard/src/metrics/__tests__/` holds `domain-sampler.test.ts`, `metrics-endpoint.test.ts`, `metrics-samplers-acceptance.test.ts`, `prometheus-text.test.ts`, and `runtime-sampler.test.ts`, and `packages/dashboard/src/routes/__tests__/metrics-endpoint.test.ts` covers the endpoint.
- The OTLP export is absent: `packages/core/src/__tests__/otel-metrics.test.ts` covers the analytics to OTLP mapping.
- The CSV export is absent: `packages/dashboard/src/__tests__/command-center-csv.test.ts` covers the serializer and the table builders.
- The agent activity surface is absent: `packages/dashboard/src/__tests__/agent-activity-route.test.ts` and `packages/dashboard/src/__tests__/sse-agent-activity.test.ts` cover the route and the SSE frames.
- The Command Center area and chart suites are absent from Key Test Files beyond the wildcard. `packages/dashboard/app/components/command-center/areas/__tests__/` holds nine files including `areas.test.tsx`, `system-controls-job-stream.test.tsx`, and `areas.github-signals.test.tsx`, and `packages/dashboard/app/components/command-center/charts/recharts/__tests__/` holds `LineChart.test.tsx` and `PieChart.test.tsx`.

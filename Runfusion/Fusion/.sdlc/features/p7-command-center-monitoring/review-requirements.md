---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Stale requirements:

- FR-3 names four providers (Sentry/Datadog/PagerDuty/webhooks) and calls the whole set HMAC-signed. The code registers six providers: `webhook`, `sentry`, `datadog`, `pagerduty`, `gitlab`, and `github` (`packages/dashboard/src/routes/register-signal-routes.ts:46` to `:53`, asserted by `packages/dashboard/src/__tests__/register-signal-routes.test.ts:211`). GitLab is verified with a secret-token header, not HMAC (`docs/signals-connectors.md:9` and `:22`).
- FR-2 describes the usage surface as "token usage, cost tabs, usage indicator". The usage indicator is a separate header component outside the Command Center (`packages/dashboard/app/components/UsageIndicator.tsx:585`, mounted from `packages/dashboard/app/components/Header.tsx:1066`), and it shows provider subscription quota windows fetched from `GET /api/usage` (`packages/dashboard/src/routes/register-usage-routes.ts:16`, `packages/dashboard/src/usage.ts`). It is not per-task cost.
- The Constraint "Usage/cost data is read-only outside the engine's accounting writer" does not hold for cost configuration. The dashboard writes `modelPricingOverrides`, `modelPricingFetchedAt`, and `modelPricingSource` into global settings (`packages/dashboard/src/routes/register-command-center-routes.ts:264` to `:271`).
- Open Question 1 ("Which usage metrics are authoritative for cost accounting (token counts vs. provider billing)?") is settled in the code. Cost is derived at read time from recorded token counts and a maintained pricing table, and is never persisted as billing truth (`packages/core/src/ai/model-pricing.ts`, `packages/core/src/board/token-analytics.ts:167` to `:206`, `docs/architecture.md:978`).

Missing requirements (behavior the code implements that no FR or NFR covers):

- OTLP metrics export is not covered. The dashboard can periodically map Command Center token, cost, and activity analytics to OTLP/HTTP JSON and POST them to a collector. It is off by default, rejects a non-https endpoint in production, redacts header values, and backs off on an unreachable collector (`packages/dashboard/src/otel-exporter.ts:1` to `:31`, `packages/dashboard/src/server.ts:2562` to `:2571`).
- The Prometheus `/metrics` surface is not covered. A public endpoint at the app level serves numeric gauges from a runtime sampler and a domain sampler with no awaited I/O (`packages/dashboard/src/server.ts:1964` to `:1977`, `packages/dashboard/src/metrics/index.ts:1` to `:38`, `packages/dashboard/src/metrics/runtime-sampler.ts`, `packages/dashboard/src/metrics/domain-sampler.ts`).
- The Command Center operator control surface is not covered. The System section rebuilds and restarts the server with a streamed job log, restarts engines and agents, backs up the database, reloads plugins, tails server logs, files a guided report, and copies a diagnostics bundle (`packages/dashboard/app/components/command-center/areas/SystemControlsArea.tsx:53` to `:76`).
- Signal connector protections beyond signature verification are not covered. The route caps the body at about 1 MB (413), applies a per-source rate limit (429), rejects a missing raw body (401), rejects a replayed delivery nonce (401), and dedupes a repeated external id against existing tasks (`packages/dashboard/src/routes/register-signal-routes.ts:186` to `:213`, `:303` to `:317`, `packages/dashboard/src/signal-source.ts`). NFR-1 covers the HMAC check only.
- The monitor regression loop is not covered. A regression signal opens at most one storm-guarded fix task back in the triage column through the `monitor` trait (`packages/dashboard/src/monitor-trait.ts:23` to `:67`, `packages/dashboard/src/monitor-trait.ts:140`). FR-4 names the monitor routes but not this task-opening behavior.
- Provider health monitoring is not covered. A background monitor probes each provider's usage API, backs off on repeated failures, and pauses work when a provider reports no usable capacity (`packages/dashboard/src/provider-health-monitor.ts:1` to `:35`, `packages/dashboard/src/server.ts:2589` to `:2604`).
- Analytics CSV export is not covered. Seven analytics endpoints answer `?format=csv` with a downloadable RFC-4180 file (`packages/dashboard/src/routes/register-command-center-routes.ts:177` to `:191` and the `wantsCsv` branches on tokens, tools, activity, productivity, workflows, GitHub, and GitLab).
- Operator-triggered data maintenance is not covered. Two authenticated POST endpoints let an operator refresh model prices from LiteLLM and preview or apply a historical commit-association LOC backfill (`packages/dashboard/src/routes/register-command-center-routes.ts:253` to `:279` and `:376` to `:387`).
- GitHub and GitLab issue-flow analytics are not covered. Two project-scoped endpoints aggregate issues filed by Fusion, issues fixed by Fusion, resolved rows, and per-repository or per-project breakdowns, with CSV export (`packages/dashboard/src/routes/register-command-center-routes.ts:540` to `:588`, `packages/dashboard/app/components/command-center/areas/GithubArea.tsx`, `packages/dashboard/app/components/command-center/areas/GitlabArea.tsx`).
- The org-wide agent activity timeline is not covered. A separate panel seeds a live feed from `GET /api/agent-activity`, receives `agent:activity` SSE frames, and pages a timeline with cursor semantics and a documented retention contract (`packages/dashboard/app/components/command-center/useAgentActivity.ts:161`, `packages/dashboard/app/components/command-center/AgentActivityPanel.tsx`, `docs/agent-activity-contract.md`).
- Organization export and import are not covered. The Team section downloads a secret-scrubbed organization bundle and applies a pasted bundle after a dry-run preview (`packages/dashboard/app/components/command-center/OrgPortabilityControls.tsx`, `packages/dashboard/app/components/command-center/__tests__/OrgPortabilityControls.test.tsx`).

Acceptance criteria gaps:

- The acceptance criteria list has no entry for FR-4, FR-5, FR-6, NFR-2, or NFR-3, so five stated requirements are unverified.
- Every acceptance criterion checkbox is unchecked while the document frontmatter reads `status: done` (`requirements.md:46` to `:61`).

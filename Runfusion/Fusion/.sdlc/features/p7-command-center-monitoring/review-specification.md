---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
---

## Sync drift: 2026-10-19

Architecture:

- The diagram names the dashboard registrars but omits the core modules that own the metric math. The aggregators live in `packages/core/src/board/`: `token-analytics.ts`, `tool-analytics.ts`, `activity-analytics.ts`, `productivity-analytics.ts`, `team-analytics.ts`, `workflow-analytics.ts`, `github-issue-analytics.ts`, `gitlab-issue-analytics.ts`, `signals-analytics.ts`, and `command-center-live.ts`. The dashboard routes are thin adapters over them (`packages/dashboard/src/routes/register-command-center-routes.ts:40` to `:47`).
- The diagram omits the two telemetry export surfaces. The Prometheus `/metrics` endpoint and the OTLP collector exporter are separate from the Command Center view and are not shown (`packages/dashboard/src/server.ts:1964` to `:1977`, `packages/dashboard/src/otel-exporter.ts`).
- The diagram places `register-diagnostics-routes` in the "system health" group. That registrar stores resume-instrumentation events in a bounded in-memory ring buffer, not health data (`packages/dashboard/src/routes/register-diagnostics-routes.ts:22` to `:23`, `:56` to `:63`, `:68` to `:116`).
- The diagram does not show the Command Center's own scale. The view has eighteen sections, including a conditional Nodes section, and the navigation is a dropdown rather than a tab strip (`packages/dashboard/app/components/command-center/CommandCenter.tsx:88` to `:115`, `packages/dashboard/app/components/command-center/CommandCenterSectionNav.tsx:17` to `:20`).

Data Models:

- The Usage / Cost table does not match the schema. There is no `tokens` json column and no `costMs` column. The `usage_events` table has an identity `id` primary key, `projectId`, `ts`, `kind`, a nullable text `taskId`, `agentId`, `nodeId`, `model`, `provider`, `toolName`, `category`, and a `meta` jsonb column (`packages/core/src/postgres/schema/project.ts:2018` to `:2038`).
- Token counts live in a different table than the data model states. `chat_token_usage` stores `inputTokens`, `outputTokens`, `cachedTokens`, `cacheWriteTokens`, and `totalTokens` as separate bigint columns, plus `modelProvider`, `modelId`, `sourceKind`, and `createdAt` (`packages/core/src/postgres/schema/project.ts:2362` to `:2382`). Cost is not stored at all.
- The data model has no table for incidents. The `incidents` table is the backing store for the Signals area and the MTTR metric, with `incidentId`, `groupingKey`, `title`, `severity`, `status`, `source`, `fixTaskId`, `openedAt`, `resolvedAt`, `link`, and `meta` (`packages/core/src/postgres/schema/project.ts:2131` to `:2161`).
- The data model has no table for deployments. The `deployments` table backs the deploy-frequency metric (`packages/core/src/postgres/schema/project.ts:2074` to `:2083`).

API Contracts:

- The endpoint path is wrong. The route is `POST /api/signals/:provider`, and the provider is a path parameter, not a body field (`packages/dashboard/src/routes/register-signal-routes.ts:293`).
- The request table names a `payload` field and a `signature` field that do not exist in the body. The payload is the raw request body, and the signature travels in a provider-specific header: `X-Fusion-Signature`, `Sentry-Hook-Signature`, `X-Datadog-Signature`, `X-PagerDuty-Signature`, `X-Hub-Signature-256`, or `X-Gitlab-Token` (`packages/dashboard/src/routes/register-signal-routes.ts:304` to `:333`, `docs/signals-connectors.md:22`, `:39` to `:40`, `:80`, `:100`, `:120`, `:131`, `:166`).
- The response table is wrong. A created task answers 201, a non-actionable payload, a deduplicated delivery, or a recovery-only resolution answers 200, a malformed payload answers 400, a failed or missing signature answers 401, an oversized body answers 413, and a rate-limited source answers 429. The code returns 202 in no case (`packages/dashboard/src/routes/register-signal-routes.ts:186` to `:207`, `:283`, `:335` to `:347`).
- The provider enum is wrong. The contract lists four providers, and the code registers six (`packages/dashboard/src/routes/register-signal-routes.ts:46` to `:53`, `docs/signals-connectors.md:9`).
- The API Contracts section documents one endpoint. The Command Center registrar exposes fifteen project-scoped analytics and control endpoints, and the monitor registrar exposes three more (`packages/dashboard/src/routes/register-command-center-routes.ts:209` to `:698`, `packages/dashboard/src/routes/monitor-routes.ts:81` to `:171`).

Sequences:

- The specification has no Sequences section. The signal ingestion sequence is a defined behavior with a fixed order: verify the signature, normalize the payload, reject a replayed nonce, dedupe an existing external id, create the triage task, then write and resolve the incident row (`packages/dashboard/src/routes/register-signal-routes.ts:186` to `:283`).

Technical Decisions:

- "Cost in core | task store accounting | Read-only outside writer" is wrong about where cost comes from. Cost is not a task-store column. It is derived at read time from recorded token counts times the effective pricing table, and it is never persisted (`packages/core/src/ai/model-pricing.ts`, `packages/core/src/board/token-analytics.ts:167` to `:206`, `docs/architecture.md:978`).
- "HMAC signing | `docs/signals-connectors.md`" holds for the generic webhook, GitHub, Sentry, Datadog, and PagerDuty connectors, but not for GitLab, which uses a secret-token header compared in constant time (`docs/signals-connectors.md:9` and `:22`).
- The decision table omits the pricing-source decision. The built-in pricing table is hand-maintained, user overrides live in global settings and win over the built-ins, and the only dashboard network path for prices is the operator-triggered LiteLLM fetch (`packages/dashboard/src/routes/register-command-center-routes.ts:250` to `:251`, `docs/architecture.md:978`).

Risks and Unknowns:

- "Cost accounting basis (token vs. billing) is unresolved" is stale. The code has settled on a read-time estimate from token counts that is explicitly not billing truth, with an unavailable sentinel for models that have no price (`packages/core/src/board/token-analytics.ts:70` to `:74`, `docs/architecture.md:978`).

Out of Scope:

- The out-of-scope list does not name the Insights surface. Insights is a separate top-level dashboard view with its own store, run executor, and sweeper, mounted at `/api/insights` (`packages/dashboard/app/App.tsx:141` and `:1880`, `packages/dashboard/src/routes.ts:1552` to `:1557`, `packages/core/src/insights/`). It is not a Command Center section (`packages/dashboard/app/components/command-center/CommandCenter.tsx:44` to `:62`).
- The out-of-scope list does not name Ideation. `IdeationPanel.tsx` lives inside the command-center directory but is rendered by the top-level Ideation view, not by the Command Center (`packages/dashboard/app/components/dashboard/MainContent.tsx:705`, `packages/dashboard/app/components/command-center/CommandCenter.tsx:108` to `:113`).

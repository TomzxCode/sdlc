---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Overview | "Server-side ingestion is a Cloudflare Worker in `telemetry-worker/` (worker.js, D1 schema, 24 migrations)." | The worker source is at `telemetry-worker/src/worker.js` (plus `oauth-account.js`, `concurrency.js`, `model-pricing.js`), and there are 31 migrations (`0001` through `0031`), not 24. | Reword to name `telemetry-worker/src/`, the additional modules, and 31 migrations. |
| Architecture | "D1 database (schema.sql + migrations/0001..0024)" | Migrations run to `0031`, and the pipeline also writes to R2 (transcript bodies) and Analytics Engine (raw firehose). | Reword the migration range and name R2 and Analytics Engine as parallel stores. |
| Architecture | "dashboards (DAU, install funnel, token value, geo, health, users, discovery)" | Seven dashboards are missing: concurrency, desktop-fleet, model-usage, opt-outs, prompt-users, token-value-daily, discovery. | Add the missing dashboards. |
| Data Models | `InstallEvent` has `platform, version` | `InstallEvent` (`crates/jcode-usage-types/src/lib.rs:275`) has `version`, `os`, `arch`. There is no `platform` field. | Replace with `version, os, arch`. |
| Data Models | `UpgradeEvent` has `from_version, to_version` | `UpgradeEvent` (`:292`) has `version`, `from_version`. There is no `to_version` field. | Replace with `version, from_version`. |
| Data Models | `AuthEvent` has `provider, method` | `AuthEvent` (`:308`) has `auth_provider`, `auth_method`. | Replace with `auth_provider, auth_method`. |
| Data Models | `SessionLifecycleEvent` has `reason` | `SessionLifecycleEvent` (`:545`) has `end_reason` plus the full session summary; `SessionEndReason` (`:192-201`) has 7 variants. | Replace with `end_reason, turns, tool_calls, input_tokens, output_tokens, total_tokens, feature_*_used, tool_cat_*, workflow_*_used, session_success`. |
| Data Models | `TurnEndEvent` has `usage` | `TurnEndEvent` (`:744`) carries `turn_index`, timings, tool counts, token counts, `turn_success`, `turn_end_reason`. | Replace with the real field list. |
| Data Models | `ErrorCounts` has `category` | `ErrorCounts` (`:699`) has five counters: `provider_timeout`, `auth_failed`, `tool_error`, `mcp_error`, `rate_limited`. | Replace with the five counters. |
| Technical Decisions | "No content collection \| event structs exclude messages" | Still true, but the second policy line ("Do not add emails to ordinary diagnostic logs or every usage event") is now missing. | Keep the row and add a separate row for the identity path. |
| Risks and Unknowns | "Server-side dashboards depend on D1 data quality and retention; retention is not documented." | `TELEMETRY.md:523-534` documents 90-day OAuth-account retention, up to 12 months for event records, and 30 days for R2 transcript bodies. | Reword to say retention is documented but rollup timing is still inferred. |
| Out of Scope | "Individual-session profiling or user tracking beyond aggregate product metrics." | `TELEMETRY.md:88-89` and `:460-462` state that provider OAuth email telemetry explicitly links installation usage to account identity. | Replace with three bullets: individual-session profiling; account linkage beyond the single provider OAuth email; collection of prompts, responses, or message content by design. |

## Missing Information

- Seven event payloads are missing from the Data Models table: `SessionStartEvent`, `OnboardingTraceEvent`, `FeedbackEvent`, `DiscoveryEvent`, `TodoSessionEvent`, `UsageReportEvent`, and the OAuth identity record.
- Three endpoints are missing from API Contracts: `POST /v1/oauth-account/check` (body `id`, `provider`, `email_hash`), `POST /v1/oauth-account` (body `id`, `provider`, `email`), and `POST /v2/usage`. `POST /v1/transcript` exists but is not listed either.
- The two identity routes are private, refuse browser origins and CORS preflights, and reject raw-email preflight requests.
- The bridge-level surfaces are missing: `jcode telemetry status`, `enable`, `disable` and the `/telemetry` three-level command.
- The client-side delivery model is missing: activity events use a bounded in-memory queue to `/v1/event`, while usage reports use a durable on-disk outbox with bounded retries to `/v2/usage`.

## Implementability

No issues found beyond the corrections above.

## Reversibility

No issues found.

## Forward Compatibility

No issues found.

## Ambiguities

No issues found.

## Incoherences

No issues found.

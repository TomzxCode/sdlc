# Telemetry

## Analytics Platform

| Property | Value |
|---|---|
| Platform | Custom in-house pipeline (Cloudflare Worker plus D1, R2, and Analytics Engine) |
| SDK | `jcode-telemetry-core` (Rust; in-memory background queue for activity events, durable on-disk outbox with retries for usage_report) |
| Integration | Server-side ingestion at `telemetry.jcode.sh` from client-queued events |
| API key location | n/a (no API key, anonymous random ID only) |
| Event endpoint | `https://telemetry.jcode.sh/v1/event` |
| Usage endpoint | `https://telemetry.jcode.sh/v2/usage` (durable receipts, contract version 2) |
| Transcript endpoint | `https://telemetry.jcode.sh/v1/transcript` (optional transcript sharing only) |
| OAuth identity endpoints | `https://telemetry.jcode.sh/v1/oauth-account/check` and `https://telemetry.jcode.sh/v1/oauth-account` (provider OAuth email, opt-out applies) |
| Full disclosure | `TELEMETRY.md` in repo root |
| Client implementation | `crates/jcode-telemetry-core/src/` |
| Server implementation | `telemetry-worker/` (Worker source, `schema.sql`, 31 migrations) |

## Event Naming Conventions

- Event names use snake_case (for example `install`, `upgrade`, `auth_success`, `session_start`, `session_end`, `session_crash`, `turn_end`, `onboarding_step`, `feedback`).
- Property names use snake_case (for example `id`, `from_version`, `auth_provider`, `session_success`, `total_tokens`).
- Feature usage flags use the `feature_*_used` prefix (for example `feature_memory_used`, `feature_mcp_used`).
- Tool mix counters use the `tool_cat_*` prefix (for example `tool_cat_write`, `tool_cat_shell`, `tool_cat_mcp`).
- Workflow classifiers use the `workflow_*_used` prefix (for example `workflow_coding_used`, `workflow_research_used`).
- Slash-command flags use the `command_*_used` prefix (for example `command_model_used`, `command_resume_used`).
- Detail tables are keyed by `event_id` and joined to `events` (for example `session_details`, `turn_details`, `discovery_details`, `todo_session_details`, `web_details`, `install_details`, `concurrency_details`, `desktop_update_details`).
- Reserved and prohibited content includes prompts, responses, code, file paths, tool inputs and outputs, MCP names, IPs, error text, and exact timestamps (except `usage_report.occurred_at`, which is needed to age out durable usage receipts).
- Coarse buckets are used instead of raw values (for example hour of day, weekday, country code, error category, end reason).
- Schema evolution uses integer `schema_version` plus `build_channel`, `is_ci`, `is_git_checkout`, and `ran_from_cargo` on shared metadata.
- Event catalog lives in `TELEMETRY.md` plus `telemetry-worker/schema.sql` and `telemetry-worker/migrations/`.

## Existing Event Taxonomy

| Event | Trigger | Key properties |
|---|---|---|
| `install` | First launch generates a random ID | `id`, `event`, `version`, `os`, `arch` |
| `upgrade` | Version change detected | `id`, `version`, `from_version`, `os`, `arch` |
| `auth_success` | Provider auth succeeds | `id`, `auth_provider`, `auth_method`, `version`, `os`, `arch` |
| `onboarding_step` | Onboarding milestone or auth transition reached | `step`, `auth_provider`, `auth_method`, `auth_failure_reason`, `milestone_elapsed_ms` |
| `onboarding_trace` | First-run onboarding traversal settles (`ready`, `degraded`, `abandoned`, `stuck`) | `env`, `steps` (`node`, `edge`, `reason`, `dt_ms`), `outcome`, `keystrokes`, `truncated`; not yet accepted by the worker allowlist |
| `session_start` | Session begins | `id`, `session_id`, `provider_start`, `model_start`, `resumed_session`, timing and concurrency buckets |
| `session_end` | Session ends normally | `turns`, `tool_calls`, `input_tokens`, `output_tokens`, `total_tokens`, `feature_*_used`, `tool_cat_*`, `workflow_*_used`, `session_success`, `end_reason` |
| `session_crash` | Best-effort crash or signal handler fires | Same session summary fields as `session_end` with crash `end_reason` |
| `session_concurrency` | Runtime Agent session registration and teardown (`phase` = `start` or `end`) | `session_id`, `concurrency_session_id`, `concurrency_tracking_version`, `concurrency_tracking_scope`, `agent_role`, concurrency snapshot counts |
| `turn_end` | Each user turn finalizes | `turn_index`, turn timing fields, per-turn tool counts, per-turn tokens, `turn_success`, `turn_end_reason` |
| `prompt_submitted` | Each user prompt is recorded | `id`, `session_id`, `turn_index`, `version`, `os`, `arch` |
| `telemetry_opt_out` | The user disables telemetry from the settings screen | `id`, `step` = `telemetry_settings`, `version`, `os`, `arch` |
| `feedback` | User runs `/feedback` or `maintainer_feedback` tool | `feedback_text`, `feedback_rating`, `feedback_reason` |
| `discovery` | Each `discover_tools` attempt completes | `request_id`, `phase`, `category`, `selected_tool`, `outcome`, `failure_reason`, `latency_ms` |
| `todo_session` | Active session with todos ends | `correlation_id`, `todos_created`, `todos_completed`, `todos_abandoned`, confidence score aggregates including `feedback_loop_relevance_*` and `feedback_loop_coverage_*` |
| `transcript` | Consented non-empty session closes or crashes | `upload_id`, `id`, `consent_version`, `provider`, `model`, `message_count`; body in R2, metadata in the `transcript_uploads` table |
| `usage_report` | Each completed model response | Token counts and model labels only, plus `usage_contract_version` and `occurred_at`; delivered to `/v2/usage` and rolled up through `usage_report_ledger` into `daily_model_usage` and `daily_model_usage_v2` (migrations `0027`, `0031`) |
| `desktop_active` | Desktop companion active check-in | Fleet activity reporting in `desktop-fleet.sql` (migration `0029`) |
| `desktop_upgrade` | Desktop companion version change | Fleet upgrade reporting (migration `0029`) |
| `desktop_update` | Desktop self-update attempt completes | Outcome fields in `desktop_update_details` by `install_kind` and failure stage (migration `0029`) |

- Website and subscription events (`web_pageview`, `web_cta_click`, `web_vital`, `web_error`, `install_funnel`, `subscription_login`, `subscription_activated`, `subscription_budget_exhausted`, `subscription_router_error`, `account_linked`) are emitted by the site and the subscription service, not by the CLI client.
- Session cadence fields include hour and weekday buckets, gap seconds, burst counts, and concurrency snapshots.
- Agent time fields include active milliseconds, model versus tool split, idle time, and time to first useful action.
- Retention helpers include days since install plus active days in the last 7 and 30 days.
- Full field definitions live in `TELEMETRY.md`.
- Storage definitions live in `telemetry-worker/schema.sql` and migrations `0001` through `0031`.

## Identity Resolution

- Identity is a random UUID (`telemetry_id`) generated on first run.
- The ID is stored at `~/.jcode/telemetry_id`.
- The ID is not derived from machine, username, email, or account identity.
- The client links telemetry to account identity only for provider OAuth emails, a separate path documented in `TELEMETRY.md`; ordinary usage events carry no account identity.
- Website beacons use a separate random `visitor_id` and per-click `conversion_id`.
- Todo session aggregates use a fresh per-session `correlation_id`, never the persistent install ID.
- Deletion requests are honored through the persistent `telemetry_id`.
- Discovery correlation uses a fresh per-session UUID, never reused across sessions.

## Privacy and Compliance

- Opt out with `jcode telemetry disable` for a persistent CLI setting.
- Opt out with `JCODE_NO_TELEMETRY=1` environment variable.
- Opt out with `DO_NOT_TRACK=1` environment variable.
- Opt out with the `~/.jcode/no_telemetry` file marker.
- Opt-out short-circuits telemetry before any network request.
- `JCODE_NO_TELEMETRY` and `DO_NOT_TRACK` also override transcript sharing and prevent uploads.
- Ordinary telemetry contains no prompts, responses, code, file paths, tool inputs, tool outputs, MCP names, IPs, error text, or precise timestamps.
- Geography is country code only (`request.cf.country`), added by the Worker edge and never sent by the client.
- Transcript sharing is a separate opt-in program, off by default, selected as Share full transcripts in telemetry settings.
- Transcript consent is versioned (`consent_version`) so older consent cannot silently cover new content programs.
- Transcript bodies are limited to 8 MiB and stored in a private R2 bucket with a 30-day deletion lifecycle rule.
- Secrets are redacted to `[REDACTED_SECRET]` on the client and checked again by the Worker before R2 write.
- Individual event records are retained up to 12 months, then deleted.
- High-volume raw events are pruned nightly after rollup (turn and session start and onboarding steps about 30 days, upgrades about 60 days, auth success about 180 days, session summaries up to 12 months, session concurrency and desktop updates 365 days, web pageviews and install funnel stages 90 days, todo sessions 365 days).
- The private `oauth_accounts` table is pruned after 90 days and the `usage_report_ledger` receipts after 8 days.

## Funnels and Key Metrics

| Funnel | Steps | Defined in |
|---|---|---|
| Activation | `install`, `auth_success`, `onboarding_step`, `session_start` | `telemetry-worker/` SQL (`dau.sql`, `users.sql`, `conversion.sql`, migration `0020`) |
| Onboarding completion | `onboarding_step` milestones through first prompt and first useful action | `TELEMETRY.md` plus `telemetry-worker/migrations/` |
| Session success | `session_start`, `turn_end`, `session_end` or `session_crash` with `session_success` | `telemetry-worker/schema.sql` (`events`, `session_details`, `turn_details`) |
| Retention | Daily active rollups with burst, cadence, and active-day fields | `telemetry-worker/dau.sql` plus `daily_active_users` table |
| Feedback signal | `feedback` rating, reason, and text | `telemetry-worker/schema.sql` plus migration `0009` |
| Discovery reliability | `discovery` phase and outcome by category and tool | `telemetry-worker/discovery.sql` plus migration `0017` |
| Todo completion | `todo_session` created, completed, and abandoned counts with confidence aggregates | Migration `0024` plus `todo_session_details` table |
| Transcript program | `transcript_uploads` metadata only, bodies in R2 | Migration `0025` plus `transcript_uploads` table |

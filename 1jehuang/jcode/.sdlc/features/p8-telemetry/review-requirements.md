---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.
The privacy model changed in v0.97.0, so this is a disclosure drift and not a cosmetic one.

### Completeness

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-9 | The system shall collect the provider OAuth account email of an account actually used for model providers, store it in a dedicated private table, and never mix it into ordinary event rows. | `crates/jcode-telemetry-core/src/oauth_account.rs:44` (`enqueue_oauth_account`), `crates/jcode-telemetry-core/src/oauth_account.rs:185,213` (the two endpoints), `telemetry-worker/migrations/0030_oauth_accounts.sql`, `TELEMETRY.md:83-127`. |
| FR-10 | The system shall show a one-time notice before uploading a provider OAuth account email, and only upload after the notice has actually been rendered. | `crates/jcode-telemetry-core/src/oauth_account.rs:14-16,18-22` (notice text and receipt), `crates/jcode-tui/src/tui/app/tui_state.rs:1149-1154`, `crates/jcode-tui/src/tui/app/remote/server_events.rs:1866`. |
| FR-11 | The system shall emit a per-response usage report to a dedicated usage endpoint through a durable, retrying outbox. | `crates/jcode-telemetry-core/src/lib.rs:42` (`/v2/usage`), `crates/jcode-telemetry-core/src/usage_outbox.rs:101-213`, `crates/jcode-usage-types/src/lib.rs:711-714` (`usage_contract_version`, `occurred_at`). |
| FR-12 | The system shall report runtime session concurrency and Desktop fleet activity as separate event families. | `crates/jcode-telemetry-core/src/concurrency.rs:498`, `crates/jcode-telemetry-core/src/desktop.rs:110,122,144`, migrations `0026` and `0029`. |
| FR-13 | The system shall offer telemetry collection levels through the CLI and the TUI, and document that the middle level still includes the provider OAuth account email. | `src/cli/args.rs:622-633`, `src/cli/telemetry.rs`, `crates/jcode-tui/src/tui/app/commands.rs:3899-3950` (the `everything`, `no-prompts`, `nothing` levels), `crates/jcode-tui/src/tui/app/commands.rs:3926`. |

### Clarity

| ID | Current wording | Problem | Suggested wording |
|---|---|---|---|
| FR-1 | "The system shall emit structured telemetry events for install, upgrade, auth success, onboarding step, feedback, sponsored discovery, session lifecycle, and turn end." | The event list is missing session start, onboarding trace, todo session, per-response usage report, concurrency, prompt submitted, telemetry opt-out, and Desktop fleet activity. | "The system shall emit structured telemetry events for install, upgrade, auth success, onboarding step, onboarding trace, feedback, sponsored discovery, session start, session lifecycle, turn end, prompt submitted, todo session, per-response usage report, concurrency, telemetry opt-out, and Desktop fleet activity." |
| FR-3 | "The system shall respect opt-out via `JCODE_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, or a file marker." | The marker path is not named, and the `/telemetry nothing` level is missing. | "The system shall respect opt-out via `JCODE_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, the `~/.jcode/no_telemetry` file marker (also written by `jcode telemetry disable`), or the `/telemetry nothing` level." |
| FR-4 | "The system shall never collect message content, prompts, or responses." | True for content, but the document is silent on identity, which changed in v0.97.0. | "The system shall never collect message content, prompts, or responses, except that it may collect the provider OAuth account email of an account actually used for model providers, as a separately-stored, non-anonymous record." |

### Overview

The overview paragraph lists only the anonymous event families.
It should state that telemetry is anonymous by default, with one exception: it may include the provider OAuth account email of an account actually used for model providers, which links installation usage to account identity.

### Non-functional requirements

NFR-1 reads "Event payloads must not contain session content or identifying message text."
Extend it: identifiable provider OAuth emails are permitted only in the dedicated `oauth_accounts` table, never in ordinary event rows or Analytics Engine.

### Constraints

The constraints section lists only "Opt-out must be discoverable and documented (`TELEMETRY.md`)."
Extend it: opt-out is also discoverable through `jcode telemetry status`, `jcode telemetry enable`, `jcode telemetry disable`, and the `/telemetry` command, and the `no-prompts` telemetry level still includes the provider OAuth account email. Only `nothing` or a full opt-out stops identity collection.

### Open questions

Open Question 1 is partly answerable: ordinary event records are retained up to 12 months, provider OAuth account records for 90 days (pruned nightly), and transcript bodies for 30 days in R2.
Rollup timing is still inferred from the worker SQL.

## Conflicts

| Requirements | Type | Description | Suggested Resolution |
|---|---|---|---|
| FR-4, NFR-1 | Functional vs non-functional tension | FR-4 and NFR-1 read as a blanket ban on identifying data, but FR-9 (identity collection) and the v0.97.0 code require one identifiable field. | Reword FR-4 and NFR-1 to state the single permitted exception, so the ban on content collection and the ban on mixed identity data both hold. |

## Clarity

No other clarity issues found.

## Testability

The acceptance criteria list ends at NFR-4 and covers none of the capabilities in FR-9 through FR-13.
Each added FR needs at least one Gherkin acceptance criterion, and the identity path in particular needs a criterion that shows the notice-before-upload ordering.

## Feasibility

No issues found.

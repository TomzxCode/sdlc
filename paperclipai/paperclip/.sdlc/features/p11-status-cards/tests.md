---
title: "Status Cards"
status: done
---

# Test Plan: Status Cards

## Scope

Tests cover validation, compile prompt construction, generation write authorization, query execution, change detection, refresh policy, scheduler behavior, idle deadlines, database migrations, and Status page components.
Out of scope: dedicated browser end-to-end coverage and the internal behavior of the summarizer model.

## Test Files Found

| File | Coverage |
|---|---|
| `packages/db/src/status-card-migrations.test.ts` | Status-card migration reapplication |
| `packages/db/src/status-card-reason-upgrade.test.ts` | Migration upgrade from base revisions without losing comment uniqueness or read history |
| `packages/shared/src/validators/status-card.test.ts` | Refresh policy timezone validation |
| `server/src/__tests__/status-card-compile-prompt.test.ts` | Compile prompt content and generation payload |
| `server/src/__tests__/status-card-update-engine.test.ts` | Fingerprints, triggers, policy, active hours, update kind, and mentions |
| `server/src/__tests__/status-card-idle-schedule.test.ts` | Idle deadline projection and dirty snapshot handling |
| `server/src/__tests__/status-card-notifications.test.ts` | Delivery queue isolation and company-scoped hints |
| `server/src/__tests__/status-card-evaluation-work.test.ts` | Scheduled evaluation, source hints, restart recovery, policy gates, and sleep interaction |
| `server/src/__tests__/status-cards.test.ts` | Routes, services, privacy, authorization, generation writes, and concurrency |
| `ui/src/lib/status-card-state.test.ts` | Lifecycle derivation and refresh policy descriptions |
| `ui/src/pages/StatusCards/StatusCardSettingsForm.test.tsx` | Cost preview and advanced settings visibility |
| `ui/src/pages/StatusCards/StatusCardTile.test.tsx` | Tile lifecycle rendering and actions |
| `ui/src/pages/StatusCards/format.test.ts` | Ledger rollups and cost estimates |

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-U1 | Valid and invalid IANA timezones in refresh policy | Timezone strings with one valid and one invalid value | Valid value parses and invalid value throws |
| TC-U2 | Compile prompt has no undeclared skill dependency | Generated compile description | No skill requirement that the summarizer run lacks |
| TC-U3 | Compile prompt inlines query format and writeback sequence | Generated compile description | Query format rules, untrusted-data rule, query write, and summary write are present |
| TC-U4 | Compile payload is copyable and parseable | Generated compile description with a generation issue id | Example query body and generation payload parse |
| TC-U5 | Fingerprint diff keeps status and membership changes | Watched issue snapshots with status transitions and membership changes | Terminal and non-terminal status changes plus membership changes are retained |
| TC-U6 | Human comments are distinct from generic updates | Issue snapshots with changed comment time and changed update time | Human comment and updated change kinds are separate |
| TC-U7 | Change signature captures replacement sets | Equal-sized change sets with different issue ids | Pending signature changes |
| TC-U8 | Manual mode schedules no background evaluation | Manual refresh policy | Next evaluation is null |
| TC-U9 | Policy gates are enforced | Debounce window, hourly rate cap, active hours, and token cap | Each gate defers or pauses evaluation |
| TC-U10 | Unchanged reactive evaluation is disarmed | No filtered changes and no membership deadline | No recurring evaluation is scheduled and exact pending eligibility remains |
| TC-U11 | Empty-window changes avoid a repeating scan | Pending change with no active hours window | No repeating eligibility scan is produced |
| TC-U12 | Active-hours conversion work is bounded | Twenty cards and repeated company writes | Formatter construction is reused and conversion work stays bounded |
| TC-U13 | Cached opening is invalidated correctly | Clock rollback and changed policy values | Cached opening is discarded |
| TC-U14 | Historical timezone offsets use the precise instant | Offset with a seconds component | Eligibility is checked at the exact instant before a minute opening |
| TC-U15 | Formatter and opening caches are retained within limits | Repeated active-hours calculations | Cache retention stays bounded |
| TC-U16 | Update kind follows rebuild rules | Drift, query version, configuration, restore, and incremental history inputs | Full rebuild or incremental update is selected |
| TC-U17 | Summary mentions are extracted | Identifiers and issue links in Markdown | Identifier and issue-link mentions are returned |
| TC-U18 | Idle schedule keeps expected deadlines | Manual, unchanged reactive, archived, repaired error, and known deadline reasons | Deadlines are retained only where policy requires them |
| TC-U19 | Dirty idle snapshot is rejected before querying | Row revision changed or owner changed during read | Snapshot is blocked |
| TC-U20 | Notification hints stay within known queues | Scoped and unscoped status-card hints | Execution queues remain intact and only known status-card scopes are emitted |
| TC-U21 | Lifecycle derivation covers every display state | Card state, archive, generation claim, and pending changes | Correct UI lifecycle is returned |
| TC-U22 | Refresh policy description covers each mode | Manual, interval, and reactive policies | One-line description matches the policy |
| TC-U23 | Settings cost preview follows policy | Manual, interval, and reactive policies with active hours and token cap | One-line estimate matches the policy |
| TC-U24 | Advanced settings visibility follows mode | Manual and auto-updating policies | Advanced group is hidden or revealed as a collapsed group |
| TC-U25 | Tile renders each lifecycle | Fresh, stale, compiling, updating, error, paused, and archived cards | Labels, banners, summary retention, and actions match the lifecycle |
| TC-U26 | Tile actions do not open the card | Click on menu trigger and Run now action | Card route is not opened |
| TC-U27 | Ledger rollups and cost estimates are correct | Lifetime rows, current day rows, and policy inputs | Compile rows are excluded and cost estimates match active hours and caps |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-I1 | Status-card migration can be reapplied | Schema already exists | Migration reapplies without failure |
| TC-I2 | Base revisions upgrade without data loss | Database at 0418 or master0419 | Comment uniqueness and read history survive the upgrade |
| TC-I3 | Experimental gate hides the API | Flag disabled | Status-card endpoints return 404 |
| TC-I4 | Compile wakeup failure rolls back creation | Wakeup throws during create | New card is removed and the caller receives the error |
| TC-I5 | Missing company issue prefix creates nothing | Company link cannot be resolved | No card is inserted |
| TC-I6 | Activity log failure keeps a queued compile | Log mutation fails after compile queue | Card and generation task remain |
| TC-I7 | Full card lifecycle works through the API | Enabled feature and actor with permissions | Create, patch, archive, restore, list updates, and delete succeed |
| TC-I8 | Due-card evaluation continues after one failure | One scheduled refresh fails | Other due cards still evaluate |
| TC-I9 | Legacy and invalid saved queries stay readable | Normalizable and non-normalizable stored queries | Counts normalize and read errors do not break cards |
| TC-I10 | Private task content is redacted | Watched set includes a private task | Summary body is null and watched-issue details are redacted |
| TC-I11 | Human comments trigger refresh | Watched issues carry human comments | Refresh is enqueued |
| TC-I12 | Mutations require task assignment permission | Actor lacking `tasks:assign` | Request is denied |
| TC-I13 | Agent authoring limits are enforced | Active company agent authors cards and long prompts | Prompt length and twenty-card limit are enforced |
| TC-I14 | Restore forces a full rebuild | Archived manual card with a compiled query | Restore refresh uses full kind |
| TC-I15 | Assignment wakeup failure cancels refresh task | Wakeup throws during refresh | Generation issue is cancelled |
| TC-I16 | Lost optimistic claim cancels its task | Card is archived while another refresh claims it | Unclaimed task is cancelled and the winner remains writable |
| TC-I17 | Stalled or cancel-led generation is finalized | Generation task done, cancelled, blocked, or without summary | Card moves to error, claim clears, and ledger row fails |
| TC-I18 | Board-authored cards are not agent-manageable | Agent tries to manage a board-authored card | Request is forbidden |
| TC-I19 | Compile tasks deduplicate by prompt | Same active prompt hash | Existing task is reused |
| TC-I20 | Blocked setup can be re-kicked | Setup task is blocked | Run now is re-offered and task reopens |
| TC-I21 | Generation writes require exact writer identity | Wrong agent, issue, or run | Write is rejected |
| TC-I22 | Per-card summarizer can write | Card has a summarizer override | Generation issue is routed and write succeeds |
| TC-I23 | Cancelled generation cannot write | Generation issue is cancelled | Write is rejected |
| TC-I24 | Cross-company write probes return 404 | Actor outside the card's company | Query and summary writes return 404 |
| TC-I25 | Summary mentions join the watched set | Summary references issues by identifier and link | Mentioned issues are stored and later changes are tracked |
| TC-I26 | Query, summary, dry-run, and recompile work end to end | Compiled card with an active generation run | Version increments and dry-run returns live matches |
| TC-I27 | Scheduler settles quiet history without recurring SQL | Disabled, manual, and unchanged reactive cards | No unnecessary queries repeat |
| TC-I28 | Issue hints drive debounce and one durable wake | Ordinary issue change on reactive card | One wake is assigned, result is written, and work becomes quiet |
| TC-I29 | Source hints consumed during writeback are rechecked | Relevant and irrelevant committed edits | Only relevant edits trigger a new evaluation |
| TC-I30 | Summary rollback clears post-commit recheck duty | Summary write fails after source hint | Transaction and obligation roll back together |
| TC-I31 | Manual and interval cadence survives evaluation | Manual or interval card writeback | No reactive recheck is added |
| TC-I32 | Hint coalescing preserves other deadlines | One hundred committed source writes | Another company's saved deadline is preserved |
| TC-I33 | Evaluation recovers after restart and drain | Pending debounce, hours, rate, budget, legacy claim, and retry state | Eligibility is restored without acting early |
| TC-I34 | Search membership deadlines survive restart | Relative expiry and off-page candidates | Eventual removal and offset-ranked refresh still occur |
| TC-I35 | Sleep sees committed work | Source hint with null card deadline during drain | Sleep is blocked until work settles |

## End-to-End Tests

No dedicated browser end-to-end test was found for the Status page.

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-E1 | Feature flag disabled | API returns 404 without exposing cards |
| TC-E2 | Compile wakeup fails | New card is rolled back |
| TC-E3 | Activity log fails | Card with queued compile remains |
| TC-E4 | Legacy or invalid stored query | Hydration remains readable |
| TC-E5 | Private task in watched set | Summary and watched-issue details are redacted |
| TC-E6 | Wrong summarizer, generation issue, run, or company | Write is rejected |
| TC-E7 | Archived card | Compile, refresh, query, and summary writes are rejected |
| TC-E8 | Blocked or cancelled generation | Claim clears and card can be re-kicked or fails cleanly |
| TC-E9 | Concurrent refresh claim | Losing task is cancelled and the newer claim stays writable |
| TC-E10 | Debounce, hourly rate, active hours, and token cap | Work is deferred or paused with a saved eligibility deadline |
| TC-E11 | Clock rollback and historical timezone offset | Exact eligibility instant is used |
| TC-E12 | Dirty idle snapshot or changed owner | Sleep projection is blocked |
| TC-E13 | One database connection during cancellation | Refresh cancellation does not deadlock |
| TC-E14 | Assignment wakeup failure | Generation issue is cancelled and evaluation can settle after retry |

## Test Infrastructure

- Vitest drives unit, integration, component, and migration tests.
- Supertest with an Express test app exercises status-card routes.
- Embedded Postgres support and an optional external Postgres URL exercise migrations and route tests.
- Database work signals verify queue hints without relying on timing.
- React component tests render tiles and settings forms with local card fixtures.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-I3, TC-I6, TC-I7 |
| FR-2 | TC-I7, TC-I12, TC-I13, TC-I18, TC-I24 |
| FR-3 | TC-I4, TC-I5, TC-I6, TC-I7, TC-I13 |
| FR-4 | TC-U2, TC-U3, TC-U4, TC-I19, TC-I20 |
| FR-5 | TC-U3, TC-U4, TC-I21, TC-I22, TC-I23, TC-I26 |
| FR-6 | TC-U16, TC-I7, TC-I14, TC-I16, TC-I20, TC-I26 |
| FR-7 | TC-U5, TC-U6, TC-U7, TC-U10, TC-I28, TC-I29 |
| FR-8 | TC-U17, TC-I25, TC-I26 |
| FR-9 | TC-U8, TC-U9, TC-U10, TC-U11, TC-U12, TC-U13, TC-U14, TC-U15, TC-U23, TC-U27, TC-I31, TC-I33 |
| FR-10 | TC-U21, TC-U22, TC-U24, TC-U25, TC-U26 |
| FR-11 | TC-I10, TC-I26 |
| FR-12 | TC-I17 |
| FR-13 | TC-I26 |
| FR-14 | TC-U23, TC-U25, TC-U27 |
| NFR-1 | TC-I21, TC-I22, TC-I23, TC-I24 |
| NFR-2 | TC-I4, TC-I16, TC-I30 |
| NFR-3 | TC-U8, TC-U10, TC-U11, TC-U18, TC-I27, TC-I32 |
| NFR-4 | TC-U18, TC-U19, TC-U20, TC-I33, TC-I35 |

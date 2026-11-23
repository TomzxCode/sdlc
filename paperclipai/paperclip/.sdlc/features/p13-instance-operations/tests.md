---
title: "Instance Operations and Settings"
status: done
---

# Test Plan: Instance Operations and Settings

## Scope

Tests cover shared settings validators, settings service normalization and overlays, settings caching, task drain state and audit ordering, Cloud control authority, Cloud lifecycle readback and unarchive, manual and automatic database backups, server metrics, and the general and experimental settings pages.
Out of scope are the external Cloud control plane that signs assertions, database restore because no HTTP endpoint exists, and the detailed behavior of every feature toggled by an experimental flag.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Experimental validator defaults and patches are tested by `packages/shared/src/validators/instance.test.ts`, including "defaults legacy composer submission off", "keeps Notebook disabled", "defaults chat connectors off", "strips retired watchdog and liveness auto-recovery settings", and "strips server-managed worktree run execution fields from patches". | Legacy storage, empty storage, explicit booleans, and deprecated keys | Defaults match the registry, explicit patches are accepted, and retired or server-managed keys are stripped. |
| TC-2 | Experimental service normalization is tested by `server/src/__tests__/instance-settings-service.test.ts`, including "retains the legacy composer preference", "keeps Agent Chat on", "defaults remote workspace enrollment on", "keeps chat connectors opt-in", "ignores retired experimental flags", and "retains the deprecated ingress key". | Legacy, invalid, empty, and explicitly stored settings | Current flags keep their schema defaults and legacy values do not reset unrelated settings. |
| TC-3 | Worktree run activation is tested by "sets worktree run execution activation fields", "clears worktree run execution activation fields", "refreshes the activation cutoff", "strips client-supplied activation fields", "resolves worktree run execution as armed only when the cutoff matches the current instance", "fails closed when worktree run execution is missing a cutoff", "fails closed when worktree run execution was activated by another instance", and "fails closed on settings read errors and avoids reads outside worktree runtimes". | False to true and true to false patches, client-supplied activation fields, and mismatched instance ids | The service sets, clears, and refreshes the cutoff, strips client fields, and treats missing or mismatched activation as not armed. |
| TC-4 | Settings caching is tested by `server/src/__tests__/instance-settings-cache.test.ts`, including "serves repeated hot reads from one statement", "reads its own writes in this process at once", "sees a default environment committed in a caller's transaction once it commits", "takes a change made by another process within the cache bound", "never shares cached rows with callers that mutate them", "reads inside a transaction bypass the cache", "never stores a read that started before an invalidation", "drops the cached row when another process announces a settings change", and "announces a settings change before the other wakes of the same write". | Repeated reads, local writes, external announcements, and transactional reads | Hot reads share one statement, writes are visible immediately, stale rows are invalidated, and callers cannot mutate cached rows. |
| TC-5 | Operator defaults are tested by `server/src/__tests__/instance-settings-operator-defaults.test.ts` and `packages/shared/src/setting-defaults.test.ts`, including "throws on malformed policy JSON (fail closed)", "overlays reads but never persists the operator value", "does not let a full-GET echo promote the operator value into a choice", "fails closed on an invalid value for a known field", and "keeps every registry entry a real general-settings field". | Parsed operator policy, schema-default values, explicit choices, and full-object echoes | The policy fails closed when malformed, overlays values on reads, and strips echoes on writes. |
| TC-6 | Cloud catalog defaults are tested by `server/src/__tests__/instance-settings-cloud-defaults.test.ts`, including "re-asserts the Cloud default when the tenant row and the overlay omit the flag", "keeps an explicit tenant value", "lets a managed feature value win through the overlay", "does not persist the self-hosted default on Cloud during an unrelated write", and "persists an explicit Cloud opt-in". | Cloud and self-hosted instances with missing, echoed, explicit, and managed flag values | Cloud defaults are reasserted on reads, explicit tenant choices are kept, and unrelated writes do not persist defaults. |
| TC-7 | Managed experimental overlays are tested by `server/src/__tests__/instance-settings-managed-overlay.test.ts`, including "fails closed at construction on a malformed managed config", "overlays managed values on getExperimental and exposes managedKeys", "overlays managed values on get()", "leaves the self-hosted read path unchanged", "never persists the overlay", and "does not let managed metadata leak into self-hosted writes". | Managed config, self-hosted config, Chat connectors, Notebook, and staging overrides | Managed values and `managedKeys` appear in responses, stored values stay unchanged, and malformed config throws. |
| TC-8 | Hidden-setting keys and parsing are tested by `packages/shared/src/settings-visibility.test.ts`, including "expands the experimental wildcard into concrete keys without hiding the page", "allows only named exceptions", "keeps explicit hides and parent page restrictions stronger than exceptions", and "treats a hidden Experimental page as hiding every toggle". | Wildcards, exceptions, unknown keys, page restrictions, and section keys | Hidden keys resolve without opening controls stronger than an explicit restriction. |
| TC-9 | Metrics collection is tested by `server/src/__tests__/server-metrics.test.ts`, including "reports rates and utilization over the sliding window", "expires buckets by elapsed time when the rotation timer fires late", "reports the real window after a block longer than the window", "reports latency percentiles only for the window", "counts missed lease renewals since start", "reads the kill switch strictly and defaults it off", and "serializes exactly the fixture the scale-ramp harness parses". | Controlled clocks, recorded statements, latency samples, and kill-switch values | Snapshots contain the version 1 fields, windowed rates, and cumulative missed renewals. |
| TC-10 | Process-local task drain state is tested by `server/src/__tests__/heartbeat-task-drain.test.ts`, including "start_task_drain_suppresses_admission", "stop_task_drain_restores_admission", "null_ttl_produces_no_expiry", "an_expired_ttl_ends_the_drain_and_restores_admission", and "status_reports_quiescent_when_both_promise_sets_are_empty". | Start, stop, null TTL, expired TTL, and active promise sets | Admission follows drain state, expiry restores admission, and status reports quiescence. |
| TC-11 | Task drain work release is tested by `server/src/__tests__/heartbeat-task-drain-admission-release.test.ts`, including "releases the run, wakeup, and issue lock when a task drain trips right after the run is claimed", "preserves the plugin worker manager when DELETE releases a queued sandbox run", "dispatches existing queued work at the drain deadline", "keeps a wake that arrives during a task drain queued and runs it once the drain lifts", and "leaves the run row running for the orphan reaper when the atomic release fails". | Runs claimed around drain boundaries and queued wakes | Work is released, queued, or dispatched in the expected order and failed atomic releases stay visible to the reaper. |
| TC-12 | Automatic backup scheduling is tested by `server/src/__tests__/database-backup-work.test.ts`, including "waits for the actual backup deadline", "startup while draining preserves the first due backup", "reports a failed attempt and retries at the next scheduled slot", "keeps the schedule after the backup owner skips an overlapping manual backup", "coalesces wakes during a slow backup and skips missed slots", "shutdown waits for the active backup", and "restart establishes a fresh interval". | Controlled timers, draining state, failures, manual overlap, and shutdown | One backup runs per due slot, failures retry, overlaps are skipped, and shutdown waits for the active run. |
| TC-13 | Idle backup durability is tested by `server/src/__tests__/idle-database-backup.test.ts`, `server/src/__tests__/idle-database-backup-sync.test.ts`, and `server/src/__tests__/database-backup-owner.test.ts`, including "keeps a restart marker until a fresh valid backup is complete", "rejects a missing archive and symlinked archive or marker", "syncs the marker, archive and directory entries before reporting completion", and "marks before retention access and retains the marker until a verified wake backup". | Restart markers, archives, symlinks, receipts, and scheduled slots | Markers survive until a verified backup completes, unsafe paths are rejected, and single-flight ownership is preserved. |
| TC-14 | Cloud control authority is tested by `server/src/__tests__/cloud-control-task-drain.test.ts`, including "accepts a well-formed assertion bound to the expected action", "rejects a replay", "rejects an assertion for a different action", "rejects an assertion for another stack", "rejects expired assertions", "installs a synthetic instance-admin board actor", "installs the complete closed body only after its exact-byte binding", and "does not turn body-read authority into start or stop authority". | Signed Ed25519 assertions, replays, wrong actions, wrong stacks, and exact body bytes | Only the exact action and request can authorize the route, and a status read never grants mutation. |

Files: `packages/shared/src/validators/instance.test.ts`, `packages/shared/src/settings-visibility.test.ts`, `packages/shared/src/setting-defaults.test.ts`, `server/src/__tests__/instance-settings-service.test.ts`, `server/src/__tests__/instance-settings-cache.test.ts`, `server/src/__tests__/instance-settings-operator-defaults.test.ts`, `server/src/__tests__/instance-settings-cloud-defaults.test.ts`, `server/src/__tests__/instance-settings-managed-overlay.test.ts`, `server/src/__tests__/server-metrics.test.ts`, `server/src/__tests__/heartbeat-task-drain.test.ts`, `server/src/__tests__/heartbeat-task-drain-admission-release.test.ts`, `server/src/__tests__/database-backup-work.test.ts`, `server/src/__tests__/idle-database-backup.test.ts`, `server/src/__tests__/idle-database-backup-sync.test.ts`, `server/src/__tests__/database-backup-owner.test.ts`, `server/src/__tests__/cloud-control-task-drain.test.ts`

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-15 | Settings HTTP reads and writes are tested by `server/src/__tests__/instance-settings-routes.test.ts`, including "allows local board users to read and update experimental settings", "allows local board users to read and update general settings", "allows non-admin board users to read general settings", "rejects non-admin board users from updating general settings", "rejects agent callers", "does not expose the retired liveness auto-recovery endpoints", "accepts the instance-wide Streamlined UI preference", and "strips server-managed worktree run execution fields before updating experimental settings". | An Express app with mocked services and board, agent, and anonymous actors | Board actors read settings, only local implicit or admin actors write, and retired routes and fields stay hidden or stripped. |
| TC-16 | Default environment validation is tested by "allows local board users to read and update the instance default environment", "refuses an instance default that gives inheriting agents an unprepared plugin", "writes an explicit default as a plain set value, touching no environment row", and "rejects unknown defaultEnvironmentId values with 422". | Environments and agents with plugin readiness fixtures | Valid defaults persist, unknown ids return 422, and unprepared inheriting agents block the write. |
| TC-17 | Settings floors are tested by "Cloud stack admin experimental settings access", "executionMode floor on cloud-managed instances", "operator-hidden settings floor", and "Cloud staging experiments", including "keeps operator-hidden experimental settings locked for stack admins", "allows a same-value executionMode echo", "deep-compares hidden backupRetention echoes", "enforces a wildcard allowlist", and "lets a staging admin change hidden experiments but keeps general settings locked". | Cloud-managed, staging, operator-hidden, and self-hosted configurations | Managed and hidden values cannot change, same-value echoes succeed, and staging restrictions stay scoped. |
| TC-18 | Task drain status and holds are tested by "task drain", including "returns the idle status", "restricts the on-demand upgrade report to instance operators", "acquires an owned bounded idle hold", "rejects an unbounded or invalid idle TTL", "rejects replacement and ownerless or stale release of an idle hold", "returns the opt-in instance-wide safety report", "collects fixed-key diagnostics only through the privileged safety report", and "reserves scheduling capability for verified Cloud control callers". | Mock heartbeat service, admin and member actors, and signed control capability fixtures | Status reads stay authorized, idle holds require a valid TTL and owner, and privileged reports require the expected actor. |
| TC-19 | Task drain audit and transition ordering are tested by "writes an activity record for every company, then applies the same drain values", "starts an indefinite drain when the caller sends no ttlMs", "writes an activity record for every company, then stops the drain", "does not apply a drain when the company list read fails", "commits no activity record for any company when one company's audit write fails", "still reports the started drain when publishing its committed audit record fails", "does not dispatch work when the drain-stop audit transaction rejects", "reports the committed drain release even when queued dispatch fails", "still publishes the second company's record when the first company's publish fails", and "queues an overlapping DELETE behind a POST whose audit transaction is still pending". | Mock database transaction, audit writers, activity publisher, and heartbeat service | Audit rows commit for all companies before live state changes, ordering is serialized, and post-commit failures do not rewrite the result. |
| TC-20 | Cloud body-bound task drain status is tested by "signed incoming capability handoff", including "reads the same owner and deadline scope through the real body-bound middleware and production handler", "rejects body tampering", "rejects unsigned and actor-only body authority and cross-route method replay", "passes only the immutable signed catalog through real middleware and the production route", "passes the signed deadline catalog only for its explicit named query", "rejects a tampered catalog signature", "leaves legacy signed reads without a catalog conservative", and "cannot install capabilities from tenant, actor, query or body values". | Generated Ed25519 key pair, signed cloud assertion, and exact raw JSON body | The route accepts only the signed, body-bound catalog and rejects tampering, replay, and capability smuggling. |
| TC-21 | Cloud lifecycle readback and unarchive are tested by "reports the primary company status and how many other companies are not archived", "reports a missing primary company without failing", "hides the cross-company lifecycle summary from non-admin board members", "answers 404 when the instance is not cloud-managed", "unarchives an archived primary company as a system actor", "attributes a human admin's unarchive to that admin", "is idempotent", and "requires instance admin rights to unarchive". | Cloud stack environment, company rows, and mocked company service | Lifecycle reports the pinned primary state, non-cloud instances return 404, and unarchive is admin-only and idempotent. |
| TC-22 | Manual backup routes are tested by `server/src/__tests__/instance-database-backups-routes.test.ts`, including "runs a manual backup for an instance admin and returns the server result", "allows local implicit board access", "rejects non-admin board users", "rejects agent callers", "returns conflict when another server backup is already running", "floors the manual trigger off for every instance admin on a cloud-managed instance", and "floors the manual trigger off for a computed cloud_tenant owner-admin". | Mock backup service and cloud or self-hosted instance configuration | Admins receive the full result, overlapping backups return 409, and non-admins, agents, and cloud tenants are blocked. |
| TC-23 | Server metrics routes are tested by `server/src/__tests__/instance-server-metrics-routes.test.ts`, including "serves numbers to an instance admin only, and they move with load" and "is absent and collects nothing when the kill switch is off". | A started server with metrics enabled or disabled and admin, member, and agent keys | Only the admin receives the version 1 snapshot, values move under load, no secrets appear, and the disabled route returns 404. |

Files: `server/src/__tests__/instance-settings-routes.test.ts`, `server/src/__tests__/instance-database-backups-routes.test.ts`, `server/src/__tests__/instance-server-metrics-routes.test.ts`, `server/src/__tests__/cloud-control-task-drain.test.ts`

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-24 | General settings page behavior is tested by `ui/src/pages/InstanceGeneralSettings.test.tsx`, including "uses the Cloud-managed top-level logout without calling local auth", "keeps authenticated self-hosted sign-out local", "disables settings changes while sign-out is pending", "hides an operator-hidden field-backed section and a UI-only section", "keeps loaded settings on screen when a refetch fails transiently", and "shows readable copy and a Retry button when settings fail to load". | Render the page with cloud or self-hosted settings, hidden sections, pending actions, and failing refetches | Sign-out and settings writes cannot overlap, hidden sections disappear, and read failures are recoverable. |
| TC-25 | Experimental settings page behavior is tested by `ui/src/pages/InstanceExperimentalSettings.test.tsx`, including toggle patches for Streamlined UI, chat connectors, GitHub review bots, memory connectors, Classic Task Interface, Decisions, fast responses, goals sidebar, built-in agents, beta skills, and Summaries, plus "renders a managed key locked with the badge while unmanaged keys stay editable", "fails closed with a re-enable hint", "renders nothing for an operator-hidden toggle", and "shows readable copy and a Retry button". | Render the page with managed keys, hidden keys, dependency changes, stale activation, and failed refetches | Managed controls lock, hidden controls disappear, dependent toggles follow policy, and failures stay readable. |

Files: `ui/src/pages/InstanceGeneralSettings.test.tsx`, `ui/src/pages/InstanceExperimentalSettings.test.tsx`
These are React Testing Library component suites.
No browser automation suite was found for this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-26 | Hidden general and experimental values are echoed back from a full-object form | The write succeeds only when every hidden value matches the stored value. |
| TC-27 | `executionMode` is echoed unchanged on a Cloud-managed instance | The write succeeds while a changed value returns `execution_mode_platform_managed`. |
| TC-28 | A company list read or audit transaction fails during a task drain transition | No drain state changes and no activity record publishes. |
| TC-29 | Activity publication or queued run dispatch fails after the audit transaction commits | The committed start or stop result is returned. |
| TC-30 | A second start, a stale owner, or an ownerless stop arrives while an owned idle hold exists | The conflicting transition returns 409. |
| TC-31 | A task drain TTL is missing for an idle hold, zero, negative, or above 24 hours | Validation rejects the request before drain state changes. |
| TC-32 | A body-bound Cloud status request has changed bytes, a replayed nonce, a wrong action, or a wrong stack | The middleware rejects it before installing capabilities. |
| TC-33 | A Cloud lifecycle unarchive runs when the primary is missing, already active, or the instance is self-hosted | The API reports `missing`, `changed: false`, or 404 without an invalid update. |
| TC-34 | A manual backup overlaps another backup or runs on a Cloud-managed instance | The API returns 409 or `database_backups_platform_managed` without starting a backup. |
| TC-35 | Server metrics are disabled or requested by a member or agent | The route returns 404 when disabled and 403 for unauthorized actors. |
| TC-36 | Operator, Cloud catalog, or managed configuration is malformed | The parser or service constructor fails closed. |

## Test Infrastructure

- Vitest runs unit, route, service, and UI component tests.
- Supertest drives most Express routes through a test app with mocked services and actors.
- The metrics route suite starts a real Express listener and uses API keys for admin, member, and agent callers.
- Cloud control tests use generated Ed25519 key pairs, signed JWS assertions, request nonces, and exact raw JSON bodies.
- Task drain tests use mocked heartbeat methods, a transaction sentinel, and controlled company lists.
- Backup tests use controlled timers, mocked backup services, and filesystem fixtures with marker and archive paths.
- UI tests use React Testing Library with mocked settings APIs and operator visibility configuration.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-15 |
| FR-02 | TC-15, TC-16 |
| FR-03 | TC-17, TC-25 |
| FR-04 | TC-1, TC-15, TC-16 |
| FR-05 | TC-2, TC-5, TC-6, TC-7 |
| FR-06 | TC-7, TC-25 |
| FR-07 | TC-8, TC-17, TC-26, TC-27 |
| FR-08 | TC-17, TC-22, TC-27 |
| FR-09 | TC-16 |
| FR-10 | TC-19 |
| FR-11 | TC-14, TC-18, TC-20 |
| FR-12 | TC-19 |
| FR-13 | TC-11, TC-19, TC-29 |
| FR-14 | TC-21, TC-33 |
| FR-15 | TC-22, TC-34 |
| FR-16 | TC-9, TC-23, TC-35 |
| FR-17 | TC-12 |
| FR-18 | TC-13 |
| FR-19 | TC-24, TC-25 |
| NFR-01 | TC-15, TC-17, TC-18, TC-21, TC-22, TC-23 |
| NFR-02 | TC-19 |
| NFR-03 | TC-19, TC-28 |
| NFR-04 | TC-5, TC-7, TC-36 |
| NFR-05 | TC-4 |
| NFR-06 | TC-1, TC-2, TC-7 |

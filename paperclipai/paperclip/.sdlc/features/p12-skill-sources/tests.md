---
title: "Skill Sources"
status: done
---

# Test Plan: Skill Sources

## Scope

Tests cover repository discovery and auditing, NDJSON progress, import and publication, selection and settings, refresh and unchanged-tree checks, repair, disconnect, project repository adoption, automatic scheduling, budgets, access control, and the Skill Sources and Skill Studio UI surfaces.
Out of scope: GitHub App installation flows, Cloud deployment policy, and release smoke coverage.

## Test Files

| Layer | Files |
|---|---|
| Source service and integration | `server/src/__tests__/skill-sources.test.ts`, `server/src/__tests__/project-skill-sources.test.ts` |
| Repository scanning | `server/src/__tests__/github-skill-source.test.ts`, `server/src/__tests__/skill-source-git-snapshot.test.ts` |
| Authorization, limits, and repair | `server/src/__tests__/skill-source-github-access.test.ts`, `server/src/__tests__/skill-source-branches.test.ts`, `server/src/__tests__/skill-source-scan-limit.test.ts`, `server/src/__tests__/skill-source-retry.test.ts`, `server/src/services/skill-source-problems.ts` |
| Scheduling and delivery work | `server/src/services/skill-source-sync-work.test.ts`, `server/src/services/skill-source-idle-schedule.test.ts`, `server/src/__tests__/skill-source-default-cadence-acceptance.test.ts` |
| Routes and API client | `server/src/__tests__/company-skills-routes.test.ts`, `server/src/__tests__/skill-update-diff-routes.test.ts`, `ui/src/api/skillSources.test.ts`, `ui/src/lib/skill-source-connect-return.test.ts` |
| UI pages and components | `ui/src/pages/SkillSources.test.tsx`, `ui/src/pages/SkillStudio.test.tsx`, `ui/src/pages/agent-skills/agent-skill-source.test.ts`, `ui/src/components/skill-studio/ForkSkillDialog.test.tsx`, `ui/src/components/skill-studio/AgentsUsingSkillDialog.test.tsx`, `ui/src/components/skill-studio/SkillPolicySurfaces.test.tsx` |
| Database migration | `packages/db/src/project-skill-sources-migration.test.ts` |

## Test Cases

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Tracks a repository with no selected valid skills without saving contents (`server/src/__tests__/skill-sources.test.ts:53`) | Discovery with zero selected valid skills | Source row exists with no installed file bodies |
| TC-2 | Publishes two assigned skills while a concurrent save holds the second version (`server/src/__tests__/skill-sources.test.ts:65`) | Concurrent refresh and version save | Both assigned skills publish with distinct versions |
| TC-3 | Repairs a missing branch while retaining connection, selection, and installed versions (`server/src/__tests__/skill-sources.test.ts:104`) | Missing tracked branch and explicit repair | New branch commit is stored and content is unchanged |
| TC-4 | Validates a selected branch and retains installed content until a successful refresh (`server/src/__tests__/skill-sources.test.ts:128,152`) | Valid then unavailable branch | Successful validation advances state, unavailable branch leaves source unchanged and writes no success audit |
| TC-5 | Requires source edit authorization before branch reads and uses only the requested connection (`server/src/__tests__/skill-sources.test.ts:167`) | Denied actor and explicit connection id | Authorization fails before provider read and no other connection is used |
| TC-6 | Skips downloads and version replacement for a new commit with an unchanged tree (`server/src/__tests__/skill-sources.test.ts:179`) | New commit with same tree hash | Commit and check time advance while installed versions stay intact |
| TC-7 | Persists automatic work limits, refills capacity, and allows explicit refresh (`server/src/__tests__/skill-sources.test.ts:207,245`) | Repeated automatic jobs and explicit refresh | Automatic work is bounded, unused capacity is refunded, and manual refresh remains available |
| TC-8 | Imports duplicate skill names independently and refreshes without duplicates (`server/src/__tests__/skill-sources.test.ts:261`) | Two paths with the same skill name | Both entries and snapshots are distinct and refresh preserves identities |
| TC-9 | Rolls back source, skills, and versions when required activity persistence fails (`server/src/__tests__/skill-sources.test.ts:311`) | Forced activity write failure | No source, skill, version, or entry remains |
| TC-10 | Retains excluded folders, additions, removed paths, pinned versions, and copies (`server/src/__tests__/skill-sources.test.ts:347`) | Selection changes and removed repository paths | Saved selection matches the request and pinned versions and copies are preserved |
| TC-11 | Serializes refreshes and preserves content after an access failure (`server/src/__tests__/skill-sources.test.ts:382`) | Concurrent refresh and revoked access | Second refresh conflicts, installed content remains, and valid siblings still publish |
| TC-12 | Handles legacy GitHub imports and URL variants (`server/src/__tests__/skill-sources.test.ts:412,478,508,548`) | Legacy ids, commit-only urls, default refs, and folder urls with slash refs | Sources refresh without provider calls for legacy ids and without duplicate skills or changed identity |
| TC-13 | Does not report a copy when an imported skill is deleted before publication (`server/src/__tests__/skill-sources.test.ts:460`) | Skill deleted during publication | Result omits the missing copy |
| TC-14 | Checks per-skill policies for additions and deselection before publishing (`server/src/__tests__/skill-sources.test.ts:564`) | Denied add and denied removal | Request is denied before publication |
| TC-15 | Authorizes preview before provider reads and uses the current caller connection (`server/src/__tests__/skill-sources.test.ts:578`) | Preview with actor-specific connection | Denied preview makes no provider call and allowed preview reads through the supplied connection |
| TC-16 | Versions repository dependencies together and preserves pinned copies offline (`server/src/__tests__/skill-sources.test.ts:588,670,748`) | Shared files, missing references, unsupported bytes, and unchanged commit dependency repair | Shared updates publish with warnings, missing bytes are omitted from versions, and cached failures can repair |
| TC-17 | Cascades repository snapshots and referencing versions on company deletion (`server/src/__tests__/skill-sources.test.ts:773`) | Company deleted with installed repository versions | Snapshots and referencing version rows are removed |
| TC-18 | Disconnects sources with copy or delete and rejects invalid states (`server/src/__tests__/skill-sources.test.ts:795,813,837,849,874`) | Legacy removal, editable copies, assigned skill, stale revision, and in-flight refresh | Copies are complete, assigned deletion is denied, stale revisions conflict, and removed sources are not resurrected |
| TC-19 | Audits packages without returning file bodies (`server/src/__tests__/github-skill-source.test.ts:192,338,378,392,422`) | Repository packages with text and binary files | Discovery returns manifests, file metadata, and bounded previews without package bodies |
| TC-20 | Streams audited metadata and cancels on disconnect (`server/src/__tests__/github-skill-source.test.ts:211,237,486`) | Stream consumer disconnect and maximum size script | Progress arrives before completion, later packages are skipped, and auditing does not block the caller |
| TC-21 | Batches dependency reads and enforces scan budgets (`server/src/__tests__/github-skill-source.test.ts:16,66,93,123,178`) | Transitive dependencies, cache hits, and excessive batch budgets | One batch per frontier or scan and rejection before Git reads when budgets are excessive |
| TC-22 | Keeps skill folders, shared files, executable bits, and nested boundaries (`server/src/__tests__/github-skill-source.test.ts:38,84,99,203,253,280,307`) | Unrelated oversized files, missing references, nested skills, and scripts | Skill folders and shared files are retained and nested packages are not assigned to parents |
| TC-23 | Reports unsafe content and fails closed on interrupted downloads (`server/src/__tests__/github-skill-source.test.ts:314,327,446`) | Oversized files, symlinks, unsafe bytes, and interrupted Git download | Per-skill errors and warnings are recorded and the whole scan fails on interruption |
| TC-24 | Rejects non-GitHub URLs and credentials (`server/src/__tests__/github-skill-source.test.ts:332`) | Credential-bearing or non-GitHub URL | Scan is rejected before any read |
| TC-25 | Resolves default branches and preserves explicit refs (`server/src/__tests__/github-skill-source.test.ts:275`) | Repository URL and explicit API ref | Default branch is used only when no ref is specified and explicit compatibility remains |
| TC-26 | Enforces caller, grant, and agent identity rules (`server/src/__tests__/skill-source-github-access.test.ts:71,86,137,146,154,164,175,183,188`) | Public urls, private repositories, revoked access, and agent runs | Only authorized grants are used, no fallback crosses identities, and failures are sanitized |
| TC-27 | Uses one lease across metadata, snapshot, and audit and enforces scan limits (`server/src/__tests__/skill-source-github-access.test.ts:25,39,54,110,128`) | Completed scan, exhausted scans, cancellation, and in-flight fetch | Lease spans all reads, denied scans make no provider calls, and cancellation aborts fetches |
| TC-28 | Classifies quota exhaustion and sanitizes retryable failures (`server/src/__tests__/skill-source-github-access.test.ts:105,198`) | Provider quota and retryable provider response | Quota is distinguished from access denial and no provider body or credential is returned |
| TC-29 | Preserves bytes, hidden paths, executable bits, and pinned commits in Git snapshots (`server/src/__tests__/skill-source-git-snapshot.test.ts:54,93,149,171,181`) | Oversized dependency graph, hidden files, callers, and older pinned commit | Exact bytes are isolated per caller and pinned commits are fetched instead of branch heads |
| TC-30 | Cancels and validates Git snapshot reads (`server/src/__tests__/skill-source-git-snapshot.test.ts:123,133,187,225,231`) | Blocked batch, cancelled child, revision expression, and provider log line | Process terminates, retry is allowed, unsafe revisions are rejected, and progress is numeric only |
| TC-31 | Lists bounded branches with default included and checked identity (`server/src/__tests__/skill-source-branches.test.ts:11,19,24,32`) | Large branch page, duplicate names, changed repository identity, and invalid ref | Default is always included, names are preserved, and identity change stops listing |
| TC-32 | Applies caller and company scan buckets (`server/src/__tests__/skill-source-scan-limit.test.ts:5,17,30,37`) | Multiple callers, cache hits, downloads, failures, and elapsed minute | Active, scan, and download limits hold per caller and company and quotas restore after a minute |
| TC-33 | Schedules retries with bounded backoff (`server/src/__tests__/skill-source-retry.test.ts:7,12`) | Repeated failures and provider delay values | Backoff doubles and caps at one hour while provider delays are bounded and validated |
| TC-34 | Maintains durable wake deadlines and claims (`server/src/services/skill-source-idle-schedule.test.ts:14,19,23,30,37,43`) | Absent feature, due attempt, malformed claim, and full project queue | Future checks are preserved, inspection does not postpone work, invalid claims are blocked, and pending admissions are represented |
| TC-35 | Holds durable reads to one owner revision (`server/src/services/skill-source-idle-schedule.test.ts:59,65,71`) | Unreconciled startup, owner change, and empty settled state | Reads stay quiet until reconciliation and owner changes are rejected |
| TC-36 | Keeps sync work quiet and reconciles coordinator lifecycle (`server/src/services/skill-source-sync-work.test.ts:123,138,152,177,202`) | Paused sources, retained bindings, direct tick, rolled back attachment, and failed sweep | No passive SQL, ticks are invalidated on stop, only committed attachments import, and failed sweeps recover |
| TC-37 | Restores deadlines and cancels refresh work safely (`server/src/services/skill-source-sync-work.test.ts:214,230,243,268,288,302,314,331`) | Restart, settings change, manual lease, shutdown, full batch, active sweep, and reactivation | Deadlines persist without polling, capacity admits deferred work, and detached or shutting work is cancelled |
| TC-38 | Bounds project queues and admission (`server/src/__tests__/project-skill-sources.test.ts:113,139,168,182,198,687`) | Full project queue, detached batch, full company queue, and live lease | Deferred provenance is retained, another project can proceed, and locks are taken after queue admission |
| TC-39 | Adopts and imports durable project repositories (`server/src/__tests__/project-skill-sources.test.ts:319,383,420,440,870`) | New selection, durable enqueue, later additions, empty repository, access change, and API key agent | Stale repository is ignored, unchanged downloads are skipped, exclusions remain, and access loss fails closed |
| TC-40 | Meters initial import budgets across workers and jobs (`server/src/__tests__/project-skill-sources.test.ts:222,251,274,298`) | Failed downloads, small jobs, large jobs, and older sweep reservation | Failed attempts are charged, small jobs refund unused bytes, and refill time is counted once |
| TC-41 | Recovers leases and setup identities (`server/src/__tests__/project-skill-sources.test.ts:644,724,752,773,883`) | Expired jobs, interrupted import, deleted setup agent, policy denial, and API key public import | Jobs recover through durable leases, backoff applies, and repair is required where identity is missing |
| TC-42 | Handles locked refs and branch changes during adoption (`server/src/__tests__/project-skill-sources.test.ts:51,911`) | Branch repair racing attachment and changed default branch | Locked ref is rechecked, explicit branch stays fixed, and default branch tracking follows the rename |
| TC-43 | Falls back to bounded packages and preserves legacy references (`server/src/__tests__/project-skill-sources.test.ts:792,826`) | Oversized tracked repository and legacy repository change | Bounded packages are used and old references remain in ordinary legacy edits |
| TC-44 | Denies policy-blocked imports before provider reads (`server/src/__tests__/project-skill-sources.test.ts:334`) | Import denied by policy | No GitHub read or retry is scheduled |
| TC-45 | Avoids new readers during private source removal (`server/src/__tests__/project-skill-sources.test.ts:349`) | Import overlapping private source removal | No additional reader is created |
| TC-46 | Preserves migration state on repeated SQL runs (`packages/db/src/project-skill-sources-migration.test.ts:11`) | Renumbered migration run | Imported content, private provenance, and scheduling remain unchanged |
| TC-47 | Streams discovery and preserves JSON compatibility (`server/src/__tests__/company-skills-routes.test.ts:1333,1350,1362`) | NDJSON accept header, scan error, and stalled client | NDJSON events end with complete or sanitized error, JSON shape remains, and stalled clients are aborted |
| TC-48 | Validates disconnect and branch inputs (`server/src/__tests__/company-skills-routes.test.ts:1394,1402`) | Missing disposition, invalid revision, invalid connection id, and valid override | Invalid requests return 400 and authorized branch calls use the validated connection |
| TC-49 | Rejects cross-company source access (`server/src/__tests__/company-skills-routes.test.ts:1413`) | Board and agent actors targeting another company | All listed source reads and mutations return 403 |
| TC-50 | Computes update diffs only when needed (`server/src/__tests__/skill-update-diff-routes.test.ts:61,69,109`) | Changed revision, unchanged revision, and disconnected client | Per-file diff is returned, unchanged revisions skip scanning, and scans abort on disconnect |
| TC-51 | Guards update diff access and unsupported states (`server/src/__tests__/skill-update-diff-routes.test.ts:77,86,93`) | Other company, unreadable skill, disconnected source, unknown revision, and oversized repository | Requests are denied or return a supported false reason without provider reads |
| TC-52 | Decodes NDJSON client frames and handles stream failures (`ui/src/api/skillSources.test.ts:20,32,38,42,48`) | Split UTF-8 bytes, no complete frame, in-stream error, 403, and abort signal | Only completed discovery resolves and errors preserve status, session recovery, and cancellation |
| TC-53 | Sends disconnect disposition and revision from the client (`ui/src/api/skillSources.test.ts:56`) | Delete with revision 7 and skills delete | Request body contains the required disposition and revision |
| TC-54 | Keeps setup return state company scoped (`ui/src/lib/skill-source-connect-return.test.ts:7,15`) | OAuth reload, abandoned setup, and arbitrary redirect | Return survives one reload, expires, and rejects unsafe destinations |
| TC-55 | Formats agent skill source labels (`ui/src/pages/agent-skills/agent-skill-source.test.ts:9,18,27,36,45`) | GitHub, local, and catalog skills | Owner and repository text is shown and long filesystem labels are hidden |
| TC-56 | Keeps Skills views and project repository grouping visible (`ui/src/pages/SkillSources.test.tsx:74,86,142,158`) | Sources route and multiple project workspaces sharing one repository | Navigation remains available, repositories are grouped, and pending imports show progress |
| TC-57 | Repairs branches and preserves conflict advice (`ui/src/pages/SkillSources.test.tsx:110,125,173`) | Missing ref, branch conflict, and connection repair sequence | Branch repair is offered, conflict text is shown, and selected connection is retained |
| TC-58 | Shows progress and cancels scans safely (`ui/src/pages/SkillSources.test.tsx:191,208,229,244`) | Download progress, streamed candidates, failed stream, large feed, and cancellation | Progress renders, partial import stays disabled, failed streams clear candidates, and late events are ignored |
| TC-59 | Handles repository inventory and setup links (`ui/src/pages/SkillSources.test.tsx:265,282,295,313`) | Combined inventory, branch url, empty repository, and partial failure | Selected repository connection is used, branch details are not reused, and draft state survives setup links |
| TC-60 | Defaults to repository packaging and warns about omitted files (`ui/src/pages/SkillSources.test.tsx:321,348,360`) | Discovered skills, omitted files, and old individual-import draft | Repository mode is selected, all discovered skills are selected, and old drafts keep repository mode |
| TC-61 | Requires explicit disconnect disposition (`ui/src/pages/SkillSources.test.tsx:385,394,407,427`) | Cancel, delete, stale confirmation, and keep copy with failed request | Source remains intact on cancel, delete and revision are sent, stale confirmations reload, and failures remain for retry |
| TC-62 | Keeps sources readable during outages (`ui/src/pages/SkillSources.test.tsx:445,460`) | Failed refetch and failed initial load | Loaded rows remain visible and initial failure shows readable copy with Retry |
| TC-63 | Creates and navigates Studio drafts (`ui/src/pages/SkillStudio.test.tsx:325,339,351,372,392,485,533,547,557`) | New route, fork query, folder query, categories, and landing states | Create mode is used, drafts are prefilled and filed, and landing and loading states render |
| TC-64 | Preserves Studio edits across conflicts (`ui/src/pages/SkillStudio.test.tsx:606,629,641,691,714,742`) | Files with and without frontmatter, dirty edits, version conflict, and read-only banner | Frontmatter rules are followed, unsaved text survives conflict, and copy action is available |
| TC-65 | Forks with usage and reassignment choices (`ui/src/components/skill-studio/ForkSkillDialog.test.tsx:205,244,274,294`) | Reassignment on or off, existing copy, and zero usage | Fork request follows the toggle, existing copy is offered, and zero usage hides the toggle |
| TC-66 | Shows skill usage and version controls (`ui/src/components/skill-studio/AgentsUsingSkillDialog.test.tsx:203,211,226,253,265,299,334`) | Unused skill, stale pin, removal, pinning, and read-only mode | Badges pluralize, version controls and hints render, and read-only mode hides mutations |
| TC-67 | Surfaces skill policy denials (`ui/src/components/skill-studio/SkillPolicySurfaces.test.tsx:65,71,76,110,119`) | Explicit policy denial, platform safety denial, dismissal, and transient error | Persistent banner text is shown, dismissal works, and transient errors stay on the toast path |
| TC-68 | Qualifies cadence acceptance stages (`server/src/__tests__/skill-source-default-cadence-acceptance.test.ts:34`) | Staged producer, signed legacy refusal, and durable acknowledgement | Stage specific acceptance assertions pass for the scheduled producer and legacy refusal |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-E1 | Repository has valid skills but none selected | Source is tracked without saving file contents |
| TC-E2 | Activity persistence fails during publication | All source, skill, version, and entry changes roll back |
| TC-E3 | Branch becomes unavailable during settings or repair | Source and installed content remain unchanged |
| TC-E4 | Commit changes but tree hash does not | No version is replaced and the check is recorded |
| TC-E5 | GitHub access is revoked mid scan | Provider work stops, lease is cleared, and a retry deadline is saved |
| TC-E6 | Repository identity changes at the same url | Branch listing stops and actionable advice is returned |
| TC-E7 | Provider returns credentials or response bodies | Stored error and audit details contain sanitized text only |
| TC-E8 | Scan client stalls or disconnects | Provider work is aborted and response resources are released |
| TC-E9 | Caller or company exceeds scan limits | Request is limited before provider reads and quotas restore over time |
| TC-E10 | Source is removed while refresh is in flight | Removal completes without resurrecting installed content |
| TC-E11 | Skill is assigned when delete disconnect is requested | Request is denied and the source remains linked |
| TC-E12 | Client sends a stale revision with selection or settings | Conflict is returned before publication |
| TC-E13 | Project access is revoked before adoption | Import fails closed and no token is used |
| TC-E14 | Project queue is full | Deferred imports keep provenance and are admitted after capacity frees |
| TC-E15 | Initial import budget is exhausted | Automatic work is deferred until capacity is available or explicit refresh is used |
| TC-E16 | Worker shuts down during import or refresh | Provider work aborts and the job remains recoverable from saved deadlines |
| TC-E17 | Repository outgrows package mode | Bounded skill packages are used with warnings or the update diff is marked unsupported |
| TC-E18 | Repository contains symlinks, unsafe bytes, or oversized files | Those files are omitted or reported per skill and installed bytes stay unchanged |
| TC-E19 | Studio save races a newer version | Unsaved text is kept until the client confirms a reload |
| TC-E20 | Sources list refetch fails during an outage | Previously loaded sources stay visible with a Retry affordance |
| TC-E21 | Cross-company actor calls any source route | Route denies access before service work |
| TC-E22 | Update diff has no tracked source or unknown revision | Response explains why the diff is unsupported |
| TC-E23 | OAuth setup state is reused or redirected | Setup expires or rejects the unsafe destination |
| TC-E24 | Renumbered migration runs again | Imported content, provenance, and scheduling remain intact |
| TC-E25 | Public repository is pasted with a branch url | Branch and credentials are not reused for another repository |

## Test Infrastructure

- Embedded Postgres test databases back the source service and project source integration suites.
- Supertest with an Express harness and module mocks backs the route suites.
- jsdom with `QueryClientProvider` and mocked API modules backs the UI page suites.
- Vitest fake timers, `AbortController`, and fetch stubs back stream, cancellation, and scheduled work assertions.
- Temporary Git repository fixtures back the snapshot and scanner byte fidelity suites.
- Shared Storybook fixtures under `ui/src/storybook/fixtures/githubSkillSources.ts` back the Skill Sources UI cases.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-19, TC-22, TC-23 |
| FR-2 | TC-20, TC-30, TC-47, TC-52, TC-58 |
| FR-3 | TC-15, TC-19 |
| FR-4 | TC-1, TC-2, TC-8, TC-9, TC-13 |
| FR-5 | TC-1, TC-56, TC-62 |
| FR-6 | TC-6, TC-12, TC-29, TC-42, TC-50 |
| FR-7 | TC-10, TC-14, TC-39 |
| FR-8 | TC-3, TC-4, TC-42, TC-57 |
| FR-9 | TC-18, TC-45, TC-53, TC-61, TC-64 |
| FR-10 | TC-36, TC-38, TC-39, TC-56 |
| FR-11 | TC-5, TC-14, TC-26, TC-44, TC-49, TC-51, TC-67 |
| FR-12 | TC-7, TC-34, TC-35, TC-36, TC-37, TC-38, TC-41, TC-68 |
| FR-13 | TC-7, TC-40 |
| FR-14 | TC-16, TC-21, TC-22, TC-29, TC-43, TC-60 |
| FR-15 | TC-50, TC-55, TC-56, TC-63, TC-64, TC-65, TC-66 |
| FR-16 | TC-25, TC-31, TC-48, TC-42 |
| FR-17 | TC-12, TC-25, TC-43, TC-59 |
| NFR-1 | TC-5, TC-15, TC-19, TC-23, TC-24, TC-26, TC-28, TC-30, TC-39, TC-41, TC-47, TC-48, TC-52, TC-54, TC-57, TC-59, TC-67 |
| NFR-2 | TC-2, TC-11, TC-18, TC-27, TC-30, TC-35, TC-37, TC-41, TC-47, TC-58, TC-61 |
| NFR-3 | TC-9, TC-11, TC-13, TC-17, TC-23, TC-36, TC-46, TC-62 |
| NFR-4 | TC-20, TC-21, TC-27, TC-29, TC-32, TC-36 |
| NFR-5 | TC-33, TC-34, TC-40, TC-41, TC-68 |
| NFR-6 | TC-7, TC-40 |

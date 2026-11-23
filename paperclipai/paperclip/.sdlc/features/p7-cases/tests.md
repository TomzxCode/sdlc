---
title: "Cases and Pipeline Cases"
status: done
---

# Test Plan: Cases and Pipeline Cases

## Scope

The suite covers the case REST surface, case handoff service and delivery ledger, native agent case tools, shared validation schemas, database migrations and constraints, and read-only board UI pages.
Runner E2E fixtures cover provider native case behavior and catalog agent journeys.
Pipeline case coverage is limited to schema persistence and constraints because no active pipeline case route or service was found during sync.
Out of scope: board-based case authoring, quarantine promotion, and an active pipeline case workflow.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Cases feature gate rejects every route | `enableCases` false with calls to case and handoff routes | Final denial with code `cases_disabled` and remediation text (`server/src/__tests__/cases-routes.test.ts:194`, `:232`) |
| TC-2 | Removed `createOnly` option is rejected | Request against an existing passive case with `createOnly` | Validation error and unchanged passive row (`server/src/__tests__/cases-routes.test.ts:338`) |
| TC-3 | Shared handoff input schemas validate kickoff, workflow, documents, observed versions, and completion intent | Kickoff without routing state, reusable workflow, blank or oversized workflow text, initial documents, binding task, transfer versions, terminal intent | Accepted or rejected at schema boundary with normalized document keys and no invented attribution (`packages/shared/src/case-handoffs.test.ts:13`, `:16`, `:27`, `:38`, `:58`, `:64`, `:74`, `:79`, `:86`) |
| TC-4 | Bounded native case reads page large case data | Small case, large fields, changed facts, changed task routing, byte offsets, document revisions, and invalid selectors | Structured case for small data, bounded UTF-8 pages with snapshot and next offset for large data, and rejection on changed inputs (`server/src/services/case-agent-read.test.ts:8`, `:28`, `:37`, `:79`, `:92`) |
| TC-5 | Native workflow case projection keeps stable facts and delivers instructions once | Unchanged facts, current routing, returning agent, cold bootstrap, withdrawn source, reordered fields, and 8 KiB field | Retained session stays small, current routing is sent, new instructions appear once, and proof carries into continuations (`server/src/services/native-runtime/case-context-projection.test.ts:57`, `:77`, `:92`, `:134`, `:151`, `:195`, `:200`) |
| TC-6 | Task document references roll up metadata only | Primary and linked task documents, quarantined references, workflow reference, and fresh wake context | Authorized metadata appears with distinct keys, bodies are not copied, and quotas apply before injection (`server/src/services/case-task-documents.test.ts:44`, `:59`, `:75`, `:93`) |
| TC-7 | Retained private ancestry is checked transitively | Same-root siblings, valid descendant, and disconnected cycle | Sibling and cycle are rejected, transitive descendant is accepted (`server/src/services/case-handoff-privacy.test.ts:59`, `:81`, `:93`) |
| TC-8 | Case references in markdown are parsed and linked | Bare identifier, uppercase normalization, issue identifier, known prefixes, inline code, and existing links | Correct case detail links are produced without descending into existing links (`ui/src/lib/case-reference.test.ts:5`, `:12`, `:16`, `:21`, `:26`, `:32`, `:51`, `:63`) |
| TC-9 | Case fields and child cases render without edit controls | Empty fields, four value types, nested objects, arrays, punctuation, URLs, identifiers, and long child lists | Flattened read-only table, linked identifiers, capped child list, and empty states (`ui/src/components/CaseFieldsPanel.test.tsx:41`, `:47`, `:116`, `:134`, `:149`, `:169`, `:184`, `:199`, `:212`; `ui/src/components/CaseChildrenTree.test.tsx:61`, `:67`, `:85`) |
| TC-10 | Case activity and issue panel reflect flags and attribution | Empty events, actor and run attribution, auto-link events, kind filter, Cases off, linked cases, and no linked cases | Correct empty states, enriched rows, filter behavior, and hidden panel (`ui/src/components/CaseActivityFeed.test.tsx:55`, `:61`, `:83`, `:99`; `ui/src/components/IssueCasesPanel.test.tsx:74`, `:83`, `:97`) |
| TC-11 | Revision rail shows saved revisions without restore controls | Two revisions and selection of an older body | Latest body renders first, older body renders on selection, and diff lines stay out of session replay (`ui/src/components/CaseRevisionRail.test.tsx:99`, `:114`, `:127`) |
| TC-12 | Runner case data contracts stay narrow | Bounded continuations, explicit document selection, facts update, kickoff routing, initial documents, and generic API access | Only case tools are advertised, explicit documents open through bounded reads, workflow and access mutations are excluded, and facts stay separate from task documents (`packages/paperclip-runner/src/protocol-actions/case-data.test.ts:55`, `:64`, `:83`, `:96`, `:123`) |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-20 | Case route surface stores and reads authorized cases | Seeded companies, agents, projects, labels, issues, documents, actors, and Postgres test database | Keyed and keyless upserts converge, identifier lookup works, run writes auto-link with a work link and event, terminal status writes stay with handoff authority, documents, links, attachments, events, filters, types, sorting, grouping, and pagination work (`server/src/__tests__/cases-routes.test.ts:253`, `:285`, `:317`, `:351`, `:366`, `:416`, `:505`, `:709`, `:792`, `:858`, `:932`, `:1013`, `:1094`, `:1145`, `:1176`) |
| TC-21 | Durable handoff service reuses one primary task | Seeded passive cases, workflows, agents, tasks, documents, actors, and delivery ledger | A to B to A transfers reuse the task, prompts and revisions are preserved, lost responses replay, workflow seeds and initial documents are atomic, concurrent routing serializes, expired leases are reclaimed, one worker claims a handoff, and terminal intents settle atomically (`server/src/services/case-handoffs.test.ts:166`, `:199`, `:240`, `:258`, `:273`, `:289`, `:302`, `:316`, `:325`, `:357`, `:368`, `:386`, `:402`, `:440`, `:457`, `:494`, `:515`, `:546`, `:581`, `:601`, `:611`, `:620`, `:631`, `:649`, `:668`, `:702`, `:715`, `:734`, `:759`, `:798`, `:814`, `:850`, `:869`, `:882`, `:928`, `:953`, `:961`, `:974`, `:1000`, `:1073`, `:1115`, `:1126`, `:1141`, `:1150`, `:1163`, `:1176`) |
| TC-22 | Heartbeat queue admits only exact durable receipts | Seeded handoffs, scheduler instances, paused recipients, stale versions, source runs, and ledger cancellation | Generic wakes are blocked, one exact receipt is admitted across schedulers, paused recipients retry the same identity, invented versions fail, unconfirmed Stop retains the fence, disabled Cases holds then cancels, and old receipts do not launch (`server/src/__tests__/heartbeat-case-handoff.test.ts:58`, `:68`, `:76`, `:123`, `:156`, `:295`, `:310`, `:326`, `:335`, `:353`) |
| TC-23 | Terminal handoff follows accepted task completion | Seeded terminal intent, review gates, governed actions, audit rows, ownership changes, and ledger state | No wake or close before completion, close happens once in the completion transaction, review and governed actions are awaited, rollback is atomic, cancellation paths do not close, and ordinary completion without intent leaves the case independent (`server/src/__tests__/heartbeat-case-terminal-handoff.test.ts:59`, `:75`, `:88`, `:105`, `:119`, `:128`, `:137`, `:144`, `:152`) |
| TC-24 | Native case tools work through production routes | Authenticated agent runtime, feature and work-mode gates, large case data, documents, and prepared handoffs | Case facts and creation are exposed without a second document tool, workflow authoring is bounded, kickoff has no side effects without workflow text, unsupported fields fail, large case reads page correctly, privacy survives continuation, and committed handoffs fence late writes (`server/src/services/native-runtime/native-case-tools.integration.test.ts:127`, `:146`, `:208`, `:230`, `:238`, `:259`, `:304`, `:329`, `:405`, `:436`, `:456`, `:481`, `:517`, `:541`, `:554`, `:563`) |
| TC-25 | Native handoff runtime waits for execution release | Persisted intent, terminal task status, missing controller marker, child process group, and manual reassignment | Yield follows accepted response, late writes are fenced, terminal intent stays writable, release needs stopped process and cleanup evidence, and manual reassignment invalidates pending intent (`server/src/services/native-runtime/native-case-handoff.test.ts:36`, `:52`, `:63`, `:79`, `:92`, `:115`) |
| TC-26 | Migration and schema guards preserve case data | Previous feature receipts, passive case rows, retained sources, and replacement guards | Passive data is preserved, sources are backfilled, actor context is nullable, old receipts are recognized, terminal rows survive, and a failed guard rolls back migration and receipt (`packages/db/src/case-handoff-migration.test.ts:91`, `:109`, `:133`, `:164`, `:187`) |
| TC-27 | Pipeline case tables persist and enforce constraints | Seeded pipeline, stages, cases, documents, links, blockers, and automations | One row per pipeline table is stored, unique keys hold, and required checks are enforced (`packages/db/src/pipelines-schema.test.ts:50`) |
| TC-28 | Deletion with retained case history behaves safely | Terminated agent, retained handoffs, and case history | Unrelated agent is purged and case history is kept (`server/src/services/case-deletion.test.ts:59`) |
| TC-29 | Legacy process and HTTP handoff boundaries transfer work | Seeded legacy runtime and HTTP adapters | Handoff crosses legacy process and HTTP boundaries and records the transfer (`server/src/__tests__/case-handoff-legacy.integration.test.ts:65`) |
| TC-30 | Native same-task journey yields and closes in order | Seeded A and B agents, accepted tool responses, sessions, reviews, and task completion | A to B to A resumes each session and closes only after accepted completion (`server/src/__tests__/case-handoff-native.integration.test.ts:84`) |
| TC-31 | Cases list page is read-only and preserves browse context | Mounted page, mocked API responses, URL filters, paging, sorting, grouping, and selected company | Batched work data is used, no edit controls render, URL filters survive detail and back navigation, sort and grouping precede paging, errors recover, and no company request occurs before selection (`ui/src/pages/Cases.test.tsx:125`, `:150`, `:168`, `:182`, `:204`, `:226`, `:247`, `:266`, `:297`, `:314`, `:327`) |
| TC-32 | Case detail page reads facts, work, documents, and handoffs | Mounted page, mocked case detail, documents, revisions, handoffs, parent and child cases, and failing refresh | Facts and passive work render, Work precedes Details, documents and revisions are read only, browse context is retained, handoff state is accurate, failed document reads hide cached content, and load failures use one unavailable state (`ui/src/pages/CaseDetail.test.tsx:102`, `:121`, `:142`, `:155`, `:189`, `:199`, `:207`, `:228`, `:257`, `:264`, `:276`) |
| TC-33 | App routes and history discovery guide agents and operators | Unprefixed case URLs, task case links, audit history docs, and enabled Cases flag | Unprefixed URLs redirect to company-prefixed pages and chat guidance locates cases, history, people, and document placement (`ui/src/App.cases-routing.test.tsx:135`, `:142`; `server/src/__tests__/case-history-api-discovery.test.ts:10`, `:20`, `:25`, `:34`) |
| TC-34 | Every case write is fenced after an accepted handoff | Seeded passive case, documents, revisions, annotation, native or legacy source run, and accepted handoff | All case mutations return `case_handoff_run_yielded`, reads stay available, no table or asset changes occur, and an upload racing Stop or handoff compensates its object (`server/src/__tests__/case-mutation-fence.integration.test.ts:117`, `:150`) |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-40 | Same-task handoff product journeys pass through provider credentials | Run fixture journeys with either credential mode, inspect correlated native tool lifecycle and persisted evidence | Public evidence passes and wrong or missing results fail (`tests/runner-e2e/case-handoffs.test.ts:51`, `:71`, `:83`, `:105`) |
| TC-41 | Case receipt evidence proves persisted case and task document reads | Run receipt smoke fixture, write documents, read case and task documents, compare revision lists and redacted persistence | Successful GET with saved metadata is required, canonical ordering is accepted, and unsuccessful first writes are not skipped (`tests/runner-e2e/case-receipt.test.ts:51`, `:73`, `:143`, `:176`, `:190`, `:319`, `:367`) |
| TC-42 | Provider native case qualifications pass for Pi, Cursor, and Copilot | Run bounded provider fixtures, native reads and edits, memory readback, permission and settlement probes | Native origin and response evidence is required, substitutions and fallbacks fail, stale or duplicated delivery fails, and cleanup evidence is complete (`tests/runner-e2e/pi-native-cases.test.ts:8`, `:30`, `:82`, `:96`, `:104`, `:113`; `tests/runner-e2e/cursor-native-cases.test.ts:17`, `:22`, `:23`, `:28`, `:32`, `:39`, `:63`; `tests/runner-e2e/copilot-protection-cases.test.ts:40`, `:45`, `:48`, `:93`, `:106`, `:119`, `:153`, `:161`, `:168`) |
| TC-43 | Catalog agent case journeys pass through browsing, creation, handoff, history, facts, relationships, prerequisites, and close | Run integrator domain fixtures with saved cases, documents, ledgers, revisions, permissions, budgets, and final results | Accepted answers require persisted case and handoff evidence, task-done-only claims fail, inferred relationships fail, missing prerequisites fail, and terminal closure waits for normal gates (`tests/runner-e2e/chat-catalog-domains/integrator-cases.test.ts:18`, `:32`, `:63`; `tests/runner-e2e/chat-catalog-domains/integrator-case-create.test.ts:18`, `:35`, `:47`, `:69`; `tests/runner-e2e/chat-catalog-domains/integrator-case-handoff.test.ts:22`, `:28`, `:36`, `:52`, `:67`, `:77`; `tests/runner-e2e/chat-catalog-domains/integrator-case-history.test.ts:18`, `:27`, `:35`; `tests/runner-e2e/chat-catalog-domains/integrator-case-facts.test.ts:22`, `:30`, `:35`, `:41`, `:51`, `:67`, `:72`; `tests/runner-e2e/chat-catalog-domains/integrator-case-related.test.ts:15`, `:21`, `:31`; `tests/runner-e2e/chat-catalog-domains/integrator-case-prerequisites.test.ts:12`, `:13`, `:16`, `:20`, `:33`, `:37`; `tests/runner-e2e/chat-catalog-domains/integrator-cases-locator.test.ts:9`, `:21`; `tests/runner-e2e/chat-catalog-domains/integrator-case-close.test.ts:24`, `:29`, `:35`, `:42`, `:59`) |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-50 | Cases are disabled during an accepted handoff lifecycle | Existing ledger state is held or cancelled and no substitute record is created (`server/src/__tests__/cases-routes.test.ts:194`; `server/src/__tests__/heartbeat-case-handoff.test.ts:310`) |
| TC-51 | Cross-company request or absent case | Identical not found response and no passive mutation (`server/src/__tests__/cases-routes.test.ts:573`, `:670`) |
| TC-52 | Readable case links to an inaccessible task or out-of-bound agent name | Enrichment omits hidden task data and names (`server/src/__tests__/cases-routes.test.ts:1241`) |
| TC-53 | Access source is unlinked or deleted | Retained boundary stays until removal is authoritative and then reads fail closed (`server/src/__tests__/cases-routes.test.ts:1303`) |
| TC-54 | Quarantined or low-trust historical case data enters execution | Automatic context and writes are blocked while authorized reads remain available (`server/src/__tests__/cases-routes.test.ts:1363`, `:1386`, `:1433`; `server/src/services/native-runtime/case-context-projection.test.ts:195`) |
| TC-55 | Case facts change between native read pages | Continuation snapshot is rejected and the client restarts at offset zero (`server/src/services/case-agent-read.test.ts:28`, `:79`) |
| TC-56 | Byte offset splits a multibyte character | Exact characters are preserved without loss (`server/src/services/case-agent-read.test.ts:37`) |
| TC-57 | Workflow seed is missing, blank, colliding, oversized, or added while binding a task | No case, task, comment, document, revision, history, or wake side effect remains (`packages/shared/src/case-handoffs.test.ts:27`, `:58`; `server/src/services/case-handoffs.test.ts:258`, `:302`, `:386`, `:402`) |
| TC-58 | Delivery lease expires or two workers scan at once | Expired lease is reclaimed, one worker claims, and superseded assignments are not dispatched (`server/src/services/case-handoffs.test.ts:601`, `:611`) |
| TC-59 | Review gate or governed action blocks terminal completion | Case stays open until ordinary completion is accepted (`server/src/__tests__/heartbeat-case-terminal-handoff.test.ts:88`) |
| TC-60 | Main process exits but a child process still owns the process group | Handoff release is withheld (`server/src/services/native-runtime/native-case-handoff.test.ts:92`) |
| TC-61 | Run is cancelled or a handoff is committed before a case write reaches the route | Write is fenced inside the route and no mutation is applied (`server/src/services/native-runtime/native-case-tools.integration.test.ts:541`, `:554`, `:563`; `server/src/__tests__/case-mutation-fence.integration.test.ts:117`, `:150`) |
| TC-62 | Case document read fails in the UI | Error stays visible and cached document contents are hidden (`ui/src/pages/CaseDetail.test.tsx:199`) |
| TC-63 | Migration guard fails during replay | Migration and receipt roll back together (`packages/db/src/case-handoff-migration.test.ts:187`) |

## Test Infrastructure

- Vitest runs server, service, shared package, DB package, and UI tests.
- Postgres test databases and transactional fixtures support case routes, handoff ledger, migrations, and schema constraints.
- Express route harnesses supply actor identities, company membership, feature settings, and seeded work items.
- React Testing Library mounts UI pages with mocked API clients for list, detail, routing, and component tests.
- Runner E2E fixtures require provider credentials or fixture evidence, persisted case data, and correlated native tool receipts.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-22, TC-24, TC-33 |
| FR-2 | TC-20, TC-40, TC-43 |
| FR-3 | TC-20, TC-31 |
| FR-4 | TC-20, TC-31, TC-33 |
| FR-5 | TC-30, TC-31, TC-32, TC-33 |
| FR-6 | TC-21, TC-23, TC-29, TC-40, TC-43 |
| FR-7 | TC-21, TC-22, TC-23 |
| FR-8 | TC-21, TC-23, TC-43 |
| FR-9 | TC-4, TC-12, TC-24, TC-41 |
| FR-10 | TC-3, TC-21, TC-24, TC-42 |
| FR-11 | TC-20, TC-21, TC-24, TC-26, TC-33, TC-34, TC-51, TC-52, TC-53 |
| FR-12 | TC-20, TC-26, TC-31, TC-33 |
| FR-13 | TC-27 |
| FR-14 | TC-2, TC-24 |
| NFR-1 | TC-20, TC-24, TC-33, TC-34, TC-52, TC-53, TC-54 |
| NFR-2 | TC-4, TC-20, TC-24, TC-31, TC-56 |
| NFR-3 | TC-21, TC-22, TC-58 |
| NFR-4 | TC-20, TC-21, TC-24, TC-42, TC-54 |
| NFR-5 | TC-20, TC-31, TC-33 |

## Gaps

- No test exercises an active pipeline case route or service because no such surface was found during sync.
- No test states an explicit latency or availability target for case list or native read operations.
- Runner E2E files grade persisted evidence and model output in several domains, so they need fixture data and provider access to run end to end.

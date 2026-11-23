---
title: "Responsibilities and Status Reports"
status: done
---

# Test Plan: Responsibilities and Status Reports

## Scope

Tests cover responsibility CRUD, owner and agent authority, linked work, areas, delegation, dashboard conversations, dashboard change sets, restorable versions, status reports, private dashboard conversations, and the Dashboard and responsibility pages.
Out of scope: bar conversations, metric definitions, automation conversations, and where things stand summaries, which have their own responsibility test files but are separate modules.

## Test Files Found

| Layer | File | Coverage |
|---|---|---|
| Shared | `packages/shared/src/responsible-user-denial.test.ts` | Denial code classification and user-facing denial copy |
| Shared | `packages/shared/src/responsibility-status-reports.test.ts` | Report body validation, freshness, reporter choice, and overview helpers |
| Shared | `packages/shared/src/responsibility-metrics.test.ts` | Metric readiness, values, and display helpers |
| Shared | `packages/shared/src/responsibility-automation.test.ts` | Automation suggestion payloads and rules |
| Server | `server/src/__tests__/activity-log-responsible-user.test.ts` | Responsible user attribution for activity entries |
| Server | `server/src/__tests__/heartbeat-responsible-user-invariant.test.ts` | Run dispatch and manual wake authority under the responsible user invariant |
| Server | `server/src/__tests__/responsibilities-rollup.test.ts` | Attainment, status thresholds, overrides, sentences, signals, and delegation text |
| Server | `server/src/__tests__/responsibilities.test.ts` | Responsibility routes, company and owner scope, links, areas, delegation, skill filing, and agent changes |
| Server | `server/src/__tests__/responsibility-automation-conversations.test.ts` | Automation conversation routes and proposals |
| Server | `server/src/__tests__/responsibility-automation.test.ts` | Automation state and persistence |
| Server | `server/src/__tests__/responsibility-bar-templates.test.ts` | Starter bar templates |
| Server | `server/src/__tests__/responsibility-bars.test.ts` | Bar conversation routes and proposals |
| Server | `server/src/__tests__/responsibility-dashboard.test.ts` | Dashboard reads, conversations, change sets, decisions, versions, and restore |
| Server | `server/src/__tests__/responsibility-metrics.test.ts` | Metric routes and readings |
| Server | `server/src/__tests__/responsibility-runs.test.ts` | Recent run aggregation for responsibility detail |
| Server | `server/src/__tests__/responsibility-status-reports.test.ts` | Reporter choice, write authority, freshness, update requests, batch reads, and access rules |
| Server | `server/src/__tests__/responsibility-summaries-routes.test.ts` | Summary read routes |
| Server | `server/src/__tests__/responsibility-summaries.test.ts` | Summary state and persistence |
| Server | `server/src/__tests__/responsibility-summary-generator.test.ts` | Generated summary wording and attribution |
| Server | `server/src/__tests__/responsibility-tools.test.ts` | Agent tool schemas and authorization messages |
| Server | `server/src/services/native-runtime/runner-api-responsibilities.test.ts` | Runner API catalog access to responsibility routes |
| Server | `server/src/services/responsible-user-denial-run-outcomes.test.ts` | Run outcome persistence for responsible user denials |
| UI | `ui/src/api/responsibilities.test.ts` | API client paths, query parameters, and request bodies |
| UI | `ui/src/components/MobileBottomNav.responsibilities.test.tsx` | Mobile navigation entry for the Dashboard |
| UI | `ui/src/components/ResponsibleUserDenialNotice.test.tsx` | Denial notice wording |
| UI | `ui/src/components/responsibilities/AddExistingWorkPicker.test.tsx` | Existing work picker used when filing items |
| UI | `ui/src/components/responsibilities/AddResponsibilityDialog.test.tsx` | Add responsibility form and validation |
| UI | `ui/src/components/responsibilities/AreaDialogs.test.tsx` | Area create, edit, and delete dialogs |
| UI | `ui/src/components/responsibilities/AutomationProposalCard.test.tsx` | Automation proposal card |
| UI | `ui/src/components/responsibilities/BarProposalCard.test.tsx` | Bar proposal card |
| UI | `ui/src/components/responsibilities/DashboardChangesCard.test.tsx` | Proposed dashboard change card and decisions |
| UI | `ui/src/components/responsibilities/DashboardChatComposer.test.tsx` | Dashboard conversation composer and draft retention |
| UI | `ui/src/components/responsibilities/DashboardEditModule.test.tsx` | Empty dashboard creation module |
| UI | `ui/src/components/responsibilities/DashboardPersonaSwitcher.test.tsx` | Dashboard persona switcher |
| UI | `ui/src/components/responsibilities/MakeRoutineDialog.test.tsx` | Routine dialog used from responsibility work |
| UI | `ui/src/components/responsibilities/ProposedResponsibilitiesReview.test.tsx` | Proposed responsibility review card |
| UI | `ui/src/components/responsibilities/ResponsibilityDelegateDialog.test.tsx` | Delegation dialog and mode selection |
| UI | `ui/src/components/responsibilities/ResponsibilityMetricSet.test.tsx` | Metric set display and editing |
| UI | `ui/src/components/responsibilities/SectionTable.test.tsx` | Responsibility section table |
| UI | `ui/src/lib/responsibilities.test.ts` | Shared UI helpers for responsibility data |
| UI | `ui/src/lib/responsibility-agent-status.test.ts` | Written status row, counts, summary, areas, and metric column |
| UI | `ui/src/lib/responsibility-automation.test.ts` | Automation view helpers |
| UI | `ui/src/lib/responsibility-dashboard.test.ts` | Change grouping, dropped changes, and version wording |
| UI | `ui/src/lib/responsibility-one-screen-v2.test.ts` | One screen layout helpers |
| UI | `ui/src/lib/responsibility-outline-v2.test.ts` | Outline layout helpers |
| UI | `ui/src/lib/responsibility-summary.test.ts` | Summary display helpers |
| UI | `ui/src/lib/responsibility-views.test.ts` | Dashboard and detail view selection helpers |
| UI | `ui/src/pages/Responsibilities.test.tsx` | Dashboard page ordering, grouping, filters, proposals, loose work, and empty states |
| UI | `ui/src/pages/Responsibilities.views.test.tsx` | Outline, board, exceptions, automation, agent status, and outline v2 views |
| UI | `ui/src/pages/ResponsibilityDetail.test.tsx` | Detail page bar, work, skills, artifacts, status, and unlink undo |
| UI | `ui/src/pages/ResponsibilityDetail.v2.test.tsx` | One screen v2 sections, add flows, recent runs, and bar states |
| UI | `ui/src/pages/ResponsibilityDetail.views.test.tsx` | Scorecard, what is moving, one screen, and default view behavior |

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Status report body validation | Report body with a forged agent id or user id | Strict validation rejects the body |
| TC-2 | Status report freshness | Report written eight days ago | Report stays visible and reads as out of date |
| TC-3 | Reporter choice rules | Agents with different work counts under one responsibility | Busiest usable agent wins with a deterministic basis |
| TC-4 | Dashboard change set validation | Contradictory or dependent dashboard changes | Validation returns indexed issues before any write |
| TC-5 | Bar readiness | Half-filled metric fields | Bar reads as not measured and create is refused |
| TC-6 | Attainment and health thresholds | Current, target, direction, and override values | Attainment maps to on track, at risk, behind, or not measured |
| TC-7 | Status sentence formatting | Values with symbol and word units | Plain status sentence names the number, target, and unit |
| TC-8 | Work signal ordering | Mixed task, project, routine, and skill signals | Signals sort by tone and kind with bounded wording |
| TC-9 | Agent tool catalog | Responsibility tool schemas | Tools expose the intended routes and denial messages |
| TC-10 | Summary generation | Responsibility rollup rows | Generated paragraph uses the expected wording and AI label |
| TC-11 | Responsible user denial codes | Two denial codes and unrelated codes | Only responsibility denial codes normalize and describe a denied user |
| TC-12 | UI agent status row | Written report with stale flag | Written status leads, an out-of-date mark stays visible, and person authorship is named |
| TC-13 | UI dashboard change grouping | Mixed area and responsibility changes | Area changes sort first and dropped dependencies are listed |
| TC-14 | UI view helpers | Dashboard and detail fixtures | The active view and layout text match the selected view |
| TC-15 | UI responsibility helpers | Filing and rollup fixtures | Derived status, counts, and signals match the fixture |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-20 | Feature gate | Instance setting `enableResponsibilities` is off | Every feature route returns 404 with code `responsibilities_disabled` and remediation guidance |
| TC-21 | Board owner scope | Board owner, other board user, and company admin | Each actor can manage only their own responsibilities |
| TC-22 | Agent run authority | Agent run directed by one person with an authorizing user | The agent reads and changes only that person's dashboard |
| TC-23 | Filing and lookup | Project, task, routine, and skill rows | Links are created once, moved between responsibilities, found by lookup, and removed |
| TC-24 | Area management | Active and archived areas with responsibilities | Create is idempotent, edits are owner-only, delete keeps responsibilities, and shared areas split by owner |
| TC-25 | Delegation | Active responsibility and an assignable agent | A private task is created under the responsibility and assignment wakeup is queued |
| TC-26 | Detail aggregation | Responsibility with tasks, routines, projects, skills, and artifacts | Detail returns ordered work and skills in a fixed number of queries |
| TC-27 | Agent changes and versions | Agent acting for the directing person | Changes succeed, dashboard versions are saved, and the response names the version |
| TC-28 | Agent deletion | Agent delete attempt without and with an accepted card | Delete is refused until the owner accepts the card, and accepted chat replies work |
| TC-29 | Dashboard reads and conversation | Dashboard with create and edit states | Owners read their own state, access rules hold, and reads use a fixed number of queries |
| TC-30 | Change proposal | Conversation assigned to one agent | Only that agent proposes, and invalid change sets write nothing |
| TC-31 | Decision application | Proposal with dependent changes | Partial accept drops dependents, a stale change fails the whole apply, and decline closes the card without changes |
| TC-32 | Versions and restore | Saved versions including older snapshots | Restore recreates areas and responsibilities, prunes to the newest 30 versions, and upgrades older snapshots in place |
| TC-33 | Status reporter choice | Agents with and without work under a responsibility | Reporter starts with the top agent and moves to the agent doing the most work |
| TC-34 | Status write authority | Reporter, worker, owner, other agent, and other board user | Authorized writers create a report with the caller as author, and others are refused |
| TC-35 | Status reads | Ten active responsibilities with reports and history | Overview returns seven-query output, bounded history, current report, and a seven-day freshness window |
| TC-36 | Update request | Responsibility with a reporter and one open request | One private task is created, later requests stay pending, instructions list only visible work, and the reporter gets reminders |
| TC-37 | Privacy and attribution | Private dashboard conversations and wakes | Other users cannot wake private conversations and activity records resolve the responsible user |
| TC-38 | Runner API | Agent using `call_api` | Responsibility routes are callable from the runner API catalog |
| TC-39 | Dashboard and detail pages | Rendered pages with fixtures | Page order, status, proposals, work, skill, artifact, and undo behavior match the fixtures |
| TC-40 | Dashboard components | Rendered dialogs, cards, composer, and navigation | Each control sends the expected call and keeps useful state such as the composer draft |
| TC-41 | UI API client | Calls through `responsibilitiesApi` | Paths, owner filters, area calls, links, delegation, and status reads match the route contract |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-50 | Browser end-to-end coverage | Search found no dedicated Playwright or release-smoke case for this feature | No browser end-to-end evidence is recorded, and route and UI integration tests carry the coverage |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-60 | Feature disabled on any route | The response distinguishes turned-off from empty with code `responsibilities_disabled` |
| TC-61 | Agent without a directing person creates a responsibility | The call creates a full bar proposal rather than a title-only responsibility |
| TC-62 | Board user creates a title-only responsibility | The row reads as not measured |
| TC-63 | Caller sends both `areaId` and `areaTitle` | Validation refuses the mixed input |
| TC-64 | Area creation succeeds but a later create step fails | No orphan area remains |
| TC-65 | Two agent calls create the same title at once | One live responsibility is reused |
| TC-66 | Company administrator reads another person's dashboard | The request is refused |
| TC-67 | Agent names another person's run authority | The request is refused |
| TC-68 | Work is filed under several responsibilities | Each responsibility has one link and totals count the item once |
| TC-69 | Deleted or unreachable linked item | Link errors and detail views explain the missing item |
| TC-70 | Responsibility is not active | Status writes, status requests, filing without owner authority, and delegation are refused |
| TC-71 | Company has no agent that can take work | Reporter is null and owner status writing remains available |
| TC-72 | Report body contains markup, only a status word, or more than four detail lines | Validation refuses the body |
| TC-73 | Report body tries to set `agentId` or `userId` | Strict validation refuses the body |
| TC-74 | Report is older than seven days | It stays visible and reads as out of date |
| TC-75 | More than ten reports exist | Read returns the newest ten including current |
| TC-76 | Status request already exists | A later request stays idle instead of creating another task |
| TC-77 | Proposal drops a new area but keeps a dependent responsibility | The dependent change is dropped and the action is recorded |
| TC-78 | Proposal no longer fits the current dashboard | The entire apply fails and the card stays waiting |
| TC-79 | More than 30 versions are saved | Older versions are pruned |
| TC-80 | Restored version predates skill filing or health fields | Restore leaves unsupported fields alone and can upgrade the snapshot in place |
| TC-81 | Restored area name is now used by a live area | Restore uses the live area |
| TC-82 | Shared area is renamed by one owner | Only that owner's copy changes |
| TC-83 | Legacy area has no owner | The area is hidden from dashboards |
| TC-84 | Agent deletes a responsibility | Deletion requires an accepted confirmation card and is not undoable |
| TC-85 | Data belongs to another company | Every route isolates the request |

## Test Infrastructure

- Server route tests seed a Postgres test database with a company, two owner ids, and agents named builder, analyst, lead, and ceo.
- Server tests use an Express app factory, a request client, and direct database reads for activity and report rows.
- Query count tests wrap the Drizzle client with a query logger and call services with ten responsibilities.
- UI tests use React Testing Library, mocked API modules, fixture overviews, and fixture detail payloads.
- Runner API tests use the native runtime catalog with an agent actor.
- No browser test server or Playwright fixture was found for this feature.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-20, TC-21 |
| FR-2 | TC-22, TC-29, TC-37 |
| FR-3 | TC-5, TC-6, TC-7, TC-26 |
| FR-4 | TC-23, TC-24, TC-26, TC-40 |
| FR-5 | TC-25 |
| FR-6 | TC-27, TC-32 |
| FR-7 | TC-30 |
| FR-8 | TC-31 |
| FR-9 | TC-32 |
| FR-10 | TC-1, TC-2, TC-33, TC-34, TC-35, TC-36 |
| FR-11 | TC-3, TC-33 |
| FR-12 | TC-36 |
| FR-13 | TC-1, TC-34 |
| FR-14 | TC-20, TC-27, TC-31, TC-32, TC-34, TC-37 |
| FR-15 | TC-22, TC-29, TC-37, TC-40 |
| FR-16 | TC-20, TC-39, TC-40 |
| FR-17 | TC-26, TC-39, TC-40 |
| FR-18 | TC-2, TC-12, TC-14, TC-39 |
| FR-19 | TC-24, TC-27 |
| NFR-1 | TC-20, TC-21, TC-22, TC-29, TC-34 |
| NFR-2 | TC-29, TC-37 |
| NFR-3 | TC-27, TC-31, TC-32 |
| NFR-4 | TC-26, TC-29, TC-35 |
| NFR-5 | TC-32, TC-35 |
| NFR-6 | TC-20, TC-29, TC-35 |

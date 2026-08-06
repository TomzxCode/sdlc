---
title: "Web Dashboard, Teams & Run UI"
status: done
---

# Test Plan: Web Dashboard, Teams & Run UI

## Scope

Testing the dashboard/team/run UI surfaces: team scoping and CRUD, dashboard poll refresh, loop and run detail pages, live activity card, timeline, compose modal, and the no-horizontal-scroll regression guards. Out of scope: onboarding wizard, template market, and notification binding internals (separate features).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | `requestScope` prefers the explicit teamId over the cookie | Route param vs cookie value | Route param wins |
| TC-2 | Non-member team scope is a generic not-found | Non-member `/t/<x>` | Same not-found as a missing loop (enumeration-safe) |
| TC-3 | Team CRUD authorizes by membership + role | Member vs owner action | Owner-only controls; server re-authorizes regardless |
| TC-4 | Last-owner guard is transactional | Concurrent self-removals | One wins; team never memberless |
| TC-5 | Delete is blocked while the team owns loops | Team with loops, delete attempt | `countLoopsForTeam` blocks; delete never cascades |
| TC-6 | Invite redeem outcomes | invalid / used / expired / already-member / fresh | Correct per-branch result; single-use stamping |
| TC-7 | Dashboard poll keeps stale data on a blip | Transient listJobs failure | Stale data kept, no loader throw |
| TC-8 | Run detail live activity renders only while running | `run.running` true vs false | LiveActivity mounted only for running; terminal pages byte-identical |
| TC-9 | Copy-prompt is agent-neutral and pure | Loop with a derivable on-disk dir | Prompt names the loop dir; generic copy names no vendor agent |
| TC-10 | Timeline is one form at every zoom | day / week / month | Only the window changes; lane = loop, marks = runs |
| TC-11 | Timeline projects future fires | Loop with a daily cron | Dashed ghosts past the now-line, capped per loop |
| TC-12 | Compose modal handles all three shapes | blank / template / bundle | One modal; template/bundle snippets share connect-key machinery |
| TC-13 | Machine presence is three-state | lastSeen deltas | online <30s / asleep <6h / offline |
| TC-14 | Files panel dedups the task file and shows front-matter chips | Synced task file + products | Task file once with TASK treatment; type/title chips for products |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-15 | Team CRUD end-to-end against pglite | Real pglite store, seeded users/teams | 15 scenarios pass (create, invite, role change, leave, delete guards) |
| TC-16 | Team URL scope integration | Teams A/B with distinct data | `/t/A` and `/t/B` show different teams; switch re-seeds state |
| TC-17 | Loop form model persistence | LoopForm state | Model persists across edits |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-18 | Page-level horizontal scroll regression | `*.regression.test.ts` guards stay green (grid/flex `min-w-0`) |
| TC-19 | Recharts animation flash | All animation off including `<Tooltip isAnimationActive={false}>` |
| TC-20 | Cross-team loop detail access | Teammate can't see another team's loop internals beyond scope |
| TC-21 | Timeline beyond the run-query cap | `truncated` surfaced, never silently clipped |

## Test Infrastructure

- vitest with jsdom; client renders under `act`; Recharts mounts via effects with a jsdom ResizeObserver stub.
- Integration tests run against real pglite (`teamCrud.integration.test.ts`, `teamUrlScope.integration.test.ts`).
- Source-reading guards keep paths in a variable (vite rewrites the literal `new URL` form).

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-16 |
| FR-2 | TC-2 |
| FR-3 | TC-7 |
| FR-4 | TC-12 |
| FR-5 | TC-8 |
| FR-6 | TC-9 |
| FR-7 | TC-10, TC-11 |
| FR-8 | TC-3, TC-6 |
| FR-9 | TC-4, TC-5 |
| FR-10 | TC-12 |
| FR-11 | TC-18 |
| FR-12 | TC-14 |
| NFR-1 | TC-3 |
| NFR-2 | TC-4 |
| NFR-3 | TC-19 |
| NFR-4 | lazy-loaded LoopView chunk |
| NFR-5 | source-reading guard tests |

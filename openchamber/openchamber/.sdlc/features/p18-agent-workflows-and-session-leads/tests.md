---
title: "Agent workflows and session leads"
status: done
---

# Test plan: Agent workflows and session leads

## Scope

The plan covers workflow script parsing, sandboxed execution, run persistence and recovery, agent session creation and replay, schema answers, HTTP routes, UI run state, and lead brief, digest, handover, and compaction behavior.
It covers the server-side flow tests that propose, approve, run, and report a workflow end to end.
It excludes browser automation and product documentation rendering.
No separate browser end-to-end suite exists for this feature; the full flow is exercised by server integration tests.

## Unit tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-01 | Parse meta and body | Script with an exported meta literal and an agent body | Name, description, phases, and body split |
| TC-02 | Parse phases from `phase()` calls | Meta with no phases and two `phase()` titles | Those titles in call order |
| TC-03 | Run sandbox primitives | Body calling agent, phase, log, parallel, and pipeline with args | Calls relayed, values returned, failed tasks mapped to null |
| TC-04 | Isolate and stop the sandbox | Body reading host names, using blocked dates, and looping forever | Names unavailable, blocked dates throw, worker terminates on stop |
| TC-05 | Validate JSON Schema answers | Matching and mismatching values, bare and fenced JSON, a required key excluded by `additionalProperties: false` | Validation errors with paths, parsed fenced answer, contradiction reported |
| TC-06 | Order run writes | A failing save followed by a queued save | Failure rejects its caller, later write commits, no phantom first run |
| TC-07 | Lighten settled runs | A settled run with a long script, prompts, and answers | Empty script and prompts, 400-character previews, full record on `get()` |
| TC-08 | Read process start identity | Linux, macOS, and Windows probes plus an invalid PID | Stable platform identity, null for invalid PID |
| TC-09 | Group and total panel data | Agents in planned and ad-hoc phases, replayed agents, zero-cost subscriptions | Stable phase order, measured spend only, text or JSON answers |
| TC-10 | Reconcile UI run state | Reads, events, deletions, and runtime changes in different orders | Deleted runs stay out, events win over older reads, stale reads never land |
| TC-11 | Resolve project scope | A worktree session, a plain folder, and an isolated space | Project root plus worktrees for runs, root for saved scripts, own scope for a space |
| TC-12 | Parse digest input | Lists, JSON strings, newline lists, options, recommendations, excluded suggestions | Normalized digest, validation errors, dismissed items dropped |
| TC-13 | Enforce lead action rules | Non-lead caller, whole brief, edits, digest, and a repeated digest | 409 for non-leads, bounded writes, whole-digest replacement with timestamp |
| TC-14 | Hold the brief entry | Read, write, refresh as lead, refresh as non-lead | Earlier brief held until refresh, then current brief, then dropped |
| TC-15 | Choose auto-approval mode | All runs on, leads only on, and both off with ordinary and lead callers | Correct immediate or waiting decision for each combination |
| TC-16 | Parse lead reply helpers | Lead metadata and reply objects | Answer text and dismissal updates without losing existing fields |

## Integration tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-17 | Propose, approve, and report | Enabled tool, valid script, mocked agent sessions | Stored awaiting run, immediate tool answer, agents start on approval, synthetic report delivered |
| TC-18 | Start without approval and stop | Auto-approval on | First state running with an explanatory log line, stop interrupts agents, no session wake |
| TC-19 | Cap concurrency and agent count | More calls than slots and a run at its agent cap | At most 8 working agents, further calls resolve to null and log the limit |
| TC-20 | Accept schema answers through the tool | Prompt with a schema and an answer slot | Tool answer wins over final text, attempts repeat up to three times, refusal outside a slot is 403 |
| TC-21 | Replay and fork on resume | A stopped run with completed and failed calls | Completed calls replay with a replayed flag, named forks resolve to completed sessions, bad names fail before prompts |
| TC-22 | Manage agent sessions | Parent with rules and model, source session for a fork | Metadata link without OpenCode parentID, inherited model and rules, answer tool allowed, fork reads source before prompting |
| TC-23 | Serve workflow routes | Runtime with stubbed methods | Session and repeated directory queries, saved body pass-through, preserved error statuses |
| TC-24 | Recover from failed checkpoints | Injected failures at proposal, approval, terminal save, and delivered-marker save | Rollback or truthful ended state, no duplicate delivery, no rerun of agents |
| TC-25 | Deliver and delete runs | Delivered, undelivered, running, and awaiting runs | 409 counts as delivered, deletion is final, an active run must stop or decline first |
| TC-26 | Save and start saved workflows | Saved script plus a session or no session | Script written with newline, listed with description or error, run starts at once in chosen or new session |
| TC-27 | Compact a sleeping lead | Lead with a large context, expired cache, stored brief, and hook calls | Authored note once, model fallback without a brief, stand down for warm or busy sessions |
| TC-28 | Hand a session to a lead | Ordinary session and a valid lead | Denied question and secret tools, ownWork link, wake note, registration of a running session's result, undo on failure |
| TC-29 | Clear inherited lead metadata | A new child and a fork of a lead | Copied mark and digest cleared on creation, fork drops the mark |

## End-to-end tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-30 | Propose to report flow | Call workflow.run, approve, let agents answer, inspect the synthetic message | The run completes and the proposing session receives one report with the run's id and name |
| TC-31 | Saved workflow from panel to session | Start a saved script with no session open, inspect the new session and run | The run starts at once and its report returns to the new session |
| TC-32 | Recovery to delivery flow | Leave a run recorded as running, restart, connect the event hub | The run is stopped and its report is delivered once |

## Edge cases and failure scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-33 | Workflows turned off | Tool actions answer 403 and no run is stored |
| TC-34 | Another session reads a run | Status and result answer 403 |
| TC-35 | Stop arrives before the worker exists | Termination is honoured once the worker starts |
| TC-36 | Schema contradiction | The agent fails before a prompt is sent |
| TC-37 | Answer tool called outside a schema slot | The call is refused with 403 |
| TC-38 | Duplicate `id` or unknown `forkFrom` | The call is rejected and the run fails before a prompt |
| TC-39 | Owner PID still alive or process identity reused | A matching live owner is skipped and a reused PID with different identity is recovered |
| TC-40 | Report marker save fails | The delivered flag and report id stay in memory and a 409 reconciles on reload |
| TC-41 | Brief edit text is absent or repeated | Nothing is written and the answer names the failed edit |
| TC-42 | Digest written without a brief or after the user unmarked the lead | Nothing is written and the answer explains why |
| TC-43 | A lead with a staged undo or a session that already runs a child | Handover is refused with 409 |
| TC-44 | Stale read or event after deletion or runtime change | The deleted run never returns and the retired runtime's response is ignored |
| TC-45 | Unreadable run file | It is moved aside and the remaining runs load |
| TC-46 | A fork whose source records cannot be read | No prompt is sent and no fork is recorded |

## Test infrastructure

- `packages/web/server/lib/workflows/script.test.js` — parser and phase planning.
- `packages/web/server/lib/workflows/sandbox.test.js` — worker, fan-out, pipeline, isolation, and termination.
- `packages/web/server/lib/workflows/json-schema.test.js` — schema validation and answer parsing.
- `packages/web/server/lib/workflows/store.test.js` — write ordering, snapshots, lightening, and full reads.
- `packages/web/server/lib/workflows/process-owner.test.js` — platform process identity.
- `packages/web/server/lib/workflows/runtime.test.js` — lifecycle, limits, recovery, deletion, and report delivery.
- `packages/web/server/lib/workflows/agent-session.test.js` — session links, permissions, models, and forks.
- `packages/web/server/lib/workflows/routes.test.js` — route parsing and error propagation.
- `packages/web/server/lib/session-lead/runtime.test.js` — digest, brief, compaction, handover, auto-approval, and inherited metadata.
- `packages/ui/src/lib/workflows/model.test.ts` — summaries, totals, phase grouping, and report envelopes.
- `packages/ui/src/lib/workflows/store.test.ts` — event and read reconciliation.
- `packages/ui/src/lib/workflows/project.test.ts` — project and worktree scope.
- `packages/ui/src/lib/sessionLead.test.ts` — lead metadata helpers and dismissed suggestions.
- Tests inject filesystem, fetch, timer, and process probes; no external OpenCode server or browser is required.
- The agent sessions and synthetic report posts are stubbed with in-memory doubles.

## Coverage matrix

| Requirement | Test cases |
|---|---|
| FR-01 | TC-01, TC-02, TC-30 |
| FR-02 | TC-33 |
| FR-03 | TC-17, TC-30 |
| FR-04 | TC-17, TC-18, TC-35 |
| FR-05 | TC-03, TC-04 |
| FR-06 | TC-21, TC-22 |
| FR-07 | TC-22 |
| FR-08 | TC-22 |
| FR-09 | TC-03, TC-21, TC-38 |
| FR-10 | TC-03, TC-09, TC-19 |
| FR-11 | TC-05, TC-20, TC-36, TC-37 |
| FR-12 | TC-21 |
| FR-13 | TC-06, TC-07, TC-08, TC-24, TC-32, TC-39, TC-45 |
| FR-14 | TC-17, TC-25, TC-30, TC-32, TC-40 |
| FR-15 | TC-26, TC-31 |
| FR-16 | TC-23, TC-25, TC-26, TC-34 |
| FR-17 | TC-09, TC-10, TC-44 |
| FR-18 | TC-13, TC-16, TC-42 |
| FR-19 | TC-29 |
| FR-20 | TC-13, TC-14, TC-41 |
| FR-21 | TC-14 |
| FR-22 | TC-12, TC-13, TC-16, TC-42 |
| FR-23 | TC-28, TC-43 |
| FR-24 | TC-14; adjacent suites `session-knowledge/runtime.test.js`, `openchamber-sessions/work-naming.test.js`, and `agent-tool/runtime.test.js` cover guidance entries and lead naming |
| FR-25 | TC-27 |
| FR-26 | TC-15, TC-18 |
| FR-27 | TC-12, TC-16 |
| FR-28 | TC-30, TC-31; runtime availability is documented in `packages/docs/content/docs/workflows.mdx` |
| NFR-01 | TC-03, TC-04 |
| NFR-02 | TC-06, TC-24, TC-25, TC-40 |
| NFR-03 | TC-07, TC-19 |
| NFR-04 | TC-09, TC-23, TC-30 |
| NFR-05 | TC-34, TC-37 |

---
title: "Todo and Goal Tracking"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Test Plan: Todo and Goal Tracking

## Scope

Covers the pure todo policy crate (quality-gate bars, continuation messages, transcript classifiers, the turn-end follow-up state machine, and the on-disk layout), the domain model in `jcode-task-types`, the `todo` and `initiative` tools, the todo persistence helpers in `jcode-base`, the goal and side-panel storage, and the terminal surfaces (the todo card, the pinned band, the info widget, and the auto-poke loop in the TUI and in `jcode run`).
Out of scope: the swarm plan DAG and its projections, live terminal interaction, and provider network behaviour.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Semantic states serialize as snake_case strings, parse case-insensitively, and map legacy 0-100 numbers onto the closest state | `crates/jcode-task-types/src/lib.rs` (inline `semantic_state_tests`) | Every state round-trips, a legacy number maps onto the closest band, and an out-of-range value is rejected. |
| TC-2 | Legacy todo, plan, and goal payloads still load, and the current field names are the only ones written back | `crates/jcode-task-types/src/lib.rs` (inline `semantic_state_tests`) | A payload with `hill_climbability`, `end_to_end_ownership`, and `alignment_score` loads onto the current fields, and the legacy names are absent from the serialized output. |
| TC-3 | The quality-gate bars, including the difficulty-calibrated relevance, coverage, and traceability requirements, the delivery bar, autonomy, iteration maturity, and stopping evidence | `crates/jcode-todo-policy/src/tests.rs` | An involved-difficulty goal with a synthetic or representative relevance fails, the delivery bar is never raised by difficulty alone, and a confirmed plateau needs stopping evidence. |
| TC-4 | The turn-end gate digest: a late climb is still raised, repeats collapse with a count, goals are separated by group, and the ungrouped goal renders cleanly | `crates/jcode-todo-policy/src/tests.rs` | One digest line per point, with the "started this work without understanding" wording for a late climb, a "flagged N times" count for repeats, and no empty quoted label for the ungrouped goal. |
| TC-5 | The synthetic continuation messages, their classification as non-user prompts, and the short user-facing display summaries | `crates/jcode-todo-policy/src/tests.rs` | Every built continuation is recognised by `is_auto_poke_message`, the spike and completion continuations name the target todos, and a real user prompt is never classified as synthetic. |
| TC-6 | Continuation privacy, the static token budget, and the cap on the number of named todos | `crates/jcode-todo-policy/src/tests.rs` | No continuation contains a threshold, percent, score, or gate wording, every static message stays within the approximate 64-token budget, and a 40-item list names 6 todos and summarizes the rest. |
| TC-7 | Session title derivation from the todo plan | `crates/jcode-todo-policy/src/tests.rs` | The title prefers the in-progress item's group, then the latest incomplete item's group, then the plan intention, then the item content. |
| TC-8 | The turn-end follow-up state machine: the decision order, the arm and disarm rules, the digest and gate budget, and the snapshot round trip | `crates/jcode-todo-policy/src/followup_tests.rs` | The digest is sent before validation and the final handoff, the final handoff is sent once, the gate budget trips with a notice, and new work re-arms the policy. |
| TC-9 | The on-disk layout, the tolerant snapshot load, and the effect application | `crates/jcode-todo-policy/src/store.rs` (inline `mod tests`) | The file names match the runtime layout, a missing session yields an empty snapshot, and clearing the observations and marking the review delivered are idempotent. |
| TC-10 | The `todo` tool schema and input parsing | `crates/jcode-app-core/src/tool/todo.rs` (inline `mod tests`) | The schema advertises the intent, todos, plan, and goals properties with the constrained enums, hides the legacy keys, discloses no calibration wording, and parses native, stringified, and synonym inputs. |
| TC-11 | The todo tool merge, prune, and change-reporting logic | `crates/jcode-app-core/src/tool/todo.rs` (inline `mod tests`) | Unmentioned goals and omitted fields are retained, a goal whose group is gone is dropped, the plan and goal changes list only the changed fields, and a forged score history is discarded in favor of the stored trail. |
| TC-12 | The todo telemetry derivation | `crates/jcode-app-core/src/tool/todo.rs` (inline `mod tests`) | Created, completed, abandoned, group, and score summaries are derived, regrouping is not counted as creation or abandonment, and the empty state is all zeros. |
| TC-13 | The todo widget rendering in the info widget | `crates/jcode-tui/src/tui/info_widget_tests.rs` | The item and aggregate confidence, the group headers, the exact pips for a small list, the feedback-loop suffix on the flat and grouped layouts, and the empty-goal case all render as expected. |
| TC-14 | Info widget layout contention between the todo widget and the background task widget | `crates/jcode-tui/src/tui/info_widget_layout_tests.rs` | The todo widget wins a short pocket without overlapping the background widget, and both place disjointly when there is room for two. |
| TC-15 | Auto-poke re-arm after the completion-gate circuit breaker | `crates/jcode-tui/src/tui/app/tests/state_model_poke_03.rs` | Open work re-arms auto-poke and still produces a poke, so one breaker trip cannot silence the feature for the session. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-16 | The `todo` tool writes the list, the plan, and the goals against an isolated home, and publishes the update | `crates/jcode-app-core/src/tool/todo.rs` (inline async tests) | The stored state matches the write, the bus event is published, and the panel shows only the current task. |
| TC-17 | The gate deferral end to end through the real tool | `crates/jcode-app-core/src/tool/todo.rs` (inline async tests) | A moderate first write returns no continuation and records the observations instead, the histories accumulate, and a later climb changes the digest wording rather than erasing the point. |
| TC-18 | Goal creation, persistence, the memory mirror, session attachment, and resume | `crates/jcode-base/src/goal_tests.rs` | The goal is stored under the project scope, mirrored into the memory graph, attached to the session, and returned by resume. |
| TC-19 | The goal page focus behaviour | `crates/jcode-base/src/goal_tests.rs` | The first goal page takes the focus, and a page written later does not steal the focus from an unrelated page. |
| TC-20 | The `initiative` tool create, resume, list, and update actions | `crates/jcode-app-core/src/tool/goal_tests.rs` | Create and list publish no side panel update, resume returns the initiative with its next step, and update refreshes an open overview while keeping the focus on the goals page. |
| TC-21 | The todo state files, the gate observation log, and the long-session review clock | `crates/jcode-base/src/todo.rs` (inline `mod tests`) | The observations round-trip and clear, the plan round-trips without the legacy key names, and the timed review is durable and fires only once. |
| TC-22 | The side panel page persistence, focus, and PDF budget | `crates/jcode-base/src/side_panel_tests.rs` | Pages persist and focus the latest, deletion falls back to the most recent page, the focus revision tracks explicit intent, and the aggregate budget is enforced before mutation. |
| TC-23 | The TUI todo card, the panel toggle, and the pinned payload | `crates/jcode-tui/src/tui/app/tests/todo_card.rs` | The card toggles and never stacks, the panel subcommand toggles the screen, the card refreshes when the todos or the goal scores change, and the pinned payload is empty when the config is off. |
| TC-24 | The TUI auto-poke cycles, the reload survival of the final handoff, and the peer poke handling | `crates/jcode-tui/src/tui/app/tests/auto_poke_cycles.rs` | A todo-free turn keeps the feature armed, an unchanged list does not consume another turn, the final handoff survives a reload, a late observation does not resurrect the gates, and a peer poke is shown without a duplicate local poke. |
| TC-25 | The `jcode run` auto-poke loop | `src/cli/commands_tests.rs` | Incomplete todos are poked first, the deferred gate digest is delivered before the confidence check, the digest log survives a poke iteration that still has open work, and the loop stays silent once the confidence is earned. |
| TC-26 | The SDK capability parity for the todo state surface | `crates/jcode-sdk/src/sdk_tests/parity.rs` | The Rust and TypeScript SDKs both implement `todo_state` and `ack_todo_follow_up`, and neither exposes a public capability that is missing from the shared list. |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-27 | The pinned todo band render regressions on a fresh session | `crates/jcode-tui/src/tui/ui_tests/pinned_todo_regressions.rs` | The band appears without consuming the prompt, the content height grows when the band appears, and a hidden todo tool message contributes zero transcript rows while the surrounding messages keep their positions. |
| TC-28 | The pinned band placement, the collapse control, and the hiding of the duplicate todo card | `crates/jcode-tui/src/tui/app/tests/todo_card.rs` | The band renders below the sticky prompt with no separator, the more row expands and collapses the band, the todo tool card is hidden from the transcript while the band shows the item, and the pinned todos are omitted from the info widgets. |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-29 | An unknown todo status such as "blocked" is sent | The call is rejected with an error naming the valid vocabulary, and the error lists pending, in_progress, completed, and cancelled. |
| TC-30 | The provider sends the whole todos array as a JSON string, an item as a stringified object, and a numeric confidence as a string | The call succeeds, the array and the item are parsed, and the numeric confidence maps onto the closest semantic state. |
| TC-31 | The agent replaces the todo list with a new task while a goal for the finished task is still stored | The orphan goal is dropped so the panel does not show a stale goal, and the ungrouped goal of a flat list is kept while it still has items. |
| TC-32 | The model supplies its own confidence history, plan history, or goal history | The supplied trail is discarded in favor of the stored trail plus the current write's observation, so a climb cannot be fabricated. |
| TC-33 | A group is created and completed in a single write | The group is still observed, because a one-step completion is where a weak feedback loop would otherwise hide. |
| TC-34 | A session id such as "../x" is used to build a todo state path | The session id is reported as unsafe, and the path cannot escape the todo state directory. |
| TC-35 | A very long iterative turn records more observations than the cap | The log keeps only the most recent capped number of observations, and the digest loses no information it would have reported. |
| TC-36 | The completion gate never passes across more turns than the gate budget allows | The policy stops sending continuations, surfaces a stall notice, stays quiet until new work appears, and pokes again once new open work exists. |
| TC-37 | The user turns the auto-poke off and open work appears later | The poke stays off for the rest of the session, and the default-on re-arm does not undo the explicit turn-off. |
| TC-38 | Another window pokes the same open work | The peer poke is shown as a system notice, is not rendered as a user prompt, and this window does not send a duplicate poke. |

## Test Infrastructure

- The pure policy crate needs no fixtures beyond in-memory structs, and it is the only place where the gate bars and the continuation text are pinned.
- The runtime tests isolate the state on disk with a temporary `JCODE_HOME` and the `storage::lock_test_env` guard, so parallel tests do not share a todo directory.
- The tool tests build a `ToolContext` with a synthetic session id and a temporary project directory.
- The TUI tests drive the app through `create_test_app` and render it with the ratatui `TestBackend`, and they serialize on the render and viewport snapshot locks.
- The pinned band tests write an isolated `config.toml` with `display.pin_todos` and restore the previous home and config cache afterwards.
- The SDK parity test compares the Rust and TypeScript client sources against a shared capability list.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-9, TC-16, TC-21 |
| FR-2 | TC-10, TC-29, TC-30 |
| FR-3 | TC-13, TC-23 |
| FR-4 | TC-2, TC-11, TC-17 |
| FR-5 | TC-1, TC-2, TC-11 |
| FR-6 | TC-3 |
| FR-7 | TC-5, TC-11, TC-32 |
| FR-8 | TC-4, TC-17, TC-33 |
| FR-9 | TC-16, TC-17 |
| FR-10 | TC-11, TC-31 |
| FR-11 | TC-5, TC-6 |
| FR-12 | TC-5, TC-6 |
| FR-13 | TC-8, TC-25 |
| FR-14 | TC-8, TC-36 |
| FR-15 | TC-12, TC-16 |
| FR-16 | TC-18, TC-19, TC-20, TC-22 |
| FR-17 | TC-20, TC-22 |
| FR-18 | TC-13, TC-23, TC-27, TC-28 |
| FR-19 | TC-7 |
| FR-20 | TC-8, TC-21, TC-26 |
| FR-21 | TC-1, TC-2, TC-9, TC-21 |
| FR-22 | TC-15, TC-24, TC-37, TC-38 |
| NFR-1 | TC-6, TC-10 |
| NFR-2 | TC-10 |
| NFR-3 | TC-6 |
| NFR-4 | TC-6 |
| NFR-5 | TC-35 |
| NFR-6 | TC-16, TC-17 |
| NFR-7 | TC-1, TC-2, TC-5, TC-21 |
| NFR-8 | TC-9, TC-34 |
| NFR-9 | TC-13, TC-14 |
| NFR-10 | TC-27, TC-28 |
| NFR-11 | TC-10, TC-30 |

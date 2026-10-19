---
title: "Todo and Goal Tracking"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Todo and Goal Tracking

## Overview

The agent keeps a session-scoped working memory that the user can watch live.
A plan records the intent the user actually expressed, broken into goals, each with steps, a quality gate, and a completion-confidence score.
The goal-level gate distinguishes a closed feedback loop from a taste judgment, so the model cannot fake progress on work that has no measurable signal.
The `todo` tool writes items, groups, and plan-level assessments, and the `initiative` tool drives long-running goals and refreshes the goal side panel without stealing focus.
A shared policy layer generates the synthetic continuation messages (auto-poke, gate digest, ownership, final response) and the same policy ships to the SDK and any embedding client.
This feature was reverse-engineered from the existing codebase during an SDLC sync, so it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | A live, honest view of what the agent is doing, why it thinks the work is progressing, and what is still blocked. |
| Agent authors | A tool contract that records intent, per-goal quality gates, and evidence state without letting the model grade its own homework. |
| Embedding clients (SDK, Desktop) | One shared follow-up policy so every client pokes, gates, and hands off identically. |
| Maintainers | A single pure policy crate that can be unit-tested without a runtime, a terminal, or a provider. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall persist a session-scoped todo list whose items carry content, status, priority, id, an optional group label, and evidence-state confidence fields, and shall reload it across turns and across session resume. |
| FR-2 | Must | The system shall accept only the todo statuses pending, in_progress, completed, and cancelled, shall canonicalize natural completion synonyms and case variants into them, and shall reject any other status with an error naming the valid vocabulary. |
| FR-3 | Must | The system shall group todos under an optional group label, one group per coherent goal, and shall render a grouped list with per-group headers and a flat list without them. |
| FR-4 | Must | The system shall record a plan-level intent assessment exactly once per plan, holding the user's stated intention and how well the agent understands it, independently of any individual group. |
| FR-5 | Must | The system shall record a goal-level quality assessment per group, covering the closed feedback loop state, the concrete feedback loop, its relevance, coverage, traceability, the delivery state, difficulty, autonomy, iteration maturity, and any stopping evidence. |
| FR-6 | Must | The system shall distinguish a goal with a closed feedback loop from a goal whose success is a taste judgment, and shall require acceptance-aligned relevance and edge-and-integration coverage for goals at or above the involved difficulty level. |
| FR-7 | Must | The system shall record a forward-looking evidence state per todo, an evidence state at completion, and a tool-owned history of every distinct state a todo has carried, so that an evidence-driven rise is distinguishable from a bulk end-of-task stamp. |
| FR-8 | Must | The system shall defer the quality-gate checks to turn end, recording an observation for every failing check during the turn and replaying them once as a digest, with the single exception of a first plan write whose intent assessment is severely low. |
| FR-9 | Must | The system shall never reject a todo write because a gate would fail, and shall save the write first and enforce the gate after the turn ends. |
| FR-10 | Must | The system shall merge each write with the stored state so that an omitted plan field, an omitted goal field, and a goal the write does not mention are all retained, and shall drop a goal whose todo group no longer exists. |
| FR-11 | Must | The system shall generate every synthetic continuation message (the incomplete-todo poke, the intent check, the feedback-loop check, the ownership check, the completion-confidence check, the confidence-spike check, the gate digest, and the final-response handoff) from one shared policy layer, and shall keep the private thresholds, scores, and elapsed-time trigger out of the model-facing text. |
| FR-12 | Must | The system shall classify those synthetic messages so the transcript never re-renders them as user prompts, and shall show a short user-facing notice in their place. |
| FR-13 | Must | The system shall decide the next follow-up after a turn ends in a fixed order: the long-session review, the incomplete-todo poke, the gate digest, the ownership gate, the completion-confidence check, the confidence-spike check, and finally the final-response handoff. |
| FR-14 | Must | The system shall bound the number of gate turns per completion cycle, surface a stall notice when the bound is reached, and re-arm for new work afterwards. |
| FR-15 | Must | The system shall expose a `todo` tool that reads and writes the todo list, the plan, and the goal assessments, that publishes the update on the bus, and that records lifecycle telemetry. |
| FR-16 | Must | The system shall expose an `initiative` tool that creates, lists, shows, resumes, updates, checkpoints, and focuses durable goals scoped to the project or to the user, and that refreshes an already-open goal side panel without stealing focus. |
| FR-17 | Must | The system shall never open the side panel from the initiative tool, and shall leave the opening of the goals overview to an explicit user command. |
| FR-18 | Must | The system shall surface the todo state in the terminal user interface as an inline chat card, an optional side-panel screen, an optional pinned band, and the persistent info widget, and shall keep the overall completed-of-total progress display visible in each of them. |
| FR-19 | Should | The system shall derive a session title from the todo plan, preferring the group of the current or latest incomplete item, then the plan intention, then the item text. |
| FR-20 | Should | The system shall ship the same policy to the SDK and to any embedding client, exposing the session todo state and a follow-up acknowledgement so those clients run the identical follow-up policy. |
| FR-21 | Should | The system shall load sessions recorded before the semantic-state migration, mapping legacy 0-100 numeric scores and the legacy field names onto the current semantic states. |
| FR-22 | May | The system shall let the user turn the auto-poke on and off, and shall make an explicit turn-off stick for the rest of the session. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The model-visible tool schema and every synthetic continuation message shall not disclose the private thresholds, the numeric scores, or the evaluator vocabulary, so the model cannot target the evaluator instead of reporting an honest assessment. |
| NFR-2 | Must | Neutrality | The model-visible tool schema shall not be biased toward one domain's validation vocabulary, so the feedback-loop guidance stays equally applicable to every kind of work. |
| NFR-3 | Must | Performance | Each static quality-gate continuation message shall stay within an approximate budget of 64 tokens, so it reads as a nudge rather than as a replacement system prompt. |
| NFR-4 | Must | Performance | A gate continuation shall name at most 6 todos explicitly and shall summarize the remainder, so a large plan cannot turn one nudge into a wall of text. |
| NFR-5 | Must | Availability | The deferred gate-observation log shall be capped per session, so a very long iterative turn cannot grow it without bound. |
| NFR-6 | Must | Reliability | A failure to persist the gate-observation log shall be logged and swallowed rather than failing the todo write itself. |
| NFR-7 | Must | Compatibility | A persisted session written under an earlier release shall still load, including the pre-rename field names and the earlier synthetic message wordings. |
| NFR-8 | Should | Security | A session id used to build a todo state path shall be restricted to a safe character set, so a session id can never escape the todo state directory. |
| NFR-9 | Should | Performance | The todo widget shall keep one logical row per visual row at narrow terminal widths, and shall truncate rather than wrap. |
| NFR-10 | Should | Usability | The pinned todo band shall render below the sticky prompt, without a horizontal separator, and shall show the overall progress rather than a collapsed summary. |
| NFR-11 | Should | Availability | The todo tool shall accept provider quirks that send tool arguments as JSON strings rather than native types, and shall reject only genuinely malformed input. |

## Constraints

- The policy layer must stay free of storage, terminal, and provider dependencies, so the SDK and any embedding client can run the same code as the TUI.
- The private elapsed-time trigger for the long-session review must never appear in model-facing text.
- The todo list format on disk must stay a bare array of items, so every existing consumer keeps reading it.
- The goal assessments must stay in their own file beside the todo list, so each format stays independently readable.
- The swarm plan DAG is a separate feature, and session-local todo and goal state must stay distinct from swarm plan data.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.
Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).
Write each criterion as a fenced `gherkin` block with a tag matching its requirement ID, so the criteria are parseable and later executable via BDD tooling (pytest-bdd, cucumber).
Multiple scenarios per requirement are allowed; tag each with the requirement ID.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Todo items survive a write and a reload
      Given a session with a todo item "write the parser" in status pending
      When the agent writes the todo list and the session is reloaded
      Then the item is present with its content, status, priority, id, and group preserved
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Unknown todo status is rejected
      Given the agent calls the todo tool with status "blocked"
      When the tool parses the call
      Then the call fails with an error naming the valid vocabulary pending, in_progress, completed, cancelled

    @FR-2
    Scenario: Completion synonyms are canonicalized
      Given the agent calls the todo tool with statuses "done", "Finished", and "Canceled"
      When the tool parses the call
      Then the statuses become completed, completed, and cancelled
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Grouped todos render under a group header
      Given todos in the groups "build" and "verify"
      When the todo widget renders the list
      Then one header row per group is shown with the group's completed-of-total count
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: The plan intent assessment survives a goals-only write
      Given a plan whose user_intention is "make search feel instant" and whose understands_user_intent is partial
      When the agent writes only the goal assessments
      Then the stored plan still carries the same intention and understanding state
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A goal assessment records the full field set
      Given the agent writes a goal for the group "optimize grep"
      When the assessment is stored
      Then the stored goal carries the feedback loop state, the feedback loop text, the relevance, coverage, traceability, delivery state, difficulty, autonomy, iteration maturity, and stopping evidence
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A substitute check does not clear the acceptance bar
      Given a goal of involved difficulty whose feedback loop relevance is synthetic
      When the completion bar is evaluated
      Then the goal does not pass, and the same holds for a representative or acceptance-blocked relevance
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: A bulk end-of-task stamp stays distinguishable from a stepped rise
      Given a completed todo whose confidence history is speculative then verified
      When the spike classifier runs
      Then the todo is reported as a confidence spike
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: A moderate first write records instead of interrupting
      Given a first plan write whose understanding is partial and whose goal has narrow coverage
      When the todo tool executes the write
      Then the tool output carries no gate continuation, and the failing checks are recorded as observations for the turn-end digest
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A low-scoring completion is still saved
      Given a write that completes a group whose delivery state is below the bar
      When the todo tool executes the write
      Then the completed todo and the low delivery state are persisted, and no ownership continuation is returned in the tool output
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A goal for a finished task is dropped
      Given stored goals for the groups "first task" and "second task"
      When the agent replaces the todo list with items only in the group "second task"
      Then only the "second task" goal remains
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: The continuations name a category but not the calibration
      Given each of the quality-gate continuation messages
      When the messages are inspected
      Then none of them contains a threshold, a percent, a score, or the word gate
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: A synthetic continuation is not replayed as a user prompt
      Given a persisted transcript containing a gate digest continuation
      When the session is reloaded and rendered
      Then the continuation is not rendered as a user prompt, and a short notice is shown instead
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: The follow-up order is respected
      Given a completed todo list with one recorded gate observation and a weak completion confidence
      When the follow-up policy decides the next continuation
      Then the gate digest is sent first, the completion-validation continuation second, and the final-response handoff last
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: The gate budget trips and then re-arms
      Given a completion cycle in which the validation gate never passes
      When more turns are requested than the gate budget allows
      Then the policy stops sending continuations, surfaces a stall notice, and pokes again once new open work appears
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: A todo write publishes the update and records telemetry
      Given the agent writes a todo list
      When the write completes
      Then a todo-updated event is published on the bus and the lifecycle counters are recorded
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: An initiative update refreshes an open overview without stealing focus
      Given the user has opened the goals overview in the side panel
      When the agent updates an initiative through the initiative tool
      Then the overview page shows the new content and the focused page is still the goals overview
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Creating an initiative does not open the side panel
      Given no side panel page is open for the session
      When the agent creates an initiative through the initiative tool
      Then no side panel update is published and no goal page is written
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: The todo card shows the plan and the goal assessments
      Given a session with todos, a plan, and one goal assessment
      When the user runs the todos command
      Then an inline card is shown carrying the todos, the plan, and the goal assessments
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: The session title comes from the active group
      Given todos where the in-progress item belongs to the group "Fix resume names"
      When the session title is derived
      Then the title is "Fix resume names"
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: An SDK client can read the todo state and acknowledge a follow-up
      Given an SDK client with the todo-state capability
      When it requests the session todo state and then acknowledges the follow-up effects
      Then it receives the snapshot and the gate-observation log is cleared
    ```

- [ ] **FR-21**

    ```gherkin
    @FR-21
    Scenario: A legacy numeric payload still loads
      Given a stored goal carrying the legacy hill-climbability and end-to-end-ownership keys with numeric values
      When the session state is loaded
      Then the goal carries the current feedback-loop and delivery states, and the legacy key names are not written back
    ```

- [ ] **FR-22**

    ```gherkin
    @FR-22
    Scenario: Turning the auto-poke off sticks for the session
      Given the user turns the auto-poke off
      When a later turn ends with incomplete todos
      Then no poke is sent, and the default-on re-arm does not undo the explicit turn-off
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The model-visible schema hides the calibration
      Given the serialized todo tool schema
      When it is inspected
      Then it contains no threshold, quality gate, internal quality check, or score wording
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: The schema does not bias one kind of work
      Given the serialized todo tool schema
      When it is inspected
      Then it contains no browser, screenshot, viewport, or console-error hint
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Every static continuation fits the token budget
      Given the long-session review, intent, feedback-loop, ownership, completion, confidence-spike, final-response, and digest messages
      When each is estimated in tokens
      Then each stays at or below the approximate budget of 64 tokens and starts with the compact automation prefix
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: A long list is summarized instead of enumerated
      Given 40 completed todos with no completion confidence
      When the completion continuation is built
      Then the first 6 todos are named, and the remainder is reported as a count
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The observation log stays bounded
      Given a turn that records more observations than the cap allows
      When the observations are appended
      Then only the capped number of most recent observations is retained
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: An unwritable observation log does not fail the write
      Given the observation log cannot be written
      When the agent writes the todo list
      Then the write still succeeds and the failure is logged
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: An earlier synthetic wording is still classified
      Given a persisted transcript containing an earlier version of the ownership continuation
      When the transcript is classified
      Then the message is recognised as a synthetic continuation and not as a user prompt
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: An unsafe session id is rejected
      Given the session id "../x"
      When a todo state path is built
      Then the session id is reported as unsafe
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: The todo widget keeps one row per item at a narrow width
      Given a todo list rendered in a narrow info widget
      When the widget renders
      Then each item occupies exactly one visual row and long content is truncated
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: The pinned band sits under the sticky prompt
      Given the pinned todo band is enabled and a user prompt is visible
      When the transcript renders
      Then the pinned todo row appears below the prompt row and no horizontal separator is drawn
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: Stringified tool arguments are accepted
      Given the agent sends the whole todos array as a JSON string and a numeric confidence as a string
      When the tool parses the call
      Then the call succeeds and the confidence maps onto the closest semantic state
    ```

## Conflicts

<!-- Identified and populated by /review-requirements: pairs or groups of requirements that cannot all be satisfied at once. Reconcile before approval, or promote to an open question. -->

None identified yet.

## Open Questions

1. None, the feature is implemented and the artifacts were derived from the code rather than from an open design question.

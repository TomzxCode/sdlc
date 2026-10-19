---
title: "Insights: Project Learning Extraction"
status: done
---

# Requirements: Insights: Project Learning Extraction

## Overview

Fusion runs a model-assisted extraction over project memory to produce normalized, deduplicated insights about a project, covering quality, security, architecture, reliability, and feature opportunities.
Each extraction is tracked as a run with a status, a retry policy, and an ordered event trail, so an operator can see what happened and retry a transient failure.
An operator reviews the insights in a dashboard view, dismisses, archives, or unarchives them, and turns a selected insight into a board task.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Reads the insights a project has produced and turns the useful ones into tracked work. |
| Project maintainer | Keeps the insight list free of noise by dismissing or archiving findings that no longer matter. |
| Agent | Queries persisted insights and insight runs through the CLI tool surface. |
| Engine scheduler | Publishes workflow insights such as backlog health and unlinked-mission advisories into the same store. |
| Model provider | Serves the extraction call, so the run must be bounded, cancellable, and retried on transient errors. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall persist each insight with an id, a project scope, a title, a body, a category, a status, a fingerprint, provenance, a link to the last run that produced it, and creation and update timestamps. |
| FR-2 | Must | The system shall classify each insight with one of the fifteen categories defined by the insight category type, covering quality, performance, architecture, security, reliability, user experience, testability, documentation, dependency, workflow, other, features, competitive analysis, research, and trends. |
| FR-3 | Must | The system shall move an insight through the generated, confirmed, stale, dismissed, and archived states, and shall return an archived insight to the confirmed state when it is unarchived. |
| FR-4 | Must | The system shall deduplicate insights by project and fingerprint, updating the matching row in place and preserving its original id and creation timestamp instead of inserting a second row. |
| FR-5 | Must | The system shall track each extraction as a run that records its trigger, status, summary, error, the number of insights created and updated, the input and output metadata snapshots, and the lifecycle fields. |
| FR-6 | Must | The system shall treat a completed, failed, or cancelled run as immutable and shall reject any status change that the run state machine does not allow. |
| FR-7 | Must | The system shall keep an ordered event trail for each run, with a monotonically increasing sequence number, an event type, a message, an optional status and failure classification, and optional metadata. |
| FR-8 | Must | The system shall execute a manual run by reading the project working memory, prompting the model with the working memory and the existing insights, parsing the returned insight list, merging the result into the insights memory file, and upserting every insight into the store. |
| FR-9 | Must | The system shall classify a run failure as cancelled, timed out, retryable transient, or non-retryable, and shall retry a retryable failure until the configured attempt limit is reached. |
| FR-10 | Must | The system shall refuse to start a second run for the same project and trigger while a pending or running run exists, and shall answer that request with a conflict status carrying the active run id. |
| FR-11 | Must | The system shall cancel a pending run immediately, and shall abort the execution of a running run when the operator requests cancellation. |
| FR-12 | Must | The system shall retry a failed run whose failure class is retryable transient, reusing the model selection, reasoning effort, and input metadata recorded on the original run. |
| FR-13 | Must | The system shall sweep pending and running runs that have no live execution owner after the grace window, and shall mark each recovered run as failed with a non-retryable cause. |
| FR-14 | Must | The system shall expose HTTP endpoints to list insights, read one insight, update one insight, delete one insight, dismiss one insight, archive one insight, and unarchive one insight. |
| FR-15 | Must | The system shall expose HTTP endpoints to trigger a run, list runs, read one run, list the events of one run, cancel one run, and retry one run. |
| FR-16 | Must | The system shall return a task payload draft for an insight so the operator can create a board task from it, and shall archive the insight as part of that flow. |
| FR-17 | Must | The system shall present a dashboard insights view that groups insights by category, shows the latest run status, and offers the dismiss, archive, unarchive, and create-task actions on each insight. |
| FR-18 | Should | The system shall let the operator select the model and the reasoning effort for a run, and shall record that selection on the run so a retry reproduces it. |
| FR-19 | Should | The system shall order insight lists ascending by creation timestamp and then by id, and shall order run lists newest first by creation timestamp and then by id. |
| FR-20 | Should | The system shall let the caller filter the insight list by category, status, and producing run, and shall filter the run list by status and trigger, and shall reject a non-numeric or out-of-range pagination value. |
| FR-21 | Should | The system shall expose persisted insights and insight runs to agents through the insight list, insight show, insight run list, and insight run show tools. |
| FR-22 | Should | The system shall recover an orphaned active run when a run request finds an active run with no live execution owner, and shall then start the new run. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | The system shall recover every pending or running run that has no live execution owner once it passes the grace window, so a crashed process cannot leave a run active forever. |
| NFR-2 | Must | Reliability | The system shall bound each attempt with a timeout and shall abort the model call when the run is cancelled or the timeout elapses. |
| NFR-3 | Must | Deduplication | The system shall compute the insight fingerprint as a deterministic hash of the lowercased and whitespace-collapsed title plus the lowercased category, so the same observation always maps to the same key. |
| NFR-4 | Must | Cost | The system shall allow at most one active run per project and trigger, so a project never pays for two concurrent extractions of the same kind. |
| NFR-5 | Must | Observability | The system shall append a durable event for every run creation, status change, attempt, retry, cancellation, and orphan recovery, so an operator can rebuild the history of a run from the event trail alone. |
| NFR-6 | Should | Observability | The system shall run the stale-run sweep at startup, on a fixed interval, and on demand before listing runs, and shall log a sweep failure without failing the surrounding request. |
| NFR-7 | Should | Cost | The system shall store the operator's model and reasoning-effort selection on the run input metadata, so a retry uses the same provider and the same effort as the original attempt. |
| NFR-8 | Should | Portability | The system shall serve the same feature from the SQLite-backed insight store and the PostgreSQL-backed async insight store through one method surface, so callers behave the same in both backends. |
| NFR-9 | Should | Security | The system shall run the extraction session with read-only tools and shall keep materialized secret values out of session diagnostics. |
| NFR-10 | Should | Performance | The system shall bound the insight list by limit and offset, and the dashboard shall cap its persisted insight cache so a long-lived browser session cannot grow without bound. |

## Constraints

- Insights are scoped to one project, and the PostgreSQL tables partition rows by the project partition column.
- The insight body is nullable so a partially generated insight can be stored with a title only.
- The insight title is derived from the extracted content and truncated to one hundred characters.
- The extraction session runs with read-only tools, so an extraction never changes the project source.
- The memory insight categories pattern, principle, convention, pitfall, and context map onto the insight categories workflow, architecture, workflow, quality, and other.
- The dashboard insights view is gated behind the experimental insights feature flag.
- The dashboard and the CLI read the same store, so both backends must expose the same records.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Persist an insight with its full field set
      Given a project with an open insight store
      When an insight is created with a title, a body, a category, and provenance
      Then the stored insight carries an id, the project scope, the category, the status, the fingerprint, the provenance, a null last run link, and creation and update timestamps
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Accept every declared insight category
      Given the insight category type
      When the category list is read
      Then it contains exactly fifteen values including features, competitive analysis, research, and trends
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Archive and unarchive an insight
      Given a confirmed insight
      When it is archived and then unarchived
      Then the status moves to archived and back to confirmed
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Re-extract the same observation
      Given a project with one insight holding fingerprint FP-1
      When the same fingerprint is upserted again with new content
      Then the row keeps its original id and creation timestamp and holds the new content
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Record a run and its outcome
      Given a project with an open insight store
      When a run is created for the manual trigger and later completes with two created and one updated insight
      Then the run records the trigger, the completed status, the summary, the two created and one updated counts, the input and output metadata, and the lifecycle attempt fields
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Mutate a terminal run
      Given a completed run
      When the run is updated with any field
      Then the store refuses the write with a terminal immutability error
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Read the event trail in order
      Given a run with a creation event and two status events
      When the run events are listed
      Then they come back ordered by sequence number with no gaps in the sequence
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Run a manual extraction
      Given a project with working memory notes and no existing insights
      When a manual run is triggered
      Then the working memory is read, the model is prompted, the parsed insights are merged into the insights memory file, and each insight is upserted into the store
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Classify and retry a transient failure
      Given a run configured for two attempts
      When the first attempt fails with a connection reset error
      Then the run records a retryable transient failure and the executor starts a second attempt
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Refuse a concurrent run
      Given a project with a running manual run
      When a second manual run is requested
      Then the request is answered with a conflict status whose details name the active run id and status
    ```

- [x] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Cancel a pending run
      Given a pending run
      When the operator cancels it
      Then the run moves to cancelled with a cancellation timestamp and a cancel_requested event
    ```

- [x] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Retry a transiently failed run
      Given a failed run whose failure class is retryable transient
      When the operator retries it
      Then a new run is created that links to the original through the lifecycle retry fields and reuses the recorded model and reasoning effort
    ```

- [x] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Recover an orphaned active run
      Given a running run with no live execution owner that is older than the grace window
      When the sweep runs
      Then the run moves to failed with a non-retryable orphaned-run cause and a warning event
    ```

- [x] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Manage one insight over HTTP
      Given a project with a stored insight
      When the insight is read, updated, dismissed, archived, unarchived, and finally deleted
      Then each call answers with the updated insight and the delete answers with an empty success status
    ```

- [x] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Exercise the run endpoints
      Given a project with an insight store
      When a run is triggered, the runs are listed, one run is read, its events are listed, and the run is cancelled
      Then the trigger answers with a created status and the reads answer with the run and its events
    ```

- [x] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Draft a task from an insight
      Given a stored insight with a title and a body
      When the task draft endpoint is called
      Then the response carries the insight, a suggested title, and a suggested description
    ```

- [x] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Browse insights in the dashboard
      Given insights in two categories and a latest completed run
      When the insights view renders
      Then it lists the populated categories, shows the run status, and offers the dismiss, archive, and create-task actions on each insight
    ```

- [x] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Choose a model and reasoning effort for a run
      Given the operator opens the model picker beside the generate action
      When a model and a reasoning effort are chosen and a run is started
      Then the selection is stored in the browser and the run records it in its input metadata
    ```

- [x] **FR-19**

    ```gherkin
    @FR-19
    Scenario: Order lists deterministically
      Given two insights written in the same millisecond
      When the insights are listed
      Then they come back ordered by creation timestamp and then by ascending id
    ```

- [x] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Reject a bad pagination value
      Given a caller filtering the insight list
      When the limit is not a number or is below one
      Then the request is answered with a bad request status
    ```

- [x] **FR-21**

    ```gherkin
    @FR-21
    Scenario: Query insights from an agent session
      Given an agent session with the insight tools registered
      When the agent lists insights and shows one by id
      Then the list tool reports the count and the show tool returns the stored insight
    ```

- [x] **FR-22**

    ```gherkin
    @FR-22
    Scenario: Recover an orphan before starting a run
      Given an active manual run with no live execution owner older than the grace window
      When a new manual run is requested
      Then the orphan is recovered to failed and the new run starts
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: No run stays active after a crash
      Given a process that stopped while a run was in the running state
      When the periodic sweep runs after the grace window
      Then the run is recovered to failed rather than left active
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Bound an attempt by timeout
      Given a run with a configured attempt timeout
      When the attempt exceeds that timeout
      Then the attempt is aborted and the run is recorded as timed out
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Fingerprint is stable across wording
      Given the same title written in different letter case and spacing
      When the fingerprint is computed for both
      Then both produce the same eight character hexadecimal value
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: One active run per trigger
      Given a project with a running scheduled run
      When a scheduled run is requested
      Then no second run is created for that project and trigger
    ```

- [x] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Rebuild a run history from events
      Given a run that was created, retried, and then completed
      When its events are read
      Then the trail holds a creation event, an attempt event, a retry event, and a completion event
    ```

- [x] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Sweep on demand before listing runs
      Given a caller listing insight runs
      When the request is served
      Then a stale-run sweep runs first and a sweep failure is logged without failing the list
    ```

- [x] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Retry keeps the original cost profile
      Given a run that recorded a model provider, a model id, and a reasoning effort
      When that run is retried
      Then the retry attempt uses the same provider, model id, and reasoning effort
    ```

- [x] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Same behavior in both backends
      Given a project served by the PostgreSQL-backed async insight store
      When an insight is upserted and a run is created
      Then the same method names return the same record shapes as the SQLite-backed store
    ```

- [x] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: Extraction cannot change the project
      Given a manual insight run
      When the extraction session is created
      Then the session is limited to read-only tools and carries no materialized secret values in its diagnostics
    ```

- [x] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: Bound the persisted insight cache
      Given a project with more than five hundred insights
      When the dashboard persists its insight cache
      Then the cache holds at most five hundred entries
    ```

## Conflicts

The insight category type declares fifteen categories, and the CLI tool and the dashboard view accept all fifteen.
The dashboard insight route validates the category filter and the category update against a shorter list of eleven categories that omits features, competitive analysis, research, and trends.
A caller that filters or updates an insight by one of those four categories is answered with a bad request status even though the same values are accepted elsewhere.

## Open Questions

1. Should the dashboard insight route accept the four extended categories in its filter and update validation lists, or should the category type be reduced to the eleven values the route accepts.
2. The `create-task` endpoint returns a payload draft and leaves the board task creation to the caller, so the endpoint name does not describe what it does. Should it be renamed or should it create the task itself.
3. The run trigger list includes schedule, task completion, and merge event, and the route accepts all of them, but no scheduler, task completion hook, or merge hook starts a run today, so the manual trigger is the one in use. Should the remaining triggers be wired or removed from the type.
4. The insight category type documents features, competitive analysis, research, and trends, and the dashboard renders them, but the model extraction prompt only asks for pattern, principle, convention, pitfall, and context. Should the prompt produce the extended categories too.

---
title: "Cases and Pipeline Cases"
status: done
---

# Requirements: Cases and Pipeline Cases

## Overview

Cases give operators and agents a persistent, company-scoped record for work that spans tasks, documents, labels, attachments, and agent handoffs.
The active REST API and board UI use the `cases` and `case_handoffs` tables.
The `pipeline_cases` tables remain in the database schema as stage-based case records.
This artifact documents code that already exists and was reverse engineered during sync.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Browse case facts, work, documents, history, and handoff state without editing case data from the board |
| Agent | Create, read, update, and hand off cases through dedicated native tools and REST routes |
| Instance operator | Enable or disable the experimental Cases feature for the whole instance |
| Delivery worker | Deliver accepted handoffs with durable retries, leases, and wakeup requests |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall gate every case and case-handoff operation with the instance setting `enableCases`. |
| FR-2 | Must | The system shall create or update company-scoped cases by type and key with advisory-lock backed idempotency and stable identifiers. |
| FR-3 | Must | The system shall list, filter, sort, group, paginate, and read authorized cases with bounded batch enrichment. |
| FR-4 | Must | The system shall store case fields, labels, task links, document references, attachments, parent links, and case events. |
| FR-5 | Must | The system shall provide read-only board pages for case lists and detail with URL retained filters and work, details, document, and handoff sections. |
| FR-6 | Must | The system shall start case work through a durable handoff that reuses one primary task and records phase, instructions, workflow transition, and actor provenance. |
| FR-7 | Must | The system shall deliver handoffs through a ledger with leases, retries, cancellation, wakeup requests, and replay of committed results. |
| FR-8 | Must | The system shall settle a `done` handoff atomically with accepted primary-task completion and leave the case open during review or human waits. |
| FR-9 | Must | The system shall expose native case tools for create, read, update, and handoff with bounded JSON and document paging and per-page reauthorization. |
| FR-10 | Must | The system shall require kickoff and nonblank workflow text for native case creation and store the text as the primary task's workflow document. |
| FR-11 | Must | The system shall enforce company scope, task visibility, retained access sources, low-trust boundaries, and a transaction-local mutation fence for case writes. |
| FR-12 | Must | The system shall log case mutations, document revisions, annotation changes, and handoff transitions to activity and case event history. |
| FR-13 | Should | The system shall persist pipeline cases with stage, fields, workspace reference, lease, parent, terminal, and retirement fields. |
| FR-14 | Should | The system shall reject unsupported native tool fields and removed REST options such as `createOnly` without changing passive records. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Every case read and write shall enforce company scoping and actor authorization before returning data or applying mutations. |
| NFR-2 | Must | Performance | Case list pagination shall use bounded candidate batches and native case reads shall limit response chunks to at most 8192 UTF-8 bytes. |
| NFR-3 | Must | Availability | Handoff delivery shall survive worker restarts through persisted state, leases, retry timestamps, and pending state uniqueness. |
| NFR-4 | Must | Privacy | Private task ancestry and quarantined low-trust work shall not widen case access or enter automatic execution context. |
| NFR-5 | Should | Observability | Case mutations, document revisions, annotation changes, and handoff transitions shall record actor identity and run attribution where available. |

## Constraints

- Cases are off unless `instance.experimental.enableCases` is enabled.
- Board case list and detail pages are read only.
- Case upserts converge on one row per company, case type, and key.
- A handoff keeps the same primary task across agent transfers.
- Handoff idempotency uses company, actor type, actor id, and idempotency key.
- Native read continuations require the snapshot from the preceding page.
- Workflow and initial document bodies share a 200000 character budget.
- Pipeline case tables have no active route or service evidence in this sync.

## Acceptance Criteria

Every FR and NFR has at least one acceptance criterion.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Cases disabled denies every route
      Given the instance setting enableCases is false
      When an actor calls any case or case-handoff route
      Then the response is a final denial with code cases_disabled
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Keyed upsert converges
      Given no case exists for a company, type, and key
      When two authorized requests upsert that identity concurrently
      Then both requests resolve to one case with one company scoped identifier
    ```

    ```gherkin
    @FR-2
    Scenario: Keyless upsert uses company and type
      Given no key is supplied
      When an authorized actor creates the same case type twice
      Then the second request updates the passive case instead of creating another
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Filters apply before pagination
      Given multiple authorized cases with different types and statuses
      When a client lists cases with filters, sort, grouping, limit, and offset
      Then the response contains the authorized page in the requested order and grouping
    ```

    ```gherkin
    @FR-3
    Scenario: Type discovery hides unauthorized types
      Given a case whose access source is not readable by the actor
      When the client lists case types
      Then that type is absent unless another readable case uses it
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Case detail includes attached context
      Given a case with fields, labels, task links, documents, attachments, and child cases
      When an authorized actor reads the case
      Then the detail includes those references and a case history event for prior mutations
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Read-only board pages retain browse context
      Given a filtered case list
      When the operator opens a case and returns to the list
      Then the case detail has no edit controls and the original filters remain in the URL
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Handoff reuses the primary task
      Given a case with an accepted handoff to one agent
      When another handoff moves the case to a second agent
      Then both handoffs reference the same primary task with incremented versions
    ```

    ```gherkin
    @FR-6
    Scenario: Handoff records provenance
      Given an agent run starts a handoff
      When the handoff is accepted
      Then the ledger stores the actor type, actor id, source run, phase, instructions, and workflow transition
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Delivery replays a committed result
      Given a handoff was committed but its HTTP response was lost
      When the caller repeats the same idempotency key
      Then the route returns the stored result with replayed set to true and creates no second wakeup
    ```

    ```gherkin
    @FR-7
    Scenario: Delivery recovers after worker loss
      Given a pending handoff with an expired lease
      When a delivery worker scans pending handoffs
      Then it claims the handoff once and preserves retry and cancellation state
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Terminal handoff waits for completion
      Given a case in review with an accepted to done handoff
      When ordinary task completion is accepted by the existing gates
      Then the handoff and case close in the same transaction
    ```

    ```gherkin
    @FR-8
    Scenario: Review keeps the case open
      Given a terminal handoff whose primary task is awaiting review
      When the task reaches review status
      Then the case remains open and the handoff stays awaiting completion
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Large case read pages are bounded
      Given a case whose fields exceed one read page
      When a native agent reads the case with offset zero
      Then the response contains a bounded text chunk, a snapshot, and a next offset
    ```

    ```gherkin
    @FR-9
    Scenario: Changed facts invalidate a continuation
      Given a native read snapshot for a case
      When the case fields change before the next page request
      Then the continuation is rejected and the client restarts at offset zero
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Native creation requires kickoff and workflow
      Given a native agent attempts to create a case without workflow text
      When the tool validates the request
      Then it fails before creating a case, task, comment, document, or wakeup
    ```

    ```gherkin
    @FR-10
    Scenario: Workflow text becomes a task document
      Given a valid native creation request with workflow text
      When the case is created
      Then the primary task has one workflow document revision containing the supplied text
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Cross-company access is denied
      Given an actor without access to the case company
      When they call any case route for that company
      Then no case data is returned and no mutation is applied
    ```

    ```gherkin
    @FR-11
    Scenario: Late write is fenced
      Given an accepted handoff has settled the source run
      When the source run sends a case write with an old run token
      Then the write is rejected inside the case write transaction
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Case mutation writes history
      Given an authorized actor patches case fields and status
      When the patch commits
      Then a case event and activity log entry describe the change with actor attribution
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Pipeline case constraints hold
      Given a pipeline and two stages in one company
      When tests insert pipeline cases and child cases
      Then case keys are unique per pipeline and parent request keys are unique among active children
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Removed REST option is rejected
      Given a passive case created by the historical upsert route
      When a caller sends the removed createOnly option
      Then the request is rejected and the passive case is unchanged
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Hidden nested content stays hidden
      Given a readable case linked to an inaccessible task
      When an actor reads the case detail and documents
      Then no body or metadata from the inaccessible task is returned
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Bounded reads and pagination
      Given a large authorized case set and a large case body
      When a client paginates the list and a native agent pages the body
      Then list requests use bounded candidate batches and each native page is at most 8192 UTF-8 bytes
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Pending handoff uniqueness survives restart
      Given one pending handoff for a case
      When delivery workers restart and rescan
      Then at most one worker claims the handoff and no duplicate wakeup request is admitted
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Low-trust provenance blocks execution
      Given historical low-trust case data
      When an agent run prepares execution context or a handoff
      Then the low-trust content is excluded while authorized operator reads remain available
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Run attribution appears in history
      Given a case event created by a heartbeat run on a task
      When the actor reads case events
      Then the event includes the actor name and run to issue attribution
    ```

## Conflicts

None identified yet.

## Open Questions

1. Are the pipeline case tables a legacy remnant or the storage for a planned stage based interface? Current evidence shows schema and tests but no active route or service.
2. What latency target should govern case list pagination and native read continuation calls? Code defines count and byte bounds but no explicit service objective.
3. Should board pages ever author case data? Current board pages are read only and agent tools own authoring.

---
title: "Responsibilities and Status Reports"
status: done
---

# Requirements: Responsibilities and Status Reports

## Overview

A person needs a private dashboard that records what they own, whether each item meets its bar, and the work filed under it.
Agents need a bounded way to read that dashboard, propose changes for the person to accept, and report how each responsibility is doing.
This feature documents already-implemented functionality grounded in `server/src/routes/responsibilities.ts`, `server/src/routes/responsibility-dashboard.ts`, `server/src/routes/responsibility-status-reports.ts`, the related `server/src/services/responsibility-*.ts` modules, the Drizzle schemas under `packages/db/src/schema/responsibility*.ts`, and the pages `ui/src/pages/Responsibilities.tsx` and `ui/src/pages/ResponsibilityDetail.tsx`.
The feature is gated by the `enableResponsibilities` experimental setting, and every route returns `404` with code `responsibilities_disabled` while the setting is off.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Owner | See a private dashboard of their areas, responsibilities, measures, and work, then accept or decline agent proposals |
| Agent | Read the owner's dashboard within its run authority, act for the directing person, propose dashboard changes, and write status reports |
| Company operator | Keep personal dashboard data out of company-wide feeds and preserve an undoable history of dashboard changes |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let a board user create, read, update, and delete responsibilities owned by that user, with a title, optional area, optional bar, status, and ordering. |
| FR-2 | Must | The system shall let an agent read another owner's dashboard only when the agent's company scope and the run's directing or authorizing user match that owner. |
| FR-3 | Must | The system shall derive each active responsibility's health from its bar and current reading, keep a separate owner health override, and surface signals from filed work. |
| FR-4 | Must | The system shall file projects, tasks, routines, and company skills under a responsibility through a link table that allows one target per row and one link per target per responsibility. |
| FR-5 | Must | The system shall create a task under an active responsibility and wake the assigned agent when a board owner delegates work. |
| FR-6 | Must | The system shall keep agent changes for a directing person as saved dashboard versions and expose those versions for restore. |
| FR-7 | Must | The system shall let a board owner start a dashboard conversation with an agent and let only that conversation's agent propose an ordered set of dashboard changes. |
| FR-8 | Must | The system shall let the board owner accept, partially accept, or decline a proposed change set and write an activity event for the applied decision. |
| FR-9 | Must | The system shall restore a saved dashboard version and write activity events for the restore and for the changes it applies. |
| FR-10 | Must | The system shall store agent or owner-written status reports for active responsibilities and return the newest report as current with a bounded history. |
| FR-11 | Must | The system shall choose a reporter agent from agents that can take work, preferring the agent doing the most under the responsibility with deterministic tie breaks. |
| FR-12 | Must | The system shall let a board owner request a status update, which opens one private task for the reporter and keeps later requests idle while one remains unanswered. |
| FR-13 | Must | The system shall restrict status report writes to the reporter, an agent working under the responsibility, or the board owner, and record the author from the caller rather than the body. |
| FR-14 | Must | The system shall log activity for responsibility mutations, dashboard decisions, version restores, and status report writes. |
| FR-15 | Should | The system shall keep dashboard conversations and personal dashboard activity out of company-wide feeds for readers who are not the owner or the assigned agent. |
| FR-16 | Should | The system shall show the owner a Dashboard page with areas, status counts, work signals, proposals, loose work, and views for outline, board, exceptions, automation, and agent status. |
| FR-17 | Should | The system shall show one responsibility page with its bar, filed work, skills, artifacts, and controls to edit, delegate, unlink, and delete. |
| FR-18 | Should | The system shall show a written agent status before the metric-derived status in agent status views and mark reports older than seven days as out of date. |
| FR-19 | May | The system shall reuse a live area with a matching title when a caller sends `areaTitle` instead of `areaId`, creating the area in the same transaction when needed. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | All responsibility, dashboard, and status report routes shall enforce company access and the owner or agent-run authority before reading or writing data. |
| NFR-2 | Must | Security | Personal conversations with origin kinds `responsibility_dashboard`, `responsibility_bar`, `responsibility_status_update`, and `automation_conversation` shall stay readable only by the owner and the assigned agent under the run constraints. |
| NFR-3 | Must | Integrity | Responsibility changes, area creation by title, dashboard change sets, and version saves shall run in one transaction so a failed step leaves no partial change. |
| NFR-4 | Must | Performance | The overview and status report reads shall use batched queries with a fixed count instead of per-responsibility queries. |
| NFR-5 | Should | Availability | Dashboard version history shall keep only the newest 30 versions per owner, and status history reads shall return at most 10 reports. |
| NFR-6 | Should | Compatibility | A disabled feature shall return a typed error code so an agent can distinguish a turned-off feature from an empty dashboard. |

## Constraints

- Every responsibility belongs to one company and one person, and the owner id has no foreign key to the auth table.
- Agent creation without a directing person produces a proposal with a complete bar, while a board user may create a title-only responsibility that reads as not measured.
- A responsibility must be active before an agent can file work under it without acting for the owner, before status can be written, and before work can be delegated.
- A status report message must be one plain line of at least 3 and at most 200 characters, and detail is optional with at most 800 characters and a few non-empty lines.
- A dashboard change set has at most 60 changes, and a removal must carry a reason.
- A responsibility link stores exactly one of project, issue, routine, or skill target id.
- An agent delete requires the identifier of a confirmation card accepted by the owner.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: A board owner manages a responsibility
      Given a board user with access to a company
      When they create, read, update, and delete a responsibility they own
      Then each allowed operation succeeds and the stored row reflects the submitted fields
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: An agent reads only within its run authority
      Given an agent whose run was directed by one owner
      When it requests another owner's dashboard
      Then the API returns not found or forbidden before reading that dashboard
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Health comes from the bar unless overridden
      Given an active responsibility with a complete bar and a current reading
      When its reading crosses the status thresholds
      Then computed health changes and effective health follows the owner override when one is set
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Work is filed once under each responsibility
      Given a project and two responsibilities owned by the same person
      When the project is filed under both and then moved from one to the other
      Then the link table has one link per responsibility and the move removes the source link
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Delegation creates a task and wakes the agent
      Given an active responsibility and an assignable agent
      When the owner delegates work with a title and mode
      Then a task is created under the responsibility and an assignment wakeup is queued
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: An agent change is undoable
      Given an agent acting for an owner
      When it updates that owner's responsibility
      Then a dashboard version records the change and the response names the version
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Only the conversation agent proposes changes
      Given a dashboard conversation assigned to one agent
      When another agent posts a change set
      Then the API refuses the proposal and leaves the dashboard unchanged
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: The owner accepts part of a proposal
      Given a proposal with an area and a responsibility filed under it
      When the owner accepts only the area change
      Then the dependent responsibility change is dropped and the applied changes are saved as a version
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: The owner restores a version
      Given a saved version from before an agent change
      When the owner restores it
      Then the areas and responsibilities match that snapshot and activity records the restore
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A report becomes the current status
      Given an active responsibility
      When an authorized writer posts a status with one plain line of why
      Then the read endpoint returns it as current with its author and bounded history
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: The busiest usable agent becomes reporter
      Given several agents that can take work and one with the most tasks under the responsibility
      When the reporter is chosen
      Then that agent is returned with basis works_under
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: An update request opens one task
      Given an active responsibility with a reporter and no open update request
      When the owner asks for an update twice
      Then one private task is created for the reporter and the second request returns created false
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: The author cannot be forged
      Given an agent that works under a responsibility
      When it posts a report body containing another agent id
      Then validation rejects the body and the stored author stays the authenticated caller
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Mutations are audited
      Given a responsibility change, a dashboard decision, and a status report write
      When each operation completes
      Then matching activity entries exist with the company, actor, entity, and action details
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: A private conversation is hidden from teammates
      Given a dashboard conversation owned by one person
      When a teammate reads the company's issues or activity feed
      Then that conversation and its personal dashboard activity are absent
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: The Dashboard page shows what the owner needs
      Given an owner with areas, responsibilities, proposals, and loose work
      When they open the Dashboard page
      Then the page shows status counts and work grouped by area with a way into each view
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: The detail page supports correction
      Given a loaded responsibility with filed work
      When the owner unlinks an item
      Then the item remains in the company and an Undo control restores its link
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: A stale written status is marked
      Given a report written eight days ago
      When the agent status view loads it
      Then the view shows the written status with an out-of-date mark
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: An area is created by title in one transaction
      Given an agent creating a responsibility with an areaTitle that does not exist
      When a later step of the create fails
      Then no orphan area remains
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Authorization runs before data access
      Given an actor without access to a company or owner
      When they call any responsibility, dashboard, or status report route
      Then the API denies the request before returning dashboard data
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Personal conversation visibility is enforced in queries
      Given a status update task with responsibleUserId set to one owner
      When another board user queries issues
      Then the task is filtered out by the conversation visibility condition
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: A failed change leaves no partial data
      Given a dashboard proposal whose later change no longer fits the current dashboard
      When the owner accepts the proposal
      Then the whole apply fails and no earlier change from that proposal is saved
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Overview reads stay batched
      Given an owner with any number of active responsibilities
      When the status report overview is read
      Then the service completes the read in seven queries
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Histories are bounded
      Given more than 30 dashboard versions and more than 10 status reports
      When the version list and one status report state are read
      Then only the newest 30 versions and newest 10 reports are returned
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: A disabled feature is distinguishable
      Given an instance with enableResponsibilities off
      When an agent calls any feature route
      Then the response is 404 with code responsibilities_disabled and remediation guidance
    ```

## Conflicts

None identified yet.

## Open Questions

1. The code stores a metric-derived health and a written status report separately and the agent status view shows the written status first, but the expected rule for other views is not stated in code.
2. The retention limit of 30 dashboard versions is present as a constant, and no product rationale for that number was found in code.
3. The seven-day freshness window for status reports has no configuration path in the inspected code, so the need for an operator-tunable window is unclear.
4. Areas without an owner are hidden as legacy rows, and the inspected code does not describe how an operator should convert them into owned areas.

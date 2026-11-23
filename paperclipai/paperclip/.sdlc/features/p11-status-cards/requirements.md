---
title: "Status Cards"
status: done
---

# Requirements: Status Cards

## Overview

A status card is a company-scoped saved request that turns an interest prompt into structured issue queries and a living Markdown summary.
Board actors create cards on the Status page, choose how updates are triggered, and see lifecycle, watched issues, history, and cost in one place.
An assigned summarizer agent compiles the prompt, writes the query and summary through the API, and later patches the summary when watched issues change.
This feature documents already-implemented behavior in `server/src/routes/status-cards.ts`, `server/src/services/status-cards.ts`, `server/src/services/status-card-update-engine.ts`, `server/src/services/status-card-evaluation.ts`, `packages/db/src/schema/status_cards.ts`, `packages/shared/src/validators/status-card.ts`, and `ui/src/pages/StatusCards/`.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Create status cards, watch issue groups, refresh or archive cards, and read summaries with lifecycle and cost context |
| Agent author | Create a bounded number of cards and hand them to a summarizer without waiting in chat |
| Summarizer agent | Receive compile and update tasks and write queries and summaries through authorized API calls |
| Instance administrator | Enable the experimental feature and keep automatic updates inside policy and cost limits |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall expose status-card list, detail, create, patch, delete, updates, and summary-revision endpoints under the instance experimental flag. |
| FR-2 | Must | The system shall scope every card to a company, enforce company access and `tasks:assign` for mutations, restrict agents to cards they authored, and log mutations to the activity log. |
| FR-3 | Must | The system shall create a card from a bounded interest prompt with an optional title, an optional same-company summarizer agent, and a validated refresh policy. |
| FR-4 | Must | The system shall compile an interest prompt into one to ten structured company-search queries in a hidden generation issue with a stable idempotency key. |
| FR-5 | Must | The system shall write the compiled query and first Markdown summary from the assigned generation run with a monotonically increasing query version and a document revision. |
| FR-6 | Must | The system shall refresh cards manually and through scheduled evaluation, choosing a full rebuild or an incremental update from change count, query version, configuration, and history. |
| FR-7 | Must | The system shall detect watched-issue changes from status, assignee, human comment, membership, and generic update fingerprints and apply the card's selected triggers. |
| FR-8 | Must | The system shall join issues mentioned by identifier or issue link in the summary to the watched set, bounded to 200 issues and resolved inside the company. |
| FR-9 | Must | The system shall enforce refresh policy gates for debounce, hourly update cap, active hours, and daily token cap and reflect `paused_budget` or `paused_hours` on the card. |
| FR-10 | Must | The system shall expose a Status page with active and archived cards, lifecycle tiles, creation, archive and restore, refresh, recompile, summary draft preview, watched issues, and history. |
| FR-11 | Must | The system shall redact summary bodies and watched-issue details when a card matches an issue the actor cannot read and restrict dry-run to a low-trust authorization boundary. |
| FR-12 | Should | The system shall finalize generation tasks that finish, get cancelled, or get blocked without writing a summary as failed updates and clear the card's generation claim. |
| FR-13 | Should | The system shall expose live query dry-run results and update and summary-revision history for debugging without invoking a model. |
| FR-14 | May | The system shall show per-card and daily token and cost estimates in settings and on the board footer. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Summary and query writes shall only be accepted from the designated summarizer or built-in summarizer, the active generation issue, the same company, and the linked agent run. |
| NFR-2 | Must | Reliability | Card creation, refresh claims, and writes shall use transactions, revision checks, and failure rollback so concurrent or failed generations do not leave orphaned claims. |
| NFR-3 | Should | Performance | Unchanged cards shall settle without recurring SQL, and active-hours calculations shall use bounded caches and bounded row scans. |
| NFR-4 | Should | Operability | Scheduled evaluation shall register with deadline work, publish source-change hints in transactions, and contribute idle deadlines so sleep logic can account for pending cards. |

## Constraints

- The feature is gated by `enableStatusCards` in instance experimental settings.
- Agents can author at most `STATUS_CARD_AGENT_MAX_CARDS`, which is 20, cards per company.
- Agent-authored interest prompts are limited to `STATUS_CARD_AGENT_MAX_INTEREST_PROMPT_LENGTH`, which is 4000 characters.
- Interest prompts are limited to 20000 characters for board actors and titles to 300 characters.
- Queries are limited to 10 per card, and compiled queries use company-search schemas.
- Generated summaries are limited to 200000 Markdown characters and change summaries to 2000 characters.
- Archived cards accept no compile, refresh, query, or summary writes.
- Policy defaults are manual mode, default limits of 100000 tokens per day and 6 reactive updates per hour, and a 60-second debounce.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Status endpoints require the experimental flag
      Given enableStatusCards is false
      When a board actor lists or creates cards
      Then the API returns 404 without exposing the card surface
    ```

    ```gherkin
    @FR-1
    Scenario: Card history is readable
      Given a card with completed updates and summary revisions
      When a board actor requests updates and summary-revisions
      Then both endpoints return company-scoped records newest first
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Cross-company card access is denied
      Given an actor outside the card's company
      When they read or mutate the card
      Then the API returns 404 or 403 before the service writes
    ```

    ```gherkin
    @FR-2
    Scenario: Mutations require task assignment permission and are logged
      Given an actor with tasks:assign permission
      When they create, patch, refresh, or delete a card
      Then an activity row records the status card action and actor
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Create queues setup and returns a link
      Given a valid interest prompt and enabled feature
      When a board actor creates a card
      Then the card starts in compiling state, a setup issue is assigned, and a company-scoped href is returned
    ```

    ```gherkin
    @FR-3
    Scenario: Invalid summarizer agent is rejected
      Given an agentId from another company
      When a card is created or patched
      Then the API returns 422 before inserting the card
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Compile prompt production carries the full write-back contract
      Given a new card
      When the setup task description is built
      Then it contains query format rules, untrusted-data handling, and the query then summary write-back sequence
    ```

    ```gherkin
    @FR-4
    Scenario: Setup task deduplication follows prompt changes
      Given an active setup task for the same prompt hash
      When compile is requested again
      Then the existing task is reused and no duplicate card generation starts
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Authorized summarizer writes query and summary
      Given a generation issue assigned to the summarizer run
      When the run writes the compiled query and Markdown summary
      Then queryVersion increments, a document revision is stored, and the card becomes active
    ```

    ```gherkin
    @FR-5
    Scenario: Pinned title survives query writes
      Given a card with titlePinned set
      When the summarizer writes a new query with an auto title
      Then the stored title remains pinned and queryVersion still increments
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Refresh chooses rebuild boundaries
      Given a card with more than ten changes or a changed query version
      When refresh runs
      Then the created generation task requests a full rebuild
    ```

    ```gherkin
    @FR-6
    Scenario: Blocked setup task can be re-kicked
      Given a setup issue in blocked state
      When a board actor requests recompile or refresh
      Then the task is reopened as todo and can write again
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Fingerprint change kinds map to triggers
      Given a watched issue changes status, assignee, human comment, and generic update fields
      When the fingerprint is diffed
      Then each change kind is produced and filtered by the card policy triggers
    ```

    ```gherkin
    @FR-7
    Scenario: Unchanged reactive card stays quiet
      Given a reactive card with no filtered changes
      When evaluation runs
      Then pending state clears and no generation issue is created
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Summary mention joins the watched set
      Given summary Markdown containing an issue identifier and an issue link
      When the summary is written
      Then only matching issues in the card's company are stored as mentionedIssueIds and later changes are watched
    ```

    ```gherkin
    @FR-8
    Scenario: Mention cap is enforced
      Given more than 200 mentions in a summary
      When mention resolution runs
      Then at most 200 issue ids are stored
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Policy pauses automatic work
      Given a card over its daily token cap or outside active hours
      When scheduled evaluation considers it
      Then state becomes paused_budget or paused_hours and a policy deadline is stored
    ```

    ```gherkin
    @FR-9
    Scenario: Manual refresh bypasses automatic gates
      Given a card paused by budget or hours
      When a board actor refreshes it
      Then the update is enqueued
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Board renders each lifecycle
      Given cards in compiling, fresh, stale, updating, error, paused, and archived states
      When the Status page loads
      Then each tile shows the matching label and keeps the last good summary where expected
    ```

    ```gherkin
    @FR-10
    Scenario: Detail drawer exposes working tabs
      Given a selected card
      When the drawer opens
      Then summary, settings, watched issues, and history tabs are available with dry-run debug data in settings
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Private task content is redacted
      Given a card whose watched set includes a private task
      When a reader without access hydrates it
      Then summaryBody is null and watched-issue details are redacted
    ```

    ```gherkin
    @FR-11
    Scenario: Dry-run respects authorization boundary
      Given an actor outside the low-trust dry-run boundary
      When they request dry-run results
      Then the API returns 403
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Stalled generation is finalized
      Given a generation task done, cancelled, or blocked without a summary write
      When finalization runs
      Then the card moves to error, the claim clears, and the open update ledger row is failed
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Dry-run shows live matches
      Given a card with compiled queries
      When the UI opens query debug
      Then each query's current issue matches and mentioned issues are returned without a model call
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Cost preview follows policy
      Given manual, interval, and reactive policies
      When the settings form renders
      Then each shows a one-line estimate that accounts for active hours and token caps
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Unauthorized writer is rejected
      Given an agent that is not the designated summarizer or an active generation run
      When it writes a query or summary
      Then the API returns 403 before any card or document write
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Failed compile wakeup rolls back creation
      Given a compile wakeup that throws
      When card creation is requested
      Then the new card is removed and the caller receives the error
    ```

    ```gherkin
    @NFR-2
    Scenario: Losing refresh claim cancels the unclaimed task
      Given another refresh or archival claims the card first
      When the losing generation issue is checked
      Then it is cancelled if unclaimed and the winner's task remains writable
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Unchanged card avoids recurring work
      Given a reactive card with no filtered change and no membership deadline
      When its evaluation runs twice
      Then no new generation issue is created and no repeating eligibility scan remains
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Deadline registration follows the experimental flag
      Given status-card evaluation work with maintenance enabled or disabled
      When startup registers delivery work
      Then registration happens only when the feature is enabled and no separate aggregate interval is created
    ```

## Conflicts

None identified yet.

## Open Questions

1. A dedicated user guide for status cards was not found, only cross-cutting references in `doc/ISSUE-PRIVACY.md` and `doc/idle-sleep-safety.md`.
2. The Cloud policy that sets `enableStatusCards` is outside Core, so its rollout owner is not recorded here.
3. Retention for `status_card_updates` rows and summary document revisions is not defined in code.
4. Status-card UI and API behavior after general availability, including removal of the experimental gate, is not recorded in code.

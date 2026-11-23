---
title: "Decision Workflows"
status: done
---

# Requirements: Decision Workflows

## Overview

Decision Workflows covers the company-scoped proposals, queues, triage, model-backed classification, and short acknowledgements that help people and agents resolve work that needs a decision.
Agents create decisions with options and issue effects from an active run.
Board users answer or dismiss those decisions, and the system rechecks authority and target state before applying effects.
Decision queues collect attention items from configurable signals.
Triage records hold decide-by dates and snoozes.
Retention records keep or archive reviewed sources.
Company decision model settings and fast response settings connect managed AI credentials to classification and short receipts.
Training examples capture bounded snapshots for export.
This documentation is derived from the decision routes, decision services, database schemas, shared validators, and decision UI in the current codebase.
Approval decisions are tracked in FEAT-0005 and are not restated here.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Answer or dismiss decisions, manage queues and triage, configure decision models and fast responses, and review history. |
| Agent | Propose decisions from an active run and receive a continuation after the outcome settles. |
| Company administrator | Manage the managed AI connections that back decision models and fast responses. |
| Auditor or reviewer | Inspect activity log entries, decision outcomes, invocation history, and training exports. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let an agent create a company decision with a title, body, options with effects, optional inputs, rule key, idempotency key, expiry, continuation policy, and metadata. |
| FR-2 | Must | The system shall sign the decision options and target snapshots and verify that signature before a decide or dismiss action. |
| FR-3 | Must | The system shall let a board user answer or dismiss an open decision and execute the chosen effects after rechecking authority and target staleness. |
| FR-4 | Must | The system shall replay the stored outcome for an idempotent decide request instead of executing its effects again. |
| FR-5 | Must | The system shall expire open decisions at their deadline or when their targets are invalidated and wake the origin agent when the continuation policy requests it. |
| FR-6 | Must | The system shall create a bundle of up to fifty decisions in one transaction with shared provenance. |
| FR-7 | Must | The system shall propose a bulk attention archive decision from a hash of the requested archive manifest entries. |
| FR-8 | Must | The system shall report decision statistics grouped by rule key with proposed, accepted, rejected, and expired counts and chosen option counts. |
| FR-9 | Must | The system shall maintain company decision queues with keys, titles, retention days, and seed rules and expose only queue items whose source the actor can read. |
| FR-10 | Must | The system shall materialize starter queues from pull request work products, plan confirmations, and ask-user-question interactions and record each source once. |
| FR-11 | Must | The system shall store per-source triage decide-by values and snoozes with versioned updates and activity events. |
| FR-12 | Must | The system shall keep per-source retention state with keep, archive, and revive actions guarded by expected versions. |
| FR-13 | Must | The system shall configure a company decision model from a managed connection and run registered decision features through that provider with bounded questions and cost accounting. |
| FR-14 | Must | The system shall configure company fast responses from a managed connection and expose model choices, availability, a fixed sample test, and history. |
| FR-15 | Must | The system shall enqueue a fast response at an accepted turn boundary, generate a short acknowledgement within three seconds, and suppress it when agent work or a real reply owns the turn. |
| FR-16 | Must | The system shall create, preview, list, export, update, and delete decision training examples with snapshots bounded by the decision cutoff. |
| FR-17 | Should | The system shall provide a decisions desk and queue pages with shared toolbar, filtering, grouping, sorting, date chips, and aging shelves, plus cards that warn on stale targets and require typed confirmation for cancel tree options. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall check company access and actor permissions on every decision, queue, model, training, and fast response route. |
| NFR-2 | Must | Integrity | The system shall use signatures, row versions, and expected manifest versions so tampered specs and stale updates fail closed. |
| NFR-3 | Must | Performance | The system shall bound open decisions, provider prompts, and background sweeps with configured caps and deadline checks. |
| NFR-4 | Must | Privacy | The system shall store invocation and fast response accounting without prompt, answer, or credential content. |
| NFR-5 | Must | Availability | The system shall recover interrupted effects, expiries, continuations, and fast response work with at-least-once delivery and idempotent settling. |

## Constraints

- Company scoping is enforced in routes and services, with a short list of instance-wide exceptions recorded in `rules/company-scope-exceptions.mdc`.
- Decision creation requires an agent run context, and board writes require a human user context for training and decision answers.
- Decision model providers are selected from managed OpenAI and OpenRouter native connections in the shared decision model code.
- The fast response feature is gated by an instance experimental setting as well as the company setting.
- Approval decisions belong to FEAT-0005.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first, sorted by ID, then NFRs, sorted by ID.

Acceptance criteria verify how a requirement is proven done, and they do not restate it.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Agent proposes a decision from an active run
      Given an agent run with access to an issue and its target issues
      When the agent posts a decision with two options and an optional input
      Then a decision row is stored with the run provenance and an open status
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Tampered decision spec is rejected
      Given a decision with a stored signature over its options and target snapshots
      When a user attempts to decide after the stored options are altered
      Then the request is refused with a signature verification error
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Board answer applies effects after authority checks
      Given an open decision whose chosen option updates an issue status
      When a board user answers with a valid option
      Then the status change is recorded once and an activity entry names the deciding user
    ```

    ```gherkin
    @FR-3
    Scenario: Stale strict target blocks an effect
      Given a strict decision whose target issue changed after proposal
      When the board user answers that option
      Then the effect is skipped and the outcome reports the stale target
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Idempotent decide replay does not rerun effects
      Given a decision already decided with a recorded idempotency key
      When the same user repeats the decide request with that key
      Then the stored outcome is returned without a second effect execution
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Expired decision wakes the origin agent
      Given an open decision with a wake origin continuation policy and a past deadline
      When the expiry worker runs
      Then the decision becomes expired and the origin agent receives a continuation
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Bundle creation is atomic
      Given an agent run that proposes a bundle of three decisions
      When one decision fails validation during creation
      Then no bundle and no decisions from that request are stored
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Archive proposal binds to the current manifest
      Given a list of attention items on the current aging shelf with versioned retention rows
      When an agent proposes to archive them
      Then a decision is created with a manifest hash and target snapshots containing the expected versions
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Statistics separate dismissals from expiries
      Given decisions with accepted, dismissed, and expired outcomes for one rule key
      When a board user requests decision statistics
      Then the response reports each count separately and lists chosen options for accepted outcomes only
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Queue hides sources the actor cannot read
      Given a company queue containing one issue source and one board-only source
      When an agent lists the queue items
      Then only the issue source allowed by the agent permissions is returned
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Starter queues materialize from signals
      Given attention items backed by a pull request work product, a plan confirmation, and a question interaction
      When a user reads the seeded queues and their items
      Then the PR, Plans, and Questions queues contain the matching sources once each
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Concurrent triage updates keep every field
      Given one triage row with a decide-by value and no snooze
      When two board users set a snooze and a decide-by value concurrently
      Then both values are present and the version has advanced without reuse
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Archive with a stale expected version fails
      Given a retention row whose version changed after the user loaded it
      When the user posts an archive action with the old expected version
      Then the whole manifest is rejected and the row is not archived
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Registered decision feature calls the configured provider
      Given a company decision model configured with a managed connection and a running agent
      When a registered feature submits a bounded boolean, choice, and score request
      Then answers and usage are returned and an invocation row records cost without input or answer content
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Fast response test uses the fixed sample
      Given a manager with a configured fast response connection and model
      When the manager posts a test request
      Then the fixed sample is processed and the result reports status, text, duration, invocation, and usage
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Acknowledgement is suppressed when the agent replies
      Given a pending fast response with no posted comment
      When the agent starts a real reply on the source comment
      Then the request becomes skipped with a real reply error and no acknowledgement is posted
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Training snapshot excludes later comments
      Given an interaction with comments before and after the decision cutoff
      When a board user previews a training example for that decision
      Then the snapshot includes the boundary comment and excludes later comments
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Destructive option requires typed confirmation
      Given an open decision with a cancel issue tree option
      When the board user selects that option
      Then the UI requires a typed confirmation before it submits the choice
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Unauthorized company access is refused
      Given a user who is not a member of a company
      When the user calls a decision or fast response route for that company
      Then the route refuses access before reading company data
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Concurrent queue creation uses one row
      Given two concurrent requests to create the same company queue key
      When both requests commit
      Then one queue exists and the second request receives the existing row
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Open decision cap is enforced
      Given a company at its configured open decision cap
      When an agent attempts to create another decision
      Then the request is refused with a rate limit error
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Invocation history contains no question content
      Given a completed decision model invocation with a provider question and answer
      When a manager reads decision history
      Then the entry contains attribution and cost fields only
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Claimed effect is recovered without replay
      Given a decided decision with a claimed effect and a stale execution row
      When the effect recovery worker runs
      Then the effect is settled once and the continuation is delivered
    ```

## Conflicts

None identified.

## Open Questions

1. The code does not state whether the seven-day default decision expiry and thirty-day maximum are product requirements or operational defaults.
2. The intended external consumer of decision training JSONL exports is not stated in the code.
3. The code fixes decision model choices to native OpenAI and OpenRouter connections, and it does not state whether other providers are planned.
4. The code does not state a product threshold for fast response latency beyond the three-second deadline and the bounded prompt size.

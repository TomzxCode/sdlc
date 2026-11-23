---
title: "Onboarding"
status: done
---

# Requirements: Onboarding

## Overview

Onboarding creates a company, hires and connects a first agent, and opens a standing chat where the customer turns an idea into scoped work.
Cloud signup answers can be pushed into an existing stack as an idempotent seed that creates a lead agent and a company goal without creating execution work.
This feature documents already-implemented functionality grounded in `server/src/routes/onboarding-seed.ts`, `server/src/services/onboarding-seed.ts`, `server/src/routes/onboarding-chat.ts`, `server/src/services/onboarding-chat.ts`, `server/src/routes/issues.ts:12995`, `server/src/services/onboarding-first-task-admission.ts`, `ui/src/components/OnboardingWizard.tsx`, `ui/src/App.tsx:172`, `ui/src/pages/AgentChat.tsx`, and `doc/onboarding-chat.md`.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| New operator | Creates an organization and a first agent without manual server setup. |
| Cloud signup flow | Pushes collected answers into the activated stack and can retry safely. |
| Board user | Opens a standing agent chat and turns an idea into an accepted task. |
| Agent | Receives a scoped brief and a deterministic welcome without inventing goals. |
| Instance administrator | Controls Agent Chat availability through experimental settings. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The wizard shall create a company from the entered name and move directly to the first agent step. |
| FR-02 | Must | The wizard shall adopt an existing agent with the same name and harness rather than hiring a duplicate. |
| FR-03 | Must | The wizard shall require a compatible model and a passing or usable environment result before it hires the first agent. |
| FR-04 | Must | The wizard shall hire the first agent with the server-owned onboarding instructions and approve the generated hire approval during onboarding. |
| FR-05 | Must | Finishing onboarding shall create the owner-bound onboarding chat and navigate to the agent chat. |
| FR-06 | Must | The system shall accept a Cloud onboarding seed only from an authorized company actor and reject fields outside the shared bounds. |
| FR-07 | Must | The system shall apply a seed at most once per revision and update the same company record when a new revision arrives. |
| FR-08 | Must | The system shall store the seed mission as a company goal with the first line as title and the remaining lines as description. |
| FR-09 | Must | The system shall create or update the seeded lead agent with structural role `ceo` and the customer supplied role as title. |
| FR-10 | Must | The system shall retain the seed first-task title and details as chat context without creating a task or project. |
| FR-11 | Must | The system shall write the seed audit entry and the seed record in one transaction and publish the activity only after commit. |
| FR-12 | Must | An onboarding chat shall be one owner-bound conversation with `originKind: onboarding_chat` and no task number. |
| FR-13 | Must | The agent chat page shall request a welcome only after the conversation paints in a visible tab and shall prevent duplicate wakes with a lock and durable receipts. |
| FR-14 | Must | A user message or a new conversation session shall supersede a welcome that has not started. |
| FR-15 | Must | The onboarding chat directive shall let the user choose an interview or ordinary conversation and shall create work only after proposal acceptance or an explicit task request. |
| FR-16 | Must | The first-task compatibility path shall allow at most one onboarding first task per company and shall seed a greeting and opening question as the assigned agent. |
| FR-17 | Must | Execution work from the onboarding first task shall require persisted human acceptance through the latest proposal and a matching plan revision when a plan is present. |
| FR-18 | Must | The onboarding route and launcher shall open the wizard at the correct company and step, and a saved draft shall be restored only for a company the signed-in user owns. |
| FR-19 | Should | The wizard shall record step, completion, dismissal, and reopen analytics only when browser analytics consent is granted. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Every onboarding endpoint and service shall enforce company scope and the actor type required by that surface. |
| NFR-02 | Must | Input validation | Seed free text shall be bounded to the limits enforced by Cloud before the request reaches the service. |
| NFR-03 | Must | Concurrency | Seed application and greeting starts shall use PostgreSQL advisory locks so concurrent requests cannot duplicate writes or wakes. |
| NFR-04 | Must | Compatibility | Onboarding chats shall not advance the task counter and existing numbered records shall keep their identifiers. |
| NFR-05 | Must | Auditability | Seed application, conversation opening, and welcome start shall write activity log entries. |
| NFR-06 | Must | Resilience | Draft storage denial, failed welcome start, and disabled Agent Chat shall surface a usable message or a retry instead of breaking the page. |

## Constraints

- Cloud creates the company before the tenant boots on a managed stack.
- Company creation in the tenant is unavailable on a managed stack because `POST /companies` is a 403 floor there.
- The Cloud identity headers are a trusted server-derived envelope, while the JSON seed body is untrusted customer text.
- Agent Chat endpoints require the `enableAgentChat` experimental setting and a board user with a user id.
- Chat conversations use the existing issue and comment infrastructure.
- The first-task path is a compatibility path and the chat path creates no execution task at onboarding time.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

Acceptance criteria verify how a requirement is proven done, they do not restate it.

Write concrete, scenario-based criteria (happy path, edge cases and error states where applicable).

Write each criterion as a fenced `gherkin` block with a tag matching its requirement ID, so the criteria are parseable and later executable via BDD tooling (pytest-bdd, cucumber).

Multiple scenarios per requirement are allowed; tag each with the requirement ID.

- [ ] **FR-01**

    ```gherkin
    @FR-01
    Scenario: Name a company and continue to the first agent
      Given the wizard is open at step one
      When the operator enters a company name and continues
      Then one company is created and the wizard opens on step three without asking for a mission
    ```

- [ ] **FR-02**

    ```gherkin
    @FR-02
    Scenario: Adopt an existing agent with the same name and harness
      Given the company already holds an agent with the chosen name and harness
      When the connect action runs without a remembered agent id
      Then the wizard adopts that agent and moves to review without hiring a second agent
    ```

- [ ] **FR-03**

    ```gherkin
    @FR-03
    Scenario: Block a hire without a usable model and environment
      Given no model is selected for a gateway connection
      When the operator tries to connect
      Then the wizard shows a model error and does not call the hire endpoint
    ```

    ```gherkin
    @FR-03
    Scenario: Block a hire on a failed environment test
      Given the adapter environment test reports a blocking result
      When the operator tries to connect
      Then the wizard shows the returned checks and does not hire the agent
    ```

- [ ] **FR-04**

    ```gherkin
    @FR-04
    Scenario: Hire the first agent and approve the generated request
      Given a valid adapter configuration and environment result
      When the connect action completes
      Then the hire request carries `onboardingFirstAgent: true` and any returned approval is approved during the wizard
    ```

- [ ] **FR-05**

    ```gherkin
    @FR-05
    Scenario: Finish into the agent chat
      Given the wizard has a created company and agent
      When the operator chooses Get started
      Then the onboarding chat is created and the browser navigates to the agent chat route
    ```

- [ ] **FR-06**

    ```gherkin
    @FR-06
    Scenario: Reject a seed from a caller without company access
      Given a Cloud envelope that does not grant access to the target company
      When the seed request is submitted
      Then the route denies the request and writes no seed record
    ```

    ```gherkin
    @FR-06
    Scenario: Reject an out-of-bound seed field
      Given an agent name longer than eighty characters
      When the seed request is submitted
      Then the request fails validation before the service runs
    ```

- [ ] **FR-07**

    ```gherkin
    @FR-07
    Scenario: Replay an applied revision
      Given a company seed row already holds the submitted revision
      When Cloud retries the same seed
      Then the response reports `changed: false` and no second agent or goal is created
    ```

    ```gherkin
    @FR-07
    Scenario: Apply a changed revision in place
      Given a company seed row holds an older revision and a recorded agent id
      When Cloud submits edited answers with a new revision
      Then the recorded agent and goal are updated and the seed row keeps the new revision
    ```

- [ ] **FR-08**

    ```gherkin
    @FR-08
    Scenario: Split a multi-line mission into a goal
      Given a seed mission with a title line and detail lines
      When the seed is applied
      Then the company goal uses the first line as title and the remaining lines as description
    ```

- [ ] **FR-09**

    ```gherkin
    @FR-09
    Scenario: Create the seeded lead agent
      Given a seed with an agent name and role text
      When the seed is applied to a company without a lead agent
      Then a non-terminated agent exists with structural role `ceo`, the supplied name, and the supplied text as title
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Retain an initial idea without creating work
      Given a seed with a first-task title and details
      When the seed is applied
      Then the values are stored for the onboarding chat context and no issue or project is created
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Roll back a seed when its audit entry fails
      Given the activity log write fails inside the seed transaction
      When Cloud submits a new revision
      Then the seed row is not committed and Cloud can retry the whole push
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Open one owner-bound onboarding conversation
      Given a board user and a resolved agent in an enabled instance
      When the onboarding endpoint is called twice
      Then one conversation exists for that user and agent and its origin kind is `onboarding_chat`
    ```

    ```gherkin
    @FR-12
    Scenario: Keep onboarding chats out of task numbering
      Given a company with no execution tasks
      When an onboarding chat is created
      Then the company task counter is unchanged and the next accepted task receives the first number
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Start one welcome after a visible paint
      Given an onboarding chat has no user comments and generation zero
      When the visible tab paints the conversation and the greeting endpoint is called concurrently
      Then one agent wakeup request with the onboarding chat greeting idempotency key is admitted
    ```

    ```gherkin
    @FR-13
    Scenario: Retry a failed welcome
      Given a previous greeting wakeup has status failed
      When the greeting endpoint is called again
      Then a new wakeup is admitted and a durable receipt records the retry
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Suppress a welcome after a user message
      Given an onboarding chat already has a visible user comment
      When the greeting endpoint is called
      Then no wakeup is created and the response reports `started: false`
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Suggest scoped work and create it after acceptance
      Given the agent has gathered a goal and exit criteria
      When the assistant sends a `suggest_tasks` interaction and the user accepts it
      Then one execution task is created through the atomic handoff and the chat links to it
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Seed a single first task with a greeting and opening question
      Given a company with no issues and a board caller using the first-task marker
      When the first task is created
      Then its origin kind is `onboarding_first_task`, an agent-attributed greeting and a two-option opening card are seeded, and a concurrent create degrades to an ordinary issue
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Refuse first-task child creation before human acceptance
      Given a run serving the onboarding first task has no persisted accepted proposal
      When it creates a child execution task
      Then the create is rejected with code `onboarding_first_task_acceptance_required`
    ```

    ```gherkin
    @FR-17
    Scenario: Refuse execution after a stale plan revision
      Given the latest accepted proposal targets a plan revision older than the current plan
      When the run creates execution work
      Then the create is rejected and no child task is written
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Restore a draft only for an owned company
      Given a saved onboarding draft names a company the signed-in user does not own
      When the wizard restores its state
      Then the saved blob is discarded and no foreign company id is used
    ```

    ```gherkin
    @FR-18
    Scenario: Open a company-prefixed onboarding route at the agent step
      Given the route names an existing company by issue prefix
      When the wizard launcher resolves the route
      Then the wizard opens on the agent step with that company selected
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: Capture onboarding analytics with consent
      Given browser analytics is enabled and the signed-in person has consented
      When the wizard moves through its steps and is dismissed and reopened
      Then each transition is captured once and the reopen starts a new onboarding session
    ```

- [ ] **NFR-01**

    ```gherkin
    @NFR-01
    Scenario: Enforce actor boundaries on chat endpoints
      Given an authenticated actor that is not a board user with a user id
      When an onboarding chat endpoint is called
      Then the request is rejected with 403 and no conversation is created
    ```

- [ ] **NFR-02**

    ```gherkin
    @NFR-02
    Scenario: Bound all seed free text
      Given a seed with mission, agent role, and first-task details at their maximum lengths
      When the request is validated
      Then the request is accepted and longer values are rejected with 400
    ```

- [ ] **NFR-03**

    ```gherkin
    @NFR-03
    Scenario: Serialize seed application for one company
      Given two Cloud pushes for the same company with different revisions
      When both requests run concurrently
      Then the advisory lock admits one at a time and the final stored revision matches one complete application
    ```

- [ ] **NFR-04**

    ```gherkin
    @NFR-04
    Scenario: Preserve historical task identifiers
      Given a company with numbered issues and an onboarding chat
      When a suggested onboarding task is accepted
      Then existing issue identifiers are unchanged and the new task receives the next unused number
    ```

- [ ] **NFR-05**

    ```gherkin
    @NFR-05
    Scenario: Audit onboarding mutations
      Given a successful seed application, chat opening, and welcome start
      When the activity log is queried for the company
      Then entries exist for `company.onboarding_seed_applied`, `issue.conversation_opened`, and `issue.onboarding_welcome_started`
    ```

- [ ] **NFR-06**

    ```gherkin
    @NFR-06
    Scenario: Degrade when Agent Chat is disabled
      Given the experimental `enableAgentChat` setting is off
      When the wizard finish action calls the chat endpoint
      Then the request returns 404 and the UI explains that Agent Chat is disabled
    ```

## Conflicts

None identified.

## Open Questions

1. Whether the first-task compatibility path is still a default entry point for any deployment or only serves historical records.
2. Whether the seed adapter environment variables are deployment policy that belongs to Cloud rather than Core defaults.
3. Whether invitation onboarding text and Dot pairing setup are part of first-run onboarding scope or separate setup flows.

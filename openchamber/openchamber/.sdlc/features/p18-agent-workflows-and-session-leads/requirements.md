---
title: "Agent workflows and session leads"
status: done
---

# Requirements: Agent workflows and session leads

## Overview

Reusable agent workflows let an agent write a short JavaScript script that fans a large task out to many agents.
OpenChamber runs the script in its own server so the proposing session stays free, and the run's report comes back into that session.
A session lead is a session the user marks to own a direction of work.
A lead keeps a brief and a digest, hands work to sessions it creates, and can start workflow runs without approval when the user allows it.
The UI exposes workflow approval cards, a Workflows panel, lead digest controls, and a hand-to-lead menu.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Fan repeated work such as file reviews, route audits, and migrations out to many agents without blocking the session |
| Power users | Long-running leads that own a direction of work and report status without scrolling the conversation |
| Team members | Review and stop runs from chat, and hand an in-flight session to a lead |
| Maintainers | Bounded cost and safe execution through approval, agent limits, and an isolated sandbox |

## Functional requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall parse a workflow script beginning with `export const meta = { name, description, phases }` and a body using `agent()`, `parallel()`, `pipeline()`, `phase()`, `log()`, and `args`, rejecting imports, non-compiling bodies, undeclared phases, and oversized text. |
| FR-02 | Must | The system shall expose the `openchamber_workflow` tool and `workflow.*` actions only when `agentWorkflowToolEnabled` is on, with the server refusing every action when it is off. |
| FR-03 | Must | The system shall store a run proposed by `workflow.run` as `awaiting-approval` and answer the tool call immediately with its id, name, and phases. |
| FR-04 | Must | The system shall start an awaiting run on approval and settle it as `declined` on decline, waking the proposing session only for completed and failed runs. |
| FR-05 | Must | The system shall execute the script body in a worker thread with a vm context that exposes only the workflow globals, caps the heap, terminates on stop, and blocks `Math.random()`, `Date.now()`, and zero-argument `new Date()`. |
| FR-06 | Must | The system shall start one OpenCode session per `agent()` call, either fresh or as a native fork of a named completed call through `session.fork`. |
| FR-07 | Must | The system shall link workflow agent sessions with `metadata.openchamber.kind = 'workflow-agent'` and `metadata.openchamber.parentID`, keep them out of subagent sidebar rows, and keep them reachable from the run card and Workflows panel. |
| FR-08 | Must | The system shall give a fresh agent the proposing session's directory, permission rules, and model when no model is named, append its allowed tools after the parent's rules, and start no agent when the parent cannot be read. |
| FR-09 | Must | The system shall validate `agent()` options so `id` and `forkFrom` are non-empty strings of at most 120 characters, `id` is unique per run, `forkFrom` names a completed call, and an invalid name fails the run before any prompt is sent. |
| FR-10 | Must | The system shall cap a run at 8 concurrent agents, 200 started agents across all attempts, 4096 `parallel()` tasks, 100000 script characters, 50000 characters of JSON args, and 100 persisted runs. |
| FR-11 | Must | The system shall check schema answers through `openchamber_workflow_answer`, accept the last admitted value, allow up to three attempts, parse bare or fenced JSON as a fallback, and reject a schema whose `required` key conflicts with `additionalProperties: false` before starting an agent. |
| FR-12 | Must | The system shall resume only a `failed` or `stopped` run, replay completed calls keyed by a hash of prompt and options plus an occurrence count, and skip replay when OpenCode confirms a saved session is gone. |
| FR-13 | Must | The system shall persist one JSON run file per run under `<data-dir>/workflow-runs/`, keep settled runs light in memory, move unreadable files aside, and mark runs left running by a stopped server as stopped using owner PID and process start identity. |
| FR-14 | Must | The system shall deliver a synthetic `<openchamber-workflow>` message with source, run id, name, and state metadata into the proposing session, mint its message id before delivery, treat 409 and 404 as delivered, and wake the session only for completed and failed runs. |
| FR-15 | Must | The system shall save workflows as `.openchamber/workflows/<name>.js`, list saved scripts with their descriptions or parse errors, and start a saved workflow immediately in the open session or in a new one. |
| FR-16 | Must | The system shall provide routes to list runs by session or directory, list saved workflows, start a saved workflow, read run and agent detail, approve, decline, stop, resume, and delete a run, with delete limited to finished runs. |
| FR-17 | Must | The system shall render chat run cards and the Workflows panel from server run state, hold action buttons during a request, show the server's refusal reason, keep detail and log refresh state per run, and remove a deleted run locally. |
| FR-18 | Must | The system shall let only the user mark a session as lead from the session menu or a New lead draft, store the mark as `metadata.openchamber.lead` with a timestamp and optional digest, and refuse lead actions for any other session with 409. |
| FR-19 | Must | The system shall clear a lead mark and digest copied by OpenCode into a new child, drop the mark on a fork, and never count a session with a parent as a lead. |
| FR-20 | Must | The system shall keep one brief per lead at `<data-dir>/leads/<id>.md`, replace it whole or apply `{ find, replace }` edits through `lead.brief` within 12000 characters, return the file path in the answer, and remove the file on session deletion. |
| FR-21 | Must | The system shall hold the `openchamber.lead-brief` instruction entry at the brief from the start of the current conversation stretch, refresh it only at compaction, and drop it when the session is no longer a lead. |
| FR-22 | Must | The system shall replace the whole lead digest in session metadata with `needsYou`, `now`, `news`, and `suggestions` under their item limits, require an existing brief, stamp `updatedAt`, and leave out suggestions the user dismissed. |
| FR-23 | Must | The system shall accept `lead.handover` only from the user, refuse leads, subagents, sessions another session runs, and leads with a staged undo, deny question and secret tools, link the session as the lead's `ownWork` child, wake the lead with a note, and undo the link and permissions on failure. |
| FR-24 | Must | The system shall inject fixed lead rules and the brief entry for a lead whose agent has the `openchamber` tool, remove both otherwise, and let `work.name` rename a lead session unless the user named it. |
| FR-25 | Must | The system shall sleep-compact only an idle lead with at least 100000 context tokens after its provider cache expires, and return an authored note from `/api/openchamber/agent-tool/lead-compaction` only for a compaction this runtime started within two minutes for a lead with a brief. |
| FR-26 | Must | The system shall start every run without approval when `agentWorkflowAutoApprove` is on, and only a lead's runs when `agentWorkflowAutoApproveLeads` is on, reading both settings on the server at each `workflow.run`. |
| FR-27 | Should | The system shall show a lead digest row with answers and dismissals in chat, and a Hand to a lead menu that calls `lead.handover`. |
| FR-28 | Should | The system shall keep workflow cards and run approval available on web, desktop, and mobile, and withhold the Workflows panel and injected workflow tool in VS Code. |

## Non-functional requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | The script sandbox shall deny access to server modules, `process`, timers, and network, and shall terminate a script that never yields. |
| NFR-02 | Must | Reliability | A terminal state and its report id shall commit before delivery, and report delivery shall remain idempotent across retries and restarts. |
| NFR-03 | Must | Performance | Run broadcasts shall be throttled to at most one per 250 ms per run, and a settled run shall keep no script, prompts, or full answers in memory. |
| NFR-04 | Should | Compatibility | Shared run contracts shall stay valid for web, desktop, and mobile, and an external OpenCode server shall require the registered OpenChamber plugin. |
| NFR-05 | Should | Security | Run files and brief files shall be owner-readable only, briefs shall stay outside the repository, and no credential or secret shall be logged. |

## Acceptance criteria

- [x] **FR-01**

    ```gherkin
    @FR-01
    Scenario: Parse a valid workflow script
      Given a script starting with an exported meta literal and a body that calls agent()
      When workflow.check parses the script
      Then the response carries the name, description, planned phases, and both agent limits

    @FR-01
    Scenario: Refuse a script that cannot run
      Given a script that imports a module, leaves meta unclosed, names an unlisted phase, or exceeds 100000 characters
      When workflow.run parses it
      Then no run is stored and the agent receives the parser error with status 400
    ```

- [x] **FR-02**

    ```gherkin
    @FR-02
    Scenario: Workflows are off
      Given agentWorkflowToolEnabled is false
      When an agent calls workflow.run
      Then the runtime answers 403 and no tool or session guidance is offered
    ```

- [x] **FR-03**

    ```gherkin
    @FR-03
    Scenario: Propose a run
      Given an enabled workflow tool and a calling session in a directory
      When the agent calls workflow.run with a valid script
      Then a run id is returned at once, the stored state is awaiting-approval, and no agent has started
    ```

- [x] **FR-04**

    ```gherkin
    @FR-04
    Scenario: Approve and decline
      Given a run in awaiting-approval
      When the user approves it
      Then it becomes running and its agents start
      Given another run in awaiting-approval
      When the user declines it
      Then it becomes declined and the proposing session is not woken
    ```

- [x] **FR-05**

    ```gherkin
    @FR-05
    Scenario: Run the script in an isolated worker
      Given a parsed workflow body that loops forever
      When the sandbox starts the worker
      Then the worker is terminated and the run settles as stopped
      Given a script that reads process or imports a Node module
      When the sandbox evaluates it
      Then the name is undefined in the script context
    ```

- [x] **FR-06**

    ```gherkin
    @FR-06
    Scenario: Start a fresh agent and a fork
      Given two completed calls where the second names the first in forkFrom
      When the script runs both calls
      Then the first opens a fresh session and the second opens a native fork of that session with the same metadata link
    ```

- [x] **FR-07**

    ```gherkin
    @FR-07
    Scenario: Hide workflow agents from the sidebar
      Given an agent session with openchamber.kind equal to workflow-agent
      When the session list is projected in chat
      Then the row is absent from Subagents and present on the run card and in the Workflows panel
    ```

- [x] **FR-08**

    ```gherkin
    @FR-08
    Scenario: Inherit the proposing session
      Given a parent session with a directory, permission rules, and a model
      When a fresh workflow agent starts without a model option
      Then the agent uses that directory and model, and its allow rules are appended after the parent's rules
      Given a parent whose rules cannot be read
      When an agent call starts
      Then no child session is created
    ```

- [x] **FR-09**

    ```gherkin
    @FR-09
    Scenario: Reject a bad agent name
      Given a call with a duplicate id or a forkFrom that names an unfinished call
      When the runtime handles the call
      Then the run fails before a prompt is sent
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Enforce agent and input limits
      Given a run with 200 started agents and another agent call
      When the call reaches its slot
      Then it resolves to null, the agent is recorded as failed, and a log line explains the limit
      Given 9 simultaneous agent calls
      When the run executes
      Then at most 8 agents work at once
    ```

- [x] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Accept a schema answer through the tool
      Given a call whose prompt asks for a schema answer
      When the agent hands over a matching value with openchamber_workflow_answer
      Then the value is accepted and the agent's final text is ignored
      Given an answer that does not match the schema
      When the tool validates it
      Then the mismatch is returned with status 400 and the agent is asked again up to three attempts
    ```

- [x] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Reuse completed answers on resume
      Given a stopped run where one agent completed and another failed
      When the user resumes it
      Then the completed answer is replayed with a replayed flag and only the failed work starts again
    ```

- [x] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Recover a run after a restart
      Given a run recorded as running with the previous server process gone
      When the new server starts
      Then the run and its working agents are marked stopped, and its report is delivered once the event hub connects
      Given a run whose owner PID is still alive with the same process start identity
      When the new server starts
      Then the run is left untouched
    ```

- [x] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Deliver the report once
      Given a run that just completed
      When its synthetic report is posted and the server receives a 409
      Then the message is treated as delivered, the marker is saved, and no agent runs again
      Given a run the user declined
      When its report is delivered
      Then the proposing session is not woken
    ```

- [x] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Run a saved workflow
      Given a saved script at .openchamber/workflows/audit-routes.js
      When the user starts it from the panel with no open session
      Then a new session is created, the run begins without another approval click, and the report returns to that session
    ```

- [x] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Manage runs over HTTP
      Given a project with one run in a worktree
      When the client lists runs for repeated directory values and opens run detail
      Then both directories are honoured and the response carries logs, script, args, and result
      Given a running run
      When the client deletes it
      Then the server answers 409 and asks for a stop or decline first
    ```

- [x] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Read run state from the server
      Given a card rendered before the proposing tool result arrived
      When the workflow-run event arrives
      Then the card shows the current server state without a local state guess
      Given a refusal from an action route
      When the request finishes
      Then the hold is released and the server reason is shown to the user
    ```

- [x] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Only the user marks a lead
      Given an ordinary session and an agent calling lead.brief
      When the action checks the session
      Then it answers 409 and writes nothing
      Given the user selects New lead
      When the draft is opened
      Then the session is marked with metadata.openchamber.lead holding the current time
    ```

- [x] **FR-19**

    ```gherkin
    @FR-19
    Scenario: Clear a copied lead mark
      Given a lead with a digest that OpenCode copies into a new child
      When session.created is processed
      Then the child's copied lead mark and digest are cleared
      Given the user forks a lead
      When the fork is created
      Then the fork has no lead mark
    ```

- [x] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Replace and edit a lead brief
      Given a lead with no brief
      When lead.brief writes a markdown brief
      Then the file at <data-dir>/leads/<id>.md holds it and the answer includes that path
      Given a brief containing one occurrence of a find string
      When a list of edits is applied in order
      Then only those replacements are written
      Given an edit whose find string is absent or repeated
      When lead.brief runs
      Then nothing is written and the answer says so
    ```

- [x] **FR-21**

    ```gherkin
    @FR-21
    Scenario: Hold the brief entry until compaction
      Given a lead whose brief changed after its current conversation stretch began
      When the brief entry is read
      Then it still holds the earlier brief
      Given a compaction hook call within two minutes of a runtime-started compaction
      When the entry is refreshed
      Then it holds the current brief
    ```

- [x] **FR-22**

    ```gherkin
    @FR-22
    Scenario: Write a lead digest
      Given a lead with a brief and three suggestions, one of which the user dismissed
      When lead.digest writes needsYou, now, news, and suggestions
      Then the stored digest has updatedAt and omits the dismissed suggestion, and the answer names what was dropped
      Given a lead with no brief
      When lead.digest is called
      Then the server answers 409 and writes no digest
    ```

- [x] **FR-23**

    ```gherkin
    @FR-23
    Scenario: Hand a running session to a lead
      Given an ordinary running session and a lead with no staged undo
      When the user hands the session over
      Then question and secret tools are denied, the session is linked as the lead's ownWork child, and the lead is woken with a note
      Given the lead cannot be woken
      When handover fails
      Then the link and permissions are restored
    ```

- [x] **FR-24**

    ```gherkin
    @FR-24
    Scenario: Inject lead instructions
      Given a lead whose agent has the openchamber tool
      When its instruction entries are synced
      Then the fixed lead rules and its brief entry are present
      Given the same session marked as an ordinary session
      When entries are synced again
      Then both entries are removed
    ```

- [x] **FR-25**

    ```gherkin
    @FR-25
    Scenario: Compact a sleeping lead
      Given an idle lead with 100000 context tokens whose cache lifetime has passed
      When the compaction timer fires
      Then the server starts a compaction and returns an authored note through the hook
      Given a lead with no brief or a compaction started elsewhere
      When the hook is called
      Then the response has no authored summary
    ```

- [x] **FR-26**

    ```gherkin
    @FR-26
    Scenario: Choose the auto-approval mode
      Given agentWorkflowAutoApprove is on
      When any session calls workflow.run
      Then the first stored state is running and the log says it started without approval
      Given only agentWorkflowAutoApproveLeads is on and the caller is an ordinary session
      When workflow.run is called
      Then the run waits for approval
    ```

- [x] **FR-27**

    ```gherkin
    @FR-27
    Scenario: Answer a lead digest
      Given a digest row with a needsYou question and a suggestion
      When the user picks an option and dismisses the suggestion
      Then a synthetic lead reply is sent and the dismissed text is stored on the lead metadata
    ```

- [x] **FR-28**

    ```gherkin
    @FR-28
    Scenario: Runtime availability
      Given a mobile client connected to a managed server
      When a run awaits approval
      Then the chat card offers approve and stop and reports arrive through the server
      Given the VS Code extension
      When workflows are checked
      Then no Workflows panel is shown and no workflow tool is injected
    ```

- [x] **NFR-01**

    ```gherkin
    @NFR-01
    Scenario: Keep the script out of the server
      Given a workflow body that touches process, require, or a timer global
      When the vm context evaluates it
      Then those names are unavailable and the server process remains responsive
      Given a script with an infinite loop
      When the run is stopped
      Then its worker terminates within the stop path
    ```

- [x] **NFR-02**

    ```gherkin
    @NFR-02
    Scenario: Withhold a report until its state is durable
      Given a terminal save that fails after the worker ended
      When the run is read
      Then its ended state is visible, its report is withheld, and a restart reads the last successful snapshot without rerunning agents
    ```

- [x] **NFR-03**

    ```gherkin
    @NFR-03
    Scenario: Bound broadcast and memory cost
      Given many run changes inside 250 ms
      When announcements are made
      Then one openchamber:workflow-run event is broadcast for that run
      Given 35 settled runs held by the server
      When they are listed
      Then no script, prompt, or full answer is held for them and fetching full detail reads the file
    ```

- [x] **NFR-04**

    ```gherkin
    @NFR-04
    Scenario: Share the run contract
      Given a run summary built by the server
      When web, desktop, and mobile clients parse it
      Then all three accept the same states, agent fields, and usage fields
      Given an external OpenCode server
      When a user enables workflows
      Then the docs require the registered OpenChamber plugin and a remote server remains unsupported
    ```

- [x] **NFR-05**

    ```gherkin
    @NFR-05
    Scenario: Keep files private
      Given a new run file and a new lead brief file
      When they are written
      Then their mode is 0600 and the brief lives under the server data directory outside the repository
    ```

## Conflicts

None identified yet.

## Open Questions

1. None. The artifacts were reconstructed from the implemented code, tests, and documentation.

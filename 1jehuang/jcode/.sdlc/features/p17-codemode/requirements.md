---
title: "Codemode"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Codemode

## Overview

Codemode is an opt-in execution mode where the model writes a short JavaScript program that orchestrates harness tool calls instead of issuing one tool call per model turn.
The program runs inside an embedded QuickJS sandbox hosted by jcode, and only what the script returns, plus its captured console output, reaches the transcript, so intermediate results never enter the conversation.
The mode is enabled with `[tools] codemode = true` or the `JCODE_CODEMODE=1` environment variable, and it is off by default.
This feature documents already-implemented code that was reverse-engineered from the repository during an SDLC sync.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Fewer and larger tool rounds, so long task chains cost fewer tokens and finish faster |
| Model and agent authors | A programmable way to chain, filter, and parallelize tool calls inside a single turn |
| Session owners | A per-session scratch store so a script can reuse data without refetching it |
| Maintainers | A sandbox that exposes no host capability beyond the tools the session already allows |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall expose the `codemode` tool only when codemode is enabled in config through `[tools] codemode = true` or through the `JCODE_CODEMODE` environment variable, and shall leave the tool unexposed when it is disabled. |
| FR-2 | Must | The system shall execute the model-written program as the body of an async function inside an embedded QuickJS runtime, so the script can use `await` and `return`. |
| FR-3 | Must | The system shall let a script invoke any other tool available to the session through `await tools.<name>(args)` and `await callTool(name, args)`, and shall raise a JavaScript `Error` inside the script when a tool call fails. |
| FR-4 | Must | The system shall route every tool call made from a script through the harness tool registry, so session allow and deny policy, tool hooks, and MCP routing apply to script calls. |
| FR-5 | Must | The system shall keep intermediate results inside the sandbox, so only the script's return value and its captured console output reach the transcript. |
| FR-6 | Must | The system shall report a failed script to the model, and shall raise the run as a tool error when the script produced no tool calls and no console output. |
| FR-7 | Must | The system shall expose a per-session JSON store to the script through `store(key, value)`, `load(key)`, and `storedKeys()`, and shall persist it between codemode calls in the same session. |
| FR-8 | Should | The system shall let a script discover the tools it may call through `listTools(filter?)` and `describeTool(name)`. |
| FR-9 | Should | The system shall decode a tool's text output into a parsed JSON value when the output is a JSON object or array, and into a string otherwise. |
| FR-10 | Should | The system shall exclude the `codemode` and `batch` tools from the set of tools a script may reach. |
| FR-11 | Should | The system shall report the number of tool calls, the elapsed time, and the names of the stored keys alongside the script result. |
| FR-12 | Should | The system shall cap the report returned to the model at a fixed character budget and mark the report as truncated when the cap is reached. |
| FR-13 | Should | The system shall report an unknown tool name together with the names of similar available tools and a pointer to `listTools()`. |
| FR-14 | May | The system shall capture `console.log`, `console.info`, `console.warn`, `console.error`, and `console.debug` output, prefixing every level above `info` with its level name. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The sandbox shall expose no filesystem, network, timer, or process API, and shall reach the outside world only through host-routed tool calls. |
| NFR-2 | Must | Resource control | Every run shall be bounded by a QuickJS heap limit, a wall-clock timeout, a maximum tool call count, and a maximum captured console size. |
| NFR-3 | Must | Availability | The system shall report codemode as unavailable on FreeBSD, where the QuickJS bindings have no prebuilt artifact, without failing the build. |
| NFR-4 | Should | Isolation | Each run shall execute on a dedicated thread with a current-thread runtime, so the non-`Send` QuickJS engine stays thread-confined while host calls run on the caller's runtime. |
| NFR-5 | Should | Reliability | Dropping the run future shall cancel the script, and tearing a run down shall abort the tool calls still in flight. |
| NFR-6 | Should | Performance | Independent tool calls made by one script shall run concurrently rather than one after another. |
| NFR-7 | Should | Observability | Every run shall be logged with the session id, the tool call count, the elapsed time, and the error, if any. |
| NFR-8 | May | Portability | The QuickJS dependency shall be optional per target, so a target without prebuilt bindings still builds. |

## Constraints

- The feature is experimental and opt-in, and it is off in the default config.
- The sandbox runs where the harness runs, not where `bash` runs.
- The embedded QuickJS engine is not `Send`, so each run is confined to a single thread.
- The `codemode` tool description is exempt from the shared tool-description token cap because it documents the sandbox API.
- The QuickJS C build lives in its own workspace crate so it is compiled once and cached.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Tool is exposed when codemode is enabled in config
      Given the config section "[tools] codemode = true"
      When the session tool registry is built
      Then the registry contains a tool named "codemode"

    @FR-1
    Scenario: Tool is absent when codemode is disabled
      Given the default config where "tools.codemode" is false
      When the session tool registry is built
      Then the registry contains no tool named "codemode"

    @FR-1
    Scenario: Environment variable enables codemode
      Given the environment variable "JCODE_CODEMODE" set to "1"
      And the config leaves "tools.codemode" false
      When the session tool registry is built
      Then the registry contains a tool named "codemode"
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Script body runs as an async function
      Given a script "const a = await tools.echo({}); return a;"
      When the script runs
      Then the result is the value the script returned
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Script calls a session tool
      Given a script that awaits "tools.echo({ x: 1 })"
      When the script runs
      Then the tool is invoked with the arguments the script passed
      And the tool result reaches the script as a value

    @FR-3
    Scenario: A failing tool throws inside the script
      Given a tool that always fails
      And a script that awaits the failing tool inside a try block
      When the script runs
      Then the script catches an Error whose message names the failing tool
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Session policy applies to script calls
      Given a session policy that denies the tool "shout"
      And a script that lists the available tools
      When the script runs
      Then the denied tool is absent from the listed tools
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Intermediate results stay in the sandbox
      Given a script that calls a tool three times and returns a summary
      When the script runs
      Then the transcript receives the summary, the console output, and a tool call count
      And the transcript receives no intermediate tool output
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A script error is reported to the model
      Given a script that throws an Error
      When the script runs
      Then the report contains the error message

    @FR-6
    Scenario: A failure with no side effects is a tool error
      Given a script that throws before calling any tool
      When the script runs
      Then the tool call fails with the script error
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: A stored value is visible to a later run in the same session
      Given a first script that stores a value under the key "n"
      When a second script in the same session loads that key
      Then the second script receives the stored value
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Tool discovery from inside a script
      Given a script that calls "listTools()" and "describeTool(\"echo\")"
      When the script runs
      Then the script receives the tool names, the tool descriptions, and the tool input schema
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: JSON tool output is decoded
      Given a tool that returns a JSON object as text
      When a script calls the tool
      Then the script receives a parsed object

    @FR-9
    Scenario: Plain text tool output stays a string
      Given a tool that returns plain text
      When a script calls the tool
      Then the script receives the text as a string
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Recursion and batch are not reachable
      Given a script that calls "tools.codemode"
      When the script runs
      Then the call fails with an unknown tool error for "codemode"
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: The run footer reports calls, time, and stored keys
      Given a script that calls one tool and stores one key
      When the run report is rendered
      Then the report shows "1 tool call", the elapsed seconds, and the stored key name
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: An oversized report is truncated
      Given a run whose report exceeds the report budget
      When the report is rendered
      Then the report is capped and states that it was truncated
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: An unknown tool name suggests alternatives
      Given a script that calls the tool "ech"
      When the script runs
      Then the error names the unknown tool and suggests the tool "echo"
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Console output is captured with level prefixes
      Given a script that logs "hi" and an object at level "log" and "careful" at level "warn"
      When the script runs
      Then the captured lines are "hi {\"a\":1}" and "[warn] careful"
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: No host API is reachable from the script
      Given a script that checks "require", "process", "fetch", "setTimeout", "std", and "os"
      When the script runs
      Then every one of them is undefined
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A busy loop hits the wall clock limit
      Given a script that loops forever
      And a run timeout of 300 ms
      When the script runs
      Then the run fails with a timeout error

    @NFR-2
    Scenario: A run stops at the tool call limit
      Given a run limit of 3 tool calls
      And a script that calls a tool five times
      When the script runs
      Then the run fails with a tool call limit error

    @NFR-2
    Scenario: A run stops at the heap limit
      Given a run heap limit of 8 MB
      And a script that allocates without bound
      When the script runs
      Then the run fails with an error
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: A FreeBSD build reports codemode as unavailable
      Given a build targeting FreeBSD
      When the codemode availability flag is read
      Then the flag is false
      And a run returns the "not available on FreeBSD" error
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: A run is confined to one thread
      Given a script that calls a tool
      When the script runs
      Then the script executes on a dedicated codemode thread
      And the tool call runs on the runtime that started the run
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Dropping the run future cancels the script
      Given a run that is waiting on a tool that never returns
      When the run future is dropped
      Then the script stops without blocking the caller
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Independent calls run concurrently
      Given a script that starts 20 independent tool calls with "Promise.all"
      And a tool that takes 50 ms
      When the script runs
      Then the run finishes in under 800 ms
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Every run is logged
      Given a completed run
      When the run is inspected in the log
      Then the log line names the session, the tool call count, the elapsed time, and the error
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: A target without prebuilt bindings still builds
      Given a target where the QuickJS bindings are not prebuilt
      When the workspace is built
      Then the build succeeds and codemode reports itself unavailable
    ```

## Conflicts

None identified yet.

## Open Questions

1. The per-run limits and the report budget are hard-coded rather than configurable, so it is undecided whether they should become config settings.
2. It is undecided whether the session store should be scoped per tool call, per turn, or per session beyond its current session-wide lifetime.
3. It is undecided whether a script that makes no tool calls and returns a value should be reported as a success or as a no-op.

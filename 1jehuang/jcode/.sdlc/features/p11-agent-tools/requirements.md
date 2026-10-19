---
title: "Agent Tool Suite"
status: done
session_link: "http://localhost:10000/?session=ses_sync_sdlc_20261019"
---

# Requirements: Agent Tool Suite

## Overview

The agent tool suite is the runtime the model invokes to act on the world.
It provides a `Tool` trait, a registry that owns the live tool set, and the tool implementations themselves (file access, shell, web, MCP, coordination, memory, desktop surfaces).
This feature was reverse-engineered from the existing codebase during an SDLC sync and documents already-implemented functionality.
The command-safety gate, the Codemode sandbox, and agent applets are documented as separate features and are only referenced here as boundaries.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Model clients | A stable, discoverable tool surface with predictable schemas and predictable failures |
| End users | Tools that finish the job without silently eating the context window or leaking credentials |
| Maintainers | One place to reason about dispatch, policy, telemetry, and the tool inventory |
| Integrators | MCP servers, SDK clients, and desktop surfaces that plug into the same registry |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall expose a registry that registers, unregisters, lists, and executes tools by name, and that publishes provider-facing tool definitions. |
| FR-2 | Must | The system shall inject a shared `intent` property into every object-shaped tool schema and mark it required, so every call carries a human-readable reason. |
| FR-3 | Must | The system shall advertise an optional `accept_large_output` property on every object-shaped tool schema and honor it when the caller sets it. |
| FR-4 | Must | The system shall resolve provider and namespace tool-name aliases (including `functions.` prefixes, Claude Code names, and PascalCase OAuth names) to canonical registry names before dispatch. |
| FR-5 | Must | The system shall enforce the per-session tool allow list and deny list at execution time, including for MCP tools addressed through aliases retired after a reconnect. |
| FR-6 | Must | The system shall reject a call to an unknown tool with an error that lists the available tools and suggests near-miss names. |
| FR-7 | Must | The system shall withhold a tool result that would exceed the context budget, and shall only return a truncated result when the caller explicitly opted in. |
| FR-8 | Must | The system shall read files as text, image, or PDF, and shall report binary files without attempting to decode them. |
| FR-9 | Must | The system shall write files, creating parent directories as needed, and shall report a diff summary plus a unified diff. |
| FR-10 | Must | The system shall apply exact-match edits so that all edits in a call apply or none do. |
| FR-11 | Must | The system shall apply multi-file patches in both the Codex envelope format and the unified-diff format, including file creation, deletion, and moves. |
| FR-12 | Must | The system shall perform literal or regular-expression replacement across files, applying every replacement or none. |
| FR-13 | Must | The system shall list directory contents on request. |
| FR-14 | Must | The system shall search code and file names, supporting grep, find, outline, and trace modes. |
| FR-15 | Must | The system shall run shell commands, capturing standard output and standard error separately and reporting exit status. |
| FR-16 | Must | The system shall forward standard input to a running command when the command reads from it. |
| FR-17 | Must | The system shall promote a command that exceeds the foreground timeout into a background task instead of discarding it. |
| FR-18 | Must | The system shall parse progress markers and progress heuristics from command output and surface them as task progress. |
| FR-19 | Must | The system shall terminate the whole process group of a timed-out command so that no descendant survives. |
| FR-20 | Must | The system shall search the web through DuckDuckGo, Bing, SearXNG, or a custom engine, and shall try the configured fallback engines in order. |
| FR-21 | Must | The system shall call a custom HTTP JSON search endpoint configured under `[websearch.custom]`, mapping the JSON response into title, URL, and snippet results. |
| FR-22 | Must | The system shall keep custom-search credentials out of diagnostics and shall not forward credentials across redirects. |
| FR-23 | Must | The system shall fetch a URL and return it as text, Markdown, or HTML, subject to a response size cap and an output size cap. |
| FR-24 | Must | The system shall manage MCP servers through the `mcp` tool, supporting listing, connecting, disconnecting, reloading, status, and logout. |
| FR-25 | Must | The system shall expose the MCP tool catalog through a deferred search tool and a deferred call tool, so that a model can find and invoke a server tool by name. |
| FR-26 | Must | The system shall register connected MCP server tools as callable tools under a namespaced alias, resolving alias collisions deterministically. |
| FR-27 | Must | The system shall cache MCP tool schemas on disk so that a new session can advertise the MCP surface before the connections settle. |
| FR-28 | Must | The system shall run independent tool calls in parallel through the `batch` tool, and shall accept the common malformed shapes models produce. |
| FR-29 | Must | The system shall coordinate multiple agents through the `swarm` tool, covering spawn, assignment, run plans, awaiting, status, and messaging. |
| FR-30 | Must | The system shall track structured work items through the `todo` tool, including status, grouping, confidence, and goal-level assessment fields. |
| FR-31 | Must | The system shall manage background tasks through the `bg` tool, including listing, status, output, tail, cancel, cleanup, and waiting. |
| FR-32 | Must | The system shall persist and query long-lived memory through the `memory` tool, supporting remember, recall, search, list, forget, tag, link, and related actions. |
| FR-33 | Must | The system shall search past chat sessions through the `session_search` tool and in-conversation history through the `conversation_search` tool, with filters and grouping. |
| FR-34 | Must | The system shall load, list, read, and reload skills through the `skill_manage` tool. |
| FR-35 | Must | The system shall search the bundled Jcode documentation through the `jcode_docs` tool. |
| FR-36 | Must | The system shall record a structured lifecycle event for every tool call, covering the requested name, the resolved name, the status, the latency, the output size, and the touched paths. |
| FR-37 | Must | The system shall let a user-configured pre-tool hook block a call, and shall let post-tool observers and post-tool feedback hooks observe the outcome and append feedback to the result. |
| FR-38 | Should | The system shall open desktop panels from Markdown or Markdown/PDF files and manage their lifecycle through the `panel` tool, and shall keep the legacy `side_panel` tool working. |
| FR-39 | Should | The system shall render an interactive native card through the `applet` tool and an inline Markdown answer through the `user_response` tool, and shall expose both only when the desktop UI capability is enabled. |
| FR-40 | Should | The system shall drive a real browser through the `browser` tool, covering navigation, content extraction, scripted evaluation, and interaction. |
| FR-41 | Should | The system shall compile source in a remote sandbox through the `compile_remote` tool, reserving and settling metered usage against the subscription. |
| FR-42 | Should | The system shall run a JavaScript program that calls other tools through the `codemode` tool, and shall register that tool only when it is enabled in the configuration. |
| FR-43 | Should | The system shall discover external integrations through the `integration_tools` tool, and shall register that tool only when integration discovery is enabled. |
| FR-44 | Should | The system shall read and send mail through the `gmail` tool and manage calendars through the `calendar` tool. |
| FR-45 | Should | The system shall open or reveal a file, a folder, or a URL for the user through the `open` tool. |
| FR-46 | Should | The system shall build, reload, test, and inspect the project under development through the `selfdev`, `desktop_selfdev`, and `debug_socket` tools. |
| FR-47 | Should | The system shall register the ambient-mode tools (`end_ambient_cycle`, `schedule_ambient`, `request_permission`, `send_message`, and `schedule`) only for ambient sessions. |
| FR-48 | Should | The system shall control the macOS desktop through the `macos_computer_use` tool on macOS hosts only. |
| FR-49 | May | The system shall let a client register session-scoped custom tool callbacks that the registry dispatches to instead of a built-in tool. |
| FR-50 | May | The system shall provide the `maintainer_feedback` and `invalid` tools for product feedback and for reporting malformed tool usage. |
| FR-51 | May | The system shall keep the `initiative` and `patch` tool implementations available but unregistered, so they can be restored without a migration. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | The system shall build the stateless base tool set once per process and reuse it across sessions, so session startup does not pay per-tool construction cost. |
| NFR-2 | Must | Performance | A single tool result shall not exceed the smaller of 30% of the context budget and 50,000 tokens, so no one result can dominate a context window. |
| NFR-3 | Must | Security | The system shall resolve relative tool paths against the session working directory, and shall not let one tool write outside the paths its input names. |
| NFR-4 | Must | Security | The system shall never write a configured credential, endpoint URL, or request body into a log line, an error message, or a hook payload. |
| NFR-5 | Must | Safety | The system shall serialize concurrent writes to the same file so that two tools cannot interleave a partial write. |
| NFR-6 | Should | Performance | The system shall skip the MCP alias rebuild when a reconnected server's tool catalog is unchanged, so a reload storm does not scale with the number of servers. |
| NFR-7 | Should | Performance | The system shall publish tool definitions in a stable sorted order, so provider prompt caches are not invalidated by registry ordering. |
| NFR-8 | Should | Maintainability | The system shall keep every tool description and every tool parameter description under a documented token cap, because the text rides on every request. |
| NFR-9 | Should | Compatibility | The system shall not emit tool schemas that strict-mode providers reject, such as an array of a union type or a `required` entry with no matching property. |
| NFR-10 | Should | Observability | The system shall emit one structured lifecycle event per tool call, so an operator can reconstruct which tool ran, with which arguments, and with what outcome. |
| NFR-11 | Should | Reliability | A failing tool shall return a diagnostic error to the caller rather than terminating the turn. |
| NFR-12 | May | Portability | The system shall keep platform-specific tools behind a target guard, so the same registry builds on Linux, macOS, and Windows. |

## Constraints

- The tool trait and the shared output types live in the `jcode-tool-core` and `jcode-tool-types` crates, and the tool implementations live in `crates/jcode-app-core/src/tool/`.
- The registry key is the provider-facing tool name, and it overrides the name the tool reports for itself.
- A tool stored inside the registry holds only a weak reference to the registry, so the registry does not own itself.
- `jcode-tool-types::resolve_tool_name` owns the alias table, so that lower-level crates can normalize names without depending on the tool subsystem.
- The command-safety gate, the Codemode sandbox, and the agent applet runtime are separate features.

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
    Scenario: Register and execute a tool by name
      Given a registry with the read tool registered
      When the registry executes "read" with a path to an existing text file
      Then the tool output contains the file contents
      And the registry lists "read" among its tool names
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Every tool schema requires an intent
      Given the provider-facing definitions of the first-party tools
      When each definition is inspected
      Then every object schema has an "intent" property
      And "intent" appears in the required list of every object schema
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: The oversized-output opt-in is advertised and honored
      Given a tool whose result is larger than the context guard allows
      When the call is made without "accept_large_output"
      Then the result is withheld and a refusal message is returned
      When the same call is made with "accept_large_output" set to true
      Then the result is returned truncated with a truncation notice
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Provider aliases resolve to the canonical tool
      Given a registry containing the bash tool
      When a call names the tool "shell_exec" or "functions.Bash"
      Then the bash tool runs
      And the lifecycle event records both the requested name and the resolved name
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A denied tool is refused
      Given a session policy that denies the bash tool
      When the model calls the bash tool
      Then the call fails with a "disabled" error
      And the shell command is never started
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: An unknown tool name yields a recoverable error
      Given a registry with the read tool registered
      When a call names the tool "reed"
      Then the error names the unknown tool
      And the error lists the available tools
      And the error suggests the read tool
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: An unaffordable result is withheld rather than truncated
      Given a context budget that is nearly exhausted
      When a tool returns a result larger than the remaining budget
      Then the result is withheld and the caller is told to compact
      And the withheld bytes are not added to the context
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Read a file, an image, and a binary file
      Given a text file, a PNG image, and a binary file in the working directory
      When the read tool is called for each of them
      Then the text file is returned as text
      And the image is returned as an image block
      And the binary file is reported as binary without a decode attempt
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Write a new file
      Given a working directory with no target file
      When the write tool is called with a file path and content
      Then the file exists with exactly that content
      And the output reports the file as created with a diff summary
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A failed edit leaves the file untouched
      Given a file whose second edit target does not exist
      When the edit tool is called with both edits
      Then the call fails
      And the file content is unchanged
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Apply a multi-file patch
      Given a Codex-style patch that adds one file and updates another
      When the apply_patch tool is called
      Then both files are changed on disk
      And the output reports the files that changed
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: A cross-file replacement either lands everywhere or nowhere
      Given two files that both contain the search string
      When the replace tool is called with a regular expression
      Then both files are updated
      And a replacement that cannot be applied to one file leaves both files unchanged
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: List a directory
      Given a working directory holding two files and one subdirectory
      When the ls tool is called
      Then the output names both files and the subdirectory
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Search for a symbol
      Given a source tree containing a matching function
      When the agentgrep tool is called in grep mode
      Then the output names the matching file and line
      When the mode is omitted
      Then the search runs in grep mode
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Run a command and capture both streams
      Given a command that writes to standard output and standard error
      When the bash tool runs it
      Then the output contains the standard output text
      And the output reports the non-zero exit status and the standard error text
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Forward input to a command that reads it
      Given a command that reads one line from standard input
      When the bash tool runs it and the session supplies that line
      Then the command output contains the supplied line
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: A command that outlasts the foreground timeout is promoted
      Given a command that runs longer than the foreground timeout
      When the bash tool runs it
      Then the call returns with a background task identifier
      And the command is still running as a background task
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Progress output becomes task progress
      Given a background command that prints a progress marker
      When the progress marker is parsed
      Then the task status reports the reported percentage
      And the marker line is not repeated in the captured output
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: A timeout kills the whole process group
      Given a command that spawns a long-lived child process
      When the command times out
      Then neither the parent nor the child process survives
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Fall back when the preferred engine yields nothing
      Given a preferred engine that returns no results
      And a configured fallback engine that returns one result
      When the websearch tool runs
      Then the fallback engine's result is returned
    ```

- [ ] **FR-21**

    ```gherkin
    @FR-21
    Scenario: Map a custom search response
      Given a custom search endpoint that returns a JSON array at the configured results pointer
      When the websearch tool runs with engine "custom"
      Then each result's title, URL, and snippet are read through the configured pointers
      And a result with a missing URL is skipped
    ```

- [ ] **FR-22**

    ```gherkin
    @FR-22
    Scenario: Credentials never leak and redirects are not followed
      Given a custom search endpoint that answers with a redirect to another host
      When the websearch tool runs
      Then the redirect is not followed
      And no error message or log line contains the configured credential
    ```

- [ ] **FR-23**

    ```gherkin
    @FR-23
    Scenario: Fetch a page as Markdown
      Given a reachable web page
      When the webfetch tool is called with format "markdown"
      Then the output is the extracted Markdown text
      And a non-HTTP scheme is rejected before any request is made
    ```

- [ ] **FR-24**

    ```gherkin
    @FR-24
    Scenario: Manage MCP servers
      Given a configured MCP server that is disabled
      When the mcp tool lists the servers
      Then the disabled server is listed and is not spawned
      When the mcp tool connects to it by name
      Then the connection is reported as established
    ```

- [ ] **FR-25**

    ```gherkin
    @FR-25
    Scenario: Find and call a server tool
      Given a connected MCP server exposing a "read_file" tool
      When the mcp_search tool searches for "read"
      Then the result names the callable tool and its input schema
      When the mcp_call tool calls that tool
      Then the server's result is returned to the caller
    ```

- [ ] **FR-26**

    ```gherkin
    @FR-26
    Scenario: Two servers exposing the same tool name get distinct aliases
      Given two connected MCP servers that each expose a "search" tool
      When the MCP surface is reconciled
      Then both tools are callable under distinct names
      And the registry maps each alias back to its own server
    ```

- [ ] **FR-27**

    ```gherkin
    @FR-27
    Scenario: The MCP surface is advertised before connections settle
      Given a cached schema for a configured MCP server
      When a new session starts
      Then the cached MCP tools are present in the first tool snapshot
    ```

- [ ] **FR-28**

    ```gherkin
    @FR-28
    Scenario: Batch runs calls in parallel and tolerates malformed shapes
      Given a batch of two independent read calls
      When the batch tool runs with the tool name given as "name" and the arguments given flat
      Then both reads run and both results are returned
      And a batch of more than ten calls is rejected
    ```

- [ ] **FR-29**

    ```gherkin
    @FR-29
    Scenario: Run a swarm plan
      Given a plan with two independent nodes
      When the swarm tool runs the plan
      Then each node is dispatched to a worker
      And the terminal summary reports the succeeded and failed nodes
    ```

- [ ] **FR-30**

    ```gherkin
    @FR-30
    Scenario: Track a multi-step task
      Given a task with three steps
      When the todo tool creates the items and marks the first one in progress
      Then the list reports one item in progress and two pending
      And each item carries its status and group
    ```

- [ ] **FR-31**

    ```gherkin
    @FR-31
    Scenario: Wait for a background task
      Given a running background task
      When the bg tool waits for it
      Then the call returns when the task finishes
      And the output carries the task output and its status
    ```

- [ ] **FR-32**

    ```gherkin
    @FR-32
    Scenario: Remember and recall a fact
      Given a memory store with no entry for a given query
      When the memory tool remembers a fact and then recalls it
      Then the recalled entry carries the fact and its category
    ```

- [ ] **FR-33**

    ```gherkin
    @FR-33
    Scenario: Search a past session
      Given a saved session that contains a matching phrase
      When the session_search tool runs
      Then the result names the session and points at the matching message
      And the current session is excluded by default
    ```

- [ ] **FR-34**

    ```gherkin
    @FR-34
    Scenario: List and load a skill
      Given a skill registry holding one skill
      When the skill_manage tool lists the skills
      Then the skill is listed
      When the skill_manage tool loads that skill
      Then the skill content is returned
    ```

- [ ] **FR-35**

    ```gherkin
    @FR-35
    Scenario: Search the bundled documentation
      Given the bundled Jcode documentation
      When the jcode_docs tool searches for a configuration key
      Then the output cites the matching documentation section
    ```

- [ ] **FR-36**

    ```gherkin
    @FR-36
    Scenario: Every call produces lifecycle events
      Given a tool that fails
      When the tool runs
      Then a start event and an error event are emitted
      And the events carry the resolved tool name, the status, the latency, and the touched paths
    ```

- [ ] **FR-37**

    ```gherkin
    @FR-37
    Scenario: A pre-tool hook blocks the call
      Given a configured pre_tool hook that exits with a block decision
      When a tool call is made
      Then the call fails with the hook's reason
      And the tool never runs
    ```

- [ ] **FR-38**

    ```gherkin
    @FR-38
    Scenario: Open a desktop panel
      Given the desktop UI capability is enabled
      When the panel tool spawns a panel from Markdown content
      Then the panel is listed by the panel tool
    ```

- [ ] **FR-39**

    ```gherkin
    @FR-39
    Scenario: Desktop-only tools stay hidden elsewhere
      Given a registry with the desktop UI capability disabled
      When the tool definitions are published
      Then neither the applet tool nor the user_response tool is advertised
      And a call to either name fails as an unknown tool
    ```

- [ ] **FR-40**

    ```gherkin
    @FR-40
    Scenario: Drive a browser
      Given a browser provider that is ready
      When the browser tool navigates to a page and requests its content
      Then the output contains the page content
    ```

- [ ] **FR-41**

    ```gherkin
    @FR-41
    Scenario: Compile remotely with metered usage
      Given a signed-in account with remote compilation entitlement
      When the compile_remote tool submits a build
      Then the output carries the compiler output and the metered usage
    ```

- [ ] **FR-42**

    ```gherkin
    @FR-42
    Scenario: Codemode chains tool calls
      Given codemode is enabled in the configuration
      When the codemode tool runs a script that calls the read tool twice
      Then the script result is returned and the two reads never enter the conversation
      And the codemode tool is absent when the feature is disabled
    ```

- [ ] **FR-43**

    ```gherkin
    @FR-43
    Scenario: Discover an integration
      Given integration discovery is enabled
      When the integration_tools tool searches for a category
      Then the output lists matching integrations
      And the tool is absent when discovery is disabled
    ```

- [ ] **FR-44**

    ```gherkin
    @FR-44
    Scenario: List calendars
      Given a connected Google account
      When the calendar tool lists the calendars
      Then the output names the available calendars
    ```

- [ ] **FR-45**

    ```gherkin
    @FR-45
    Scenario: Reveal a file
      Given a file in the working directory
      When the open tool is called with action "reveal" and that path
      Then the tool reports that the file was revealed
    ```

- [ ] **FR-46**

    ```gherkin
    @FR-46
    Scenario: The CLI self-dev tool refuses to run in a Desktop checkout
      Given a working directory that is a Jcode Desktop checkout
      When the selfdev tool is called
      Then the call fails and points at the desktop_selfdev tool
    ```

- [ ] **FR-47**

    ```gherkin
    @FR-47
    Scenario: Ambient tools are ambient-only
      Given a session that is not an ambient session
      When the request_permission tool is called
      Then the call is rejected
    ```

- [ ] **FR-48**

    ```gherkin
    @FR-48
    Scenario: The computer-use tool only exists on macOS
      Given a registry built on a macOS host
      When the tool definitions are published
      Then the macos_computer_use tool is advertised
    ```

- [ ] **FR-49**

    ```gherkin
    @FR-49
    Scenario: A client-registered tool is dispatched
      Given a client that registered a custom tool for the session
      When the model calls that tool name
      Then the client callback runs
      And the callback result is returned to the caller
    ```

- [ ] **FR-50**

    ```gherkin
    @FR-50
    Scenario: Report invalid tool usage
      Given a malformed tool call
      When the invalid tool is called
      Then the output records the malformed usage
    ```

- [ ] **FR-51**

    ```gherkin
    @FR-51
    Scenario: Retained tools stay unregistered
      Given a registry with the base tool set
      When the tool definitions are published
      Then neither the initiative tool nor the patch tool is advertised
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The base tool set is built once per process
      Given two sessions created in the same process
      When both registries are created
      Then the per-tool construction work happens only for the first session
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A single huge result is capped
      Given a context budget of 1,000,000 tokens
      When a tool returns a result of 200,000 tokens
      Then the result is withheld
      And the refusal message states the cost
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Relative paths resolve against the session working directory
      Given a session whose working directory holds a target file
      When the read tool is called with a relative path
      Then the file inside the working directory is read
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Diagnostics carry no secrets
      Given a custom search endpoint configured with a header credential
      When the request fails
      Then neither the error message nor the log output contains the credential value
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Concurrent writes to one file are serialized
      Given two write calls naming the same file
      When both run at the same time
      Then the file ends with one complete write, not an interleaved mixture
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: An unchanged reconnect does not rebuild the surface
      Given a connected MCP server whose catalog did not change
      When the server reconnects
      Then the alias set is left untouched
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Definitions are emitted in a stable order
      Given a registry with several tools
      When the definitions are published twice
      Then both listings are in the same sorted order
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Descriptions stay under the token cap
      Given the provider-facing definitions of the first-party tools
      When each description is measured
      Then no tool description exceeds the cap
      And no tool parameter description exceeds the cap
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: Schemas stay acceptable to strict providers
      Given the provider-facing definitions of the first-party tools
      When each schema is validated
      Then no array property is typed as a union
      And no required entry lacks a matching property
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: A tool run is reconstructable from the event log
      Given a tool that touches two files
      When the tool runs
      Then the lifecycle event names both touched paths and the outcome
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: A tool error does not end the turn
      Given a tool that always fails
      When the tool runs
      Then the failure is returned as a tool error
      And the surrounding turn continues
    ```

- [ ] **NFR-12**

    ```gherkin
    @NFR-12
    Scenario: Platform-specific tools are guarded
      Given a registry built on a non-macOS host
      When the tool definitions are published
      Then no macOS-only tool is advertised
    ```

## Conflicts

<!-- Identified and populated by /review-requirements: pairs or groups of requirements that cannot all be satisfied at once. Reconcile before approval, or promote to an open question. -->

None identified yet.

## Open Questions

1. None. The feature is already implemented; any future change should be tracked as a new issue.

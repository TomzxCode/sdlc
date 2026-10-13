---
title: "MCP Client"
status: done
session_link: "none"
---

# Requirements: MCP Client

## Overview

Pi needs a standalone Model Context Protocol client plus a built-in replaceable extension so the agent can call tools and read resources from user-configured MCP servers without depending on the official MCP SDK.
The client core owns initialization, request correlation, timeouts, cancellation, progress, and server-request handling, while pluggable transports own framing and I/O.
The built-in extension connects servers from `mcp.json` and extension-registered servers, adapts their tools into pi's tool pipeline, and exposes them to the model through configurable exposure modes.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Agent users | Call MCP tools and read MCP resources from their configured servers reliably |
| Extension authors | Register additional MCP servers and replace the built-in extension behavior |
| MCP server operators | Serve tools and resources to pi over stdio or Streamable HTTP with OAuth sign-in |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall connect to an MCP server through a transport, negotiate a supported protocol version, and send `notifications/initialized` |
| FR-2 | Must | The system shall list all tools of a server by following `tools/list` pagination cursors |
| FR-3 | Must | The system shall call a server tool and return its `CallToolResult` including structured content and the `isError` flag |
| FR-4 | Must | The system shall list resources, list resource templates, and read resources from a server |
| FR-5 | Must | The system shall answer server `ping` and `roots/list` requests with the configured roots |
| FR-6 | Must | The system shall support per-request timeouts, abort-signal cancellation with `notifications/cancelled`, and progress callbacks with timeout renewal |
| FR-7 | Must | The system shall expose a generic notification subscription API covering logging and tool-list-change notifications |
| FR-8 | Must | The system shall provide a stdio transport that spawns the server and shuts it down per the spec |
| FR-9 | Must | The system shall provide a Streamable HTTP transport with session handling, the server-to-client GET stream with reconnection, and `Last-Event-ID` resumption |
| FR-10 | Must | The system shall provide an in-memory transport pair for client and adapter tests |
| FR-11 | Must | The system shall convert a `CallToolResult` to model-facing text and image content via `toLlmContent` |
| FR-12 | Must | The system shall implement the MCP OAuth client subset covering protected-resource and authorization-server discovery, PKCE authorization code flow, dynamic client registration, shared token refresh, and step-up authorization |
| FR-13 | Must | The system shall connect servers from `mcp.json` and extension-registered servers, with `mcp.json` entries taking precedence over same-name registered servers |
| FR-14 | Must | The system shall register each server tool as `mcp__<server>__<tool>` sanitized to provider limits with a hash suffix on collision or overflow |
| FR-15 | Must | The system shall honor per-server `exposure` and per-tool `toolExposure` across the `codemode`, `deferred`, `direct`, and `hidden` modes |
| FR-16 | Must | The system shall list enabled servers with indirect tools in the `mcp_servers` system prompt section |
| FR-17 | Must | The system shall provide the `/mcp` manager for sign-in, reconnect, enable or disable, and exposure changes |
| FR-18 | Must | The system shall expose MCP resources through the Codex-compatible `list_mcp_resources`, `list_mcp_resource_templates`, and `read_mcp_resource` tools |
| FR-19 | Should | The system shall wait for still-connecting `direct` servers only briefly before the first prompt so a hanging server never blocks prompting indefinitely |
| FR-20 | Should | The system shall run every MCP tool call through pi's tool pipeline so hooks and permission extensions apply uniformly |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Maintainability | The system shall have no dependency on the official MCP SDK or on other pi packages, keeping `cross-spawn` as its only runtime dependency |
| NFR-2 | Must | Portability | The system shall run on Node.js 22.19 or newer |
| NFR-3 | Must | Reliability | The system shall default every request to a 30 second timeout that progress notifications renew |
| NFR-4 | Must | Performance | The system shall cap model-facing MCP text output and spill the full text to a temp file the model can read |
| NFR-5 | Should | Reliability | The system shall cap inbound JSON-RPC messages at 16 MiB by default |
| NFR-6 | Should | Usability | The system shall report startup config errors, failed connections, and sign-in needs exactly once per session start |

## Constraints

- The client shall not depend on the official MCP SDK.
- Batch JSON-RPC messages, legacy HTTP+SSE, MCP servers, sampling, and tasks are out of scope for the client core.
- The OAuth implementation is adapted from the MIT-licensed MCP TypeScript SDK v1.29.0 and its license is carried under `LICENSES/`.

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
    Scenario: Client initializes against an in-memory server
      Given an in-memory transport pair with a server that accepts protocol version 2025-11-25
      When the client connects and the server selects a supported version
      Then the client records the server info and capabilities and sends notifications/initialized
    ```

    ```gherkin
    @FR-1
    Scenario: Server selects an unsupported version
      Given a server whose initialize result names an unknown protocol version
      When the client connects
      Then the connection fails with an unsupported-version error and the client ends closed
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Tools are collected across pages
      Given a server that returns two pages of tools/list with a nextCursor
      When the client lists tools
      Then every tool from every page is returned in order
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Tool failure arrives in the result
      Given a server whose tools/call result carries isError true with content blocks
      When the client calls the tool
      Then the returned result preserves the content and reports isError true instead of raising a protocol error
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Resources round-trip through the client
      Given a server offering one resource and one template
      When the client lists resources, lists templates, and reads the resource URI
      Then the listings contain the offered entries and the read returns their contents
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Server requests roots
      Given a client configured with a workspace root
      When the server sends roots/list
      Then the client answers with the configured root entries
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Slow request times out and cancels remotely
      Given a server that never answers tools/call
      When the client calls the tool with a short timeout
      Then the call rejects with a timeout error and the server receives notifications/cancelled
    ```

    ```gherkin
    @FR-6
    Scenario: Progress renews the timeout
      Given a server that emits progress notifications for a long call
      When the client calls the tool with a progress callback
      Then the callback receives the progress and the request outlives a single timeout window
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Tool list change reaches subscribers
      Given a subscribed notifications/tools/list_changed listener
      When the server emits the notification
      Then the listener fires with the notification params
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Stdio server lifecycle
      Given a stdio server command
      When the client connects and later closes
      Then the process group is terminated after stdin close, SIGTERM, and SIGKILL escalation
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Dropped stream resumes
      Given a Streamable HTTP server with a session and event IDs
      When the response stream drops mid-call
      Then the client reconnects the GET stream with Last-Event-ID and completes the pending call
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: In-memory pair delivers both directions
      Given a connected in-memory transport pair
      When the client side sends a JSON-RPC message
      Then the server side receives an equal copy without shared references
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Tool result becomes model content
      Given a CallToolResult with text, an embedded image resource, and an audio block
      When toLlmContent converts it
      Then text and images pass through and the audio block becomes a short text placeholder
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: OAuth sign-in against a protected server
      Given a Streamable HTTP server that answers 401 with protected-resource metadata
      When the client runs discovery, dynamic registration, and the PKCE code flow
      Then subsequent calls carry a valid bearer token and concurrent 401s share one refresh
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Config entry wins over registration
      Given an extension-registered server and an mcp.json entry with the same name
      When the session starts
      Then the mcp.json entry connects and the registered one is reported as overridden
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Colliding tool names stay unique
      Given two tools whose sanitized mcp__server__tool names are identical
      When the server connects
      Then both register under distinct names with a hash suffix and calls still reach the right tool
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Exposure modes route tools correctly
      Given one codemode server, one deferred server, one direct server, and one hidden server
      When the session starts
      Then direct tools are declared immediately, deferred tools load through tool_search, codemode tools resolve through scripts, and hidden tools are unreachable
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: Prompt section lists indirect servers
      Given enabled codemode and deferred servers with descriptions
      When the agent prompt is assembled
      Then the mcp_servers section names each server with its reach mode and one-line summary within the character budget
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Manager disables and re-enables a server
      Given a connected server
      When the user disables it in /mcp and then enables it again
      Then its tools become hidden while disabled and reconnect on enable
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: Model reads a resource through tools
      Given a connected server with resources
      When the model calls list_mcp_resources and then read_mcp_resource with the returned server and URI
      Then the resource contents return as model content with the JSON payload intact
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: First prompt does not hang on a slow direct server
      Given a direct server that never finishes connecting
      When the first prompt starts
      Then prompting proceeds after the startup wait and the tools appear once the server connects
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: Permission hook sees MCP calls
      Given a permission extension that observes tool_call events
      When an MCP tool is invoked
      Then the hook observes the call exactly as it would for a built-in tool
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Dependency surface stays minimal
      Given the published package manifest of @earendil-works/pi-mcp
      When its runtime dependencies are listed
      Then the only entry is cross-spawn with no MCP SDK or pi workspace dependency
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Engine floor is enforced
      Given a Node.js 22.19 runtime
      When the package builds and its tests run
      Then every step passes without engine warnings
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Default timeout applies
      Given a client created without an explicit timeout
      When a request runs past 30 seconds with no progress
      Then the request rejects with a timeout error naming the elapsed budget
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Oversized output spills to disk
      Given a tool result whose text exceeds 20 KiB
      When it is converted for the model
      Then the model sees a truncated middle-cut rendering plus the temp file path holding the full text
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Oversized message is rejected
      Given a transport receiving a JSON-RPC message larger than 16 MiB
      When the frame completes
      Then the message is rejected without being delivered to the client
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Startup problems are reported once
      Given a session start with one broken config entry and one failing server
      When startup completes
      Then the user sees a single warning covering both problems and no repeats
    ```

## Conflicts

None identified yet.

## Open Questions

1. Will any supported server require the legacy HTTP+SSE transport that the client core currently excludes.
2. Will any consumer need the client to act as an MCP server (sampling) rather than only calling tools and reading resources.

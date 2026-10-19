---
title: "Agent Applets"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Agent Applets

## Overview

Today the agent can only return text to the user, so any interactive interface it produces is described in prose and the user has to translate it into action.
Agent applets let a provider describe native UI declaratively instead.
A provider (the agent itself, an MCP server, a local process, or native desktop code) emits a validated tree of closed-set native components, the host renders that tree and owns layout, theme and input, and the host sends user intents back to the provider as actions.
No provider code runs in the host process, so an applet cannot compromise the app.
This feature documents already-implemented functionality that was reverse-engineered from the existing codebase during an SDLC sync.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Agent authors | A way to show interactive native UI instead of printing instructions |
| Desktop users | Rich, themed, interactive surfaces that live in the workspace rather than in the transcript |
| Desktop app team | A rendering surface that keeps providers outside the host process |
| MCP server authors | A way to ship UI alongside a tool result, without a custom client |
| Maintainer | A versioned schema that stays compatible as node types are added |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall define a versioned applet wire schema (`jcode.applet/1`) whose view is a tree drawn from a closed set of native node types, so a provider describes UI without shipping code to the host. |
| FR-2 | Must | The system shall validate every document against the schema, the structural limits, and the capabilities the applet declares before the document is stored or rendered. |
| FR-3 | Must | The system shall expose an `applet` tool to the agent with `mount`, `update`, `patch`, `move`, `close` and `list` actions. |
| FR-4 | Must | The system shall mount an instance under a generated session-local identifier when the agent does not supply one. |
| FR-5 | Must | The system shall persist mounted instances per session, one file per session under the jcode home directory, and remove the file when the last instance in the session is closed. |
| FR-6 | Must | The system shall apply incremental updates as revision-checked patch operations restricted to the `/view`, `/state` and `/title` paths, and shall reject a patch as a whole when its result does not validate. |
| FR-7 | Must | The system shall move a mounted instance to a different placement and bump the instance's document revision. |
| FR-8 | Must | The system shall close an instance, remove it from the session snapshot, and report whether the instance existed. |
| FR-9 | Must | The system shall stream the complete set of mounted instances for a session to connected clients as a full-snapshot event on every change. |
| FR-10 | Must | The system shall route a user intent back to the agent as a compact action message carrying the action name, the action arguments, the instance's current state, and the key of the node that emitted it. |
| FR-11 | Must | The system shall let the agent block on an applet tool call until a user action arrives on that instance, with a bounded wait. |
| FR-12 | Must | The system shall store host-supplied user state into an instance without changing the instance's document revision. |
| FR-13 | Should | The system shall support the standalone panel, sidebar, overlay, composer strip, background and inline placements, with inline anchored to a tool call, a message, or the end of the conversation. |
| FR-14 | Should | The system shall render MCP-UI resources returned by an MCP tool as mounted applets anchored to the tool call that produced them. |
| FR-15 | May | The system shall render sandboxed HTML inside an applet, gated by the `html` capability. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | No provider code shall run in the host process. The host renders a declarative tree and executes only its own built-in host actions. |
| NFR-2 | Must | Compatibility | The host shall accept node types it does not know, render their fallback text, and round-trip them losslessly, so a provider built against a newer host still works on an older host. |
| NFR-3 | Must | Resource | The number of mounted instances per session shall be bounded at 64, and every document shall be bounded by structural limits on depth, node count, text size, asset size, asset count, table cells, HTML size and state size. |
| NFR-4 | Must | Security | Host actions and image sources shall be rejected unless the applet declares the matching capability, and `host.open_url` shall accept only `http`, `https` and `mailto` URLs. |
| NFR-5 | Should | Availability | A failed mount, patch, move or state write shall leave the persisted session state unchanged. |
| NFR-6 | Should | Performance | A published change shall carry a full snapshot rather than a delta, so a client never has to apply incremental updates, and the snapshot stays bounded by the per-session instance limit. |
| NFR-7 | Should | Isolation | The `applet` tool shall not be advertised or executable by terminal, headless, batch or codemode clients. |

## Constraints

- The applet schema is versioned as `jcode.applet/1`; the version suffix changes only for breaking changes, and additive changes such as new node types keep the same version.
- Placement is independent of tool calls; a tool call is one possible anchor for an inline placement.
- The host owns layout, theme, focus and scrolling; providers describe intent using spacing tokens rather than raw pixel values.
- The `applet` tool is registered only when the client advertises the desktop inline response renderer capability.
- Session state lives in `~/.jcode/agent_applets/`, one file per session named after the session id with a `.json` suffix; the session id may not be empty, contain a path separator, or start with a dot.
- Instance ids are 1 to 64 characters drawn from `[A-Za-z0-9-_.]`.
- Agent-mounted instances use the applet id `jcode.agent` and a session-scoped visibility scope.
- The agent applet manifest declares the `open_url`, `clipboard`, `send_prompt`, `start_chat` and `html` capabilities, and does not declare `read_files` or `remote_images`.

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
    Scenario: A provider describes UI as a validated native node tree
      Given an applet document whose view is a stack of text and button nodes
      When the document is deserialized and validated
      Then the view is accepted as a tree of known native node types
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: An invalid document is rejected before it is stored
      Given a mount request whose view references an image asset that was never declared
      When the host validates the document
      Then the mount fails with an unknown asset error
      And the session snapshot still holds the instances that were mounted before
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: The agent drives applets through one tool
      Given the applet tool is registered for a desktop-capable session
      When the agent calls the tool with action mount, patch, move, list and close in turn
      Then each action is accepted and reports the resulting instance and revision
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A mount without an instance id gets a generated one
      Given the agent mounts an applet titled "Sales Chart!" without naming an instance
      When the host stores the instance
      Then the instance id is a slug of the title followed by four hex digits
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Mounted instances survive a reload and the file disappears when empty
      Given a session with two mounted applets
      When the session snapshot is read from the applet state file and the last applet is closed
      Then the file for the session no longer exists
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A patch updates the document and a stale or invalid patch is refused
      Given a mounted applet at revision 1
      When a patch replaces the title at base revision 1
      Then the title changes and the revision becomes 2
      When the same patch is applied at base revision 1 again
      Then the patch is refused with a revision mismatch
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Moving an instance changes its placement
      Given a mounted applet placed inline in the transcript
      When the agent moves it to the sidebar
      Then the instance placement becomes sidebar
      And the document revision increases by one
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Closing removes the instance and reports whether it existed
      Given a mounted applet
      When the agent closes it
      Then the tool reports that the applet was closed
      And the session snapshot no longer contains the instance
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Clients receive the whole snapshot on every change
      Given a connected client attached to a session
      When an applet is mounted, patched and then closed
      Then the client receives one applet state event per change
      And each event carries the complete set of instances for the session
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A user intent reaches the agent as a compact action message
      Given a mounted applet with bound state
      When the user presses a control that emits a custom action
      Then the agent receives one message naming the instance, the action and the arguments
      And the message carries the instance's current state
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: A waiting mount returns the user action
      Given the agent mounts an applet with wait enabled
      When the user acts on the applet before the wait ends
      Then the tool call returns the action message
      And the agent is not woken separately
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: A user state write does not change the revision
      Given a mounted applet at revision 3
      When the host stores new user state on the instance
      Then the state is updated
      And the document revision stays at 3
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Every documented placement is expressible
      Given the placement shorthands inline, end, panel, sidebar, overlay and composer
      When each is resolved for a session
      Then the resolved placements match the panel, sidebar, overlay, composer and inline forms
      And an inline placement defaults to anchoring at the calling tool call
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: An MCP UI resource becomes a mounted applet
      Given an MCP tool result carrying a ui:// resource with HTML content
      When the tool result is processed
      Then an applet is mounted inline at the tool call and the tool output says the UI was rendered
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: HTML rendering requires the html capability
      Given a document whose view contains an html node
      When the document is validated for an applet that does not declare the html capability
      Then validation fails with a missing capability error
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The host runs no provider code
      Given an applet whose view contains only declarative nodes and host actions
      When the host renders and stores the document
      Then the host loads no provider binary and evaluates no provider script
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: An unknown node type degrades and round-trips
      Given a document containing a node type the host does not know, with fallback text
      When the document is deserialized, validated and re-serialized
      Then the node is kept as an unknown node with its fallback and its original fields
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Documents and instance counts are bounded
      Given a session that already holds the maximum number of instances
      When the agent mounts one more instance
      Then the mount is refused with a message naming the maximum
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Capabilities gate host actions and image sources
      Given a document with a host.open_url action
      When the document is validated for an applet without the open_url capability
      Then validation fails with a missing capability error
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: A failed write leaves the stored state untouched
      Given a mounted applet
      When a patch that would produce an invalid document is applied
      Then the patch is refused
      And the stored document is unchanged
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Clients never apply deltas
      Given a session with one mounted applet
      When the applet is patched
      Then the event delivered to clients carries the full instance set
      And it carries the new revision of the patched instance
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Headless clients cannot run applets
      Given a client that does not advertise the desktop inline response renderer capability
      When the tool list is built for that client
      Then the applet tool is absent from the list
      And calling it by name fails
    ```

## Conflicts

<!-- Identified and populated by /review-requirements: pairs or groups of requirements that cannot all be satisfied at once. Reconcile before approval, or promote to an open question. -->

None identified yet.

## Open Questions

1. Should adding node types bump the schema to `jcode.applet/2`, or do additive node types keep version 1 forever, as the wire type documentation currently states?
2. The agent applet manifest grants the `html` capability to every agent-mounted applet by default; should sandboxed HTML require an explicit user approval instead?
3. A waiting `applet` call can hold a tool call open for up to one hour; should that ceiling be lowered now that the agent is woken by later action messages anyway?

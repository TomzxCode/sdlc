---
title: "Canvas Dynamic UI"
status: done
---

# Requirements: Canvas Dynamic UI

## Overview

Agents need a visual surface beyond plain chat text for presenting interactive widgets and dynamic interfaces.
The Canvas dynamic UI feature gives agents two presentation paths: hosted widget documents shown on a paired macOS panel through the Canvas plugin, and A2UI JSONL interfaces rendered as dashboard widgets in the Control UI.
The Control UI hosting surface itself (iframe lease, URL resolution, sandboxing) belongs to FEAT-p8; this feature covers the agent-driven content model and the plugin that produces and presents it.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | See agent-built widgets and dynamic interfaces rendered visually instead of as raw text |
| Agent authors | A single tool path (`canvas`, `show_widget`) to present visual content on a panel or dashboard |
| macOS app operators | A predictable present/navigate/hide panel surface driven only by eligible paired nodes |
| Gateway operators | Hosted widget routes that stay auth-gated, sandboxed, and cheap to serve |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a `canvas` agent tool with `present`, `hide`, and `navigate` actions targeting a paired node panel |
| FR-2 | Must | The system shall resolve the target panel only to a connected macOS node advertising `canvas.present`, rejecting anything else with an actionable error |
| FR-3 | Must | The system shall expose `openclaw nodes canvas present`, `hide`, and `navigate` CLI commands with the same panel semantics as the agent tool |
| FR-4 | Must | The system shall register a `node_panel` widget presenter so `show_widget` can present a hosted document on the selected Mac panel |
| FR-5 | Must | The system shall validate agent-authored A2UI JSONL source, accepting exactly one action key per message, one dialect per file (v0.8 unversioned or v0.9 versioned), and rejecting mixed or malformed input |
| FR-6 | Must | The system shall compose an A2UI board widget document from validated source, embedding the boot messages and loading the matching versioned renderer bundle |
| FR-7 | Must | The system shall serve A2UI renderer assets under `/__openclaw__/a2ui/` and hosted widget documents under `/__openclaw__/canvas/`, gated by the host enablement switch |
| FR-8 | Must | The system shall gate all Canvas hosting behind `plugins.entries.canvas.config.host.enabled` (default on) with an `OPENCLAW_SKIP_CANVAS_HOST` escape hatch |
| FR-9 | Should | The system shall repair retired `canvasHost` file-host settings and migrate custom-root widget documents into core storage via `openclaw doctor --fix` |
| FR-10 | Should | The system shall render Canvas and A2UI content in the Control UI through scoped capability URLs with sandboxed iframes, reusing the FEAT-p8 hosting surface |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall keep widget content untrusted by serving it from an opaque-origin sandboxed frame and rejecting path traversal on hosted routes |
| NFR-2 | Must | Reliability | The system shall make node invocations idempotent and keep document migration atomic so interrupted copies stay invisible |
| NFR-3 | Should | Performance | The system shall load Canvas tool, CLI, and A2UI renderer implementations lazily so idle Gateways pay no startup cost |

## Constraints

- The macOS panel is render-only; host-integrated widget actions live in Control UI chat and session dashboards, not in the panel.
- A2UI widgets render on session dashboards; the macOS panel does not accept A2UI push/reset commands.
- The plugin boundary holds: Canvas imports only `openclaw/plugin-sdk/*` and its own local barrels, never core internals.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Agent presents a widget on the panel
      Given a connected macOS node advertising canvas.present
      When the agent calls the canvas tool with action present and a target URL
      Then the node receives canvas.present with that URL and the tool returns ok with the node id
    ```

    ```gherkin
    @FR-1
    Scenario: Agent hides and navigates the panel
      Given a connected macOS node advertising canvas.present
      When the agent calls the canvas tool with action hide or navigate with a URL
      Then the node receives canvas.hide or canvas.navigate and the tool returns ok
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Non-macOS node is rejected
      Given only a connected Linux node is available
      When the agent calls the canvas tool with action present
      Then the call fails with an error naming the canvas.present eligibility requirement
    ```

    ```gherkin
    @FR-2
    Scenario: Ambiguous panels require an explicit node
      Given multiple eligible Canvas panels are connected
      When the agent calls the canvas tool without naming a node
      Then the call fails listing the eligible node ids
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Operator drives the panel from the CLI
      Given a paired macOS node
      When the operator runs openclaw nodes canvas present, navigate, or hide with --node
      Then the matching node.invoke command reaches the node and reports success
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Widget is shown on the node panel
      Given a connected canvas-capable Mac and a hosted widget document
      When show_widget targets node_panel
      Then the presenter navigates the selected node to the hosted URL and returns the node id
    ```

    ```gherkin
    @FR-4
    Scenario: No eligible node keeps chat working
      Given no connected canvas-capable device
      When show_widget targets node_panel
      Then availability reports no_eligible_node and the widget still appears inline in chat
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Valid v0.9 A2UI source passes
      Given a JSONL file with one v0.9 action key per line and version v0.9 on each message
      When the board widget kind validates the source
      Then validation succeeds and reports version v0.9 with the message count
    ```

    ```gherkin
    @FR-5
    Scenario: Mixed dialects are rejected
      Given a JSONL file containing both v0.8 and v0.9 messages
      When the board widget kind validates the source
      Then validation throws naming the mixed-dialect violation
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Document embeds boot state and renderer
      Given validated A2UI source of a known version
      When the board widget kind composes the document
      Then the output contains the serialized boot messages, the host element, and the matching versioned bundle URL
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Renderer bundle is served
      Given the Canvas host is enabled and prebuilt bundles exist
      When the Gateway receives a request under /__openclaw__/a2ui/ for a registered bundle
      Then it responds with the JavaScript bundle and a JavaScript content type
    ```

    ```gherkin
    @FR-7
    Scenario: Disabled host serves nothing
      Given the Canvas host is disabled
      When the Gateway receives a request under /__openclaw__/a2ui/
      Then no Canvas route handles it
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Host defaults to enabled
      Given no explicit canvas host config
      When the plugin entry registers
      Then the widget presenter and hosted routes are registered
    ```

    ```gherkin
    @FR-8
    Scenario: Skip switch disables the host
      Given OPENCLAW_SKIP_CANVAS_HOST is truthy
      When the plugin entry registers
      Then the presenter and hosted routes are not registered while the tool and CLI remain
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Doctor migrates custom-root documents
      Given widget documents under a retired custom host root
      When the operator runs openclaw doctor --fix
      Then the documents move atomically into core canvas/documents storage and the retired setting is removed
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Canvas URL resolves through the scoped surface
      Given a canvas entry path and a current node-scoped plugin surface URL
      When the Control UI resolves the iframe URL
      Then the entry path is rewritten under the scoped capability prefix
    ```

    ```gherkin
    @FR-10
    Scenario: External URLs are never treated as Canvas content
      Given an arbitrary external URL
      When the Control UI checks it as a Canvas entry
      Then it is rejected as an internal Canvas entry URL
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Traversal paths are rejected
      Given a hosted-route request with a path escaping the asset root
      When the file resolver handles it
      Then the request is rejected without reading outside the root
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Retried migration leaves no partial state
      Given a migration interrupted mid-copy
      When doctor reruns the migration
      Then the partial copy is cleaned and the source document remains until a complete copy publishes
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Idle gateway avoids Canvas payloads
      Given a Gateway that never uses Canvas
      When it starts with the Canvas plugin enabled
      Then the tool, CLI, and A2UI renderer modules load only on first use
    ```

## Conflicts

None identified yet.

## Open Questions

1. Should the macOS panel ever accept A2UI push/reset commands, or does the dashboard-only rule for A2UI stand permanently?
2. Is there a retention or quota policy for hosted widget documents in core storage, or do they accumulate until manually removed?
3. Should non-macOS platforms gain panel eligibility, or is the macOS-only gate a durable product decision?

---
title: "Boards, Projects, and Session Cards"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Boards, Projects, and Session Cards

## Overview

An operator running a long session needs to see what the session is doing and steer it without reading raw transcripts.
The boards feature gives every session a dashboard of tabs and widgets that the agent and the operator both edit through a single normalized layout, with widget capabilities held behind an explicit grant so a widget cannot quietly reach the network or the agent's tools.
The projects feature keeps a registry of the repositories a session works in, resolves each path to a real git checkout, clones remotes into managed checkouts, and serializes every write behind a per-checkout lease so two operators cannot corrupt the same working tree.
The session-cards feature records a short progress card per session, either free-form markdown or a list of steps, so the operator can read the current state at a glance.
The bundled Workboard plugin adds a separate card-based board for agent-owned work, with its own SQLite file, its own RPC methods, and its own CLI, and it ships disabled by default.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Session operators | See the state of a session at a glance, in a dashboard, a project list, and a progress card |
| Agent authors | Author dashboard widgets, report blocks, and progress cards through stable tool actions and names |
| Control UI clients | Read and mutate boards, project registries, and progress cards over the Gateway RPC surface |
| Security reviewers | Keep widget content untrusted, capabilities explicitly granted, and writes lease-protected |
| Plugin authors | Reuse the shared Workboard column taxonomy and renderer contract from `@openclaw/workboard-contract` |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall normalize a board layout so that tab positions are dense and zero-based, widget positions are dense and zero-based within their tab, and any invalid input raises `BoardValidationError` with a code of `not_found`, `conflict`, or `invalid_operation` |
| FR-2 | Must | The system shall apply board operations `tab_create`, `tab_update`, `tab_delete`, `tabs_reorder`, `widget_move`, `widget_resize`, and `widget_remove` as one atomic batch, so a rejected operation leaves the stored layout unchanged |
| FR-3 | Must | The system shall lay widgets out on a 12-column grid using the size presets `sm`, `md`, `lg`, `xl`, and `full`, and clamp explicit widget sizes to a width of 1 to 12 and a height of 1 to 20 |
| FR-4 | Must | The system shall validate every declared widget capability so that network origins are exact HTTPS origins without credentials, wildcards, paths, queries, or fragments, declared tools are non-empty, free of control characters, and bounded in count, and the resulting declaration is a subset of the sandbox host's supported connect domains |
| FR-5 | Must | The system shall hold a widget that declares network origins or tools in a `pending` grant state until an operator records a `granted` or `rejected` decision, and shall refuse a grant whose widget revision or instance identifier no longer matches the current widget |
| FR-6 | Must | The system shall accept the native widget kinds `session:report` and `session:website` with schema-validated props, and shall reject a report block carrying HTML, scripts, styles, network reads, or executable actions |
| FR-7 | Must | The system shall expose a `dashboard` agent tool with the actions `read`, `tab_create`, `tab_update`, `tab_delete`, `tabs_reorder`, `widget_put`, `widget_move`, `widget_resize`, `widget_remove`, `focus_tab`, `set_presentation`, and `set_default_presentation` |
| FR-8 | Must | The system shall persist each session's board in the SQLite tables `board_tabs` and `board_widgets`, keyed by session key, with a monotonically increasing snapshot revision and a cascading delete when the owning session node is removed |
| FR-9 | Must | The system shall register a project only after resolving the requested path to a git checkout root that has at least one commit, and shall hold a per-checkout lease for the duration of every registry write |
| FR-10 | Must | The system shall clone a remote repository into a managed project checkout, record the clone in the registry with source `cloned`, and remove the checkout and its registry row together |
| FR-11 | Must | The system shall store one progress card per session as markdown plus an optional list of steps whose status is `pending`, `in_progress`, or `completed`, guard the write with an optional `expectedRevision`, and clear the card when both the markdown and the steps are empty |
| FR-12 | Must | The system shall publish board widget events to the session as `[dashboard]` system-event notices, refusing a payload larger than 8 KiB and dropping an identical payload repeated within 5 seconds |
| FR-13 | Should | The system shall expose the project registry through Gateway RPC only, and shall not ship an `openclaw projects` CLI command |
| FR-14 | Should | The system shall ship the bundled Workboard plugin disabled by default, persisting its boards and cards in its own SQLite file and exposing `workboard.*` RPC methods plus the `openclaw workboard list\|create\|show\|move\|dispatch` CLI |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall treat widget content as untrusted, serving it from a sandboxed frame, and shall require an explicit operator grant before a widget reaches a declared network origin or tool |
| NFR-2 | Must | Reliability | The system shall serialize board writes, project registry writes, and progress card writes so that a failed operation leaves the stored state unchanged and a stale writer cannot overwrite a newer revision |
| NFR-3 | Must | Performance | The system shall bound the work a single board and a single session can hold, capping a board at 48 widgets, the widget JSON props at 8 KiB, and a session at one progress card |
| NFR-4 | Should | Security | The system shall authorize the board widget HTTP route with a signed view ticket rather than with session credentials in the URL |
| NFR-5 | Should | Maintainability | The system shall keep board, project, and progress card state in SQLite with `STRICT` tables and cascading foreign keys, and shall keep the Workboard plugin's state in its own database file rather than in the core schema |

## Constraints

- Boards are per session, not per agent, and a board is addressed by its session key.
- A board holds at most 48 widgets and a widget name is a stable slug that identifies the same widget across updates.
- Widget names, tab identifiers, and plugin kinds are slugs, so they are safe to embed in URLs and file names.
- Plugin widgets are trusted content and may not carry sandbox capability declarations; untrusted HTML and MCP App widgets may.
- A grant narrows but never widens a widget's declaration, and a grant on HTML content is bound to the exact approved bytes.
- The last board tab may not be deleted while it still holds widgets; the widgets move to the first remaining tab instead.
- Projects are either `registered` (an existing local checkout) or `cloned` (a checkout OpenClaw created).
- The Workboard column taxonomy is a shared contract in `@openclaw/workboard-contract`, not a core-owned enumeration.
- The Workboard plugin ships with `enabledByDefault: false` and keeps its database in the plugin state directory.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Normalize a layout with gaps in tab and widget positions
      Given a board layout with tabs at positions 3 and 7 and widgets at positions 0, 4, and 9
      When the layout is normalized
      Then tab positions are 0 and 1 and widget positions are 0, 1, and 2 within their tab
      And the snapshot revision is unchanged
    ```

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Reject an operation naming a tab that does not exist
      Given a board layout with one tab
      When a widget move targets the tab "missing"
      Then a BoardValidationError is raised with code "not_found"
      And the stored layout is unchanged
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Apply a batch where a later operation is invalid
      Given a board layout with one tab and one widget
      When a batch contains a valid tab create followed by a widget resize of an unknown widget
      Then a BoardValidationError is raised with code "not_found"
      And the newly created tab is not present in the stored layout
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Reorder tabs with an incomplete tab list
      Given a board layout with three tabs
      When tabs_reorder is applied with only two tab identifiers
      Then a BoardValidationError is raised with code "invalid_operation"
      And the stored tab order is unchanged
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Place a widget with the md size preset
      Given a board layout with a default tab
      When a widget is placed with size "md"
      Then the widget is stored with sizeW 6 and sizeH 4
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Clamp an explicit widget resize beyond the grid
      Given a board layout with a widget
      When the widget is resized to sizeW 40 and sizeH 40
      Then the widget is stored with sizeW 12 and sizeH 20
      And the widget height mode is "fixed"
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Reject a declared network origin that is not an exact HTTPS origin
      Given a widget declaration with the network origin "https://example.com/path"
      When the declaration is normalized
      Then a BoardValidationError is raised with code "invalid_operation"
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Reject a declared network origin the sandbox host does not support
      Given a widget declaration with the network origin "https://example.com"
      When the declaration is normalized and the sandbox host does not support that origin
      Then a BoardValidationError is raised with code "invalid_operation"
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Hold a declared widget pending until the operator decides
      Given a board widget that declares a tool capability
      When the widget is put on the board
      Then the widget grant state is "pending"
      And no declared capability is active
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Refuse a grant for a stale widget revision
      Given a pending board widget at revision 3
      When a grant is recorded for revision 2
      Then a BoardValidationError is raised with code "conflict"
      And the widget grant state remains "pending"
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Accept a report widget with text and metric blocks
      Given a report widget with a text block and a metrics block
      When the report props are parsed
      Then the parsed report contains both blocks
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Reject a website widget whose URL carries credentials
      Given a website widget with the URL "https://user:pass@example.com"
      When the website props are parsed
      Then a BoardValidationError is raised with code "invalid_operation"
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Read the current board through the dashboard tool
      Given a session with a board holding one tab and two widgets
      When the dashboard tool is called with action "read"
      Then the result reports the session key, the revision, one tab, and two widgets
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Reject an unknown dashboard action
      Given the dashboard tool
      When it is called with action "explode"
      Then the call is rejected as invalid input and names the unknown action
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Persist a board write and bump the snapshot revision
      Given a session board stored at revision 4
      When a widget put is committed for that session
      Then the stored snapshot revision is 5
      And the widget row is present in board_widgets for that session key
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Drop boards when the owning session node is removed
      Given a session node with a board tab and a board widget
      When the session node is deleted
      Then the board tab and the board widget for that session key are gone
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Register a git checkout as a project
      Given a directory that is a git checkout with at least one commit
      When the project is registered
      Then the registry stores the checkout root as the repo root and the source as "registered"
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Reject a path that is not a git checkout
      Given a directory that is not a git checkout
      When the project is registered
      Then a ProjectCheckoutError is raised naming the path
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Serialize two registrations of the same checkout
      Given two concurrent registrations of the same checkout root
      When both are attempted
      Then the checkout lease admits them one at a time and both registry writes settle
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Clone a remote repository into a managed checkout
      Given a remote repository URL that can be cloned
      When the project is cloned
      Then the registry stores the clone with source "cloned" and the origin URL
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Remove a cloned project and its checkout together
      Given a cloned project in the registry
      When the project is removed
      Then the registry row is gone and the managed checkout directory is removed
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Store a progress card with steps
      Given a session with no progress card
      When a progress card with two steps is written
      Then the stored card holds the steps and the markdown
      And the stored revision is 1
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Refuse a progress card write against a stale revision
      Given a progress card stored at revision 3
      When a write with expectedRevision 2 is attempted
      Then the write is refused and the stored card still reports revision 3
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Clear a progress card when both fields are empty
      Given a progress card holding markdown and steps
      When a write with no markdown and no steps is committed
      Then the card is cleared and the revision is incremented
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Publish a widget event as a dashboard notice
      Given a board widget named "deploy"
      When a board event with a small payload is published for that widget
      Then a system event is queued whose text starts with "[dashboard]" and names the widget
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Drop a repeated widget event inside the dedupe window
      Given a board event notice for a widget was just published
      When the same payload is published again within 5 seconds
      Then no second system event is queued
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: List projects over Gateway RPC
      Given a registry holding one workspace project and one registered project
      When the projects.list RPC is called
      Then both projects are returned sorted by display name
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Have no projects CLI command
      Given the openclaw CLI command tree
      When the command list is inspected
      Then no "projects" command is registered
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Ship the Workboard plugin disabled
      Given the bundled Workboard plugin manifest
      When the manifest is read
      Then enabledByDefault is false
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Run a Workboard CLI command against the Gateway
      Given the Workboard plugin is enabled and the Gateway is reachable
      When "openclaw workboard list" runs
      Then the cards of the selected board are printed
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Keep a declared capability inactive before the grant
      Given a board widget declaring the network origin "https://example.com"
      When the widget is stored but not granted
      Then the widget cannot fetch that origin
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Serve the board widget document from a sandboxed origin
      Given a granted HTML board widget
      When the widget document is requested through the board HTTP route
      Then the response carries a content security policy and an opaque sandbox origin
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Keep a failed board write out of the store
      Given a board stored at revision 7
      When a widget put is rejected because the content exceeds the widget budget
      Then the stored board still reports revision 7
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Refuse a board that would exceed the widget budget
      Given a board holding 48 widgets
      When a 49th widget is put on the board
      Then the write is rejected and the board still holds 48 widgets
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Reject widget props above the JSON budget
      Given a plugin widget whose serialized props exceed 8 KiB
      When the widget is put on the board
      Then the write is rejected naming the 8 KiB budget
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Refuse a board widget view without a valid ticket
      Given a board widget document
      When the board HTTP route is requested without a valid view ticket
      Then the request is refused and no widget bytes are returned
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Keep Workboard state in its own database file
      Given the Workboard plugin is enabled
      When a board is created
      Then the board is stored in the plugin's own workboard.sqlite file
      And the core state schema is unchanged
    ```

## Conflicts

None identified yet.

## Open Questions

1. The board snapshot revision is bumped by every mutating operation, so a busy session can churn revisions; there is no compaction policy for a board revision history.
2. The `projects` table has no `agent_id` column, so a registered project is visible to every agent on the Gateway and the registry offers no per-agent scoping yet.
3. The Workboard plugin keeps its own copy of the card taxonomy in its SQLite file, so a change to the shared contract requires a plugin migration rather than a core migration.

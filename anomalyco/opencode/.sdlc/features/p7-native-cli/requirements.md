---
title: "Native Rust CLI"
status: done
session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA
---

# Requirements: Native Rust CLI

## Overview

`opencode-native` is a Rust CLI and TUI that gives OpenCode a second client built against the same server and client-local files as the TypeScript client.
It runs on OpenTUI's Rust crates and talks to the TypeScript `opencode` server over HTTP.
It finds or starts a server, mirrors the TypeScript client's command tree and screens, and supports built-in, Luau and TypeScript plugins through one plugin ABI.
Parity harnesses compare its output, cells, files and requests with the TypeScript client, and recorded deviations document intended differences.
The workspace lives in `packages/cli-rs`, and the binary does not ship yet.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | A native terminal client with the same sessions, commands and screens as the TypeScript client |
| Core team | A second client that stays aligned with the server contract and the TypeScript client's behavior |
| Plugin authors | One ABI for built-in, Luau and TypeScript TUI plugins, with documented limits and lifecycle |
| Contributors | Reproducible builds, generated bindings and parity checks that show when behavior drifts |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide an `opencode-native` binary with a command tree, aliases, flags, help, completions, usage errors and exit codes matching the TypeScript CLI. |
| FR-2 | Must | The system shall provide a full-screen TUI on OpenTUI Rust crates with home, session and plugin routes, panes, dialogs, tabs, keymap, themes and bounded task queues. |
| FR-3 | Must | The system shall resolve a server from `--server`, a standalone private server, a ready registered service, or a started background service, and follow a restarted service's new address or password. |
| FR-4 | Must | The system shall read and write client-local files with the same paths and formats as the TypeScript client, including `cli.json`, TUI storage, prompt history, stash, frecency, model preference, pins and service registrations. |
| FR-5 | Must | The system shall consume the server's HTTP API and event stream, apply events to a local store, and expose change tracking to views. |
| FR-6 | Must | The system shall run built-in Rust plugins, Luau plugins and unmodified TypeScript TUI plugins through plugin ABI 2.0 with one JSON Schema and generated bindings. |
| FR-7 | Must | The system shall serve the Agent Client Protocol over standard input and output against a private server. |
| FR-8 | Must | The system shall generate API bindings, request builders, CLI goldens, keybind names, themes, grammars, plugin schema, Luau stubs and the JS host compatibility layer from TypeScript sources. |
| FR-9 | Should | The system shall provide a `mini` interface in the terminal scrollback and a `serve`, `uninstall` and `plugin` delegation path to the TypeScript binary. |
| FR-10 | Should | The system shall install the pinned OpenTUI native library, checked against a sha256 table, before cargo runs. |
| FR-11 | Should | The system shall bound plugin work with per-frame and per-call limits, VM and process supervision, cancellation on mount close, and a failure path that isolates one plugin. |
| FR-12 | Should | The system shall verify parity with the TypeScript client through oracle, component, in-memory app, file, CLI, pseudo-terminal, simulated TUI and ACP transcript suites. |
| FR-13 | Should | The system shall record every intended behavioral difference in a deviation file and fail a parity comparison that has no deviation file. |
| FR-14 | Must | The system shall pass `cargo fmt`, `cargo clippy`, `cargo test`, `check:drift` and `parity:machines` before a change merges. |
| FR-15 | May | The system shall provide a live script against the elected background service, performance profiles and a Windows pseudoconsole smoke test. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Compatibility | Wire types shall ignore unknown fields, preserve absent versus `null`, and decode values from a newer server without failing. |
| NFR-2 | Must | Security | A plugin shall receive only declared reads and effects, and a project plugin shall run only after the user approves its file digest. |
| NFR-3 | Must | Performance | Network work shall run off the UI thread, every task-to-UI queue shall be bounded, and one plugin shall stay within a 1 ms frame budget. |
| NFR-4 | Should | Portability | The workspace shall build on Linux, macOS and Windows with a pinned Rust toolchain and a pinned OpenTUI release. |

## Constraints

- The Rust workspace is private to the monorepo, with workspace version `0.1.0`, edition 2024 and `publish = false`.
- The client consumes the TypeScript server's HTTP API; it does not implement a server.
- OpenTUI is pinned to one exact crates.io version, and the native library installer checks a sha256 table.
- Third-party crates are declared once in `[workspace.dependencies]`.
- Generated files and parity fixtures are committed, and `check:drift` fails when they are stale.
- OpenTUI handles are not `Send`, so network work goes through the app runtime and the UI thread owns widgets.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: The Rust command tree matches the TypeScript tree
      Given the generated command tree and output goldens
      When the CLI parses an invocation or prints help, completions or a usage error
      Then the command path, output and exit code match the TypeScript CLI fixtures
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: The TUI renders a session
      Given a mounted Rust TUI and a store fixture with one session
      When the store publishes a change batch
      Then only the named widgets update and the rendered cells match the TypeScript TUI within documented deviations
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: The client follows a restarted service
      Given a registered service with a known port and password
      When a request fails to connect or returns 401 after a restart
      Then the client discovers the new registration and sends the request once to it
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Both clients share local files
      Given the TypeScript client wrote `cli.json` with comments and TUI storage with extra fields
      When the native client reads and updates those files
      Then the TypeScript client reads the values and the comments and extra fields survive
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: The store applies an event batch
      Given an event stream that starts with `server.connected`
      When a batch of session deltas arrives
      Then the store records one flush, views receive the change union, and a full batch queue triggers resynchronization
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A plugin runs on each carrier
      Given the same plugin registered as a linked Rust plugin, a Luau directory and a TypeScript TUI module
      When each carrier registers a command and draws a slot tree
      Then the host applies the same command and slot behavior through ABI 2.0 messages
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: An ACP client opens a session
      Given a private server started for ACP
      When a JSON-RPC client exchanges initialize, session and prompt messages over standard input and output
      Then the transcript matches the TypeScript ACP agent transcript after normalization
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Generated bindings stay current
      Given the TypeScript API definition and TUI sources
      When `bun run generate` completes
      Then the committed Rust types, methods, goldens and plugin schema match their sources and `check:drift` passes
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Mini and delegated commands run
      Given a project directory and a server URL
      When the user runs `mini` or a delegated `serve`, `uninstall` or `plugin` command
      Then the interface or TypeScript binary runs with the same arguments, streams and exit code as the TypeScript client
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Cargo runs with the pinned native library
      Given a clean worktree and one pinned OpenTUI version
      When `bun run cargo` starts
      Then the installer verifies the release archive against its sha256 table and cargo finds the library through `.cargo/config.toml`
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: One plugin fails without stopping the client
      Given a Luau plugin that exceeds its CPU limit and a healthy plugin
      When the host calls the failing plugin's handler
      Then the failing plugin is disabled with a toast and the healthy plugin keeps its registrations
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Parity suites compare both clients
      Given a recorded scenario with cells and request logs
      When the TypeScript and Rust sides run the scenario with the same input
      Then screens, writes, reads, stdout, stderr and exit codes match within masks and recorded deviations
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: An undocumented difference fails
      Given two screens that differ in one cell
      When no deviation file names the difference
      Then the parity run fails and reports the differing cell
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: The merge checks pass
      Given a change to any crate under `packages/cli-rs`
      When the package checks run
      Then format, clippy, tests, drift and plugin machine checks all pass
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: A developer runs against the live service
      Given an elected background service and its private password
      When `script/live.sh` starts the debug binary
      Then the client uses the service URL and the `dev` storage channel
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: A newer server adds fields
      Given a response with a new field, a null optional field and an absent optional field
      When the generated Rust type decodes it
      Then the new field is ignored and the null and absent fields stay distinct
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A project plugin needs approval
      Given an unapproved plugin directory inside a project
      When the TUI loads plugins
      Then the plugin claims nothing and the approval dialog shows the directory and its file digest
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Fast store flushes do not flood the UI
      Given a store that publishes batches faster than frames render
      When the pump forwards changes
      Then at most one wake is pending and each queue between a task and the UI stays bounded
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: The workspace compiles for another target
      Given the pinned toolchain and OpenTUI release
      When `check-windows.sh` or `check-target.sh` runs
      Then the workspace compiles for the named target without linking or running it
    ```

## Conflicts

None identified yet.

## Open Questions

1. When and how will `opencode-native` ship, given its README states that the binary does not ship yet, and which release workflow and distribution channels will own it?
2. No dedicated GitHub workflow for this package was found in this checkout; should its checks gain one, or stay on the package-local scripts?
3. Will third-party native plugin libraries return as supervised helper processes, and on what timeline?
4. Which recorded parity deviations must be retired before the binary ships?
5. How will the manual Windows terminal checklist be gathered and recorded for a release?

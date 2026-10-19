---
title: "Internal Event Hooks"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Internal Event Hooks

## Overview

Internal event hooks let the operator extend the assistant with small handlers that run inside the Gateway process when OpenClaw emits an event. A hook is a directory containing a `HOOK.md` descriptor and a handler module; the descriptor's `metadata.openclaw` frontmatter declares the event keys the handler subscribes to, the export name to call, the runtime requirements it needs, and the optional config key used to enable it. The system discovers hooks from five roots (bundled, plugin, managed, operator extra directories, and the agent workspace), merges them by hook name under a source precedence, filters them through an enablement policy and a runtime eligibility check, and registers the surviving handlers against the internal event dispatcher. A bundled hook pack (`boot-md`, `bootstrap-extra-files`, `command-logger`, `compaction-notifier`, `session-memory`) ships with OpenClaw so most operators never author a handler. Hook packs can be installed and updated through the unified plugin installer, which records install provenance in shared SQLite state and enables the installed hook names in config. The `openclaw hooks` command reports the discovered inventory, shows why a hook is not eligible, and toggles per-hook enablement in local config. A built-in Gmail watcher turns inbound mail into assistant work by provisioning and supervising the `gog` watch and serve processes.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Enable, inspect, and disable hooks without editing config by hand; know why a hook is not eligible |
| Hook author | A documented `HOOK.md` contract, a predictable event catalog, and a stable handler signature |
| Gateway runtime | Load hook code safely, keep a failing hook from breaking the operation that triggered it |
| Plugin author | Contribute hook directories that participate in the same discovery and event system |
| Privacy-sensitive user | Know which hooks run in-process, what they record, and that per-hook enablement is global |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall discover hook descriptors from `HOOK.md` files found in the bundled, plugin, managed, operator extra-directory, and agent workspace hook roots, and shall merge the discovered entries by hook name |
| FR-2 | Must | The system shall resolve source precedence so that managed hooks override bundled and plugin hooks, and so that workspace hooks can add new names but cannot replace bundled, plugin, or managed hook code |
| FR-3 | Must | The system shall read the `HOOK.md` `metadata.openclaw` frontmatter contract, including `events`, `export`, `hookKey`, `emoji`, `homepage`, `os`, `requires`, `always`, and `install`, and shall refuse to load a hook that declares no events |
| FR-4 | Must | The system shall load the first supported handler file present in the hook directory among `handler.ts`, `handler.js`, `index.ts`, and `index.js`, and shall resolve the declared export as a callable handler |
| FR-5 | Must | The system shall apply the enablement policy from `hooks.internal.enabled` and `hooks.internal.entries.<hookKey>.enabled`, shall keep workspace hooks disabled until they are explicitly enabled, and shall treat plugin-sourced hooks as enabled |
| FR-6 | Must | The system shall evaluate runtime eligibility from the hook metadata, covering the allowed OS list, required binaries, at-least-one binary alternatives, required environment variables satisfied by the process environment or the per-hook `env` map, and required config paths |
| FR-7 | Must | The system shall dispatch an internal event to family subscribers before exact-action subscribers, in registration order within each group, and shall catch and log a handler error so that later handlers still run |
| FR-8 | Must | The system shall support the `command`, `session`, `agent`, `gateway`, and `message` event families and the documented exact event keys, and shall warn without failing when a hook subscribes to an event key that core does not emit |
| FR-9 | Must | The system shall prepare a replacement hook generation before publishing it, so that a failed reload leaves the previously committed handlers active and later events use the new selection |
| FR-10 | Must | The system shall expose `openclaw hooks list`, `openclaw hooks info <name>`, and `openclaw hooks check` to report the discovered hook inventory, and shall expose `openclaw hooks enable <name>` and `openclaw hooks disable <name>` to write `hooks.internal.entries.<hookKey>.enabled` in local config |
| FR-11 | Must | The system shall refuse to enable or disable a plugin-managed hook through the hooks CLI, shall refuse to enable a hook whose runtime requirements are unmet, and shall reject an ambiguous hook selector without writing config |
| FR-12 | Should | The system shall ship the bundled hook pack set `boot-md`, `bootstrap-extra-files`, `command-logger`, `compaction-notifier`, and `session-memory` in the bundled hooks directory so they are discovered without any operator setup |
| FR-13 | Should | The system shall install and update hook packs through the unified plugin installer, shall record the install provenance and the declared hook names in shared SQLite state under the `hooks.internal.installs` state key, and shall enable the installed hook names in `hooks.internal.entries` |
| FR-14 | Should | The system shall provide a built-in Gmail watcher that resolves the Gmail runtime config from `hooks.gmail` plus `hooks.token`, starts and supervises the `gog gmail watch` and `gog gmail watch serve` processes, and renews the watch on the Gateway scheduler |
| FR-15 | May | The system shall expose the native harness hook relay through the hidden `openclaw hooks relay` verb and the `nativeHook.invoke` Gateway RPC method, with a bounded deadline and a bounded stdin payload |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall read hook metadata and handler files through the boundary file reader, shall cap metadata reads at 1 MiB, and shall reject handler and package paths that resolve outside their hook directory or package root |
| NFR-2 | Must | Reliability | The system shall bound the fire-and-forget dispatch path at 16 concurrent jobs and 256 queued jobs, shall log a timeout after 2000 ms without cancelling the hook, and shall never let a hook failure reject the operation that triggered it |
| NFR-3 | Must | Availability | The system shall restart the Gmail serve process after an unexpected exit, shall bound address-in-use retries at 3 attempts with backoff, and shall terminate the watcher process tree on stop |
| NFR-4 | Should | Performance | The system shall answer the hooks status report within the 1500 ms Gateway RPC timeout that the CLI uses for `hooks list`, `hooks info`, and `hooks check` |
| NFR-5 | Should | Security | The system shall redact the Gmail token arguments from the logged watch serve command line |
| NFR-6 | Should | Observability | The system shall report hook failures as a bounded single-line log message that carries the hook label and a sanitized error text |

## Constraints

- Internal event hooks run as trusted code in the Gateway process, with the process filesystem, network, and environment access.
- Hook handlers are awaited inside the dispatch loop; there is no general handler timeout, cancellation signal, durable event queue, automatic retry, or exactly-once guarantee.
- `event.messages` is delivered as a chat reply only on the replyable producers; every other core event ignores it.
- Hook files and metadata are not watched; a hook code or descriptor change requires a Gateway restart.
- The per-hook config entry is global; `--agent` selects the inspected workspace, not a per-agent registry.
- A hook pack is installed and updated through the unified plugin installer; `openclaw hooks install` and `openclaw hooks update` are deprecated aliases that forward to it.
- The `hooks.internal` config block owns directory hooks; the separate `hooks.enabled`, `hooks.path`, `hooks.token`, and `hooks.mappings` keys own the HTTP webhook ingress surface.

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
    Scenario: Discover hooks across every hook root
      Given a bundled hook directory, a managed hook directory, and a workspace hook directory
      And each contains a HOOK.md descriptor and a handler module
      When the Gateway prepares the internal hook generation
      Then the discovered entry set contains the hook from every root
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: A managed hook overrides a bundled hook of the same name
      Given a bundled hook named "shared-name"
      And a managed hook named "shared-name"
      When the discovered entries are resolved by name
      Then the managed hook is kept
      And the bundled hook is dropped
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: A workspace hook cannot override a managed hook
      Given a managed hook named "shared-name"
      And a workspace hook named "shared-name"
      When the discovered entries are resolved by name
      Then the managed hook is kept
      And the ignored workspace hook is reported as a collision warning
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: A hook without declared events is not loadable
      Given a hook whose HOOK.md declares no events under metadata.openclaw
      When the hook is prepared
      Then the hook is not loadable
      And the blocked reason is "no events defined"
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: The first supported handler file wins
      Given a hook directory that contains both handler.js and index.js
      When the handler path is resolved
      Then handler.js is selected
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A workspace hook stays disabled until it is explicitly enabled
      Given a hook discovered in the agent workspace hooks directory
      And no hooks.internal.entries entry for that hook
      When the enablement policy is resolved
      Then the hook is disabled with the reason "workspace hook (disabled by default)"
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A required binary that is not on PATH blocks the hook
      Given a hook whose metadata requires the binary "definitely-not-installed"
      When the eligibility check runs
      Then the hook reports missing requirements
      And the hook is not loadable
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: A throwing handler does not stop later handlers
      Given two handlers subscribed to the same exact event key
      And the first handler throws
      When the event is dispatched
      Then the second handler still runs
      And the failure is logged as a hook error
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: An unknown event key warns but still loads
      Given a hook subscribed to the event key "command:nwe"
      When the hook is loaded
      Then the load succeeds
      And a warning names the event key as not emitted by OpenClaw core
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A failed reload keeps the previously committed handlers
      Given a committed hook generation serving the event "command:new"
      And a replacement generation whose handler fails to import
      When the replacement is prepared and committed
      Then the previously committed handler still serves the event
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Enabling a hook writes the per-hook config entry
      Given a discovered hook named "command-logger"
      When the operator runs "openclaw hooks enable command-logger"
      Then local config contains hooks.internal.entries["command-logger"].enabled set to true
      And hooks.internal.enabled is set to true
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: A plugin-managed hook cannot be toggled
      Given a hook reported as managed by a plugin
      When the operator runs "openclaw hooks enable" for that hook
      Then the command fails
      And local config is unchanged
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: The bundled hook pack set is discovered out of the box
      Given a Gateway with the default bundled hooks directory
      When the hook inventory is reported
      Then the report lists boot-md, bootstrap-extra-files, command-logger, compaction-notifier, and session-memory
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Installing a hook pack records provenance and enables the hook
      Given a local hook pack whose package manifest declares one hook
      When the pack is installed through the unified plugin installer
      Then the hook install record is written under the "hooks.internal.installs" state key
      And local config contains hooks.internal.entries for the declared hook set to true
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: The Gmail watcher starts only when it is fully configured
      Given hooks.enabled is true and hooks.gmail.account is set
      And the "gog" binary is not installed
      When the Gateway starts the Gmail watcher
      Then the watcher reports that it did not start because the gog binary was not found
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: The native relay rejects oversized stdin
      Given a native hook relay invocation with more than 1 MiB of stdin payload
      When the relay runs
      Then it fails without contacting the Gateway
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: A handler that escapes its hook directory is rejected
      Given a package whose declared hook path resolves outside the package root
      When the hook directory is discovered
      Then the out-of-package path is ignored with a warning
      And no handler is loaded from it
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A saturated fire-and-forget queue drops work instead of growing
      Given the fire-and-forget dispatch queue is at its bound
      When another fire-and-forget hook is submitted
      Then the job is dropped
      And the drop is logged
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: The Gmail serve process is restarted after an unexpected exit
      Given a running Gmail watcher
      When the serve process exits with a nonzero code
      Then a replacement serve process is started after the restart delay
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: The hooks status report answers within the CLI timeout
      Given a Gateway that can serve the hooks status report
      When the CLI requests the report with its 1500 ms timeout
      Then the report is returned before the timeout expires
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The logged watch serve arguments omit the token
      Given a resolved Gmail runtime config
      When the watch serve log arguments are built
      Then the token argument and its value are absent from the logged arguments
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: A hook failure is logged as one bounded line
      Given a hook whose handler throws a multi-line error
      When the failure is logged
      Then the log entry is a single line
      And the log entry is at most 500 characters
    ```

## Conflicts

- **FR-14 versus the HTTP webhook boundary.** `startGmailWatcher` refuses to start unless `hooks.enabled` is true, and `hooks.enabled` is the HTTP webhook ingress master switch that also requires `hooks.token`. The Gmail watcher therefore cannot run on a Gateway that serves only directory hooks, and enabling an internal hook through `openclaw hooks enable` does not satisfy it, because that command writes `hooks.internal.enabled` and not `hooks.enabled`. The requirement stands as written because it matches the shipped behavior; the tension is resolved by treating the Gmail watcher as an HTTP-ingress dependent integration rather than a directory hook.
- **NFR-2 versus the awaited dispatch contract.** NFR-2 bounds the fire-and-forget dispatch path, but the awaited internal hook dispatch loop has no handler timeout, no cancellation signal, and no queue bound. The two paths are separate, so both statements hold, and a handler running inside the awaited loop is not covered by the NFR-2 bounds.

## Open Questions

1. Should the deprecated `openclaw hooks install` and `openclaw hooks update` aliases be removed now that the unified plugin installer owns hook pack installation?
2. Should `hooks internal.entries` gain a per-agent scope so that the global entry no longer applies wherever a hook key is discovered?
3. Should the internal event dispatcher gain a bounded per-handler timeout, given that the current contract has no handler timeout and a handler that never settles can delay Gateway shutdown?

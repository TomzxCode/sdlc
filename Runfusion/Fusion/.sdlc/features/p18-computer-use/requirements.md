---
title: "Computer Use: Desktop GUI Automation"
status: done
---

# Requirements: Computer Use: Desktop GUI Automation

## Overview

`fn computer` lets an agent inspect and operate local desktop application windows through a strict snapshot, act, snapshot loop.
The CLI captures the accessibility tree of a window, persists it as a snapshot, performs one deliberate action bound to that snapshot, and then requires a fresh capture before the next action.
Every element action is fenced by a snapshot, so an agent cannot act on a window state it never observed.
The surface is macOS-only today and returns an explicit unsupported-platform error elsewhere.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Solo developer | Drives a desktop application from an agent session without clicking through the GUI by hand |
| Agent author | Needs one command surface with a stable JSON contract so an agent can read the window state and act on it safely |
| Operator / power user | Needs the automation to fail closed when a window changed, so a stale plan cannot damage the machine |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall expose `fn computer` with the twelve subcommands `capabilities`, `permissions`, `list-apps`, `list-windows`, `get-app-state`, `click`, `set-value`, `type-text`, `press-key`, `hotkey`, `scroll`, and `drag` |
| FR-2 | Must | The system shall capture the accessibility tree of a target app window in `get-app-state` and persist a snapshot record under the resolved project root before returning its snapshot id |
| FR-3 | Must | The system shall resolve every element-bound action through a snapshot record, and shall refuse the action with `SNAPSHOT_REQUIRED` when the target app has no snapshot |
| FR-4 | Must | The system shall consume the app's latest snapshot pointer after a successful action, so the next element action fails with `SNAPSHOT_STALE` and reason `consumed-by-action` until a new capture re-arms the pointer |
| FR-5 | Must | The system shall re-resolve the recorded window and replay the recorded accessibility locator before an action, and shall fail with `ELEMENT_UNRESOLVABLE` when the path no longer resolves or the role, subrole, or identifier no longer match |
| FR-6 | Must | The system shall refuse an unusable snapshot and report exactly one reason from the fixed set `not-found`, `superseded`, `expired`, `pid-changed`, `window-mismatch`, `window-gone`, `consumed-by-action` |
| FR-7 | Must | The system shall store element indexes as a sparse map keyed by the index emitted during capture, and shall fail with `ELEMENT_INDEX_NOT_FOUND` when the requested index is absent from that map |
| FR-8 | Must | The system shall resolve an app target as an exact bundle id, then an exact unambiguous app name, then a `pid:` prefix with the numeric process id, and shall fail with `APP_NOT_FOUND` or `AMBIGUOUS_APP` |
| FR-9 | Must | The system shall report Accessibility and Screen Recording permission state as `granted`, `denied`, or `unknown` from non-mutating preflights, and shall never report a grant it did not probe |
| FR-10 | Must | The system shall report `supported: false` from `capabilities` and `permissions` on a platform other than macOS, and shall fail every other subcommand there with `UNSUPPORTED_PLATFORM` |
| FR-11 | Must | The system shall emit one envelope per invocation carrying `schemaVersion` 1, `ok`, `command`, and either `result` or `error`, and shall exit 0 on success and 1 on failure |
| FR-12 | Must | The system shall read a value from stdin when `--value-stdin` or `--text-stdin` is used, and shall not place that value in process arguments |
| FR-13 | Should | The system shall capture the selected window as a screenshot stored under the project root and report the file path, and shall report a screenshot failure as `screenshotError` without discarding the captured accessibility tree |
| FR-14 | Should | The system shall select a window with `--window-id` or `--window-index`, refuse both together, and restore a minimized window when `--restore-window` is passed to `get-app-state` |
| FR-15 | Should | The system shall support a coordinate drag form and an element drag form as mutually exclusive forms, and shall support targetless `type-text`, `press-key`, and `scroll` that act on the focused element of the target app |
| FR-16 | Should | The system shall render the full command guide from the binary through `fn skills get computer-use`, and the shipped `computer-use` discovery skill shall carry no static command or flag list |
| FR-17 | Should | The system shall report capabilities as the platform, the adapter id, the supported flag, the action inventory split into supported and unsupported actions, and the feature flags for screenshot, restore-window, stdin secrets, and cross-invocation snapshots |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Safety | The system shall never act on an element it did not observe, so every element action re-resolves the window and the locator and verifies identity before the operating-system call |
| NFR-2 | Must | Security | The system shall keep a secret value out of process arguments, out of the snapshot record the command writes, out of error messages, and out of the JSON envelope |
| NFR-3 | Must | Security | The system shall keep the operating-system automation program static, and shall pass untrusted app names, window ids, and locator paths as arguments or stdin instead of interpolating them into the program source |
| NFR-4 | Must | Portability | The system shall run on macOS only, using the operating-system `osascript` and `screencapture` built-ins, with no downloaded helper, native module, or automation dependency |
| NFR-5 | Must | Error contract | The system shall emit exactly one error per invocation, let the first failing stage win, and order the stages as group routing, flag parsing, platform resolution, action support, built-in and permission gate, stdin read, app resolution, supplied-window resolution, snapshot resolution, sparse element lookup, window and locator replay, then the operating-system call |
| NFR-6 | Must | Availability | The system shall bound every operating-system command with a fixed timeout of 5 seconds for the permission probe, 10 seconds for discovery, 20 seconds for state capture, 15 seconds for a screenshot, 10 seconds for locator replay, and 10 seconds for an action, and shall offer no user-configurable timeout flag |
| NFR-7 | Must | Compatibility | The system shall change `schemaVersion` and the error code list only for a breaking reshape, and shall add error codes without removing or renaming existing ones |
| NFR-8 | Should | Isolation | The system shall keep snapshots, latest pointers, and screenshots under the resolved Fusion project root, so state is not shared across projects and a capture from one directory is visible to a later invocation from another directory in the same project |
| NFR-9 | Should | Concurrency | The system shall serialize concurrent CLI processes on a per-app lock, so a capture cannot be lost and a stale action cannot consume a newer capture |
| NFR-10 | Should | Maintainability | The system shall check the command surface descriptor, the parser flag literals, the emitted error codes, and the rendered guide against each other, so the shipped guide cannot drift from the binary |

## Constraints

- The surface is the `fn computer` CLI. It exposes no HTTP route.
- macOS is the only supported platform. Linux and Windows use the unsupported adapter.
- Only the macOS `osascript` and `screencapture` built-ins are used. Fusion downloads no helper, native module, or automation dependency.
- The JXA automation program is static and receives values as arguments or stdin.
- Snapshots, latest pointers, and screenshots live under the `.fusion/computer-use/` directory of the resolved project root. The root is resolved once per invocation by walking upward for a Fusion project marker.
- Element indexes are sparse and snapshot-scoped. An index is never derived from `elementCount`, position, or bounds.
- A snapshot expires five minutes after capture by default, and `expiresAt` publishes the exact deadline.
- One latest pointer exists per app, not per window.
- The `--snapshot-id` value must match `^cs_[A-Za-z0-9]{10,40}$` and is validated before any filesystem access.
- The command surface descriptor is the single source for the help text, the shipped guide, and the flag validation rules.
- The shipped `computer-use` skill is a thin discovery stub. It lists no subcommand and no flag.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: The command surface lists the shipped subcommands
      Given the fn CLI
      When the operator runs fn computer --help
      Then the output names capabilities, permissions, list-apps, list-windows, get-app-state, click, set-value, type-text, press-key, hotkey, scroll, and drag
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Capturing a window persists a snapshot before returning it
      Given a running app with one window
      When the operator runs fn computer get-app-state --app com.apple.Safari --json
      Then the envelope carries a snapshot id starting with cs_ and a record file exists under the project root
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: An element action without a snapshot is refused
      Given a running app that has never been captured
      When the operator runs fn computer click --app com.apple.Safari --element-index 7 --json
      Then the envelope carries error code SNAPSHOT_REQUIRED and no operating-system action runs
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A successful action consumes its capture
      Given a fresh capture of an app
      When the operator runs fn computer click --app com.apple.Safari --element-index 7 --json
      Then the result reports snapshotConsumed true and the next element action fails with reason consumed-by-action
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: A changed element is refused before the action
      Given a capture whose element no longer resolves
      When the operator runs fn computer click --app com.apple.Safari --element-index 7 --json
      Then the envelope carries error code ELEMENT_UNRESOLVABLE and no operating-system action runs
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A superseded capture is refused with its reason
      Given two captures of the same app
      When the operator runs fn computer click --app com.apple.Safari --element-index 7 --snapshot-id cs_01HABCDE123456 --json
      Then the envelope carries error code SNAPSHOT_STALE and details reason superseded
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: An index absent from the capture is refused
      Given a capture whose elements are indexed sparsely
      When the operator runs fn computer click --app com.apple.Safari --element-index 2 --json
      Then the envelope carries error code ELEMENT_INDEX_NOT_FOUND and the remediation asks for a fresh capture
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: An ambiguous app name is refused
      Given two running apps share a name
      When the operator runs fn computer hotkey --app Notes --keys cmd+k --json
      Then the envelope carries error code AMBIGUOUS_APP with a remediation to use a bundle id or pid
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Permission state is reported without a claim
      Given a host where the permission probe cannot run
      When the operator runs fn computer permissions --json
      Then every check reports status unknown and granted false
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A platform other than macOS is unsupported
      Given a host that is not macOS
      When the operator runs fn computer capabilities --json
      Then the result reports supported false and lists every action as unsupported
      And running fn computer list-apps --json fails with error code UNSUPPORTED_PLATFORM
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: The envelope is versioned and single
      Given any computer subcommand
      When the operator runs it with --json
      Then stdout carries exactly one object with schemaVersion 1, ok, and command
      And a successful run exits 0 and a failed run exits 1
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: A secret value travels through stdin
      Given an editable element in a captured window
      When the operator pipes the value into fn computer set-value --app com.apple.Safari --element-index 7 --value-stdin --json
      Then the value is absent from the process arguments and from the record the command writes
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: A failed screenshot keeps the captured tree
      Given a capture whose screenshot step fails
      When the operator runs fn computer get-app-state --app com.apple.Safari --json
      Then the result carries the snapshot and a screenshotError, and no screenshot path
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: The two window selectors are mutually exclusive
      Given a running app
      When the operator runs fn computer get-app-state --app com.apple.Safari --window-id w1 --window-index 0 --json
      Then the envelope carries error code INVALID_ARGUMENTS
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: A coordinate drag needs no snapshot
      Given a running app
      When the operator runs fn computer drag --app com.apple.Safari --from-x 1 --from-y 2 --to-x 3 --to-y 4 --json
      Then the action runs with a null snapshot id and no element indexes
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: The guide matches the binary that runs it
      Given the installed fn CLI
      When the operator runs fn skills get computer-use
      Then the output names every subcommand, every flag, and every error code
      And the shipped computer-use skill file lists no subcommand and no flag
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: Capabilities describe the platform and the action inventory
      Given the installed fn CLI
      When the operator runs fn computer capabilities --json
      Then the result carries the platform, the adapter id, the supported flag, both action lists, and the four feature flags
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The action replays the locator before it acts
      Given a capture of an app
      When the operator runs fn computer click --app com.apple.Safari --element-index 7 --json
      Then the window is resolved and the locator is replayed before the action call
      And the action uses the bounds observed during that replay
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: A secret value never reaches the output
      Given a value supplied through stdin
      When the operator runs fn computer set-value --app com.apple.Safari --element-index 7 --value-stdin --json
      Then the envelope, the error text, and the record the command writes contain no part of the value
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Untrusted values stay out of the program source
      Given an app name and a locator path
      When the operator runs an element action
      Then the program source passed to the operating system is unchanged and the values arrive as arguments
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: No automation dependency is installed
      Given the published CLI package
      When the operator inspects its contents
      Then the computer surface runs through the operating-system built-ins only
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The first failing stage decides the error
      Given a malformed flag on an unsupported platform
      When the operator runs the subcommand with --json
      Then the envelope carries error code INVALID_ARGUMENTS and no other error appears
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Every operating-system call is bounded
      Given an action that never returns
      When the operator runs fn computer click --app com.apple.Safari --element-index 7 --json
      Then the call is terminated at the action timeout and the envelope carries error code TIMEOUT
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: The error code list grows without renames
      Given the published contract
      When the error code inventory is compared with the codes emitted by the source
      Then every emitted code is a member of the published list
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: A capture is visible across directories in one project
      Given a capture made from a nested directory of a project
      When the operator runs an element action from the project root
      Then the action finds the same snapshot record under the project root
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: A capture that runs during an action is not lost
      Given an action in progress on an app
      When a capture for the same app starts concurrently
      Then the capture completes after the action and the newest capture stays usable
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: The shipped guide matches the descriptor
      Given the command surface descriptor
      When the guide is rendered
      Then the guide contains every subcommand, every flag, and every error code without truncation
    ```

## Conflicts

None identified yet.

## Open Questions

1. Which platform receives the next adapter if the surface is extended beyond macOS. The code today has only the macOS adapter and the unsupported adapter.
2. Whether `paste-text` and `perform-secondary-action` are planned additions. The documentation records them as absent from capabilities rather than as stubs.

---
title: "Computer Use: Desktop GUI Automation"
status: done
---

# Specification: Computer Use: Desktop GUI Automation

## Overview

The computer surface lives in the published CLI package at `packages/cli/src/commands/computer.ts` and `packages/cli/src/commands/computer/`.
A single dispatcher validates the flags, resolves the state root, runs the handler, validates the result against the contract, and prints one versioned envelope.
The contract in `computer/contract.ts` holds the frozen subcommand, action, and error-code tuples, the result shapes, and the envelope.
The snapshot store in `computer/snapshot-store.ts` persists capture records and the per-app latest pointer under the resolved project root, and it enforces the freshness order that decides whether an action may run.
The adapter registry in `computer/adapter-registry.ts` returns the macOS adapter on `darwin` and the unsupported adapter everywhere else.
The macOS adapter drives the operating-system built-ins through the exec seam, and the exec seam spawns them asynchronously with a bounded lifetime and no shell.
The agent-facing guide is rendered in-process from the same descriptor, and the shipped skill stays a thin discovery stub.

## Architecture

```
  fn computer SUBCOMMAND [--json]                 packages/cli/src/bin.ts
        │
        ▼
  runComputer                                        commands/computer.ts
        │  validateFlags → resolveComputerStateRoot → handler → validateResult → envelope
        │
        ├──► contract.ts        frozen tuples, result shapes, envelope, error codes
        │
        ├──► snapshot-store.ts  records + per-app latest pointer, freshness order
        │      PROJECT_ROOT/.fusion/computer-use/
        │        snapshots/SNAPSHOT_ID.json
        │        latest/TARGET_KEY_SLUG.json
        │        screenshots/computer-EPOCH_MS.png
        │
        └──► adapter-registry.ts
               ├── darwin  ──► adapter-macos.ts
               │                  │  ComputerExecSeam (exec-seam.ts)
               │                  ▼
               │              osascript -l JavaScript -e STATIC_PROGRAM
               │              screencapture -x -l CAPTURE_WINDOW_ID FILE
               │              static program source: computer/scripts/macos-jxa.ts
               │
               └── other   ──► adapter-unsupported.ts
                                  capabilities/permissions report supported: false
                                  every other method raises UNSUPPORTED_PLATFORM

  Agent-facing surface
        fn skills get computer-use  ──► guide.ts renderComputerUseGuide()
        packages/cli/skill/computer-use/SKILL.md  (thin discovery stub, no command list)
```

## Data Models

### App snapshot

| Field | Type | Constraints | Description |
|---|---|---|---|
| snapshotId | string | matches `^cs_[A-Za-z0-9]{10,40}$`, not null | Identifier of the capture, used as the action fence |
| targetKey | string | the `bundle:` prefix followed by the bundle id, or the `pid:` prefix followed by the process id, not null | App scope of the capture |
| windowKey | string | the target key, a hash sign, and the window id, not null | Window scope of the capture |
| capturedAt | string | ISO 8601 timestamp, not null | Time of the capture |
| expiresAt | string | ISO 8601 timestamp after `capturedAt`, not null | Deadline after which the capture is refused |
| app | AppRef | not null | The captured application |
| window | WindowRef | not null | The captured window |
| elementCount | number | integer, not null | Number of elements in the capture |
| elements | map of string to Element | sparse map keyed by the element index, not null | The captured elements |

### App reference

| Field | Type | Constraints | Description |
|---|---|---|---|
| bundleId | string or null | nullable | The application bundle id, null when the operating system reports none |
| name | string | not null | The application display name |
| pid | number | integer, not null | The operating-system process id |

### Window reference

| Field | Type | Constraints | Description |
|---|---|---|---|
| windowId | string | not null | Identifier of the window |
| windowIndex | number | integer, not null | Position of the window in the application window list |
| title | string | not null | The window title |
| bounds | Bounds or null | nullable | The window rectangle |
| minimized | boolean | not null | Whether the window is minimized |

### Element and locator

| Field | Type | Constraints | Description |
|---|---|---|---|
| index | number | integer, sparse, not null | The index emitted during capture |
| role | string | not null | The accessibility role |
| title | string or null | nullable | The accessibility name |
| value | string or null | nullable | The current value |
| label | string or null | nullable | The accessibility description |
| enabled | boolean | not null | Whether the element accepts actions |
| focused | boolean | not null | Whether the element holds focus |
| bounds | Bounds or null | nullable | The element rectangle |
| actions | array of string | not null | The accessibility actions the element offers |
| locator | ElementLocator | not null | The replay identity of the element |

The locator carries `kind` (literal `ax-path`), `path` (the path from the window root), `role`, `subrole`, `identifier`, and `title`.
The role, subrole, and identifier are compared on replay, so a different element that now occupies the path is refused.

### Action result

| Field | Type | Constraints | Description |
|---|---|---|---|
| action | string | one of the seven action names, not null | The action that was performed |
| app | AppRef | not null | The target application |
| snapshotId | string or null | null for hotkey and coordinate drag, else the fence id | The snapshot the action was bound to |
| elementIndex | number or null | null for drag and hotkey, else the targeted index | The targeted element index |
| fromElementIndex | number or null | null except for element-form drag | The drag start index |
| toElementIndex | number or null | null except for element-form drag | The drag end index |
| performed | boolean | literal `true`, not null | The action reached the operating system |
| snapshotConsumed | boolean | not null | Whether the app's latest capture was burned |

### Envelope and error

| Field | Type | Constraints | Description |
|---|---|---|---|
| schemaVersion | number | literal `1`, not null | Contract version |
| ok | boolean | not null | Whether the invocation succeeded |
| command | string | the `computer.` prefix followed by the subcommand, or `computer` for a group-level failure, not null | The command name |
| result | unknown | present only when `ok` is true | The command payload |
| error | ComputerError | present only when `ok` is false | The failure payload |

The error carries `code` (a member of the published error-code list), `message`, an optional `remediation`, and an optional flat `details` map whose values are strings, numbers, or booleans.
Remediation is required for `UNSUPPORTED_PLATFORM`, `PERMISSION_DENIED`, `PERMISSION_UNVERIFIED`, `SNAPSHOT_REQUIRED`, `SNAPSHOT_STALE`, `ELEMENT_INDEX_NOT_FOUND`, `ELEMENT_UNRESOLVABLE`, `AMBIGUOUS_APP`, and `ACTION_UNSUPPORTED`.

## API Contracts

The feature exposes no HTTP route, so there is no OpenAPI document.
The contract surface is the `fn computer` command set below.

| Subcommand | Required flags | Operation | Result |
|---|---|---|---|
| `capabilities` | none | Report the platform, the adapter id, the supported flag, the action inventory, and the feature flags | `CapabilitiesResult` |
| `permissions` | none | Report the Accessibility and Screen Recording permission state | `PermissionsResult` |
| `list-apps` | none | List the running applications available for selection, sorted by name | `ListAppsResult` |
| `list-windows` | `--app` | List the windows of one application | `ListWindowsResult` |
| `get-app-state` | `--app` | Capture a window and its accessible elements, then persist the snapshot | `AppStateResult` |
| `click` | `--app`, `--element-index` | Click a captured element | `ActionResult` |
| `set-value` | `--app`, `--element-index`, and one of `--value` or `--value-stdin` | Set the value of a captured editable element | `ActionResult` |
| `type-text` | `--app`, and one of `--text` or `--text-stdin` | Type text into the app or a captured element | `ActionResult` |
| `press-key` | `--app`, `--key` | Press a key in the app or a captured element | `ActionResult` |
| `hotkey` | `--app`, `--keys` | Send a plus-separated key chord to the app | `ActionResult` |
| `scroll` | `--app`, `--direction` | Scroll the app or a captured element, three steps by default | `ActionResult` |
| `drag` | `--app`, and either all four coordinate flags or both element-index flags | Drag between coordinates or two captured elements | `ActionResult` |

Optional flags on the element actions are `--snapshot-id`, `--window-id`, and `--window-index`.
`--window-id` and `--window-index` are mutually exclusive.
`hotkey` and coordinate-form `drag` accept neither snapshot nor window flags.
`type-text`, `press-key`, and `scroll` accept `--element-index`, and they require it when a snapshot or window flag is present.
`get-app-state` also accepts `--no-screenshot` and `--restore-window`.
Every subcommand accepts the global `--json` flag.

Error codes shared across the subcommands:

| Code | Meaning |
|---|---|
| `UNSUPPORTED_PLATFORM` | No supported adapter on this platform |
| `PERMISSION_DENIED` | A required permission is denied, or a required built-in is missing |
| `PERMISSION_UNVERIFIED` | An unknown probe was followed by a permission-shaped operating-system failure |
| `INVALID_ARGUMENTS` | An invalid subcommand, flag, number, enum, or snapshot id |
| `APP_NOT_FOUND` | No running application matches the target |
| `AMBIGUOUS_APP` | More than one application name matches the target |
| `WINDOW_NOT_FOUND` | The supplied live window selector did not match |
| `SNAPSHOT_REQUIRED` | An element action has no snapshot for the target app |
| `SNAPSHOT_STALE` | The snapshot is no longer usable, with a reason in the fixed stale-reason list |
| `ELEMENT_INDEX_NOT_FOUND` | The sparse index is absent from the snapshot |
| `ELEMENT_UNRESOLVABLE` | The recorded locator no longer resolves, or the identity differs |
| `ACTION_UNSUPPORTED` | The adapter does not support the action |
| `ACTION_FAILED` | The operating-system action failed |
| `SCREENSHOT_FAILED` | The screenshot failed, reported inside `screenshotError` |
| `TIMEOUT` | A bounded operating-system call ran out of time |
| `INTERNAL` | An unexpected failure, reported redacted |

## Key Sequences

### Capture a snapshot

```
  operator            runComputer          snapshot store            macOS adapter        osascript
     │                    │                     │                        │                   │
     │ get-app-state      │                     │                        │                   │
     │------------------->│ validateFlags      │                        │                   │
     │                    │ resolve state root │                        │                   │
     │                    │------------------->│                        │                   │
     │                    │ withAppFence       │                        │                   │
     │                    │ captureState ──────────────────────────────>│                   │
     │                    │                     │                        │ permission probe  │
     │                    │                     │                        │------------------->│
     │                    │                     │                        │ accessibility ok  │
     │                    │                     │                        │------------------->│
     │                    │                     │                        │ list windows      │
     │                    │                     │                        │------------------->│
     │                    │                     │                        │ state capture     │
     │                    │                     │                        │------------------->│
     │                    │                     │                        │ tree + elements   │
     │                    │                     │<──────────────────────│                   │
     │                    │ persist record ───>│                       │                   │
     │                    │                     │ write snapshot.json   │                   │
     │                    │                     │ write latest pointer  │                   │
     │                    │<────────────────────│                       │                   │
     │<───────────────────│ envelope            │                       │                   │
```

### Act on a snapshot

```
  operator            runComputer            store            adapter
     │                    │                     │                 │
     │ click --element-index 7                 │                 │
     │------------------->│ validateFlags      │                 │
     │                    │ resolve app        │                 │
     │                    │ withAppFence ──────────────────────>│
     │                    │ resolve record ───>│                 │
     │                    │                     │ freshness order │
     │                    │                     │ not-found / superseded / consumed-by-action /
     │                    │                     │ expired / pid-changed / window-mismatch
     │                    │<--------------------│ refusal         │
     │                    │ getElement(index) ─>│                 │
     │                    │ resolve window ─────────────────────>│
     │                    │ resolve locator ────────────────────>│
     │                    │                     │                 │ verify role, subrole, identifier
     │                    │                     │                 │ ELEMENT_UNRESOLVABLE on mismatch
     │                    │ perform action ────────────────────>│
     │                    │ consume pointer ──>│                 │
     │                    │<--------------------│ consumed        │
     │<-------------------│ envelope: snapshotConsumed true     │
```

### The snapshot, act, snapshot loop

```
   ┌────────────────────────────── one iteration ──────────────────────────────┐
   │                                                                          │
   │  fn computer get-app-state --app com.apple.Safari --json                  │
   │      capture the tree, persist the record, publish snapshotId             │
   │                                                                          │
   │  fn computer click --app com.apple.Safari --element-index 7              │
   │      resolve the record, replay the window and the locator, act,         │
   │      then consume the app's latest capture                               │
   │                                                                          │
   └──────────────────────────────────────────────────────────────────────────┘
          │                                    │
          │ next element action                │ next element action
          ▼                                    ▼
   SNAPSHOT_STALE / consumed-by-action   SNAPSHOT_STALE / consumed-by-action
   (until a new capture re-arms)         (until a new capture re-arms)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Safety model | Bind every element action to a snapshot and consume the capture after each action | A successful action can change focus, navigation, scrolling, or the rendered tree, so a second index from the first capture may name a different element |
| Locator identity | Replay the recorded accessibility path and compare role, subrole, and identifier | A path that now holds a different element must be refused instead of acted on |
| Bounds source | Use the bounds observed during the replay | Saved bounds from the capture are stale by definition |
| Snapshot storage | Persist records and the latest pointer on disk under the project root | Each CLI invocation is a separate process, so the capture must survive the process |
| State root | Resolve the project root once per invocation by walking upward for a project marker | Capture and replay often run from different directories in the same project |
| Pointer scope | One latest pointer per app, not per window | The app's tree is the unit that changes, and the pointer decides whether a fresh capture exists |
| Concurrency | Hold a per-app directory lock across capture, replay, and consumption | A concurrent capture must not be lost and a stale action must not consume a newer capture |
| Platform support | macOS only, with an unsupported adapter elsewhere | A clear failure is safer than a silent no-op that makes a caller believe an action happened |
| Operating-system access | Use the `osascript` and `screencapture` built-ins through a spawn seam | Fusion downloads no helper, native module, or automation dependency |
| Program safety | Keep the JXA program static and pass values as arguments or stdin | App names, window ids, and locator paths are untrusted input |
| Secrets | Read values from stdin and redact long tokens in error text | A secret must not reach the process table, the snapshot records, or the output |
| Permissions | Report granted, denied, or unknown from non-mutating preflights | A denied screen capture can still save wallpaper pixels, so capture success is not proof of permission |
| Error contract | One append-only error-code list, one flat details map, one deterministic failure order | Callers branch on codes safely, and the first failing stage decides the outcome |
| Guide ownership | Render the guide in-process from the command surface descriptor | The shipped guide cannot drift from the binary that will run the commands |
| Skill form | Ship a thin discovery stub with no command or flag list | A static list in the skill file would drift from the installed binary |

## Risks and Unknowns

1. The adapter surface is macOS-only. Another platform needs a new adapter behind the same contract, and no such adapter exists yet.
2. The macOS adapter depends on the accessibility tree, so an application that draws its controls without accessibility metadata cannot be inspected or driven.
3. Screenshot capture maps the accessibility window to a Quartz window id by process id, title, and bounds. A collision or a title change degrades the screenshot without affecting the captured tree.
4. The permission preflight reads the state of the host process, so a headless host or a remote shell reports unknown and the action outcome then depends on the form of the operating-system failure.
5. The state root falls back to the resolved start path when no project marker is found, so two invocations from unrelated directories in the same project can miss each other's captures.

## Out of Scope

- Linux and Windows adapters. Both report `supported: false` and fail with `UNSUPPORTED_PLATFORM`.
- A dashboard or HTTP surface for computer use. The feature is the `fn computer` CLI.
- Any native automation helper, native module, or downloaded binary.
- `paste-text` and `perform-secondary-action`. They are absent from the action inventory rather than present as stubs.
- A user-configurable timeout. The seam timeouts are fixed.
- Cross-project sharing of snapshots, pointers, or screenshots.
- A remote or networked desktop. The surface drives the local desktop only.

---
title: "Computer Use: Desktop GUI Automation"
status: done
---

# Test Plan: Computer Use: Desktop GUI Automation

## Scope

Covers the `fn computer` command surface, the snapshot store and its freshness order, the macOS adapter driven through an injected exec seam, the unsupported adapter, the command surface descriptor, the rendered guide, and the shipped discovery skill.
The tests never touch the host desktop. The macOS adapter is exercised through a fake exec seam that returns canned stdout, stderr, exit codes, and timeouts.
Out of scope are the operating-system built-ins themselves, the macOS permission prompts, the screenshot image content, and the Hermes and Claude skill staging paths that only install the shipped skill.

Two behaviors have no direct assertion today. The stdin transport for a secret value is covered only through the exactly-one-source rule, and the restore of a minimized window is covered only through the flag validation. Both are listed in the coverage matrix with the test that comes closest.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Sparse element indexes persist as map keys | A capture with indexes 0, 3, and 7 | Index 7 resolves, index 2 raises `ELEMENT_INDEX_NOT_FOUND`, and the record file stores the element under key `7` |
| TC-2 | A capture keeps its identity across a fresh store instance | A record read by a new store over the same root | The app, window, and locator of the record are returned unchanged |
| TC-3 | The freshness order raises the documented codes | Resolve with no snapshot, with a superseded id, with an unknown id, and after the deadline | `SNAPSHOT_REQUIRED`, then `SNAPSHOT_STALE` with `superseded`, `not-found`, and `expired`, each with remediation naming `get-app-state` |
| TC-4 | Supersession is checked before expiry, then pid and window | A superseded id after the deadline, a changed pid, and a mismatched asserted window | `superseded` first, then `pid-changed`, then `window-mismatch` |
| TC-5 | Consumption burns the app pointer | Consume after a capture, then resolve with and without the id | Both resolves raise `SNAPSHOT_STALE` with `consumed-by-action`, and a fresh capture re-arms the pointer |
| TC-6 | A late consumption does not consume a newer capture | A consume and a persist interleaved, including a concurrent pair | The newer capture stays resolvable |
| TC-7 | A legacy pointer and an unparsable record | A pointer without `consumedAt`, and a record file that is not JSON | The legacy pointer resolves, and the unparsable record raises `not-found` |
| TC-8 | Expired records are pruned | A capture with a past deadline | The record file is removed by a single-level directory read |
| TC-9 | The contract keeps frozen inventories and a stable envelope | The exported tuples and envelope builders | The subcommand, action, error-code, and stale-reason tuples are frozen and duplicate free, the envelope carries `schemaVersion` 1, and the timeout table holds the six fixed values |
| TC-10 | The contract validates ids, permissions, state, and action shapes | A valid id, a path-shaped id, a permission result, a state result, and action results for drag, hotkey, and click | The path-shaped id is rejected, the permission result without a probe is rejected, a state result with both a screenshot and an error is rejected, and an action result without `snapshotConsumed` is rejected |
| TC-11 | App and window addressing stay separate | An app with a bundle id, two window ids, and a hostile target key | The target key is the `bundle:` prefix followed by the bundle id, the window keys differ per window, and the slug holds no path separator |
| TC-12 | The state root resolves from the project marker | A marked root, a nested directory, an unmarked directory, and a relative path | The marked root and the nested directory resolve to the root, the unmarked directory resolves to itself, and a relative path resolves to an absolute path |
| TC-13 | The registry injects the macOS adapter dependencies | A `darwin` platform with an injected factory | The factory receives the seam, the clock, and the project root |
| TC-14 | The unsupported adapter rejects every operation | A `linux` and a `win32` platform | Capabilities report `supported: false` with every action unsupported, permissions report no checks, and every other method raises `UNSUPPORTED_PLATFORM` with a macOS remediation |
| TC-15 | A denied Accessibility grant blocks automation | A probe that reports a denied Accessibility grant | `hotkey` and `drag` raise `PERMISSION_DENIED` after one probe and no automation call |
| TC-16 | A missing osascript is reported as unknown permissions | A seam that fails to spawn `osascript` | Permissions report both checks as `unknown` and not granted, and every operation raises `PERMISSION_DENIED` with the missing-binary detail |
| TC-17 | A probe that times out, exits non-zero, or returns malformed output | Three failing probe results | Each keeps both checks `unknown` and does not report a missing binary |
| TC-18 | The guide renders the whole descriptor | The rendered guide | Every subcommand, every flag, and every error code appears, every required heading appears once, and no truncation marker is present |
| TC-19 | The guide renders the invocation rules | The rendered guide | The mutually exclusive pairs, the exactly-one-value rules, the element-index requirement, and the drag form rules all appear |
| TC-20 | The shipped skill stays a thin discovery stub | Every shipped `SKILL.md` | The computer-use skill names only the three read-only probes, no other shipped skill carries a computer command, and the frontmatter parses |
| TC-21 | The built-in guide matches the installed binary | `fn skills get computer-use` and `fn --version` | The guide is printed and its version matches the binary version |
| TC-22 | The computer-use skill ships in the published package | The packed package contents | `skill/computer-use/SKILL.md` is present |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-23 | A capture emits one envelope and persists a record | A fake adapter and a temporary project root | The envelope carries `schemaVersion` 1, `ok` true, the `computer.get-app-state` command, and a `cs_` prefixed snapshot id |
| TC-24 | A capture crosses directories in one project | A capture from a nested directory and an action from the project root | The action finds the same record, and the nested directory holds no state directory |
| TC-25 | A stale id is refused and the latest id replays before the action | Two captures and a recording fake adapter | The stale id raises `SNAPSHOT_STALE` with `superseded` and the action does not run, while the latest id resolves the window, then the locator, then the action, and the action uses the bounds from the replay |
| TC-26 | The loop refuses the next element action until a fresh capture | A capture, a click, a second click, and a new capture | The click reports `snapshotConsumed` true, the second click raises `consumed-by-action` with remediation naming `get-app-state`, and the click after the new capture succeeds |
| TC-27 | Every action form consumes the captured pointer | A capture before each of the eight action forms | Each action reports `snapshotConsumed` true, and the following element action raises `consumed-by-action` |
| TC-28 | A failed action and read commands do not consume the pointer | A failing click, then a read, then targetless actions | The failing action does not consume the pointer, the read does not consume it, and each targetless action does consume it |
| TC-29 | The command fence is held through consumption | An action that blocks while a capture starts | The capture completes after the action, and the newest capture stays usable |
| TC-30 | Both drag endpoints come from one snapshot fence | A concurrent latest update during a drag | The record is resolved once, and the drag receives both endpoints and the one snapshot id |
| TC-31 | A coordinate drag runs without a snapshot | A complete set of coordinate flags | The action receives a null snapshot id, the four coordinates, and no element indexes |
| TC-32 | Element-scoped typing uses the replay path | A capture and a typed element | The locator is replayed once and the typing action runs once |
| TC-33 | The descriptor, the dispatcher, and the contract agree | The exported subcommand sets | The three sets are equal, and each declared required and mutually exclusive flag is enforced by the validator |
| TC-34 | The conditional forms, the parser literals, and the error codes are checked | The descriptor, the parser source, and the emitting sources | The conditional forms are refused, the parser flag literals equal the declared flags, and every emitted code belongs to the published list |
| TC-35 | A coordinate drag posts a CoreGraphics event sequence | The macOS adapter over a fake seam | The program posts a mouse event creation and a post for the drag, the arguments carry the operation, the app name, and the four coordinates, and the call uses the 10 second action timeout |
| TC-36 | The scroll direction maps to a fixed key code | The macOS adapter over a fake seam for each of the four directions | The program carries the direction and the amount, and the fixed key code for that direction |
| TC-37 | A failed screenshot keeps the captured tree | A seam that fails to spawn `screencapture` | The state carries the tree, the screenshot is null, the error is `SCREENSHOT_FAILED`, and the capture call used the screenshot timeout |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-38 | The recorded window no longer exists | The action raises `SNAPSHOT_STALE` with reason `window-gone` and a remediation naming `get-app-state` |
| TC-39 | The recorded locator no longer resolves | The action raises `ELEMENT_UNRESOLVABLE` and the details carry the snapshot id and the element index |
| TC-40 | A replay raises a timeout, an unverified permission, or a denied permission | Each code is preserved as raised, and none is rewritten as a stale-element error |
| TC-41 | One drag endpoint cannot be resolved | The action raises `ELEMENT_UNRESOLVABLE` and the details carry the failing endpoint index |
| TC-42 | The replayed element has a different role or is not live | The action raises `ELEMENT_UNRESOLVABLE` after two operating-system calls and no further automation |
| TC-43 | A permission-shaped replay failure | The action raises `PERMISSION_UNVERIFIED` instead of reporting an unresolvable element |
| TC-44 | `osascript` disappears during a replay | The action raises `PERMISSION_DENIED` with the missing-binary detail |
| TC-45 | An unknown subcommand and a missing subcommand | Both raise `INVALID_ARGUMENTS` under the group-level command name |
| TC-46 | Both text sources are supplied | The invocation is refused with `INVALID_ARGUMENTS` before any app discovery |
| TC-47 | A dotted bundle spelling matches no bundle id | The target falls back to an exact app name and the action runs against that app |

## Test Infrastructure

- The suite runs with Vitest in the CLI package under `packages/cli/src/commands/__tests__/`.
- A fake `ComputerAdapter` implements the whole adapter interface, so no test touches the host desktop.
- A fake `ComputerExecSeam` returns canned stdout, stderr, exit codes, and timeout flags for the `osascript` and `screencapture` calls.
- A `ComputerSnapshotStore` is built over a temporary directory with an injected clock, so the freshness order and the expiry are deterministic.
- A temporary project root with a `.fusion/project.json` marker exercises the state-root resolution.
- The `runComputer` dispatcher is called with injected `stdout`, `stderr`, `stdin`, `adapter`, `store`, and `clock` options, so the envelope and the exit code are observable without a process.
- The tests run on every platform, so the macOS adapter is only reached through the injected seam.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-18, TC-33 |
| FR-2 | TC-23, TC-1, TC-8 |
| FR-3 | TC-3, TC-26 |
| FR-4 | TC-5, TC-26, TC-27, TC-28 |
| FR-5 | TC-25, TC-39, TC-42 |
| FR-6 | TC-3, TC-4, TC-38 |
| FR-7 | TC-1 |
| FR-8 | TC-47 |
| FR-9 | TC-16, TC-17 |
| FR-10 | TC-14 |
| FR-11 | TC-23, TC-45 |
| FR-12 | TC-46 |
| FR-13 | TC-37 |
| FR-14 | TC-33 |
| FR-15 | TC-30, TC-31, TC-32 |
| FR-16 | TC-18, TC-19, TC-20, TC-21 |
| FR-17 | TC-9, TC-14 |
| NFR-1 | TC-25, TC-39, TC-42 |
| NFR-2 | TC-46 |
| NFR-3 | TC-35, TC-36 |
| NFR-4 | TC-14, TC-22 |
| NFR-5 | TC-40, TC-45, TC-46 |
| NFR-6 | TC-9, TC-37 |
| NFR-7 | TC-9, TC-34 |
| NFR-8 | TC-11, TC-12, TC-24 |
| NFR-9 | TC-6, TC-29, TC-30 |
| NFR-10 | TC-18, TC-33, TC-34 |

## Key Test Files

- `packages/cli/src/commands/__tests__/computer-commands.test.ts`
- `packages/cli/src/commands/__tests__/computer-snapshot-index.test.ts`
- `packages/cli/src/commands/__tests__/computer-adapter-registry.test.ts`
- `packages/cli/src/commands/__tests__/computer-contract.test.ts`
- `packages/cli/src/commands/__tests__/computer-state-root.test.ts`
- `packages/cli/src/commands/__tests__/computer-surface-descriptor.test.ts`
- `packages/cli/src/commands/__tests__/computer-use-guide.test.ts`
- `packages/cli/src/commands/__tests__/computer-use-skill.test.ts`
- `packages/cli/src/commands/__tests__/skills-get.test.ts`
- `packages/cli/src/__tests__/package-config.test.ts`

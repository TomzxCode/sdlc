---
title: "Command Safety Gate"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Command Safety Gate

## Overview

The command safety gate stands between a model's shell and file-mutation tool calls and the user's data.
It is a two-stage cascade: stage 1 is a deterministic, offline classifier that judges a command by its blast radius, and stage 2 turns an ambiguous verdict into a reflection prompt that the model must satisfy with a justification.
Catastrophic targets such as the filesystem root, the home directory, credential stores, and device nodes are denied outright, and no justification can unlock them.
This feature documents already-implemented code that was reverse-engineered during an SDLC sync, so every requirement below describes behaviour that exists today.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Confidence that an agent cannot silently destroy their home directory, credentials, or system files |
| Model authors | Refusal text that names the offending target and tells the model what to check before it retries |
| Maintainers | One auditable policy for what a destructive command may touch, backed by adversarial test coverage |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall assess every shell command submitted to the `bash` tool with a deterministic, offline blast-radius assessment before the command is executed. |
| FR-2 | Must | The system shall classify a command by what it would destroy and whether that can be undone, rather than by command name, so that `find -delete`, `shred`, `truncate`, `dd`, and truncating redirects are covered alongside `rm -rf`. |
| FR-3 | Must | The system shall deny a catastrophic target outright, and no justification shall ever unlock it. |
| FR-4 | Must | The system shall treat the filesystem root, protected system paths and their contents, the user's home directory, credential stores and their contents, and raw device nodes as catastrophic targets. |
| FR-5 | Must | The system shall convert a `Confirm` verdict into a reflection prompt that the model must satisfy by re-issuing the call with a substantive `justification` naming the user request the command serves. |
| FR-6 | Must | The system shall refuse a blind retry of a held command, so that repeating the identical call without a justification produces the same refusal. |
| FR-7 | Must | The system shall escalate to `Confirm` whenever the set of affected paths cannot be determined statically, including unresolved variables, command substitution, globs, operands supplied by a pipe, opaque wrappers, and inline shell scripts. |
| FR-8 | Must | The system shall apply the same classifier to `apply_patch` deletion targets, and shall refuse to delete a protected path. |
| FR-9 | Should | The system shall unwrap command wrappers such as `sudo`, `env`, `nice`, `ionice`, `timeout`, `nohup`, `xargs`, `command`, and `exec`, so that the destructive program underneath is the one that gets classified. |
| FR-10 | Should | The system shall split a command line into segments on shell separators and assess each segment independently, so that chaining cannot launder a catastrophic command. |
| FR-11 | Should | The system shall treat a truncating redirect to a protected path as a destructive write, and shall treat an append (`>>`) and the standard sinks (`/dev/null`, `/dev/stdout`, `/dev/stderr`, `NUL`) as non-destructive. |
| FR-12 | Should | The system shall let routine in-project cleanup run without a reflection turn, so that the gate does not train users to bypass it. |
| FR-13 | Should | The system shall apply the gate at the single `Tool::execute` chokepoint of the `bash` tool, before background dispatch, so that foreground, background, and batch dispatch paths cannot bypass it. |
| FR-14 | Should | The system shall record each gate decision in the log, distinguishing a denial from a hold for justification. |
| FR-15 | May | The system shall expose the protected path lists (home subpaths, credential subpaths, system paths, and recursively protected system paths) so that other tools and documentation can reuse the same policy. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | The assessment shall run entirely offline, with no model call and no network call, and shall complete in under 5 ms for a typical command line. |
| NFR-2 | Must | Security | The system shall reason only from the command text and path strings, and shall not read, log, or transmit the contents of any file that a command names. |
| NFR-3 | Must | Reliability | The assessment shall be total: any input, including empty, malformed, or garbage input, shall yield a verdict rather than an error or a panic. |
| NFR-4 | Must | Determinism | The same command string and the same risk context shall always produce the same verdict, independent of wall-clock time, randomness, or network state. |
| NFR-5 | Must | Security | The classifier crate shall declare no runtime dependency and shall make no network call, so that the safety decision cannot be subverted by an upstream service. |
| NFR-6 | Should | Usability | A refusal shall name the offending path or target, shall ask the model to check the command against the user's actual request, and shall tell the model to ask the user when it is unsure. |
| NFR-7 | Should | Performance | The safe path shall add no model round trip and no extra tool call, so an ordinary command costs only the assessment itself. |
| NFR-8 | Should | Architecture | The classifier shall be consumable by any tool without pulling in the agent runtime, so the destructive-command policy has one source of truth. |

## Constraints

- The gate is defense in depth, not a sandbox.
- The classifier is a static parser: it does not execute, expand, or resolve the command it is given.
- Path resolution is lexical, so it never touches the filesystem and is not symlink-aware.
- The `bash` tool on Windows runs `cmd.exe`, whose syntax the POSIX-shaped classifier does not model.
- The gate must not read file contents, so it can only reason about command text and path strings.
- The policy is deliberately biased toward recall, because a false positive costs one reflection turn while a false negative costs the user's data.

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
    Scenario: Command is assessed before any process starts
      Given a tool call to the `bash` tool carrying the command `rm -rf /home/u`
      When the tool call is executed
      Then the assessment runs before a process is spawned
      And the command does not execute
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Destructive verbs other than rm are covered
      Given a working directory of `/home/u/proj` and a home directory of `/home/u`
      When `find /home/u -delete` is assessed
      Then the verdict is Catastrophic
      And the same holds for `shred`, `truncate`, `dd`, and a truncating redirect to a protected path
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: A catastrophic verdict is unconditional
      Given a command whose assessment level is Catastrophic
      When the gate is evaluated with an elaborate justification naming the user's request
      Then the outcome is Deny
      And the reason states that the command cannot be confirmed
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Protected targets are catastrophic and ordinary paths are not
      Given a home directory of `/home/u`
      When `/`, `/etc/passwd`, `/home/u`, `~/.ssh/id_ed25519`, and `/dev/sda` are classified
      Then each one is classified as Catastrophic
      And `/home/u/proj/src/old.rs` is not
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: An ambiguous verdict produces a reflection prompt
      Given the command `rm -rf $TARGET`
      When the gate is evaluated with no justification
      Then the outcome is Reflect with a prompt that names the target
      And the prompt asks which user request requires the deletion
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A blind retry is refused again
      Given a command that the gate held for justification
      When the identical call is issued again with no justification
      Then the same refusal is returned
      And no path is deleted
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: An unresolvable target escalates
      Given the command `rm -rf $TARGET`
      When it is assessed
      Then the verdict is at least Confirm
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: apply_patch refuses a protected deletion
      Given a file at `$HOME/.ssh/id_ed25519`
      When an apply_patch call deletes that file by absolute path
      Then the tool reports a refusal
      And the file still exists
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A wrapper does not hide the destructive program
      Given the command `sudo env nice -n 5 rm -rf ~`
      When it is assessed
      Then the verdict is Catastrophic
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Chaining does not launder a catastrophic command
      Given the command `echo starting && rm -rf ~`
      When it is assessed
      Then the verdict is Catastrophic
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Only truncation counts as a destructive write
      Given the command `echo bad > /etc/passwd`
      When it is assessed
      Then the verdict is Catastrophic
      And the command `echo line >> /home/u/other/log.txt` runs immediately
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Routine in-project cleanup is not interrupted
      Given the command `rm -rf target` inside the working directory
      When it is assessed
      Then the verdict runs immediately without a reflection turn
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Background dispatch is gated
      Given a bash tool call with `run_in_background` set to true and the command `rm -rf $HOME`
      When the tool call is executed
      Then the call fails with a refusal
      And the home directory still exists
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Gate decisions are logged
      Given a bash tool call that the gate denies
      When the tool call is executed
      Then a denial is written to the log
      And a command that is only held for justification is logged as a hold
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: The protected path lists are reusable
      Given the protected path policy
      When the home subpaths, credential subpaths, system paths, and recursively protected system paths are read
      Then each list is non-empty and contains the expected entries
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The assessment is offline and fast
      Given a typical command line of a few hundred characters
      When it is assessed
      Then no model call and no network call is made
      And the assessment completes in under 5 ms
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: File contents never reach the gate
      Given a command that names an existing file
      When it is assessed and the refusal is produced
      Then the file is not read
      And neither the refusal text nor the log records the file contents
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Garbage input still yields a verdict
      Given the command strings ``, `   `, `'`, `\`, `;;;`, `&&`, and `rm -rf "unterminated`
      When each one is assessed
      Then each one produces an assessment rather than an error or a panic
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: The same input always yields the same verdict
      Given a command string and a risk context
      When it is assessed twice
      Then both verdicts are identical
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The classifier has no runtime dependencies
      Given the `jcode-command-risk` crate
      When its dependency list is inspected
      Then it declares no runtime dependency
      And the gate makes no network call
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: The refusal is actionable
      Given a command that the gate held
      When the refusal text is produced
      Then it names the offending target
      And it asks the model to check the command against the user's actual request and to ask the user when unsure
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: The safe path adds no round trip
      Given a command that is classified Safe
      When it is executed
      Then the tool runs it directly with no additional model turn
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: The policy has one source of truth
      Given the `jcode-command-risk` crate
      When another tool needs a destructive-command policy
      Then it can depend on the crate without pulling in the agent runtime
    ```

## Conflicts

<!-- Identified and populated by /review-requirements: pairs or groups of requirements that cannot all be satisfied at once. Reconcile before approval, or promote to an open question. -->

None identified.

## Open Questions

1. Should the classifier learn `cmd.exe` syntax so the gate is equally effective on the Windows build of the `bash` tool?
2. Should the latency budget in NFR-1 be pinned by a benchmark so that a future refactor cannot silently make the safe path expensive?
3. Should the protected path set be user-configurable, so that a home directory laid out differently from the defaults is still protected?

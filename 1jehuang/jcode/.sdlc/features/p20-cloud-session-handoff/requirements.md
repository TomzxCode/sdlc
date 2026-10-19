---
title: "Cloud Session Handoff"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Cloud Session Handoff

## Overview

A jcode session is a single linear transcript, so it cannot run on two machines at the same time.
`jcode cloud move` hands a live session to a cloud host, carrying the transcript, the todo list, the project memory, and the repository state.
`jcode cloud return` brings the session back and merges the cloud work into the local checkout as a 3-way merge.
A per-machine lease file decides which machine owns the session at any moment, so a stale local copy can neither run a turn nor overwrite a newer transcript.
This feature was reverse-engineered from the existing codebase during an SDLC sync, so it documents already-implemented functionality.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developer moving a session to a cloud host | Keep the conversation, the todos, and the uncommitted work, and keep the local files editable while the session is away |
| Developer working on the cloud host | Receive a transcript that still makes sense, and know what did not travel with it |
| Developer returning to the local machine | Get the cloud work back without losing the local edits made in the meantime |
| Operator of a shared or cloud machine | Have exactly one machine running turns for a session at a time |
| Maintainer | One ownership rule, the lease, that the CLI, the TUI, and the agent all enforce the same way |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall stage the session transcript, the todo list, the project memory, and the repository state, transfer them to the target host, and verify the cloud copy before ownership changes. |
| FR-2 | Must | The system shall refuse to move a session whose lease names an away host, and shall tell the operator to run `jcode cloud return` first. |
| FR-3 | Must | The system shall refuse to move a session that is mid-turn unless `--allow-active` is passed. |
| FR-4 | Must | `jcode cloud move --dry-run` shall stage and verify the cloud copy without writing a lease, without changing the working tree, and without changing the index. |
| FR-5 | Must | The system shall increment a monotonic migration epoch on every move and return, and shall stamp the shipped transcript with that epoch. |
| FR-6 | Must | The system shall check before staging that the cloud host's jcode supports the move protocol, and shall name the host and the remedy when it does not. |
| FR-7 | Must | The system shall capture the repository as a git bundle plus a snapshot commit that includes the staged, unstaged, and untracked non-ignored work, without modifying the user's index or working tree. |
| FR-8 | Must | The system shall restore the repository on the cloud host at the same absolute path, on the same branch, with the same uncommitted work, and with the git identity when the cloud checkout has none. |
| FR-9 | Must | The system shall carry only allowlisted environment variables, and shall copy only allowlisted ignored files that are git-ignored and at most 256 KiB each, so that no machine-local, display, secret, or build-output state travels. |
| FR-10 | Must | The system shall append an agent-facing migration notice to the transcript that covers the source and target hosts, the epoch, the repository path, branch, and uncommitted state, the build caches that did not travel, the toolchain hints, the local MCP servers, and the local background tasks that did not travel. |
| FR-11 | Must | The system shall close any unanswered tool use in the last assistant message with a tool result, so that the shipped transcript stays valid for the provider. |
| FR-12 | Must | The system shall hand ownership to the cloud host only after the cloud copy is verified, and shall restore the previous local lease when the activation fails. |
| FR-13 | Must | The system shall refuse to overwrite a cloud checkout that holds work jcode did not place there, and shall name the path in the refusal. |
| FR-14 | Must | `jcode cloud return` shall install the cloud transcript locally, replacing the local snapshot and removing the old journal. |
| FR-15 | Must | The system shall merge the cloud repository work into the local checkout as a 3-way merge whose base is the snapshot both sides agreed on at move time. |
| FR-16 | Must | The system shall report the merge outcome as no repository, unchanged, refs only, applied, or conflicts, and shall name the conflicting files. |
| FR-17 | Must | On a conflict the system shall leave the local working tree untouched, shall keep the cloud work reachable at `refs/jcode-cloud/session_abc/cloud`, and shall tell the operator how to resolve it. |
| FR-18 | Must | `jcode cloud return --refs-only` shall fetch the cloud work into refs without touching the working tree. |
| FR-19 | Must | The system shall append a return notice to the transcript that names the cloud host, the local machine, the time, the merge outcome, and the fact that the cloud processes did not come back. |
| FR-20 | Must | The system shall restore local ownership and bump the epoch when a session comes back. |
| FR-21 | Must | The system shall refuse to return a session that was never moved, and shall refuse to return a session that already lives on this machine. |
| FR-22 | Must | `jcode cloud where` shall report, for every moved session, the session id, the location, the epoch, the repository root, and the number of commits the local checkout is ahead of the last synced head. |
| FR-23 | Must | `jcode cloud attach` shall attach this terminal to the host that owns the session and resume the same session id there. |
| FR-24 | Must | The system shall resolve the target host from `--host` or `JCODE_CLOUD_HOST`, and the remote binary from `--remote-binary` or `JCODE_CLOUD_REMOTE_BINARY`, and shall name both in the error when they are missing. |
| FR-25 | Must | The system shall keep one lease file per session under `~/.jcode/session_leases`, named after the session id, recording the epoch, the away host, the repository root, the last agreed snapshot and head, and the update time. |
| FR-26 | Must | A session copy on a machine whose lease says the session moved away shall neither start a turn nor persist. |
| FR-27 | Must | A session copy whose epoch is older than the lease epoch shall neither start a turn nor persist. |
| FR-28 | Must | A session that never migrated shall run and persist normally. |
| FR-29 | Should | The TUI shall offer `/cloud [host]`, `/cloud back`, `/cloud return`, `/cloud status`, and `/local`, shall run the matching CLI command between turns, and shall reattach at the new location. |
| FR-30 | Should | The TUI shall refuse a move or a return while the agent is mid-turn, and shall leave everything where it was. |
| FR-31 | Should | `jcode cloud sessions` shall upload, upload the latest, sync, list, verify, render a dashboard for, and view session transcripts through the private Jade helper, and shall pass the API token in the helper environment rather than on the command line. |
| FR-32 | Should | `jcode cloud sessions configure` shall persist the Jade defaults with owner-only file permissions, `jcode cloud sessions status` shall report them without printing the token, and `--clear` shall remove the config file. |
| FR-33 | Should | `jcode cloud sessions sync` shall skip unchanged sessions, shall honor `--since-days`, `--max`, `--min-interval-mins`, `--force`, and `--dry-run`, and shall not record sync state during a dry run. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Integrity | The system shall not lose a transcript message across a move or a return: the cloud copy shall be verified to hold the same session id, the same epoch, and the same message count as the local copy before ownership changes. |
| NFR-2 | Must | Isolation | At most one machine shall run turns for a given session at a time, enforced by the lease check before every turn, before every turn-loop iteration, and before every save. |
| NFR-3 | Must | Correctness | A return shall merge the cloud tree into the local tree with a real 3-way merge, so that edits made on either side during the migration survive, and a merge that cannot complete shall not modify the working tree. |
| NFR-4 | Must | Durability | The lease file shall be written to a temporary file and then renamed, so that a crash during the write cannot leave a corrupt lease. |
| NFR-5 | Must | Security | The system shall not persist secrets into the lease, the manifest, or the transcript, and shall not copy machine-local or secret environment variables. |
| NFR-6 | Must | Security | A session id used as a lease file name shall be restricted to ASCII alphanumerics, underscore, dash, and dot, and shall not start with a dot, so that a session id cannot escape the lease directory. |
| NFR-7 | Must | Operability | A failed move shall leave the local session usable: the previous lease shall be restored, the local transcript shall be untouched, and the failure shall name the stage that failed. |
| NFR-8 | Should | Performance | The transfer size shall stay proportional to the tracked source, because build output, dependency trees, and other ignored directories are never copied. |
| NFR-9 | Should | Compatibility | A cloud host whose jcode predates the move protocol shall be detected before any state changes, and the error shall name the host. |
| NFR-10 | Should | Compatibility | The transfer format shall carry a version number, and a host that does not support the incoming format shall refuse the move and name the version it expects. |
| NFR-11 | Should | Observability | The move and the return shall emit one progress line per stage, and shall emit none when `JCODE_CLOUD_QUIET` is set. |
| NFR-12 | Should | Operability | The `where` report shall show how far the local checkout has diverged from the last synchronized head, so the operator can tell whether local work is pending. |

## Constraints

- The transfer runs over SSH to the target host, so the target host must be reachable with key-based authentication in batch mode.
- The repository is restored at the same absolute path on the cloud host, because every path in the transcript must stay valid.
- The cloud host must run a jcode that understands the `cloud receive`, `cloud activate`, and `cloud export` subcommands.
- The transfer format version is currently 1, and the manifest carries it in every transfer.
- The lease lives on local disk under the jcode home, so a machine that loses its jcode home loses its proof of ownership.
- The `jcode cloud sessions` half talks to a private Jade helper that lives outside this repository.
- The managed AWS control plane described in `docs/JCODE_CLOUD_AWS.md` is a design document and is not part of this feature.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Move a live session to a cloud host
      Given a local session with a transcript, todos, and a git checkout
      When the operator runs `jcode cloud move --session session_abc --host cloud-e2e`
      Then the cloud host holds the transcript, the todos, and the repository state
      And the move reports the cloud host, the epoch, and the snapshot commit
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Refuse to move a session that already lives elsewhere
      Given a session whose lease names an away host
      When the operator runs `jcode cloud move`
      Then the move fails and names the away host
      And the message tells the operator to run `jcode cloud return` first
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Refuse to move a session that is mid-turn
      Given a session with a turn in flight
      When the operator runs `jcode cloud move`
      Then the move fails and says the session is mid-turn
      And the move proceeds when `--allow-active` is passed
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A dry run leaves the local session alone
      Given a local session and a reachable cloud host
      When the operator runs `jcode cloud move --dry-run`
      Then the cloud copy is staged and verified
      And no lease file is written locally
      And the local working tree and the local index are unchanged
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: The epoch increments on every move
      Given a session that has never moved
      When the session is moved to a cloud host
      Then the shipped transcript carries migration epoch 1
      And the next move of the same session ships epoch 2
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: The cloud host does not speak the move protocol
      Given a cloud host whose jcode does not know the `cloud receive` subcommand
      When the operator runs `jcode cloud move`
      Then the move fails before any state changes
      And the error names the host and points at `--remote-binary` or `JCODE_CLOUD_REMOTE_BINARY`
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: The snapshot captures the whole working tree
      Given a checkout with a committed change, a staged file, an untracked file, and an ignored file
      When the session is moved
      Then the snapshot commit holds the committed, staged, and untracked work
      And the ignored file is not in the snapshot
      And the local index and the local working tree are unchanged
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: The cloud checkout matches the local one
      Given a session moved from a checkout at `/work/repo` on branch `main`
      When the cloud host stages the move
      Then the repository exists at `/work/repo` on branch `main`
      And the uncommitted and untracked work is present
      And the git identity is set when the cloud checkout has none
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Only allowlisted environment and ignored files travel
      Given a local machine with `EDITOR` set, `DISPLAY` set, and a git-ignored `.env` file
      When the session is moved
      Then the manifest carries `EDITOR` and does not carry `DISPLAY`
      And the `.env` file is copied to the cloud host
      And no build output is copied
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: The transcript explains where the session now runs
      Given a session that is moved to a cloud host
      When the cloud host installs the transcript
      Then the transcript ends with a notice naming the source host, the target host, and the epoch
      And the notice states the repository path, the branch, and the uncommitted state
      And the notice names the build caches, the local MCP servers, and the background tasks that did not travel
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: The interrupted tool call is closed
      Given a transcript whose last assistant message has an unanswered tool use
      When the session is moved
      Then the shipped transcript carries a tool result for that tool use
      And the tool result says the call was interrupted by the move
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Ownership moves only after the cloud copy is verified
      Given a cloud host that stages the move but fails to activate
      When the operator runs `jcode cloud move`
      Then the move fails and the local lease is left as it was
      And the local session stays usable
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: The cloud checkout holds unrelated work
      Given a cloud checkout whose files match neither the snapshot jcode placed nor its HEAD
      When a move arrives for that path
      Then the receive is refused with a message that names the path
      And the existing files are left alone
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Return installs the cloud transcript locally
      Given a session that lives on a cloud host
      When the operator runs `jcode cloud return`
      Then the local transcript is the cloud transcript
      And the local journal file is gone
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Both sides keep their edits
      Given a local edit and a cloud edit to different parts of the same file
      When the operator runs `jcode cloud return`
      Then the merged file holds both the local edit and the cloud edit
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: The merge outcome is reported
      Given a session that is returned
      When the return finishes
      Then the report names one of no repository, unchanged, refs only, applied, or conflicts
      And a conflicts outcome names the conflicting files
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: A conflicting return keeps the working tree intact
      Given a local edit and a cloud edit to the same lines
      When the operator runs `jcode cloud return`
      Then the local file content is unchanged
      And the cloud work is reachable at `refs/jcode-cloud/session_abc/cloud`
      And the transcript tells the operator how to resolve the conflict
    ```

- [ ] **FR-18**

    ```gherkin
    @FR-18
    Scenario: A refs-only return does not touch the working tree
      Given a session that lives on a cloud host
      When the operator runs `jcode cloud return --refs-only`
      Then the cloud work is fetched into `refs/jcode-cloud/session_abc/cloud`
      And the local working tree is unchanged
    ```

- [ ] **FR-19**

    ```gherkin
    @FR-19
    Scenario: The transcript explains the return
      Given a session that is returned from a cloud host
      When the local transcript is installed
      Then the transcript ends with a notice naming the cloud host, the local machine, and the time
      And the notice states the merge outcome
      And the notice states that the cloud processes did not come back
    ```

- [ ] **FR-20**

    ```gherkin
    @FR-20
    Scenario: The local machine owns the session again
      Given a session that lives on a cloud host
      When the operator runs `jcode cloud return`
      Then the local lease names no away host
      And the epoch is one higher than it was before the move
    ```

- [ ] **FR-21**

    ```gherkin
    @FR-21
    Scenario: Refuse to return a session that never moved
      Given a session with no lease file
      When the operator runs `jcode cloud return`
      Then the return fails and says the session was never moved
    ```

- [ ] **FR-22**

    ```gherkin
    @FR-22
    Scenario: Where reports the location of a moved session
      Given a session that lives on a cloud host
      When the operator runs `jcode cloud where`
      Then the report names the session id, the location, the epoch, and the repository root
      And the report says how many commits the local checkout is ahead of the last synced head
    ```

- [ ] **FR-23**

    ```gherkin
    @FR-23
    Scenario: Attach resumes the session on the owning host
      Given a session that lives on a cloud host
      When the operator runs `jcode cloud attach`
      Then this terminal is replaced by a client that resumes the same session id on the owning host
    ```

- [ ] **FR-24**

    ```gherkin
    @FR-24
    Scenario: The target host is resolved from a flag or the environment
      Given no `--host` flag
      When the environment variable `JCODE_CLOUD_HOST` is set
      Then the move targets that host
      And with neither the flag nor the variable the move fails with a message that names both
    ```

- [ ] **FR-25**

    ```gherkin
    @FR-25
    Scenario: The lease records the ownership state
      Given a session that was moved to a cloud host
      When the local lease file is read
      Then it holds the epoch, the away host, the repository root, the last synced snapshot and head, and the update time
    ```

- [ ] **FR-26**

    ```gherkin
    @FR-26
    Scenario: The old machine cannot run the session after a move
      Given a session that was moved to a cloud host
      When an agent on the old machine tries to run a turn
      Then the turn is refused with a message that names the new host
    ```

- [ ] **FR-27**

    ```gherkin
    @FR-27
    Scenario: A stale copy cannot overwrite a returned transcript
      Given a session that was returned with a higher epoch
      When an in-memory copy at the old epoch tries to save
      Then the save is skipped and the on-disk transcript is unchanged
    ```

- [ ] **FR-28**

    ```gherkin
    @FR-28
    Scenario: A session that never migrated is unaffected
      Given a session with no lease file
      When the agent runs a turn and saves
      Then the turn runs and the transcript is written
    ```

- [ ] **FR-29**

    ```gherkin
    @FR-29
    Scenario: The TUI moves and returns the session
      Given an idle agent in the TUI
      When the operator types `/cloud cloud-e2e`
      Then the session is moved and the terminal reattaches on the cloud host
      And when the operator types `/local` the session comes back and the terminal resumes it locally
    ```

- [ ] **FR-30**

    ```gherkin
    @FR-30
    Scenario: The TUI refuses a move during a turn
      Given an agent that is mid-turn in the TUI
      When the operator types `/cloud`
      Then the TUI reports that the move happens between turns
      And nothing moves
    ```

- [ ] **FR-31**

    ```gherkin
    @FR-31
    Scenario: Uploading a session to Jade cloud storage
      Given a configured Jade helper
      When the operator runs `jcode cloud sessions upload session_abc.json`
      Then the helper is invoked with the session file
      And the API token is passed in the helper environment rather than on the command line
    ```

- [ ] **FR-32**

    ```gherkin
    @FR-32
    Scenario: Configuring the Jade defaults
      Given an empty Jade config
      When the operator runs `jcode cloud sessions configure --api-base https://jade.example --api-token-env JADE_TOKEN`
      Then the config file is written with owner-only permissions
      And `jcode cloud sessions status` reports the base URL and that a token is configured, without printing the token
      And `jcode cloud sessions configure --clear` removes the file
    ```

- [ ] **FR-33**

    ```gherkin
    @FR-33
    Scenario: Syncing is idempotent and throttled
      Given sessions that were already uploaded
      When the operator runs `jcode cloud sessions sync --all`
      Then the unchanged sessions are skipped
      And a run with `--min-interval-mins` inside the interval is skipped
      And a dry run reports the plan without uploading and without writing sync state
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: No transcript message is lost across a move
      Given a local session with 42 messages
      When the session is moved to a cloud host
      Then the cloud report states 42 messages and the same session id and epoch
      And the move is abandoned before ownership changes when the count differs
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: One machine runs the session
      Given a session that was moved to a cloud host
      When a turn is requested on the old machine and on the cloud host
      Then the request on the old machine is refused
      And the request on the cloud host runs
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: A merge that cannot complete leaves the tree alone
      Given a local edit and a cloud edit to the same lines
      When the operator runs `jcode cloud return`
      Then no conflict markers are written into the local files
      And the local file content is byte for byte what it was before the return
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: The lease is written atomically
      Given a session that is moved to a cloud host
      When the lease is written
      Then the lease file is created by renaming a temporary file into place
      And a reader never sees a partially written lease
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Secrets stay out of the moved state
      Given a local machine with a secret in its environment and a git-ignored `.env` file
      When the session is moved
      Then the manifest, the lease, and the transcript contain no environment secret
      And only the allowlisted environment variables are recorded
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: A hostile session id cannot escape the lease directory
      Given a session id of `../escape`
      When the lease is written
      Then the write fails with an invalid session id error
      And no file is created outside the lease directory
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: A failed move leaves the session local
      Given a cloud host that cannot be reached
      When the operator runs `jcode cloud move`
      Then the move fails and names the stage that failed
      And the local transcript and the local lease are unchanged
      And the session can still run a turn on this machine
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: The transfer skips build output
      Given a checkout with a large ignored build directory
      When the session is moved
      Then the transfer does not contain the build directory
      And the transfer size grows with the tracked source rather than with the build output
    ```

- [ ] **NFR-9**

    ```gherkin
    @NFR-9
    Scenario: An old cloud host is detected early
      Given a cloud host whose jcode predates the move protocol
      When the operator runs `jcode cloud move`
      Then the failure happens before any local or remote state changes
      And the error names the host
    ```

- [ ] **NFR-10**

    ```gherkin
    @NFR-10
    Scenario: An unsupported transfer format is refused
      Given a move package whose format version is not the one the host supports
      When the cloud host receives it
      Then the receive is refused and the expected format version is named
    ```

- [ ] **NFR-11**

    ```gherkin
    @NFR-11
    Scenario: The stages are visible unless quiet mode is on
      Given a move that runs to completion
      When the move prints its progress
      Then one line is printed for the prepare, transfer, verify, and commit stages
      And with `JCODE_CLOUD_QUIET` set no progress line is printed
    ```

- [ ] **NFR-12**

    ```gherkin
    @NFR-12
    Scenario: The divergence of the local checkout is visible
      Given a local checkout that is three commits ahead of the last synced head
      When the operator runs `jcode cloud where`
      Then the report says the local checkout is three commits ahead
    ```

## Conflicts

None identified yet.

## Open Questions

1. Should the cloud host lease the session for a fixed period, so that a host that dies mid-session releases the session automatically?
   Today the operator runs `jcode cloud return` by hand.
2. Should the ignored-file allowlist be configurable, and should the operator be warned that `.env` files are copied to the cloud host?
   Today the allowlist is a fixed constant in `src/cli/cloud_move.rs`.
3. Should a mid-turn move wait for the turn to finish instead of requiring `--allow-active`?
   Today the agent itself passes `--allow-active` when the operator types `/cloud` from inside a turn.
4. Should the managed AWS control plane in `docs/JCODE_CLOUD_AWS.md` replace the SSH transport for the move and return path?
   The document is a design direction and the control plane is not deployed.

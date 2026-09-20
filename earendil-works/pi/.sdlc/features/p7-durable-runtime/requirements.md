---
title: "Durable runtime"
status: done
---

# Requirements: Durable runtime

## Overview

`@earendil-works/pi-durable` provides the durable conversation, task, and document runtime for Pi.
It implements the Pico model in which a Session atomically commits immutable entries, full task records, and Chord-tracked documents.
The package currently ships the durable record contracts, the `Storage` persistence boundary, and the detached in-memory `MemoryStorage` reference implementation.
The root conversation always uses the reserved `ROOT_CONVERSATION_ID` (`1`), and fresh IDs are minted from `2` upward.
The normative design sequence lives in `packages/durable/docs/pico-v5.md`, `pico-v5-handoff.md`, and `pico-v5-chord-usage.md`.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Session implementers | A stable record and storage contract for building the Pico Session mutation line. |
| Storage backend authors | A conformance baseline (`MemoryStorage`) for serialization-backed stores. |
| Contributors | Typed record contracts that fail fast at compile time on invalid state transitions. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall model conversations as immutable records with an ID, an optional fork parent edge, and an optional task owner edge. |
| FR-2 | Must | The system shall model entries as immutable transcript events with kind, optional model messages, optional JSON data, optional head marker, optional context edits, and optional producing task ID. |
| FR-3 | Must | The system shall model host inputs through the queued, placed, done, and unanswered lifecycle states with conversation-scoped request ID deduplication. |
| FR-4 | Must | The system shall model tasks as pending, running, and terminal states with completed, failed, aborted, orphaned, and faulted outcomes. |
| FR-5 | Must | The system shall model document incarnations with session, conversation, and task scopes plus history and fork policies. |
| FR-6 | Must | The system shall expose a `Storage` boundary with atomic commit, global ID minting, conversation lookup and scan, entry lookup with commit sequence, head-marker search, fork-aware entry scan, task lookup and filtered scan, input lookup by ID and request key, and close. |
| FR-7 | Must | The system shall provide `MemoryStorage` as a detached in-memory `Storage` with atomic commits, sorted indexes, opaque cursors, fork-aware history scans, a single global ID namespace, and post-close rejection. |
| FR-8 | Must | The system shall reserve `ROOT_CONVERSATION_ID` (`1`) for the root conversation and start minted IDs at `2`. |
| FR-9 | Must | The system shall enforce omit and replace context-edit discriminators so omissions carry no messages and replacements always carry messages. |
| FR-10 | Should | The system shall expose pagination (`Page`, `Cursor`), scan filters (`EntryQuery`, `TaskQuery`), and the atomic `StorageWrite` table-mutation union. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | Commits shall be atomic so a failed batch persists none of its writes. |
| NFR-2 | Must | Security | Stored and returned values shall be detached clones that never pollute object prototypes. |
| NFR-3 | Must | Maintainability | The package shall use erasable TypeScript with top-level imports only and no `any`. |
| NFR-4 | Should | Performance | In-memory reads and scans shall use sorted-index seeks rather than full-table sorts. |

## Constraints

- `MemoryStorage` is a conformance reference, not a persistent backend.
- Storage trusts the owning Session for semantic validity of records, references, ancestry, and transitions.
- The package has no HTTP surface and therefore ships no `api.yaml`.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: create and read a forked conversation
      Given a storage with a root conversation
      When a child conversation with a parent edge is committed
      Then reading the child returns the exact parent edge
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: commit and read an immutable entry
      Given a storage with a root conversation
      When an entry with kind, model messages, and data is committed
      Then reading the entry returns the same kind, messages, and data with its commit sequence
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: advance an input through its lifecycle
      Given a queued input with a request ID
      When the input is replaced by placed and then done records
      Then lookups by ID and by request key return the latest record
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: run a task to a terminal outcome
      Given a pending task with a checkpoint
      When the task is replaced by running and then terminal records
      Then the stored task carries the terminal outcome and no live checkpoint
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: declare scoped document incarnations
      Given the document record contracts
      When a conversation document declares rewindable history with as-of fork
      Then the type system accepts it and rejects session documents with conversation policies
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: exercise the full storage boundary
      Given an empty storage
      When conversations, entries, tasks, and inputs are committed and scanned
      Then every lookup, filtered scan, and cursor page returns the committed records
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: scan deep fork history newest-first
      Given a grandchild conversation forked through two ancestor caps
      When entries are scanned newest-first with cursors
      Then results cross each ancestor cap in order and excluded entries never appear
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: reserve the root conversation ID
      Given a fresh storage
      When the first ID is minted and the root conversation is committed
      Then the minted ID is 2 and recommitting ID 1 is rejected
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: enforce context-edit discriminators
      Given the context-edit contracts
      When a replacement without messages or an omission with messages is assigned
      Then the type system rejects the assignment
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: paginate scans with opaque cursors
      Given three conversations in storage
      When the first page of size two is read and continued with its cursor
      Then the second page returns only the remaining conversation
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: roll back a failed mixed-table batch
      Given committed entry, task, and input records
      When a batch containing a duplicate conversation ID is committed
      Then the commit rejects and none of the batch writes are visible
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: resist prototype pollution through stored JSON
      Given an entry carrying `__proto__` and `constructor` keys
      When the entry is committed and read back twice
      Then the reads keep `Object.prototype` and the stored values stay unchanged
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: hold the erasable TypeScript boundary
      Given the package sources and tests
      When the root check runs
      Then no strip-only violations are reported for the package
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: seek sorted indexes on scan
      Given entries committed out of ID order
      When entries are scanned newest-first
      Then results arrive in ID order without caller-side sorting
    ```

## Conflicts

None identified yet.

## Open Questions

1. Which serialization-backed store becomes the first persistent `Storage` beyond `MemoryStorage`?
2. Should document deltas ship inside this package or stay in the Chord package with usage docs only?
3. Does the Session-level commit path need a published conformance suite shared by every backend?

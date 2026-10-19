---
title: "Memory and Recall"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Memory and Recall

## Overview

OpenClaw gives the assistant durable recall across conversations. Curated memory files live in the agent workspace (`MEMORY.md`, `USER.md`, and dated `memory/YYYY-MM-DD.md` notes), episodic notes and session transcripts are indexed into a SQLite-backed store, and prospective memory is held as standing intents. A searchable index combines hybrid vector search with SQLite FTS, and the Active Memory plugin runs a bounded pre-reply deep recall for eligible private conversations. Behind the model sits a dreaming consolidation loop with light, deep, and REM phases that promotes qualified short-term candidates into `MEMORY.md`. The write path is the trust boundary: every memory artifact records an origin class, and only content with authoritative trusted provenance is injected automatically. The system is selected by the `memory` plugin slot (default `memory-core`), and the bundled `memory-core`, `active-memory`, `memory-lancedb`, and `memory-wiki` plugins implement the product surface.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | The assistant remembers facts, decisions, and preferences across sessions and conversations, and can inspect, correct, or delete what it remembers |
| Model authors | Recall happens inside a bounded turn budget with a predictable cost, so recall never starves the reply |
| Operators | Index health, embedding provider readiness, and dreaming artifacts are inspectable and repairable from the CLI and the Gateway |
| Security reviewers | Untrusted content cannot be promoted into automatically injected memory, and the trust decision is recorded per chunk rather than inferred at read time |
| Plugin authors | A documented `memory` plugin slot and tool contract let alternative backends replace the built-in index without forking the host |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall resolve the canonical root memory file of a workspace to `MEMORY.md` and exclude the legacy `memory.md` name and the `.openclaw-repair/root-memory` directory from auxiliary workspace memory scans |
| FR-2 | Must | The system shall index workspace memory files and session transcripts into chunk rows that carry the source path, line range, content hash, embedding model, embedding vector, and per-chunk recall metadata |
| FR-3 | Must | The system shall answer a memory query by combining vector similarity with SQLite FTS keyword matching and merging the two ranked result sets into a single scored list |
| FR-4 | Must | The system shall record an origin class of `agent` or `untrusted` for every memory artifact write and persist it per indexed chunk, and shall treat a write that does not match the previously recorded content hash as `untrusted` |
| FR-5 | Must | The system shall expose the `memory_search`, `memory_get`, and `intent` agent tools through the memory plugin, and shall restrict the `intent` tool to owner-authorized senders |
| FR-6 | Must | The system shall persist recall, promotion, and dreaming events in a durable memory host event store keyed by workspace, with bounded per-event payloads |
| FR-7 | Must | The system shall run a dreaming consolidation loop with light, deep, and REM phases that scores short-term candidates against fixed thresholds and appends qualified candidates to `MEMORY.md` |
| FR-8 | Must | The system shall expose an `openclaw memory` CLI with `status`, `index`, `reset`, `search`, `forget`, `promote`, `promote-explain`, `rem-harness`, `rem-backfill`, and `session-backfill` subcommands |
| FR-9 | Must | The system shall expose Gateway RPC methods for memory search, memory retrieval, memory status, session backfill preview/apply/rollback, doctor memory repair actions, and memory import migrations |
| FR-10 | Should | The system shall store standing intents as prospective memory in SQLite, match them against an incoming turn by trigger keywords and scope, and inject the matched intent into the reply context |
| FR-11 | Should | The system shall run a bounded pre-reply deep recall through the Active Memory plugin for eligible private conversations, with a circuit breaker and a timeout that degrades to no recall rather than blocking the reply |
| FR-12 | Should | The system shall support remote embedding providers with a configurable base URL, API key, extra headers, and batched document upload, and shall fall back to a configured local embedding model |
| FR-13 | Should | The system shall let an operator delete derived memories and artifacts for selected sessions, hook sources, or participants, with a dry-run mode that reports without writing |
| FR-14 | May | The system shall support alternative memory backends through the `memory` plugin slot, including the bundled LanceDB backend and the wiki knowledge vault |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | A memory search shall honor the per-call search deadline, and a nested phase that owns its own budget shall be able to pause the deadline owner instead of consuming it |
| NFR-2 | Must | Availability | Every memory step on the reply path shall have a timeout or a fallback, so that a degraded or unavailable memory subsystem reduces recall quality without failing the turn |
| NFR-3 | Must | Security | The system shall inject memory content into the model context only when the recorded origin class is `owner` or `agent` |
| NFR-4 | Must | Durability | Index state, chunk provenance, entry origins, session tombstones, the embedding cache, and standing intents shall survive a gateway restart |
| NFR-5 | Should | Isolation | The system shall scope each agent's memory index and stores to that agent, and shall refuse reads of sessions that belong to another agent |
| NFR-6 | Should | Observability | The system shall expose index status, embedding provider readiness, and dreaming artifact health through `openclaw memory status` and the `doctor.memory.*` RPC methods |

## Constraints

- The memory system owns retrieval and persistence only. Context assembly and compaction are owned by the context engine, which is selected by the separate `plugins.slots.contextEngine` slot (default `legacy`).
- The memory slot and the context engine slot are mutually exclusive plugin slots: `plugins.slots.memory` defaults to `memory-core` and `plugins.slots.contextEngine` defaults to `legacy`.
- The write path is the trust boundary. Content-level scanning of memory is not used to detect poisoned facts, so trust is enforced at write time and gated structurally at promotion time.
- Scoring, thresholds, eligibility, matching, and lifecycle use fixed code rules. The language model is used only inside bounds that those fixed rules enforce.
- Memory state is stored in SQLite, not in new JSON, JSONL, or sidecar stores.
- Third-party and other bundled memory plugins receive the same Plugin SDK contract as the built-in plugin; the built-in index remains core-owned.

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
    Scenario: Canonical root memory file resolves to MEMORY.md
      Given a workspace that contains a regular file named MEMORY.md
      When the core resolves the canonical root memory path for that workspace
      Then the resolved path is the workspace MEMORY.md file
      And a symlink named MEMORY.md is not treated as the canonical root memory file
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Indexing a workspace memory file produces chunk rows with recall metadata
      Given a workspace with a memory file that contains two sections
      When the memory index is built for that agent
      Then each chunk row records its path, start line, end line, content hash, embedding model, and embedding
      And each chunk row has a matching recall metadata row that can hold an importance score between 1 and 10
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: A query returns merged vector and keyword hits
      Given an indexed memory corpus that contains a semantically related passage and an exact keyword passage
      When a search runs for a query matching the keyword passage
      Then the response reports the search mode as hybrid when the vector provider is enabled
      And the returned hits carry both a vector score and a text score
      And the hits are ordered by the merged score
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A write that does not match the recorded content hash is downgraded to untrusted
      Given a memory artifact whose recorded provenance is agent with hash H
      And a new write whose content-before hash differs from H
      When the write provenance is recorded
      Then the stored origin class for that artifact is untrusted
      And the chunk provenance row for the artifact carries an origin class from the owner, agent, untrusted, or system set
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: The memory tools are declared by the memory plugin
      Given the memory-core plugin is loaded
      When its manifest contracts are read
      Then the declared tools are intent, memory_get, and memory_search
      And the intent tool requires sender owner identity on Gateway-scoped surfaces, including on internal turns
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A recall event is stored and later read back
      Given a memory host event store for a workspace
      When a recall is recorded with a query and three results
      Then a memory.recall.recorded event is persisted with the query and the result count
      And an oversized result list is stored truncated while the aggregate result count stays exact
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: A deep dreaming phase promotes only qualified candidates
      Given short-term candidates with a weighted score below the configured deep dreaming minimum
      When the deep dreaming phase runs
      Then no candidate is appended to MEMORY.md
      And the phase outcome is recorded as a memory.dream.completed event
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: The memory CLI exposes the documented subcommands
      Given the memory-core plugin is installed
      When the CLI help for "openclaw memory" is printed
      Then the subcommands include status, index, reset, search, forget, promote, promote-explain, rem-harness, rem-backfill, and session-backfill
      And "openclaw memory search" without a query exits with an error naming the missing query
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Memory RPC methods are registered with operator scopes
      Given the gateway core method descriptors
      When the memory related methods are listed
      Then memory.search, memory.get, and memory.status require operator.read
      And memory.search.owner requires operator.admin
      And migrations.memory.apply requires operator.admin
      And the memory session backfill methods are registered by the memory plugin
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: A standing intent fires on a matching trigger
      Given an armed standing intent with trigger keywords and a sender scope
      When a turn arrives from the matching sender containing one of the trigger keywords
      Then the intent context is prepended to the reply context
      And the intent fire count is incremented
      And an intent whose status is cancelled is never matched
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: A slow recall subagent degrades to no recall
      Given Active Memory is enabled for a private conversation
      And the recall subagent exceeds the configured timeout
      When the turn proceeds
      Then the reply is still produced
      And the recall result reports an unavailable status with a timeout reason
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: A remote embedding provider batches document uploads
      Given a remote embedding provider with batch upload enabled
      When a document indexing run uploads its chunks
      Then the provider is called with a batched request for the document inputs
      And the returned vectors are stored in the embedding cache keyed by provider, model, provider key, and content hash
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: A dry run forget reports without deleting
      Given a memory store that contains artifacts derived from two sessions
      When "openclaw memory forget --session ses_9f2 --dry-run" runs
      Then the command prints the complete deletion report
      And no memory row is removed
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: The memory slot selects exactly one backend
      Given two installed memory plugins and an unset memory slot
      When the effective plugin ids are resolved
      Then the memory slot resolves to the default owner memory-core
      And setting the memory slot to a specific plugin id pins that plugin for the memory slot
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: A nested phase pauses the search deadline owner
      Given a memory search deadline owner with a running nested phase
      When the nested phase reports a pause and then a resume
      Then the deadline owner observes the pause on the first transition and the resume on the final transition
      And overlapping nested phases do not re-arm the budget early
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: An unavailable memory provider still answers the turn
      Given the memory provider cannot be acquired
      When a memory search request is handled
      Then the gateway responds with an unavailable error that names the cause
      And the calling agent turn is not aborted by the memory failure
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Untrusted content is excluded from automatic injection
      Given a search result whose provenance origin class is untrusted
      When the automatic recall eligibility check runs
      Then the entry is not eligible for automatic injection
      And an entry whose origin class is owner or agent is eligible
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Memory state survives a restart
      Given a gateway that has indexed memory and created a standing intent
      When the gateway process restarts
      Then the memory index revision, chunk provenance rows, entry origins, session tombstones, and standing intents are still present
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: A search cannot read another agent's session
      Given agent A and agent B with separate memory scopes
      When agent A requests a memory search that resolves a session owned by agent B
      Then the request is refused
      And a session belonging to agent A resolves normally
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Doctor reports memory and dreaming health
      Given a gateway with a memory index and a dream diary
      When the doctor.memory.status RPC method is called
      Then the response reports index status and the embedding provider state
      And the doctor.memory.dreamDiary method returns the dream diary entries for the resolved workspace
    ```

## Conflicts

None identified yet.

## Open Questions

1. The `memory.search.sources` schema accepts only `memory` and `sessions`, but the `active-memory` plugin and the LanceDB backend expose additional provider-side recall surfaces. The contract for a third source value is not written down.
2. The `CompactResult.result.sessionFile` field is marked deprecated in the context engine contract, but the memory-side backfill paths still reason about transcript file paths. A single storage-neutral locator contract for both features is not settled.
3. The standing intents table enforces a `cooldown_seconds` default of 86400 and a `max_fires` limit, but the product-facing rule for what a user sees when an intent is blocked by cooldown is not specified.

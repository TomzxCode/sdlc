---
title: "Context Engine and Compaction"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Requirements: Context Engine and Compaction

## Overview

The context engine owns what the model sees. OpenClaw defines a `ContextEngine` interface with a required core (`ingest`, `assemble`, `compact`) and an optional surface (`bootstrap`, `maintain`, `ingestBatch`, `afterTurn`, `commitTurn`, `prepareSubagentSpawn`, `onSubagentEnded`), and a registry that resolves exactly one engine per logical turn from the `plugins.slots.contextEngine` slot. The built-in `legacy` engine preserves the original behavior: ingest is a no-op, assembly passes through to the runtime sanitize/validate/limit pipeline, and compaction delegates to the built-in summarization runtime. A plugin engine can replace any of that, declare that it owns compaction, request a bounded context view, project its context into a persistent backend thread, and rewrite transcript entries through a runtime-provided helper. Failures are isolated: a throwing engine is quarantined for the process and the default engine takes over, so a broken plugin degrades context quality rather than failing the turn.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Their turn keeps working, context stays inside the model window, and a broken context plugin does not take the assistant offline |
| Plugin authors | A documented interface, a documented registration path, and a clear contract for which host parameters the engine receives |
| Operators | The active engine is discoverable, quarantined engines are visible, and the selection is a single config slot rather than a scattered flag |
| Model and provider owners | A provider-native compaction path is disabled exactly when an engine owns compaction, so the two never fight over the same context |
| Security reviewers | The write path for context is bounded: the host, not the engine, decides how much history reaches the model and how long a compaction may run |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall define a `ContextEngine` interface whose required members are `info`, `ingest`, `assemble`, and `compact`, and whose optional members are `bootstrap`, `maintain`, `ingestBatch`, `afterTurn`, `commitTurn`, `prepareSubagentSpawn`, `onSubagentEnded`, and `dispose` |
| FR-2 | Must | The system shall resolve exactly one context engine per logical turn from `plugins.slots.contextEngine`, and shall resolve the core-owned `legacy` engine when the slot is unset, empty, or set to `none` |
| FR-3 | Must | The system shall register the built-in `legacy` engine so that ingest returns `ingested: false`, assembly returns the input messages unchanged, and compaction delegates to the built-in runtime compactor |
| FR-4 | Must | The system shall quarantine a context engine that throws during a guarded invocation, fall back to the default engine for the rest of the process, and keep the first failure as the recorded reason |
| FR-5 | Must | The system shall bound the assembled model view so that the retained messages fit `agents.defaults.compaction.maxActiveTranscriptBytes` when that limit is configured, and shall drop older messages only when the byte budget is exceeded |
| FR-6 | Must | The system shall bound every compaction call with a finite safety timeout and shall hand the engine an abort signal that it can honor to cancel in-flight work |
| FR-7 | Must | The system shall evaluate the host capabilities an engine requires for a given operation before invoking it, and shall refuse the operation when the host does not advertise every required capability |
| FR-8 | Must | The system shall persist an accepted but unacknowledged turn in a durable context engine turn outbox, and shall settle that turn exactly once by its advancement key |
| FR-9 | Must | The system shall pass an engine only the host parameters that the engine declares in `info.acceptedHostParams`, and shall never inject an undeclared host field, with the compaction abort signal always preserved |
| FR-10 | Should | The system shall let an engine declare that it owns compaction, and shall then disable native provider compaction and stored checkpoint replay on the routes where the engine's assembly is authoritative, while leaving those routes unchanged for engines that do not own compaction |
| FR-11 | Should | The system shall support a projection lifecycle for persistent backend threads, letting an engine ask the host to inject the assembled context once for a stable epoch and then reuse the backend thread until that epoch changes |
| FR-12 | Should | The system shall report runtime settings to the engine, including the resolved model and provider, the prompt token budget, the selected engine id and its selection source, the execution host id, and the fallback or degraded reason |
| FR-13 | Should | The system shall support the optional subagent context hooks `prepareSubagentSpawn` and `onSubagentEnded`, and shall invoke the rollback handle returned by a preparation when the spawn fails after preparation succeeds |
| FR-14 | Should | The system shall let an engine rewrite transcript entries through a runtime-provided rewrite helper, so that the runtime remains the single owner of the on-disk session DAG |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | The assembled model view shall not exceed the configured maximum active transcript bytes, and the retained messages shall not exceed the model token budget |
| NFR-2 | Must | Availability | A context engine failure shall not fail the turn; the system shall fall back to the default engine, record the quarantine, and continue the reply |
| NFR-3 | Must | Durability | An accepted turn shall be committed at most once; a host retry that presents an already committed advancement key shall report `duplicate` and produce no additional effect |
| NFR-4 | Must | Isolation | Engine resources shall be retained for the lifetime of the logical turn that uses them and released when the turn ends, and a shared engine shall be disposed exactly once |
| NFR-5 | Should | Observability | The system shall expose the active engine selection and the quarantined engines through `openclaw doctor`, `openclaw status`, and `openclaw plugins list` and `openclaw plugins inspect` |
| NFR-6 | Should | Compatibility | The legacy engine shall preserve the pre-existing assembly, compaction, and transcript behavior so that an installation with no context engine plugin configured behaves as before |

## Constraints

- The context engine is not the memory system. Memory is selected by `plugins.slots.memory` (default `memory-core`) and provides search and retrieval; the context engine is selected by `plugins.slots.contextEngine` (default `legacy`) and controls what the model sees.
- The memory slot and the context engine slot are mutually exclusive plugin slots and are resolved independently.
- The default engine id `legacy` is core-owned. A plugin may not register an engine under that id.
- The host always bounds a compaction call with a finite safety timeout, and the engine's own estimate of assembled tokens never controls host request admission.
- The host owns the session DAG. An engine may request a transcript rewrite through the runtime helper, never by writing the session store directly.
- Engines that declare `turnAdvancementIdempotency: "atomic-idempotent-v1"` must implement `commitTurn` as one atomic write keyed by the advancement key.
- A failed commit stays queued in the outbox and is retried; a blocked row is terminal audit evidence and does not hold later same-session turns behind it.
- There is no dedicated `openclaw context` CLI and no dedicated `contextEngine.*` Gateway RPC method. Operators observe the engine through the config slot, `openclaw doctor`, and the plugin inspection commands.

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
    Scenario: A factory that does not implement the required members is rejected
      Given a context engine factory that returns an object without an assemble method
      When the registry validates the resolved engine
      Then the resolution fails with a message naming the missing assemble method
      And the same validation names a missing info id or info name
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: An unset slot resolves to the core-owned default engine
      Given a configuration with no plugins.slots.contextEngine value
      When the effective context engine is resolved
      Then the resolved engine id is legacy
      And a slot explicitly set to none also resolves to the default engine
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: The legacy engine delegates compaction to the runtime
      Given the built-in legacy context engine
      When ingest is called with one message
      Then the result reports that nothing was ingested
      And assemble returns the input messages unchanged
      And compact delegates to the built-in runtime compaction path
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: A throwing engine is quarantined and the default engine takes over
      Given a selected context engine that throws during assemble
      When the engine is invoked for a turn
      Then the error is recorded in the context engine quarantine list
      And the turn continues on the default legacy engine
      And a second failure of the same engine keeps the first recorded reason
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: The assembled view is bounded by the transcript byte limit
      Given an assembled context whose total bytes exceed the configured maximum active transcript bytes
      When the assembly is bounded
      Then the retained messages are the most recent ones that fit the byte limit
      And the retained view does not start with an orphaned tool result
      And the projection mode becomes thread_bootstrap with a bounded epoch fingerprint
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: A compaction that outlives the safety timeout is cancelled
      Given an engine whose compact method never resolves
      When the host compaction safety timeout fires
      Then the compaction call is aborted and the engine receives an aborted signal
      And the watchdog deadline is not extended by a progress report after the abort
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: An operation requiring a missing host capability is refused
      Given a context engine that requires the thread-bootstrap-projection capability for the agent-run operation
      And a host that does not advertise that capability
      When the agent-run operation is requested
      Then the request fails with a message naming the engine, the operation, and the missing capabilities
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: An unacknowledged accepted turn stays queued and settles once
      Given an engine that does not acknowledge an accepted turn
      When the outbox is drained
      Then the pending turn remains listed for its engine and session
      And after the engine acknowledges, the row is completed
      And a blocked row is not retried and does not hold later same-session turns behind it
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Only declared host parameters reach the engine
      Given a context engine that declares accepted host params sessionKey and runtimeContext
      When the host calls the engine with a sessionKey, a prompt, and a runtimeContext
      Then the engine receives the sessionKey and runtimeContext
      And the engine does not receive the prompt
      And the compaction abort signal is still delivered
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: An engine that owns compaction disables native compaction on its route
      Given a context engine that declares ownsCompaction true
      And a direct OpenAI API-key route using the openai-responses API
      When a request is prepared on that route
      Then native compaction and stored Responses checkpoint replay are disabled by default
      And an engine that does not own compaction leaves the default-on behavior unchanged
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: A thread-bootstrap projection injects the context once per epoch
      Given an engine whose assembly returns a thread_bootstrap projection with a stable epoch
      When consecutive turns run against the same backend thread
      Then the assembled context is injected once for that epoch
      And a changed epoch causes the backend thread to rotate
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Runtime settings describe the resolved engine and model
      Given a resolved engine and a resolved model
      When the runtime settings are built
      Then the settings report the selected engine id and its selection source
      And the settings report the requested and resolved model, the provider, and the prompt token budget
      And a degraded reason sets the runtime mode to degraded
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: A failed spawn rolls back the prepared subagent state
      Given an engine whose prepareSubagentSpawn returns a rollback handle
      And a subagent spawn that fails after preparation succeeded
      When the spawn is abandoned
      Then the engine's rollback handle is invoked
      And onSubagentEnded is notified with the end reason
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: A transcript rewrite goes through the runtime helper
      Given an engine that requests a transcript rewrite through the runtime context
      When the rewrite is applied
      Then the runtime reports the number of rewritten entries and the bytes freed
      And the engine does not write the session store directly
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: The bounded view respects the byte and token limits
      Given an assembled context of 100 messages and a maximum active transcript byte limit
      When the assembly is bounded
      Then the retained messages serialize to no more than the configured byte limit
      And the retained token estimate does not exceed the model token budget
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: An engine failure degrades the turn instead of failing it
      Given a selected context engine that throws during a lifecycle call
      When a model turn runs
      Then the turn completes on the default engine
      And the failure is visible in the context engine quarantine list
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: A repeated advancement key is committed only once
      Given an engine that committed a turn for an advancement key
      When the host retries the same advancement key
      Then the engine reports the status duplicate
      And no additional durable effect is produced
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: A shared engine is disposed exactly once
      Given two logical turns that share one engine instance
      When both turns end
      Then the engine is disposed once
      And both factory source claims are released
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: The active engine and its quarantines are observable
      Given a gateway with a selected context engine and one quarantined engine
      When the operator inspects the installation
      Then the doctor report names the selected engine and its host requirement inspection result
      And the status report lists the context engine quarantine entries
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: An installation without a context engine plugin behaves as before
      Given a configuration with no context engine plugin
      When a model turn runs and a manual compaction is requested
      Then the legacy engine serves the turn
      And the manual compaction produces the built-in summary result
    ```

## Conflicts

None identified yet.

## Open Questions

1. The `CompactResult.result.sessionFile` field is marked deprecated in favor of the typed `sessionTarget`, but shipped third-party engines still report rotation through the raw field. The removal window for the compat path is not written down.
2. The context engine slot has no dedicated `openclaw context` CLI and no dedicated Gateway RPC method, so a scripted operator must read the config slot to learn which engine is active. Whether a read-only inspection method should be added is undecided.
3. `info.ownsCompaction` currently disables native compaction only on the direct OpenAI API-key `openai-responses` route. The behavior on the Codex app-server harness, where Codex owns its own thread history and compactor, is documented as unchanged but the resulting interaction with an engine that declares compaction ownership is not specified.
4. The `context_engine_turn_outbox` table stores the full turn payload as JSON, and the recovery read is bounded at 20000 events and 8 MiB. The product behavior when a single turn exceeds that bound is not specified.

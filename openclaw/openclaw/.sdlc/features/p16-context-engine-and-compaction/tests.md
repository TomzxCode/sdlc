---
title: "Context Engine and Compaction"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Context Engine and Compaction

## Scope

This plan covers the context engine contract, the registry and its slot policy, failure quarantine, the host-side bounding and timeout controls, host parameter projection, host capability checks, runtime settings, and the durable turn outbox.

Covered:

- The `ContextEngine` contract, including the required members and the factory validation that rejects an invalid engine.
- Slot selection, the default engine, and the owner mapping from engine id to plugin.
- Quarantine, fallback, and the persisted quarantine health mirror.
- Bounded assembly, the compaction watchdog, the transcript byte limit, and abort recognition.
- Host capability evaluation, host parameter projection, and runtime settings.
- Resource lifetime for a logical turn, including shared engines and copied registry views.
- The durable context engine turn outbox.

Out of scope:

- The memory system, which owns retrieval and persistence and is selected by `plugins.slots.memory`.
- Provider request formatting and provider authentication.
- Session transcript storage and the session DAG format, which the runtime owns.
- The chat command reports (`/context list`, `/context detail`, `/context map`) and the `openclaw doctor` and `openclaw status` renderers, which consume engine state without adding engine behavior.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Bounded assembly of the model view | `src/context-engine/bounded-context.test.ts` | Displaced tool-call and tool-result occurrences are dropped together and the newest complete pair is retained; an oversized latest historical turn is omitted rather than sliced; required instructions are kept and the projection identity advances when the engine context changes |
| TC-2 | Host watchdog for a runtime compaction reached through an engine | `src/context-engine/delegate-watchdog.test.ts` | Plugin-owned work after the delegate stays inside one host window, and the watchdog deadline is not extended past the operation ceiling |
| TC-3 | Host capability evaluation | `src/context-engine/host-compat.test.ts` | An engine with no host requirements is allowed; a generic CLI host is rejected when the engine requires pre-prompt assembly; missing capabilities are evaluated without throwing; the Codex app-server and the OpenClaw embedded hosts satisfy pre-prompt assembly; the Codex app-server host satisfies thread-bootstrap projection |
| TC-4 | Host parameter projection | `src/context-engine/host-param-projection.test.ts` | Declared host parameters are projected for `commitTurn`; a validator-shaped engine failure is not retried; raw call identity is preserved despite a process quarantine |
| TC-5 | Quarantine health mirror | `src/context-engine/quarantine-health.test.ts` | A warning is produced when the persisted quarantine inventory cannot be read; an empty warm turn does not dispatch health cleanup again; empty health receipts are invalidated after worker and native registrations |
| TC-6 | Runtime settings | `src/context-engine/runtime-settings.test.ts` | The mode is `fallback` when the resolved model differs from the requested model; the mode is `degraded` when a degraded reason is present; the host and selection ids stay nullable when unknown |
| TC-7 | Slot selection with plugins disabled | `src/context-engine/registry.selection.test.ts` | The default slot is used while plugins are disabled; a plugin disable produces ordinary logical turns without registration or degradation warnings |
| TC-8 | Admitted engine metadata | `src/context-engine/registry.metadata.test.ts` | The admitted byte budget is retained across separate core and SDK module instances, so the transcript byte limit resolves identically in both |
| TC-9 | Factory admission failure | `src/context-engine/registry.factory-admission.test.ts` | A host admission failure propagates without quarantining an uncalled factory, in both the closed-scope and the released-source mode, and the same registration stays usable for a fresh caller |
| TC-10 | Copied registry view resources | `src/context-engine/registry.copied-view-resources.test.ts` | An uncovered view is not treated as a retired donor's owner after a failed dependency |
| TC-11 | Fallback factory resources | `src/context-engine/registry.fallback-resources.test.ts` | Foreground factory resources are released after a lazy fallback in the rejected-factory, primary-failure, and shared modes, and the fallback engine's own resources are released too |
| TC-12 | Logical turn resource retention | `src/context-engine/registry.logical-turn-resources.test.ts` | A shared engine is disposed once while both factory source claims are released |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-13 | Engine contract, registry, and fallback behavior | `src/context-engine/context-engine.test.ts` | `delegateCompactionToRuntime` reuses the legacy runtime bridge; runtime identity is normalized after host projection omits the caller key; agent context passes through delegated memory prompt assembly, and an inactive memory prompt path contributes nothing; async memory state is prepared before context-engine prompt rendering; a registration from a different owner is rejected; the default engine id is reserved even in an empty builder registry; repeated baseline transcript-host selection stays stable after the turn starts; disposal happens once after retained turn work rejects; configured and fallback disposal are bounded in parallel; a started engine operation is not replayed and the configured engine is retried next turn; an incompatible fallback host is rejected after the logical turn starts; a missing or invalid requested engine falls back to the default engine; fallback initialization is coalesced across concurrent lifecycle failures; a legacy resolver fence failure routes through normal quarantine; a missing-engine quarantine is cleared when the plugin registers later; a cancelled compaction is not quarantined; quarantine clearing is deferred for builder-context direct registrations; a missing default engine throws; a default engine that fails contract validation propagates the error; registrations are shared across bundle chunks and concurrent registration |
| TC-14 | Durable turn outbox settlement | `src/agents/harness/context-engine-turn-outbox.test.ts` | An accepted turn is enqueued with a unique advancement key, an acknowledged turn is completed, a failed commit stays queued and is retried, and a blocked row is terminal and does not hold later same-session turns behind it |
| TC-15 | Agent harness context engine lifecycle | `src/agents/harness/context-engine-lifecycle.test.ts` | Runtime settings pass through a configured engine across the lifecycle hooks; an oversized assembly is bounded without changing the stored messages; the authoritative history survives an assembly that mutates and then throws; bootstrap maintenance runs for an existing session that has no `bootstrap` method; context ingestion does not advance for a yielded turn |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-16 | Chat-facing context reporting and manual compaction | `src/auto-reply/reply/commands-context-report.ts` and `src/auto-reply/reply/commands-compact.ts` | `/context list` returns a short breakdown, `/context detail` returns the per-file, per-tool, per-skill, system prompt, and compactable transcript counts, and `/compact` routes the manual-compact operation to the selected engine |
| TC-17 | Operator visibility of the selected engine and its quarantines | `src/commands/doctor/shared/context-engine-host-compat.ts` and `src/status/status-plugin-health.ts` | Doctor names the selected engine and reports the host requirement inspection result, including the warning when the engine plugin failed to load or is registered for read-only discovery, and the status report lists the context engine quarantine entries |
| TC-18 | Compaction through a real Gateway with the Codex app-server harness | `test/e2e/qa-lab/runtime/gateway-compaction-state.fixture.ts`, `test/e2e/qa-lab/runtime/gateway-compaction-provider.fixture.ts`, `test/e2e/qa-lab/runtime/gateway-compaction-abort.ts`, `test/e2e/qa-lab/runtime/gateway-codex-heartbeat-compaction.ts` | A compaction over a real Gateway child commits the summarized history, keeps the original rows, preserves the replacement writer, and settles the run. The abort scenario proves that a cancelled compaction leaves the original rows uncommitted and does not quarantine the engine |
| TC-19 | Provider-side compaction replay on the OpenAI Responses route | `test/gateway-openai-compaction-replay.e2e.test.ts` | A compaction checkpoint written by the provider runtime is replayed on the next embedded turn, so the persisted provider state is not lost when the engine does not own compaction |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-20 | A plugin registers an engine under the default id `legacy` | The registration is refused and the existing core owner is reported |
| TC-21 | The default engine itself is not registered | Resolution throws rather than silently running without an engine |
| TC-22 | The default engine fails contract validation | The validation error propagates instead of being swallowed as a plugin failure |
| TC-23 | A compaction is cancelled by the host abort signal | The rejection is recognized as an abort and the engine is not quarantined |
| TC-24 | The selected engine id matches the plugin id but the plugin is disabled | The slot preference is preserved and the legacy engine is used, without a degradation warning |
| TC-25 | An engine requests a transcript rewrite that cannot be applied | The runtime reports the failure through the rewrite result and the session DAG is left unchanged |
| TC-26 | A logical turn is disposed while retained work is still pending | Disposal is bounded, happens once, and the retained resources are released |
| TC-27 | The persisted quarantine inventory is unreadable | A warning is produced and the authoritative in-process quarantine still applies |
| TC-28 | A read-only discovery registration is resolved | The discovery factory is not constructed and the engine is not quarantined |

## Test Infrastructure

- An in-process plugin registry fixture (`src/context-engine/registry.test-support.ts` and `src/context-engine/registry-resources.test-support.ts`) that registers engines with controllable factories and disposal behavior.
- A `withPluginRuntimeRegistryScope` helper so each test resolves against its own registry instead of the ambient one.
- An `AsyncWorkScope` for the admission and disposal ordering assertions.
- SQLite fixtures for the agent database that holds `context_engine_turn_outbox`.
- A `LegacyContextEngine` subclass with overridden `assemble` and `dispose` for the failure and lifetime scenarios.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-13, TC-20, TC-21, TC-22 |
| FR-2 | TC-7, TC-13, TC-24 |
| FR-3 | TC-13, TC-16 |
| FR-4 | TC-11, TC-13, TC-23, TC-27, TC-28 |
| FR-5 | TC-1, TC-8, TC-17 |
| FR-6 | TC-2, TC-18, TC-23 |
| FR-7 | TC-3, TC-13 |
| FR-8 | TC-14 |
| FR-9 | TC-4, TC-13 |
| FR-10 | TC-13, TC-19 |
| FR-11 | TC-1, TC-3 |
| FR-12 | TC-6, TC-13 |
| FR-13 | TC-13, TC-16 |
| FR-14 | TC-25 |
| NFR-1 | TC-1, TC-8 |
| NFR-2 | TC-9, TC-11, TC-13, TC-23 |
| NFR-3 | TC-13, TC-14 |
| NFR-4 | TC-10, TC-12, TC-26 |
| NFR-5 | TC-17 |
| NFR-6 | TC-13, TC-16 |

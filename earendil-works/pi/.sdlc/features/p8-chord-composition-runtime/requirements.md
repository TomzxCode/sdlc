---
title: "Chord Composition Runtime"
status: done
session_link: "backfilled-from-shipped-code"
---

# Requirements: Chord Composition Runtime

## Overview

Chord is a standalone application-composition runtime that assembles applications from plugins whose facets declare, provide, and consume typed services with replicated state across local and remote boundaries.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Application host authors | Compose worker, TUI, and WebUI environments from one plugin model |
| Plugin authors | Declare services once and run each facet where it belongs |
| Agent developers | Build extensions without owning transport, framing, or lifecycle |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall let plugins declare facets as synchronous setup units that state the services they provide and require. |
| FR-2 | Must | The system shall validate the complete facet dependency graph and reject missing dependencies, duplicate providers, cycles, and asynchronous setup. |
| FR-3 | Must | The system shall support singleton services with one provider behind a stable consumer-facing handle. |
| FR-4 | Must | The system shall support keyed services with dynamically spawned and retired per-key instances. |
| FR-5 | Must | The system shall bind services after graph validation, activate providers before consumers, and dispose resources in reverse dependency order. |
| FR-6 | Must | The system shall provide replicated state where producers mutate a tracked state proxy and publish while consumers receive immutable values. |
| FR-7 | Must | The system shall expose remotely consumable services through an application-supplied transport carrying strict-JSON calls and subscriptions. |
| FR-8 | Must | The system shall track and coalesce JSON delta operations with durable base batches and validation of untrusted operations at apply time. |
| FR-9 | Should | The system shall reload facets by replacing singletons without an unavailable interval and giving keyed replacements fresh generations. |
| FR-10 | Should | The system shall bundle facet entries into content-addressed artifacts and load them with integrity verification in an isolated module scope. |
| FR-11 | Should | The system shall provide a Go-like context carrying cancellation and invocation-scoped values through operations. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Portability | The system shall ship as a standalone package with no dependency on any other Pi workspace package. |
| NFR-2 | Must | Security | The system shall validate every value crossing the remote boundary as strict JSON. |
| NFR-3 | Should | Reliability | The system shall mark replicas unready on disconnect or replacement and rehydrate them before delivering new updates. |
| NFR-4 | Should | Performance | The system shall flush at most one decoded operation batch per publication with independent path-codec state per client stream. |

## Constraints

- Chord prescribes no transport, framing, routing, or application wire envelope.
- Process-local services accept unrestricted contracts and are never published remotely.
- Chord never installs dependencies and never runs package lifecycle scripts.

## Acceptance Criteria

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: facet declares its service shape synchronously
      Given a plugin facet with a synchronous setup function
      When the host collects provided and required services
      Then the facet shape is registered without running any async work
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: invalid dependency graphs are rejected before binding
      Given facets with a missing dependency, a duplicate provider, or a dependency cycle
      When the host validates the complete dependency graph
      Then activation fails with a descriptive error and no service is bound
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: singleton facade survives provider replacement
      Given a consumer holding a singleton service handle
      When the providing facet is replaced by a reload
      Then the same handle routes to the new provider without an unavailable interval
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: keyed instances spawn and retire independently
      Given a keyed service owned by one facet
      When the owner spawns two keys and retires one
      Then observers see both instances appear and only the retired key close
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: activation and disposal follow dependency order
      Given a provider facet and a consumer facet depending on it
      When the host activates the graph and later disposes it
      Then the provider activates first and disposes last
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: published mutations reach subscribers as immutable values
      Given a producer mutating its tracked state proxy
      When the producer publishes with a context
      Then each subscriber receives a complete immutable value reflecting the mutation
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: remote calls cross an application-supplied transport
      Given a remotely exposable service and a transport adapter
      When a consumer invokes a method and subscribes to its state
      Then arguments, results, snapshots, and updates all cross as strict JSON
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: deltas coalesce and untrusted ops are validated
      Given tracked plain JSON with buffered mutations
      When the tracker flushes and a replica applies the batch
      Then the replica converges and malformed operations are rejected
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: reload keeps singleton consumers connected
      Given active singleton consumers on a running host
      When a candidate generation activates and cuts over successfully
      Then singleton handles stay connected while keyed replacements get fresh generations
    ```

- [x] **FR-10**

    ```gherkin
    @FR-10
    Scenario: bundles verify integrity and isolate module scope
      Given a content-addressed facet bundle built from a plugin package
      When the loader verifies SHA-256 and compiles the entry in a VM scope
      Then corrupt entries fail to load and host externals resolve through the restricted require
    ```

- [x] **FR-11**

    ```gherkin
    @FR-11
    Scenario: cancellation and values flow through context
      Given an operation invoked with a cancellable context carrying a typed value
      When the caller cancels or the callee reads the value
      Then waiting stops promptly and the callee observes the carried value
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: package boundary stays Pi-free
      Given the Chord package source tree
      When the boundary test scans its imports and file references
      Then no import reaches any other Pi workspace package or file outside Chord
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: non-JSON values are rejected at the boundary
      Given a candidate value containing undefined, functions, or other non-JSON data
      When the adapter validates it with the strict-JSON check
      Then the value is rejected without normalization
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: disconnected replicas rehydrate before updating
      Given a subscribed replica whose provider disconnects
      When the provider returns and publishes new state
      Then the replica reports unready until rehydration completes
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: one publication produces one batch per stream
      Given a producer with two remote client streams on one state
      When the producer publishes once
      Then each stream encodes exactly one operation batch with its own path-codec state
    ```

## Conflicts

None identified yet.

## Open Questions

1. Should symmetric RPC peers ship as the first optional transport over the remote-service boundary?
2. Should the reserved `$chord.*` service namespace become a permanent part of the Chord contract?
3. Do delta batches need a canonical or minimal form beyond the current convergence guarantee?

---
title: "Telemetry Contracts"
status: done
session_link: "none"
---

# Requirements: Telemetry Contracts

## Overview

The pi-telemetry package defines vendor-neutral telemetry contracts for explicit callback-managed spans.
TelemetryContext exposes startSpan for creating child spans around callbacks.
TelemetrySpan exposes addEvent and setAttributes and setStatus for recording diagnostics.
Typed schema utilities define serializable span and event and attribute vocabularies with inferred TypeScript types.
Noop and in-memory backends provide passive defaults and process-local reference recording without exporters.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Pi package maintainer | Needs explicit telemetry propagation without global state. |
| Backend adapter author | Needs a stable contract with observable conformance semantics. |
| Application operator | Needs diagnostic spans without business behavior changes. |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide TelemetryContext with startSpan that admits the callback synchronously exactly once. |
| FR-2 | Must | The system shall provide TelemetrySpan with setAttributes that merges attribute bags with last-defined-wins semantics. |
| FR-3 | Must | The system shall provide TelemetrySpan with addEvent that records ordered named events with attributes. |
| FR-4 | Must | The system shall provide TelemetrySpan with setStatus that records explicit ok or error outcomes with last-write-wins semantics. |
| FR-5 | Must | The system shall treat normal completion as ok and throws or rejections as errors unless an explicit status was set. |
| FR-6 | Must | The system shall provide a shared noop context that invokes callbacks without inspecting or retaining payloads. |
| FR-7 | Must | The system shall provide an in-memory context that records detached span snapshots in span-start order. |
| FR-8 | Must | The system shall provide serializable schema helpers that infer exact start and end and event attribute types. |
| FR-9 | Must | The system shall provide a typed span starter that binds a parent context to one or more schema vocabularies. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Reliability | The system shall keep recording methods synchronous and passive and non-throwing. |
| NFR-2 | Must | Portability | The system shall remain runtime-neutral without ambient context APIs. |
| NFR-3 | Should | Performance | The system shall keep noop overhead negligible by sharing one frozen inert span. |
| NFR-4 | Must | Security | The system shall restrict attribute values to primitive scalars and arrays and avoid sensitive payloads by default. |

## Constraints

- The package shall not include exporters or global current-span state.
- Backend-specific identifiers and buffering and flushing belong to adapters.
- Schema objects shall remain JSON-serializable data without runtime validation.

## Acceptance Criteria

Every FR and NFR has at least one executable criterion below.

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: synchronous single admission preserves result
      Given a fresh TelemetryContext
      When startSpan is called with a callback returning a value
      Then the callback runs synchronously exactly once and the returned promise resolves with the same value
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: attribute merging keeps last defined values
      Given a span with start attributes
      When setAttributes is called repeatedly with overlapping keys
      Then later defined values replace earlier values and undefined entries are ignored
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: events are recorded in call order
      Given an open span
      When addEvent is called twice with distinct names
      Then the snapshot contains both events in call order with their attributes
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: explicit status uses last-write-wins semantics
      Given an open span
      When setStatus is called with error and then with ok
      Then the final snapshot status is ok
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: throw without explicit status becomes error
      Given a fresh TelemetryContext
      When the callback throws synchronously without setting a status
      Then the returned promise rejects with the identical value and the span status is error
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: noop context stays inert
      Given the shared noop context
      When startSpan runs nested callbacks that record attributes and events
      Then values pass through unchanged and nested spans reuse the same frozen span
    ```

- [x] **FR-7**

    ```gherkin
    @FR-7
    Scenario: in-memory context returns detached snapshots
      Given an in-memory context with one completed span
      When getSpans is called and the caller mutates the result
      Then a subsequent getSpans call still returns the original recorded values
    ```

- [x] **FR-8**

    ```gherkin
    @FR-8
    Scenario: schema helper infers exact attribute types
      Given a serializable schema with closed string sets
      When TypeScript infers start attributes for a declared span
      Then missing required attributes and unknown keys and out-of-set values are rejected at compile time
    ```

- [x] **FR-9**

    ```gherkin
    @FR-9
    Scenario: typed starter binds children to their parent span
      Given a typed starter over operation and request schemas
      When an operation span starts a nested request span
      Then the recorded child carries the parent identifier and the callback result passes through
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: unreadable payloads never break business work
      Given recording payloads that throw on property reads
      When setAttributes and addEvent and setStatus are called with those payloads
      Then no call throws and the business callback still executes exactly once
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: explicit propagation works without ambient state
      Given parent spans passed only as context arguments
      When nested and concurrent children run
      Then parentage is recorded correctly without ambient context APIs
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: noop path performs no recording work
      Given the shared noop context
      When many spans run with attributes and events
      Then callbacks execute directly against one shared frozen span
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: attribute surface stays primitive-only
      Given the AttributeValue type definition
      When a schema declares attribute types
      Then only scalar and array primitives are expressible without payload fields
    ```

## Conflicts

No conflicts were identified.

## Open Questions

No open questions remain because the contracts are implemented and documented.

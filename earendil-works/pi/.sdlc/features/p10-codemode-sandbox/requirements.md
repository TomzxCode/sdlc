---
title: "Codemode Sandbox"
status: done
session_link: "none"
---

# Requirements: Codemode Sandbox

## Overview

Model-written JavaScript must run with the least possible capability, so the package executes scripts in a QuickJS VM compiled to WebAssembly where calling injected tools is the only capability.
Nested tool calls never enter the LLM context, and only the script output and return value do.
The coding agent exposes this sandbox as its built-in `codemode` tool, and the package has no pi dependencies so any host can expose its own functions to model-written scripts.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Coding agent (`codemode` tool) | Batch, chain, and filter nested tool calls in one model step without flooding context |
| Model authors | A small stable script surface (`tools`, `ALL_TOOLS`, `text`, `image`, `exit`, `store`, `load`) with TypeScript declarations |
| Cloudflare deployers | A non-blocking sandbox Worker plus Durable Object for agent sessions |
| External hosts | A dependency-free sandbox for exposing remote APIs, MCP servers, or application services to scripts |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall execute model-written JavaScript in a fresh QuickJS VM per execution where calling injected tools is the only host capability. |
| FR-2 | Must | The system shall provide one script environment on every sandbox: `tools.<name>(args)` plus `tools["<name>"]`, `ALL_TOOLS`, `text(value)`, `image(urlOrItem)`, `exit()`, `console.*`, `store(key, value)`/`load(key)`, host `globals`, top-level `await`, and `return`. |
| FR-3 | Must | The system shall offer three sandboxes with one API, one script environment, and one result format: `CodemodeSandbox` on a worker thread per execution, `RemoteCodemodeSandbox` in another isolate, and `InlineCodemodeSandbox` on the calling thread. |
| FR-4 | Must | The system shall accept an optional first-line `// @options:` directive carrying `max_output_tokens` and `timeout_ms`, and reject empty input, invalid JSON, unknown fields, a directive without code, and a directive on any line but the first. |
| FR-5 | Must | The system shall return a `CodemodeResult` that never rejects for script failures, with `ok`, `value` or `error` (`script`, `timeout`, `aborted`, `sandbox`), `output` kept for failed executions, per-call `calls`, and `storeWrites` on success. |
| FR-6 | Must | The system shall implement `store`/`load` as a caller-owned snapshot: the caller passes `options.store`, the script reads copies synchronously, `store(key, undefined)` deletes, and a successful result reports `{ set, delete }`. |
| FR-7 | Must | The system shall render TypeScript declarations for tools and globals from their descriptions and JSON schemas so a model description can embed them. |
| FR-8 | Must | The system shall support deterministic runs via `start()` with fixed `startedAt`, `seed`, caller-answered calls, ordered result delivery, a VM fingerprint, and a monotonic clock. |
| FR-9 | Should | The system shall deploy on Cloudflare Workers via a stateless sandbox Durable Object in a separate Worker plus an inline constructor, with server-side caps on interrupt budget and memory. |
| FR-10 | Should | The system shall let the coding agent wrap `execute()` as an agent tool whose nested calls run through the agent tool pipeline while only script output reaches the model. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | The system shall isolate scripts so nested tool calls and their results never enter the LLM context, and scripts reach no timers, `fetch`, `process`, `require`, modules, or `WebAssembly`. |
| NFR-2 | Must | Reliability | The system shall enforce a per-execution deadline (default 300000 ms, `Infinity` disables it) and fail scripts that wait on a promise nothing can settle instead of hanging. |
| NFR-3 | Must | Capacity | The system shall bound script output to `MAX_OUTPUT_CHARS` (16 Mi) and `MAX_OUTPUT_ITEMS` (100000), failing with a `RangeError` past either limit. |
| NFR-4 | Must | Capacity | The system shall cap VM heap use via `memoryLimitBytes` (Cloudflare default 32 MiB) and surface overuse inside the script as `InternalError: out of memory`. |
| NFR-5 | Must | Portability | The system shall keep zero pi dependencies (only `quickjs-wasi`) and a `/portable` entry with no Node imports for Workers, Durable Objects, and browsers. |
| NFR-6 | Should | Performance | The system shall keep worker-thread startup including VM creation around 20 ms and keep pure computation interruptible via a poll-counted interrupt budget. |

## Constraints

- `CodemodeSandbox` requires Node or Bun (worker threads plus reading the QuickJS binary from disk).
- Cloudflare Workers cannot compile WebAssembly at runtime, so the Cloudflare entry relies on the module Wrangler compiles.
- QuickJS is an interpreter, so heavy pure computation in scripts is slower than in V8.

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
    Scenario: Script calls an injected tool and returns a value
      Given a sandbox with a `read` tool
      When the script awaits `tools.read` and returns the parsed name
      Then the result is ok with the tool return value and one call recorded
    ```

    ```gherkin
    @FR-1
    Scenario: Script cannot reach host capabilities
      Given a sandbox with default configuration
      When the script reads `typeof process`, `typeof fetch`, and `typeof require`
      Then all three are `undefined` and the result is ok
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Output helpers collect ordered items
      Given a sandbox with no tools
      When the script calls `text`, `console.log`, and `image` with a base64 data URL then returns
      Then `result.output` holds the text, console, and image items in order
    ```

    ```gherkin
    @FR-2
    Scenario: exit ends the script successfully
      Given a sandbox with a tool that was never called
      When the script emits output then calls `exit()`
      Then the result is ok with `value` undefined and the output kept
    ```

    ```gherkin
    @FR-2
    Scenario: Tool names map to identifiers
      Given a tool named `my-tool`
      When the script calls it as `tools.my_tool`
      Then the host tool executes and the call is recorded under `my-tool`
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: All sandboxes share one result shape
      Given the worker, inline, and remote sandboxes with the same tool
      When the same script runs on each
      Then every result has `ok`, `output`, `calls`, and the same value
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Options line parses and preserves line numbers
      Given source starting with `// @options: {"timeout_ms": 30000}`
      When `parseCodemodeSource` runs
      Then options carry `timeoutMs` 30000 and the code keeps its line count
    ```

    ```gherkin
    @FR-4
    Scenario: Misplaced options line is rejected
      Given source with the options line on line 3
      When `parseCodemodeSource` runs
      Then it throws `CodemodeSourceError`
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Thrown script error keeps partial output
      Given a sandbox with no tools
      When the script calls `text("part")` then throws
      Then the result has `ok` false, kind `script`, and the partial output
    ```

    ```gherkin
    @FR-5
    Scenario: Abort reports kind aborted
      Given a running execution with an abort signal
      When the signal fires
      Then the result has `ok` false and kind `aborted`
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Store round trip reports writes
      Given a sandbox executed with a store snapshot
      When the script loads a counter, increments it, and stores it
      Then the result reports the key under `storeWrites.set`
    ```

    ```gherkin
    @FR-6
    Scenario: Loaded values are copies
      Given a store holding an object
      When the script mutates the loaded object without storing
      Then the result reports no writes for that key
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Declarations render tool signatures
      Given a tool with a description and input and output schemas
      When `renderDeclarations` runs
      Then the output declares an async function with a doc comment
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Same seed and answers replay the same calls
      Given a script started twice with the same `startedAt` and `seed`
      When the host answers both runs with the same ordered results
      Then both runs issue identical calls and output
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Remote sandbox caps client limits
      Given a Durable Object with a lower `maxInterruptBudget` than the client asks for
      When a runaway script executes remotely
      Then the execution fails as `timeout` at the server cap, not the client value
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Nested calls stay out of model context
      Given the agent `codemode` tool over two nested tools
      When a script calls both and returns a summary
      Then the model result holds the summary and output, not the raw nested results
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Failed nested call rejects inside the script
      Given a tool that throws
      When the script awaits it without catching
      Then the script fails with kind `script` carrying the tool message
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Deadline stops a spinning script
      Given a sandbox with a short `timeoutMs`
      When the script spins without calling tools
      Then the result has kind `timeout`
    ```

    ```gherkin
    @NFR-2
    Scenario: Stalled await fails fast
      Given a script awaiting a promise nothing can settle with no tool pending
      When the VM detects the stall
      Then the execution fails right away instead of hanging
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Output flood fails with RangeError
      Given a script appending text past `MAX_OUTPUT_CHARS`
      When it crosses the limit
      Then the execution fails with a `RangeError` even if the script catches
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Heap overuse fails inside the script
      Given a sandbox with a tiny `memoryLimitBytes`
      When the script allocates past it
      Then the script observes `InternalError: out of memory`
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: Portable entry imports without Node
      Given a runtime without `node:*` built-ins
      When `@earendil-works/pi-codemode/portable` is imported
      Then the import succeeds and both portable sandboxes construct
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: Runaway compute ends on interrupt budget
      Given an inline sandbox with a small interrupt budget
      When the script loops without yielding
      Then the result has kind `timeout` within the test deadline
    ```

## Conflicts

None identified yet.

## Open Questions

None.
The behavior above is reverse-engineered from the shipped implementation, so no open question blocks anything.

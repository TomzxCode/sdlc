---
title: "Codemode Sandbox"
status: done
session_link: "none"
---

# Test Plan: Codemode Sandbox

## Scope

The plan covers the script environment, the three VM placements, the source format, declarations, deterministic runs, and the Cloudflare remote from the actual vitest suites under `packages/codemode/test/`.
It excludes the coding-agent `codemode` tool behavior, which belongs to the consumer package, and live Cloudflare deployments, which the in-process remote double stands in for.
Suite counts at sync time: `sandbox.test.ts` 54 tests, `deterministic.test.ts` 24, `declarations.test.ts` 17, `portable.test.ts` 7, `source.test.ts` 5.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Source options line parses | `// @options: {"max_output_tokens": 2000, "timeout_ms": 30000}` plus code | Options `{ maxOutputTokens: 2000, timeoutMs: 30000 }`, code line count unchanged |
| TC-2 | Source rejects bad input | Empty input, invalid JSON, unknown field, options-only input, misplaced options line | `CodemodeSourceError` for each |
| TC-3 | Schema renders primitives, unions, arrays, tuples | JSON schemas with literals, bounds, `$defs` refs | One-line TypeScript with sorted properties and constraint tags |
| TC-4 | Renderer budgets long types to unknown | Oversized schema | Constraint tags dropped first, then the type becomes `unknown` |
| TC-5 | Recursive references stop | Self-referential schema | Renders as `unknown` without hanging |
| TC-6 | Tool sample and declarations render | Tools with normalized identifiers and namespaced globals | Valid `declare const` block with doc comments |
| TC-7 | Comment terminators escaped | Description containing `*/` | Escaped so the declaration block stays valid |
| TC-8 | Store and load names reserved | Tool or global named `store` or `load` | Constructor rejects the registration |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | Script execution across all backends | Worker, inline, and in-process remote sandboxes | Return value after JSON round trip, top-level await, ordered text/image/console output |
| TC-10 | Tool calling across all backends | Registered tools including `my-tool` | Async calls, concurrent calls, identifier normalization, `ALL_TOOLS` listing, unknown-tool rejection with close-match hint |
| TC-11 | Tool errors become catchable script errors | Tool that throws | Script `Error` with the same message; uncaught failure keeps partial output |
| TC-12 | Unawaited calls abort on return | Script returning with a pending call | Call reported `cancelled` and its signal aborts |
| TC-13 | Store snapshot and writes | Snapshot passed via `options.store` | `load` reads copies, `store` reports `{ set, delete }`, oversized writes throw `RangeError` with an explanation |
| TC-14 | `exit()` keeps output and writes | Script calling `exit()` after output and a store write | Ok result with `value` undefined |
| TC-15 | Stack traces map to script lines | Syntax error and thrown error | `codemode.js:<line>` frames in V8 `Name: message` style without prelude frames |
| TC-16 | Deterministic replay on worker and remote | Same `startedAt`, `seed`, and ordered results | Identical calls and output; fingerprint before any call; monotonic clock enforced |
| TC-17 | Out-of-order delivery applies in seq order | Delayed first result on the remote transport | VM waits for the missing number and applies results strictly 1, 2, ... |
| TC-18 | Abort ends a run uncatchably | Aborted `start()` run signal | Run fails with an error the script cannot catch and `finished` is set |
| TC-19 | `execute()` stays non-deterministic | Default execution | Real clock and real randomness observed |
| TC-20 | Inline budget ends compute as timeout | Small `interruptBudget` with spinning scripts | Kind `timeout` for `while (true) {}` and `while (true) await null` |
| TC-21 | Remote runs tools in the caller | In-process recording remote | Script runs remotely, tools execute locally, output is batched not per-line |
| TC-22 | Remote caps client limits | Client asking above server `maxInterruptBudget` | Server cap wins and runaway compute fails as `timeout` |
| TC-23 | Caller abort stops the remote | Aborted remote execution | Remote told to stop; failing or vanishing remote reports kind `sandbox` |
| TC-24 | Embedded sources parse as JavaScript | `raw-worker.ts` fixture | Fixture content parses with the project parser |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-25 | Agent-style tool round trip | Expose agent tools to a sandbox, run a script calling two of them, collect output and return value | Ok result whose output plus JSON return value carry the composed answer |
| TC-26 | Cloudflare example wiring | Follow `examples/cloudflare` agent plus sandbox Workers with per-session object naming | Scripts execute in the sandbox Worker and tool calls resolve in the agent Worker |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-27 | Stalled await with nothing pending | VM reports stalled | Execution fails immediately instead of hanging |
| TC-28 | Non-serializable return value | Script returns a non-JSON value | Kind `script` error |
| TC-29 | Non-Error throw | Script throws a string | Reported with the thrown value and script stack |
| TC-30 | Invalid `text()`/`image()` arguments | Bad shapes and remote URLs | Script-side rejection; large and wrapped base64 accepted |
| TC-31 | Unserializable call answer in a run | Host delivers a value JSON cannot carry | Call stays waiting for a valid answer |
| TC-32 | Duplicate result number or unknown call id | Host mis-delivers | `deliver` throws for the reused `seq` and the unknown call |
| TC-33 | Non-finite clock value | Host delivers `NaN` as `now` | `deliver` throws and the clock stays monotonic |
| TC-34 | Register and unregister between executions | Tool added then removed | Later scripts cannot call it; earlier call records unchanged |

## Test Infrastructure

- Vitest suites under `packages/codemode/test/` with a backend matrix (worker, inline, in-process remote) in `sandbox.test.ts` and `deterministic.test.ts`.
- The in-process remote double structured-clones every message, matching Workers RPC semantics.
- `test/fixtures/raw-worker.ts` fixture for the embedded worker source parse test.
- No live Cloudflare account or deployment is needed for any suite.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-9, TC-10, TC-24 |
| FR-2 | TC-9, TC-10, TC-11, TC-14, TC-15, TC-30 |
| FR-3 | TC-9, TC-20, TC-21 |
| FR-4 | TC-1, TC-2 |
| FR-5 | TC-11, TC-12, TC-14, TC-15, TC-23, TC-27, TC-28, TC-29 |
| FR-6 | TC-13, TC-34 |
| FR-7 | TC-3, TC-4, TC-5, TC-6, TC-7 |
| FR-8 | TC-16, TC-17, TC-18, TC-19, TC-31, TC-32, TC-33 |
| FR-9 | TC-21, TC-22, TC-23, TC-26 |
| FR-10 | TC-25 |
| NFR-1 | TC-10, TC-11 |
| NFR-2 | TC-20, TC-27 |
| NFR-3 | TC-13 |
| NFR-4 | TC-22 |
| NFR-5 | TC-9, TC-21 |
| NFR-6 | TC-20 |

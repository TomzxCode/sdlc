---
title: "LSP Integration"
status: done
---

# Test Plan: LSP Integration

## Scope

Built-in server catalog matching, spawn behavior (enabled/disabled/out-of-instance), config overrides and custom servers, lifecycle/init, diagnostics formatting, and event publication.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Does not spawn builtin LSP for files outside instance | File outside instance dir | No `lsp.spawn` call |
| TC-2 | Does not spawn builtin LSP when LSP is unset | Supported file inside instance, no config | No spawn |
| TC-3 | Would spawn builtin LSP when `lsp: true` | Supported file inside instance | Spawn called for matching server |
| TC-4 | Would spawn builtin LSP when config object provided | Supported file inside instance, `lsp: {}` | Spawn called |
| TC-5 | Publishes `lsp.updated` after custom LSP initialization | Custom server config, initialize completes | `lsp.updated` event published |
| TC-6 | `init()` completes without error | Instance with LSP enabled | No error |
| TC-7 | `status()` returns empty array initially | Fresh instance | Empty |
| TC-8 | `diagnostics()` returns empty object initially | Fresh instance | Empty object |
| TC-9 | `hasClients()` false for `.ts` files when LSP unset | Instance, test.ts | false |
| TC-10 | `hasClients()` true for `.ts` files when `lsp: true` | Instance with `lsp: true`, test.ts | true |
| TC-11 | `hasClients()` keeps built-ins when config object provided | Instance with `lsp: {}`, test.ts | true |
| TC-12 | `hasClients()` false for files outside instance | File outside instance | false |
| TC-13 | `workspaceSymbol()` returns empty array with no clients | Query on fresh instance | Empty array |
| TC-14 | `definition()` returns empty array for unknown file | Unknown file | Empty array |
| TC-15 | Diagnostic formatter maps severities and positions | Diagnostic with severity/range | `SEVERITY [line:col] message` |
| TC-16 | Diagnostic report caps errors per file | > 20 errors | 20 shown plus `... and N more` |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-17 | Sends `workspace/workspaceFolders` request to server | Client connected | Request handled |
| TC-18 | Handles `client/registerCapability` and `client/unregisterCapability` | Client connected | Requests handled without error |
| TC-19 | `initialize` does not overclaim unsupported diagnostics capabilities | Client connected | Capabilities reflect supported subset |
| TC-20 | `workspace/configuration` returns one result per requested item | Client connected | Array with one result per item |
| TC-21 | Sends ranged `didChange` for incremental sync servers | Text change on file | Correct incremental change sent |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-22 | Server executable missing or spawn fails | Error contained; agent process unaffected |
| TC-23 | JDTLS with non-standard root layout | Root resolved correctly (see `jdtls-root.test.ts`) |
| TC-24 | Unicode or unusual file paths | Client still matched and spawned correctly |
| TC-25 | Auto-download disabled via `OPENCODE_DISABLE_LSP_DOWNLOAD` | No download attempted |

## Test Infrastructure

- Mock/spied `lsp.spawn` via `Process.spawn` overrides.
- `it.instance` fixtures with `lsp` config variations.
- Fake JSON-RPC servers responding to `initialize`, `workspace/*`, and `client/*` requests.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-3, TC-4 |
| FR-02 | TC-3, TC-4 |
| FR-03 | TC-5, TC-11 |
| FR-04 | TC-2, TC-9 |
| FR-05 | TC-1, TC-12 |
| FR-06 | TC-5 |
| FR-07 | TC-15, TC-16 |
| FR-08 | TC-13, TC-14, TC-17, TC-20 |
| FR-09 | TC-25 |
| FR-10 | TC-7, TC-9, TC-10, TC-11 |
| NFR-01 | TC-22 |
| NFR-02 | TC-9, TC-10, TC-11 |
| NFR-04 | TC-16 |

## Test Files

- `packages/opencode/test/lsp/index.test.ts`
- `packages/opencode/test/lsp/lifecycle.test.ts`
- `packages/opencode/test/lsp/client.test.ts`
- `packages/opencode/test/lsp/launch.test.ts`
- `packages/opencode/test/lsp/jdtls-root.test.ts`

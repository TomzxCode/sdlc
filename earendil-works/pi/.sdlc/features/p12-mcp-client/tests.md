---
title: "MCP Client"
status: done
session_link: "none"
---

# Test Plan: MCP Client

## Scope

Unit and transport tests in `packages/mcp/test/` cover the client core, content conversion, stdio, Streamable HTTP, and OAuth against the in-memory pair and fixtures.
Extension adapter coverage lives with the coding-agent MCP extension tests for tools, resources, and config.
Conformance against the official suite runs through `packages/coding-agent/test/mcp-conformance/` and the `mcp-conformance` CI job.
Out of scope are legacy HTTP+SSE servers, sampling, and tasks, which the client core does not implement.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Initialize negotiates the protocol version | `initialize` result selecting `2025-11-25` over the in-memory pair | Client records server info and sends `notifications/initialized` |
| TC-2 | Unsupported version fails connect | `initialize` result with an unknown version | Connect rejects and the client ends closed |
| TC-3 | Paginated tool listing collects every page | Two `tools/list` pages joined by `nextCursor` | All tools returned in order |
| TC-4 | Duplicate pagination cursor is rejected | Repeated `nextCursor` across pages | Listing throws a duplicate-cursor error |
| TC-5 | Tool result validation tolerates missing content | `tools/call` result with only `structuredContent` | Result defaults `content` to an empty array |
| TC-6 | Content conversion maps blocks to model content | Text, image, embedded resource, audio, and resource-link blocks | Text and images pass through while audio and links become placeholders |
| TC-7 | Request timeout rejects and cancels remotely | Unanswered `tools/call` with a short timeout | Timeout error plus `notifications/cancelled` to the server |
| TC-8 | Progress renews the timeout and fires the callback | `notifications/progress` during a long call | Callback fires and the request survives one timeout window |
| TC-9 | Roots provider answers server requests | `roots/list` from the server side | Configured roots returned |
| TC-10 | In-memory pair isolates messages | One JSON-RPC message sent client to server | Equal structured-cloned copy delivered exactly once |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-11 | Stdio server lifecycle | Fixture server command from `packages/mcp/test/fixtures` | Connect, list, call, and spec-ordered process-group shutdown all succeed |
| TC-12 | Streamable HTTP session with resume | HTTP fixture server with event IDs | Dropped response stream reconnects with `Last-Event-ID` and the call completes |
| TC-13 | OAuth PKCE flow against a protected server | Authorization and token endpoints plus loopback callback | Bearer-authenticated calls succeed after discovery, registration, and code exchange |
| TC-14 | Concurrent 401s share one refresh | Expired token with two racing calls | Exactly one token refresh serves both retries |
| TC-15 | MCP tool naming stays unique | Two tools sanitizing to the same `mcp__server__tool` name | Distinct registered names with a hash suffix routing to the right tools |
| TC-16 | Exposure routing reaches tools correctly | Servers configured as codemode, deferred, direct, and hidden | Each tool resolves only through its configured reach path |
| TC-17 | Resource tools round-trip listings and reads | Connected server with resources | `list_mcp_resources` plus `read_mcp_resource` return contents and JSON payloads |
| TC-18 | Startup does not hang on a slow direct server | Direct server that never finishes connecting | First prompt proceeds after the startup wait and tools register on connect |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-19 | Official conformance suite stays at baseline | Run `npm run test:mcp-conformance` across negotiated protocol versions | No baseline-passing check fails and no unlisted failure appears |
| TC-20 | OAuth sign-in through the real connection path | Run the conformance client with the simulated browser against auth scenarios | Protected scenarios complete including step-up re-sign-in within the retry limit |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-21 | `resources/list` page ends with a null cursor | Pagination stops after that page without an extra request |
| TC-22 | Resource without a name | Listing uses the URI as the name |
| TC-23 | Oversized model text beyond 20 KiB | Middle-cut rendering plus a temp file holding the full text |
| TC-24 | Inbound message beyond 16 MiB | Message rejected before delivery to the client |
| TC-25 | Unknown response ID arrives | Client emits an error without disturbing pending requests |

## Test Infrastructure

- `createInMemoryTransportPair()` from `@earendil-works/pi-mcp/testing` for deterministic client and adapter tests.
- Fixture servers under `packages/mcp/test/fixtures` plus `helpers.ts` for stdio and HTTP harnesses.
- Pinned official conformance suite `@modelcontextprotocol/conformance@0.2.0-alpha.11` with `baseline.json` locking known results.
- The `mcp-conformance` job in `.github/workflows/ci.yml` running `npm run test:mcp-conformance` on every main push and pull request.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2 |
| FR-2 | TC-3, TC-4 |
| FR-3 | TC-5 |
| FR-4 | TC-17 |
| FR-5 | TC-9 |
| FR-6 | TC-7, TC-8 |
| FR-7 | TC-25 |
| FR-8 | TC-11 |
| FR-9 | TC-12 |
| FR-10 | TC-10 |
| FR-11 | TC-6 |
| FR-12 | TC-13, TC-14, TC-20 |
| FR-13 | TC-15 |
| FR-14 | TC-15 |
| FR-15 | TC-16 |
| FR-16 | TC-18 |
| FR-17 | TC-18 |
| FR-18 | TC-17 |
| FR-19 | TC-18 |
| FR-20 | TC-16 |
| NFR-1 | TC-19 |
| NFR-2 | TC-19 |
| NFR-3 | TC-7 |
| NFR-4 | TC-23 |
| NFR-5 | TC-24 |
| NFR-6 | TC-18 |

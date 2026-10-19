---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### TC-4, the duplicate-cursor case, has no test
- **Evidence:** `packages/mcp/src/client.ts:370-372` throws `MCP ${method} returned duplicate cursor: ${cursor}` when a page repeats a cursor.
- **Evidence:** `packages/mcp/test/client.test.ts` has 13 cases, and none of them repeats a `nextCursor`.
- **Artifact says:** TC-4 "Duplicate pagination cursor is rejected | Repeated `nextCursor` across pages | Listing throws a duplicate-cursor error".
- **Required change:** Add the test, or record TC-4 as an uncovered case.
- **Blocking:** yes, a documented test case does not exist.

### TC-10, the in-memory isolation case, has no test
- **Evidence:** `packages/mcp/src/transports/in-memory.ts:19-25` copies each message with `structuredClone` before delivering it, and delivers it once through `queueMicrotask`.
- **Evidence:** There is no `packages/mcp/test/in-memory.test.ts`, and no case in `packages/mcp/test/client.test.ts` asserts the copy or the absence of shared references.
- **Artifact says:** TC-10 "In-memory pair isolates messages | One JSON-RPC message sent client to server | Equal structured-cloned copy delivered exactly once".
- **Required change:** Add the test, or record TC-10 as an uncovered case.
- **Blocking:** yes, a documented test case does not exist.

### TC-25, the unknown response id case, has no test
- **Evidence:** `packages/mcp/src/client.ts:481-489` emits `Received response for unknown MCP request ${id}` through the error listeners and leaves pending requests untouched.
- **Evidence:** `packages/mcp/test/client.test.ts:228-249` covers transport errors, not an unknown response id, and no other test in `packages/mcp/test/` sends a response with an unknown id.
- **Artifact says:** TC-25 "Unknown response ID arrives | Client emits an error without disturbing pending requests".
- **Required change:** Add the test, or record TC-25 as an uncovered case.
- **Blocking:** yes, a documented test case does not exist.

### The coding-agent MCP test files are not named anywhere in the plan
- **Evidence:** `packages/coding-agent/test/mcp-command.test.ts` (8 cases, the `pi mcp` command), `packages/coding-agent/test/mcp-extension.test.ts` (28 cases, config validation, tool naming, result conversion, connections and the servers section), `packages/coding-agent/test/mcp-manager-view.test.ts` (2 cases, regression #10565), `packages/coding-agent/test/mcp-oauth-refresh.test.ts` (11 cases), `packages/coding-agent/test/mcp-oauth-store.test.ts` (3 cases, regression #10252), `packages/coding-agent/test/suite/agent-session-mcp.test.ts` (44 cases), `packages/coding-agent/test/suite/agent-session-mcp-oauth.test.ts` (9 cases) and the helper `packages/coding-agent/test/suite/mcp-oauth-server.ts`.
- **Artifact says:** The scope section mentions "the coding-agent MCP extension tests" generically and names only `packages/coding-agent/test/mcp-conformance/`.
- **Required change:** Name these files in the scope and add the test cases they carry, especially the `pi mcp` command, the manager view, the credential store and the session-level exposure routing, which no TC covers today.
- **Blocking:** yes, the plan does not account for the test files that materially cover the feature.

### TC-20 claims a passing step-up scenario that the baseline records as failing
- **Evidence:** `packages/coding-agent/test/mcp-conformance/baseline.json:300-316` lists `auth/scope-retry-limit` with `pi-client` under `failing`, and `packages/coding-agent/test/mcp-conformance/README.md:43` states that the client gives up by design there.
- **Evidence:** `packages/coding-agent/test/mcp-conformance/baseline.json:282-299` lists `auth/scope-step-up` with every check passing.
- **Artifact says:** TC-20 "OAuth sign-in through the real connection path | Run the conformance client with the simulated browser against auth scenarios | Protected scenarios complete including step-up re-sign-in within the retry limit".
- **Required change:** State that `auth/scope-step-up` passes and that `auth/scope-retry-limit` is a baselined failure by design, so the plan does not promise a passing case the suite does not deliver.
- **Blocking:** yes, the expected outcome contradicts the committed baseline.

### TC-11 overstates the stdio coverage
- **Evidence:** `packages/mcp/test/stdio.test.ts:9-28` covers connect, list, call and stderr capture, and `packages/mcp/test/stdio.test.ts:30-63` covers killing a server that ignores shutdown, including its children.
- **Evidence:** The stdin-close, then SIGTERM, then SIGKILL ordering in `packages/mcp/src/transports/stdio.ts:152-179` is not asserted by any test.
- **Artifact says:** TC-11 "Stdio server lifecycle | Fixture server command from `packages/mcp/test/fixtures` | Connect, list, call, and spec-ordered process-group shutdown all succeed".
- **Required change:** Narrow TC-11 to what the tests assert, or add a test for the shutdown ordering.
- **Blocking:** no, advisory.

### TC-24 is asserted for the SSE transport only, and with a custom limit
- **Evidence:** The 16 MiB default is `packages/mcp/src/transports/transport.ts:3`, and `packages/mcp/test/streamable-http.test.ts:106-120` asserts the cap with a custom `maxEventBytes: 256`, not with the default.
- **Evidence:** The stdio path checks the same limit at `packages/mcp/src/transports/stdio.ts:187` and `packages/mcp/src/transports/stdio.ts:196`, and no test in `packages/mcp/test/stdio.test.ts` drives an oversized frame.
- **Artifact says:** TC-24 "Inbound message beyond 16 MiB | Message rejected before delivery to the client".
- **Required change:** Say that the cap is asserted for the Streamable HTTP transport with a custom limit, or add a case that exercises the 16 MiB default.
- **Blocking:** no, advisory.

### TC-21 asserts a null cursor that no test uses
- **Evidence:** `packages/mcp/src/client.ts:106` treats a `null` cursor as the end of pagination, and the only pagination test ends the pages with an empty-string cursor (`packages/mcp/test/client.test.ts:113`).
- **Artifact says:** TC-21 "`resources/list` page ends with a null cursor | Pagination stops after that page without an extra request".
- **Required change:** Align the case with the empty-string cursor the test uses, or add a null-cursor case.
- **Blocking:** no, advisory.

## Open questions

- None. Every claim in the plan could be checked against a test file, a fixture, or the conformance baseline.

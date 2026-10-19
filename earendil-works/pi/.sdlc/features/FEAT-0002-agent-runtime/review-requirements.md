---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf83563ffeRejJwzXWhPYVQK
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### Requirements point at `@earendil-works/pi-durable` and a `./node` entrypoint the package does not have
- **Severity:** blocking
- **Evidence:** `packages/agent/package.json:25-28` — the only runtime dependencies are `@earendil-works/pi-ai` 1.3.0 and `typebox` 1.3.27, so the package never consumes `@earendil-works/pi-durable`.
- **Evidence:** `packages/agent/package.json:8-14` — the `exports` map contains only `"."` and `"./package.json"`, so there is no `./node` entrypoint.
- **Evidence:** `packages/agent/CHANGELOG.md:31` — the 1.0.0 breaking change removed `AgentHarness`, the durable runtime, compaction, skills, and the `./node`, `./harness/*`, `./experimental/pico3` subpaths.
- **Artifact says:** `requirements.md:36` (FR-09), `requirements.md:39-41` (FR-12, FR-13, FR-14), `requirements.md:53` (NFR-05) require the system to "consume" durable sessions, compaction, skills, branch summarization, system-prompt building, and the `NodeExecutionEnv` from `@earendil-works/pi-durable`, and `requirements.md:52` (NFR-04) places Node-specific code "behind the `./node` entrypoint".
- **Required change:** rewrite FR-09, FR-12, FR-13, FR-14, NFR-04, and NFR-05 as negative requirements, for example "the package shall not provide durable sessions, compaction, skills, branch summarization, or a Node execution environment, those live in `@earendil-works/pi-durable`", and drop the `./node` entrypoint reference from NFR-04.

### The `AgentHarness` name is still used for a symbol that no longer exists
- **Severity:** advisory
- **Evidence:** `packages/agent/src/index.ts:1-5` — the barrel exports only `agent.ts`, `agent-loop.ts`, `proxy.ts`, `stream-fn.ts`, and `types.ts`, none of which define `AgentHarness`; a repo-wide search finds `AgentHarness` only in `packages/agent/CHANGELOG.md` history and in `packages/coding-agent/CHANGELOG.md`.
- **Evidence:** `packages/durable/src/index.ts:41` — the durable runtime exports the harness as `Harness`, not `AgentHarness`.
- **Artifact says:** `requirements.md:18` (stakeholders) asks for "a reliable `Agent`/`AgentHarness`", and `requirements.md:102` (Open Questions) asks about "the long-term relationship between `AgentHarness` and the coding-agent's own `AgentSession`".
- **Required change:** replace `AgentHarness` with `Harness` (from `@earendil-works/pi-durable`) or drop the name, and reword the open question so it does not depend on a symbol that was removed in 1.0.0.

### FR-05 does not state the tool-call pipeline order
- **Severity:** blocking
- **Evidence:** `packages/agent/src/agent-loop.ts:694-706` — `prepareToolCallArguments` applies the optional `tool.prepareArguments` shim to the raw arguments.
- **Evidence:** `packages/agent/src/agent-loop.ts:726-727` — the shim output is what `validateToolArguments` validates, so the prepared arguments are validated, not the raw ones.
- **Evidence:** `packages/agent/src/agent-loop.ts:728-756` — `beforeToolCall` receives the validated arguments and may mutate that object in place; the mutated object is what `execute` receives (`packages/agent/src/agent-loop.ts:768`, `packages/agent/src/agent-loop.ts:833-834`) and it is not revalidated.
- **Evidence:** `packages/agent/src/agent-loop.ts:870-902` — `afterToolCall` applies field-by-field overrides to `content`, `details`, `structuredContent`, `isError`, `usage`, and `terminate`; replacing `content` without `structuredContent` drops the structured content.
- **Artifact says:** `requirements.md:32` (FR-05) says only "validate tool arguments before execution and support `beforeToolCall`/`afterToolCall` hooks that can block, override, or terminate a tool call".
- **Required change:** state the pipeline explicitly: resolve the tool by name, apply `prepareArguments`, validate the prepared arguments with TypeBox, run `beforeToolCall` (which may block, and may mutate the validated arguments without revalidation), execute, then apply `afterToolCall` overrides field by field.

### FR-05 does not state the batch termination rule
- **Severity:** blocking
- **Evidence:** `packages/agent/src/agent-loop.ts:690-692` — `shouldTerminateToolBatch` returns true only when the batch is non-empty and every finalized result has `terminate === true`.
- **Evidence:** `packages/agent/src/agent-loop.ts:272` — the batch result decides `hasMoreToolCalls`, so a partially terminating batch keeps the loop running.
- **Artifact says:** `requirements.md:32` (FR-05) says the hooks can "terminate a tool call", which reads as a per-call effect.
- **Required change:** state that a tool batch ends the loop early only when every finalized result in the batch sets `terminate: true`.

### No requirement covers the refusal to execute tool calls from a truncated response
- **Severity:** blocking
- **Evidence:** `packages/agent/src/agent-loop.ts:267-270` — when the assistant message has `stopReason === "length"`, tool calls go to `failToolCallsFromTruncatedMessage` instead of `executeToolCalls`.
- **Evidence:** `packages/agent/src/agent-loop.ts:478-503` — every tool call in such a message becomes an error result and is never executed, because streamed arguments may be truncated.
- **Artifact says:** `requirements.md:29` (FR-02) and `requirements.md:32` (FR-05) describe tool calls being executed; nothing states the length-truncation guard.
- **Required change:** add a requirement that tool calls from an assistant message with `stopReason: "length"` are reported as error results without being executed.

### No requirement covers announcing tool loadout changes to the model
- **Severity:** blocking
- **Evidence:** `packages/agent/src/agent-loop.ts:333-363` — `declareToolChanges` diffs the executable `context.tools` against the tools the transcript declares and returns a system message carrying `toolsAdded`/`toolsRemoved`, merging it into a pending system message when one exists.
- **Evidence:** `packages/agent/src/agent-loop.ts:110` and `packages/agent/src/agent-loop.ts:211` — the diff runs before the initial request and before every subsequent request.
- **Artifact says:** no requirement or acceptance criterion mentions tool declaration changes.
- **Required change:** add a requirement that the runtime announces the difference between the executable tool set and the transcript's declared tools to the model in a system message before each request.

### Acceptance criteria do not cover every requirement the artifact lists
- **Severity:** advisory
- **Evidence:** `requirements.md:62` states "Every FR and NFR shall have at least one acceptance criterion", but the criteria at `requirements.md:66-93` cover only FR-02, FR-04, FR-05, FR-06, FR-07, NFR-01, and NFR-02.
- **Artifact says:** the acceptance criteria list leaves FR-01, FR-03, FR-08, FR-10, FR-11, NFR-03, NFR-04, and NFR-05 without a criterion.
- **Required change:** add criteria for the uncovered requirements, or relax the statement at `requirements.md:62`.

## Open questions
- Should the `prepareArguments` shim still be supported, given that it is the only place raw provider arguments are rewritten before validation?
- Does the runtime still need to announce tool loadout changes through the transcript, or could the executable set be declared directly in the request context?

---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf83563ffeRejJwzXWhPYVQK
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The provider and session hook surface lives in this package, not in `@earendil-works/pi-durable`
- **Severity:** blocking
- **Evidence:** `packages/agent/src/types.ts:264-280` — `AgentLoopConfig` defines `finishTurn`, `prepareRequest`, and `prepareNextTurn`.
- **Evidence:** `packages/agent/src/agent.ts:120-122` — `AgentOptions` exposes `onPayload`, `onResponse`, and `onProviderStreamEvent`.
- **Evidence:** `packages/agent/src/agent.ts:85-86` — the agent owns the leading system message built from `systemPrompt` and the tool declarations.
- **Evidence:** `packages/agent/package.json:25-28` — there is no dependency on `@earendil-works/pi-durable`, so the package cannot "consume" that surface.
- **Artifact says:** `specification.md:12` says "the provider/session hook surface live[s] in `@earendil-works/pi-durable`", and `specification.md:138` repeats it in the "Core vs durable" decision.
- **Required change:** state that the provider and session hooks (`finishTurn`, `prepareRequest`, `prepareNextTurn`, `onPayload`, `onResponse`, `onProviderStreamEvent`) and the leading system message are implemented in this package, and that only durable sessions, compaction, skills, and the Node execution environment moved to `@earendil-works/pi-durable`.

### The `AgentTool` data model omits two fields and marks a required field optional
- **Severity:** blocking
- **Evidence:** `packages/agent/src/types.ts:468` — `label: string` is required, not optional.
- **Evidence:** `packages/agent/src/types.ts:478` — `outputSchema?: TSchema` describes the JSON Schema of `structuredContent`.
- **Evidence:** `packages/agent/src/types.ts:490` — `replay?: "never" | "safe"` is the recovery policy for a tool whose durable intent exists but whose outcome is unknown.
- **Artifact says:** `specification.md:51-61` lists `name`, `description`, `parameters`, `label` (optional), `execute`, `prepareArguments`, and `executionMode`, and omits `outputSchema` and `replay`.
- **Required change:** add `outputSchema` (optional) and `replay` (optional, `"never" | "safe"`), and mark `label` as required.

### The agent-loop sequence omits the request hooks, the turn finalizer, and the tool-declaration diff
- **Severity:** blocking
- **Evidence:** `packages/agent/src/agent-loop.ts:333-363` — `declareToolChanges` produces the system message that announces tool loadout changes.
- **Evidence:** `packages/agent/src/agent-loop.ts:219-239` — `prepareRequest` runs before every provider request and can replace the context, model, and thinking level.
- **Evidence:** `packages/agent/src/agent-loop.ts:185-207` — `prepareNextTurn` runs after `turn_end` and can replace the context, model, thinking level, and pending messages.
- **Evidence:** `packages/agent/src/agent-loop.ts:286-287` — `finishTurn` runs after the assistant message and the tool results and before `turn_end`.
- **Evidence:** `packages/agent/src/agent-loop.ts:478-503` — tool calls from a `stopReason: "length"` message are failed instead of executed.
- **Artifact says:** `specification.md:101-119` shows `turn_start` -> `transformContext` -> `convertToLlm` -> `StreamFn` -> tool calls -> `beforeToolCall` -> execute -> `afterToolCall` -> `turn_end`, with none of the hooks above.
- **Required change:** insert `declareToolChanges` before the request, `prepareRequest` before every provider request, `prepareNextTurn` after `turn_end`, `finishTurn` after the tool results and before `turn_end`, and the `prepareArguments`/validation/length-truncation steps inside the tool branch.

### The failure-handling sequence omits two emitted events
- **Severity:** blocking
- **Evidence:** `packages/agent/src/agent.ts:544-547` — `handleRunFailure` emits `message_start`, then `message_end`, then `turn_end`, then `agent_end`.
- **Artifact says:** `specification.md:123-128` lists "emit message_end, agent_end" only.
- **Required change:** list the four events in order, and note that the synthetic failure message carries `stopReason: "aborted"` when the signal was aborted and `"error"` otherwise.

### The public API contract omits `runToolCall` and the low-level loop entry points
- **Severity:** blocking
- **Evidence:** `packages/agent/src/agent-loop.ts:811` — `runToolCall` runs a single tool call through the same prepare, validate, `beforeToolCall`, execute, `afterToolCall` pipeline without emitting events or adding messages, and never rejects for tool failures.
- **Evidence:** `packages/agent/src/agent-loop.ts:38`, `packages/agent/src/agent-loop.ts:71`, `packages/agent/src/agent-loop.ts:102`, `packages/agent/src/agent-loop.ts:128` — `agentLoop`, `agentLoopContinue`, `runAgentLoop`, and `runAgentLoopContinue` are all public.
- **Evidence:** `packages/agent/src/index.ts:1-5` — the barrel re-exports every one of them.
- **Artifact says:** `specification.md:77-97` documents only `Agent.prompt`/`Agent.continue` and `StreamFn`.
- **Required change:** add an API contract section for `runToolCall` and for the low-level `agentLoop`, `agentLoopContinue`, `runAgentLoop`, and `runAgentLoopContinue` entry points, including that the low-level streams are observational and are not a barrier (the `Agent` class is).

### The `AgentEvent` table understates the payload and the message scope
- **Severity:** blocking
- **Evidence:** `packages/agent/src/types.ts:519` — `agent_end` carries `messages: AgentMessage[]`.
- **Evidence:** `packages/agent/src/types.ts:522` — `turn_end` carries `message: AgentMessage` and `toolResults: ToolResultMessage[]`.
- **Evidence:** `packages/agent/src/types.ts:523` — the message lifecycle is "emitted for system, user, assistant, and toolResult messages".
- **Artifact says:** `specification.md:70-75` gives "-" as the payload of `agent_start`/`agent_end` and `turn_start`/`turn_end`, and describes `message_start`/`update`/`end` as carrying a "partial/full assistant message".
- **Required change:** fill in the carried payloads for `agent_end` and `turn_end`, and widen the message lifecycle row to system, user, assistant, and toolResult messages.

### The `AgentState` table does not match the declared types
- **Severity:** advisory
- **Evidence:** `packages/agent/src/types.ts:389` — `systemPrompt` is a required `string`, not optional.
- **Evidence:** `packages/agent/src/types.ts:416` — `streamingMessage` is `AgentMessage | undefined`, not `AssistantMessage`.
- **Evidence:** `packages/agent/src/types.ts:418` — `pendingToolCalls` is a `ReadonlySet<string>`.
- **Evidence:** `packages/agent/src/types.ts:420` — `errorMessage` is `string | undefined`.
- **Artifact says:** `specification.md:39-49` marks `systemPrompt` optional, types `streamingMessage` as `AssistantMessage`, and types `pendingToolCalls` as `Set`.
- **Required change:** correct the four types and their nullability.

### The `Agent.prompt` and `Agent.continue` contract omits the string overload and the queue drain
- **Severity:** advisory
- **Evidence:** `packages/agent/src/agent.ts:371-373` — `prompt` accepts a string with optional `ImageContent[]`, a single `AgentMessage`, or an array of `AgentMessage`.
- **Evidence:** `packages/agent/src/agent.ts:394-408` — when the transcript tail is an assistant message, `continue()` drains queued steering messages first, then queued follow-up messages, and only then throws.
- **Artifact says:** `specification.md:79-85` describes the request as "`AgentMessage[]` for `prompt`" and says only that `continue` "resumes from current context; last message must be user/toolResult".
- **Required change:** document the string and image overloads, and the queue-drain behaviour of `continue()`.

### Risk 1 names a symbol that was removed in 1.0.0
- **Severity:** advisory
- **Evidence:** `packages/agent/CHANGELOG.md:31` — `AgentHarness` was removed from this package in 1.0.0, and `packages/durable/src/index.ts:41` shows the durable runtime exports it as `Harness`.
- **Artifact says:** `specification.md:142` describes overlap "between `AgentHarness` and coding-agent's `AgentSession`".
- **Required change:** rewrite the risk against `Harness` from `@earendil-works/pi-durable`, or drop it.

## Open questions
- Should `runToolCall` be listed as a first-class public capability in the specification, given that the codemode example depends on it (`packages/agent/examples/mcp-codemode/tools.ts:91`)?
- Is the `AgentTool.replay` field consumed by any caller in this repo, or is it declared for downstream hosts only?

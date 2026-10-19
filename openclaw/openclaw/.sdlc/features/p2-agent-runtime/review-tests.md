---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Test plan review: Agent Runtime

## Sync drift: 2026-10-19

Eight of the ten listed test files still exist.
One file listed in the unit test table no longer exists, and two coverage-matrix rows point at files that cover a different requirement than the row claims.

### Blocking: the FR-4 row points at a deleted test file

- Classification: blocking.
- Artifact says (line 21): "| `src/agents/subagent-spawn.test.ts` | Subagent spawning lifecycle |"
- Artifact says (line 55): "| FR-4 (Subagent spawning) | `subagent-spawn.test.ts` |"
- Code says: `src/agents/subagent-spawn.test.ts` does not exist.
- Code says: the coverage was split into `src/agents/subagents/spawn/subagent-spawn.authority.test.ts`, `subagent-spawn.in-process-gateway.test.ts`, `subagent-spawn.context-resources.test.ts`, `subagent-spawn.preparation-authority.test.ts`, `subagent-spawn-cleanup.test.ts`, `subagent-spawn.thread-binding.test.ts`, `acp-spawn.test.ts`, `acp-spawn.authority.test.ts`, and `subagent-capabilities.test.ts`.
- Code says: adjacent suites also exist at `src/agents/subagents/subagent-terminal-outcome.test.ts` and `src/agents/subagents/requester-cron-authority.test.ts`.
- Impact: the artifact points a reader at a path that returns nothing, and understates the split coverage that exists.

### Blocking: the FR-2 row maps compaction to a context-window test

- Classification: blocking.
- Artifact says (line 20): "| `src/agents/context.test.ts` | Context window management |"
- Artifact says (line 53): "| FR-2 (Context compaction) | `context.test.ts` |"
- Code says: `src/agents/context.test.ts:35-140` holds nine top-level cases about configured context windows, discovered token caps, and provider-reported capacity. None of them starts or drives a compaction.
- Code says: the compaction coverage lives in `src/agents/sessions/agent-session-compaction.test.ts`, `src/agents/sessions/agent-session-compaction.admission.test.ts`, `src/agents/sessions/agent-session-compaction-boundary.test.ts`, `src/agents/sessions/agent-session-compaction-headroom.test.ts`, `src/agents/sessions/agent-session-compaction-noop-budget.test.ts`, `src/agents/sessions/agent-session-small-context-compaction.test.ts`, `src/agents/sessions/session-compaction-persistence.test.ts`, `src/agents/sessions/compaction/request-budget.test.ts`, and `src/agents/embedded-agent-runner/run.overflow-compaction.loop.test.ts`.
- Impact: the artifact asserts a compaction requirement is covered by a test that cannot fail for compaction.

### Blocking: the FR-7 row maps transcript persistence to a replay-policy test

- Classification: blocking.
- Artifact says (line 24): "| `src/agents/transcript-policy.test.ts` | Transcript recording policy |"
- Artifact says (line 56): "| FR-7 (Transcript persistence) | `transcript-policy.test.ts` |"
- Code says: `src/agents/transcript-policy.test.ts:145` opens `describe("resolveTranscriptPolicy")` and the cases from `:183` onward assert provider-specific replay behavior such as `sanitizeToolCallIds` for Google and Mistral, reasoning stripping for OpenAI, and prefill stripping for Claude routes.
- Code says: the persistence coverage lives in `src/agents/sessions/session-compaction-persistence.test.ts`, `src/agents/sessions/agent-session-transcript-worker.test.ts`, `src/agents/sessions/session-manager-async-message.test.ts`, `src/agents/command/transcript-persistence.test.ts`, and `src/gateway/server-methods/chat-transcript-persistence.*.test.ts`.
- Impact: the artifact asserts a persistence requirement is covered by a test that only covers replay policy.

### Advisory: the coverage matrix omits five functional requirements

- Classification: advisory.
- Artifact says (lines 50-57): the matrix covers FR-1, FR-2, FR-3, FR-4, FR-7, and FR-8 only.
- Code says: FR-5, FR-6, FR-9, FR-10, and FR-11 have no row.
- Code says: FR-5 is covered in `src/channels/draft-stream-loop.test.ts`, `src/channels/draft-stream-controls.test.ts`, and `src/channels/streaming.lifecycle.test.ts`, which sit outside `src/agents/`.
- Code says: FR-6 and FR-9 are covered in `src/agents/failover/` suites such as `context-overflow.test.ts` and in `src/agents/auth-profiles/` suites.
- Code says: FR-10 is covered in `src/agents/code-mode-headless.cancellation.test.ts` and `src/agents/code-mode-program-data.test.ts`.
- Code says: FR-11 is covered in `src/agents/memory-search.test.ts`.
- Impact: the map is incomplete rather than wrong.

### Advisory: the Test Infrastructure section describes in-memory SQLite

- Classification: advisory.
- Artifact says (line 45): "- In-memory SQLite for transcript persistence"
- Artifact says (line 46): "- Embedded runner for end-to-end agent turns"
- Code says: the transcript store is worker-backed and engine-selectable, per `src/infra/database-engine/registry.ts:24-33`.
- Code says: the embedded runner suite now holds more than 200 test files, and the harness suites in `src/agents/harness/` cover run authority separately.
- Impact: the infrastructure description understates the current shape.

### Advisory: large agent-runtime areas have no listed coverage

- Classification: advisory.
- Artifact says (lines 12-30): the plan lists nine unit files and one end-to-end file.
- Code says: `src/agents/` holds more than 1,000 test files.
- Code says: unlisted but notable areas include the context engine registry in `src/context-engine/registry.*.test.ts` and `src/context-engine/quarantine-health.test.ts`.
- Code says: unlisted but notable areas include the harness run-authority suites in `src/agents/harness/attempt-deadlines.test.ts` and `src/agents/harness/context-engine-lifecycle.test.ts`.
- Code says: unlisted but notable areas include the tool execution and approval pipeline in `src/agents/agent-tools.before-tool-call.*.test.ts`.
- Code says: unlisted but notable areas include the code-mode execution suite in `src/agents/code-mode-*.test.ts`.
- Code says: unlisted but notable areas include the agent bundle MCP lifecycle in `src/agents/agent-bundle-mcp-*.test.ts`.
- Impact: the plan under-represents the runtime by a wide margin, which matters for future coverage planning.

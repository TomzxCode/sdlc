---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-16

The test plan artifact was not changed since the 2026-10-19 review.
The three blocking and four advisory items in the 2026-10-19 section still apply.
Two replacement paths cited in that review no longer exist, so the code has moved again.

### Blocking: two replacement paths in the 2026-10-19 review are now stale

- Classification: blocking.
- The 2026-10-19 review cites `src/agents/sessions/agent-session-compaction.test.ts` as compaction coverage and `src/agents/sessions/session-manager-async-message.test.ts` as transcript persistence coverage.
- Code says: neither path exists on disk.
- Code says: current compaction coverage includes `src/agents/sessions/agent-session-compaction-boundary.test.ts`, `src/agents/sessions/agent-session-compaction-headroom.test.ts`, `src/agents/sessions/session-compaction-persistence.test.ts`, and suites under `src/agents/embedded-agent-runner/compact.*.test.ts` and `run.overflow-compaction*.test.ts`.
- Code says: current async message coverage includes `src/agents/sessions/session-manager-async-message-custody.test.ts` and `src/agents/sessions/session-manager-async-entries.test.ts`.
- Impact: a reader following the prior review would again land on dead paths.

### Blocking: the FR-4 row still points at a deleted file

- Classification: blocking.
- The artifact still lists `src/agents/subagent-spawn.test.ts` in the unit test table and the coverage matrix.
- Code says: that path does not exist, and the split subagent suites under `src/agents/subagents/spawn/` do exist.
- Impact: unchanged from 2026-10-19, still wrong.

### Advisory: the test inventory has grown again

- Classification: advisory.
- The 2026-10-19 review counted more than 1,000 test files under `src/agents/`.
- Code says: there are now 2,437 `*.test.ts` files under `src/agents/`.
- Code says: new areas include the compaction safeguard hooks in `src/agents/agent-hooks/compaction-safeguard*.test.ts` and the native compaction suite in `src/agents/cli-runner/prepare.native-compaction.test.ts`.
- Impact: the plan's ten listed files represent an even smaller share of the runtime.

### Advisory: the coverage matrix still omits five requirements

- Classification: advisory.
- Code says: FR-5, FR-6, FR-9, FR-10, and FR-11 still have no row in the coverage matrix.
- Impact: unchanged from 2026-10-19, still incomplete.

## Sync drift: 2026-11-23

The test plan artifact was not changed since the 2026-11-16 review.
The blocking and advisory items recorded in 2026-10-19 and 2026-11-16 still apply.
Two evidence paths cited in the 2026-11-16 section have moved again.

### Blocking: the FR-4 row still points at a deleted file

- Classification: blocking.
- The artifact still lists `src/agents/subagent-spawn.test.ts` at line 21 and in the coverage matrix at line 55.
- Code says: that path does not exist.
- Code says: split coverage lives under `src/agents/subagents/spawn/`, including `subagent-spawn.authority.test.ts`, `acp-spawn.test.ts`, `acp-spawn.authority.test.ts`, and `subagent-capabilities.test.ts`.
- Impact: a reader following the row lands on a dead path.

### Blocking: the FR-2 row still maps compaction to a test that never compacts

- Classification: blocking.
- The artifact maps FR-2 to `src/agents/context.test.ts` at lines 20 and 53.
- Code says: `src/agents/context.test.ts` is now 93 lines with four `it(...)` cases about configured context windows and token caches.
- Code says: the file contains zero occurrences of `compact`.
- Code says: compaction coverage now includes `src/agents/sessions/agent-session-compaction-boundary.test.ts`, `agent-session-compaction-headroom.test.ts`, `agent-session-compaction-noop-budget.test.ts`, `session-compaction-persistence.test.ts`, and suites under `src/agents/embedded-agent-runner/compact.*.test.ts`.
- Impact: the mapped test cannot fail for compaction.

### Blocking: the FR-7 row still maps persistence to a replay-policy test

- Classification: blocking.
- The artifact maps FR-7 to `src/agents/transcript-policy.test.ts` at lines 24 and 56.
- Code says: `describe("resolveTranscriptPolicy")` now starts at line 77, not line 145 as recorded in 2026-10-19.
- Code says: the cases assert provider-specific replay behavior such as `sanitizeToolCallIds`.
- Code says: persistence coverage now includes `src/agents/command/transcript-persistence.test.ts`, `src/gateway/server-methods/chat-transcript-persistence.mirrors.test.ts`, `chat-transcript-persistence.node-loss.test.ts`, and `src/agents/sessions/session-compaction-persistence.test.ts`.
- Impact: the mapped test does not exercise persistence.

### Advisory: the coverage matrix still omits five requirements

- Classification: advisory.
- The artifact covers FR-1, FR-2, FR-3, FR-4, FR-7, and FR-8 at lines 50-57.
- Code says: FR-5, FR-6, FR-9, FR-10, and FR-11 still have no row.

### Advisory: the inventory and infrastructure descriptions remain stale

- Classification: advisory.
- The artifact says at line 45 that tests use in-memory SQLite for transcript persistence.
- Code says: the store is worker-backed and engine-selectable per `src/infra/database-engine/registry.ts:26` and `:43-52`.
- Code says: `src/agents/` still holds 2,437 `*.test.ts` files, so the ten listed files remain a small share of the runtime.

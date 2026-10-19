---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_6b3f0a1c2d4e5f60718293a4b5c6d7e8
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

Every test file the plan names exists in `packages/coding-agent/test/`. The drift is coverage in the other direction: the repository has materially more session, compaction, branching, export, and trust tests than the plan records.

## Sync drift: 2026-10-19

### The SessionManager unit test list is missing `load-entries.test.ts`
- **Evidence:** `packages/coding-agent/test/session-manager/load-entries.test.ts` (`describe("SessionManager.inMemory with preloaded entries")`) exists. `tests.md:15` lists seven of the eight files in `test/session-manager/` and omits this one.
- **Artifact says:** "SessionManager operations (session-manager/save-entry.test.ts, session-manager/file-operations.test.ts, session-manager/build-context.test.ts, session-manager/labels.test.ts, session-manager/tree-traversal.test.ts, session-manager/migration.test.ts, session-manager/custom-session-id.test.ts)".
- **Required change:** Add `session-manager/load-entries.test.ts`.
- **Blocking.**

### Compaction and branch-summary coverage is under-recorded
- **Evidence:** These files exist and materially cover compaction and branch summarization: `test/agent-session-auto-compaction-queue.test.ts`, `test/branch-summarization.test.ts`, `test/branch-summary-extensions.test.ts`, `test/compaction-extensions.test.ts`, `test/compaction-extensions-example.test.ts`, `test/compaction-nested-calls.test.ts`, `test/interactive-mode-compaction.test.ts`, `test/interactive-mode-tree-navigation.test.ts`, `test/settings-manager-compaction.test.ts`, `test/suite/agent-session-compaction.test.ts`, `test/suite/agent-session-compaction-model-overrides.test.ts`. None is in the plan.
- **Artifact says:** "Session compaction (agent-session-compaction.test.ts, compaction.test.ts, compaction-serialization.test.ts, compaction-summary-reasoning.test.ts)" and "Session tree navigation (agent-session-tree-navigation.test.ts, tree-selector.test.ts)".
- **Required change:** Add the missing compaction and branch-summary test files.
- **Blocking.**

### Session-manager-adjacent coverage is missing
- **Evidence:** `test/session-context-edit.test.ts` (`describe("session context edits")`) covers the `context_edit` entry type, `test/sdk-session-manager.test.ts` (`describe("createAgentSession session manager defaults")`) covers the SDK session-manager wiring, and `test/suite/agent-session-runtime.test.ts` covers runtime replacement including JSONL import and cross-cwd replacement. None is in the plan.
- **Artifact says:** the plan's "Session lifecycle events (suite/agent-session-queue.test.ts)" is the only suite file named outside the regressions list.
- **Required change:** Add `session-context-edit.test.ts`, `sdk-session-manager.test.ts`, and `suite/agent-session-runtime.test.ts`.
- **Blocking.**

### Export and share coverage is missing
- **Evidence:** `test/export-jsonl-share.test.ts` (`describe("JSONL share export")`) covers `serializeSessionBranch`/`exportSessionToJsonl`, `test/session-share.test.ts` (`describe("shareSession")`) covers the Radius and gist share paths, and `test/export-html-xss.test.ts` covers HTML export sanitization. The plan names only `export-html-whitespace.test.ts` and `export-html-skill-block.test.ts`.
- **Artifact says:** "HTML export (export-html-whitespace.test.ts, export-html-skill-block.test.ts)".
- **Required change:** Add `export-jsonl-share.test.ts`, `session-share.test.ts`, and `export-html-xss.test.ts`.
- **Blocking.**

### Project trust and keybinding migration coverage is missing
- **Evidence:** `test/trust-manager.test.ts` (`describe("ProjectTrustStore")`) and `test/trust-selector.test.ts` (`describe("TrustSelectorComponent")`) cover the trust store and the `/trust` selector; `test/keybindings-migration.test.ts` (`describe("keybindings migration")`) covers the startup keybindings migration. None is in the plan, even though project trust is part of this feature's scope.
- **Artifact says:** the plan's scope line reads "Covers session format, JSONL persistence, tree-structured entries, branching, compaction, migration, export, and session lifecycle."
- **Required change:** Add `trust-manager.test.ts`, `trust-selector.test.ts`, and `keybindings-migration.test.ts`, and add project trust to the stated scope.
- **Blocking.**

### Session and compaction regression files are missing
- **Evidence:** These exist under `packages/coding-agent/test/suite/regressions/` and are not in the plan's regression list: `2753-reload-stale-resource-settings`, `5217-compaction-reason`, `6647-compaction-retries-transient-stream-drop`, `6768-copilot-compaction-base-url`, `7048-compaction-truncated-summary`, `7150-rpc-prompt-during-compaction`, `7253-manual-compact-during-response`, `7497-session-discovery-symlink`, `8328-zero-usage-auto-compaction`, `8724-in-memory-fork-active-tool`, `8989-fork-compaction-label-boundary`, `9178-tree-during-compaction`, `9340-9777-auto-compaction-cancellation`, `tree-during-streaming`, `startup-session-rebind-duplicate-subscription`.
- **Artifact says:** "Suite regressions (6324-branch-summary-ambient-auth.test.ts, 3686-session-name-event.test.ts, 3688-tree-cancel-compacting.test.ts, 5943-session-start-notify.test.ts, 5996-session-name-newlines.test.ts, 2860-replaced-session-context.test.ts, pre-prompt-compaction-no-continue.test.ts)".
- **Required change:** Add the missing regression files.
- **Blocking.**

### The FR-08 coverage row names no test file
- **Evidence:** The session lifecycle hooks are covered by `test/compaction-extensions.test.ts` (before_compact/compact events), `test/branch-summary-extensions.test.ts`, `test/suite/regressions/5217-compaction-reason.test.ts`, and `test/suite/regressions/3688-tree-cancel-compacting.test.ts`. The plan says only "(suite harness tests)".
- **Artifact says:** "| FR-08 (Session lifecycle hooks) | (suite harness tests) |".
- **Required change:** Replace the placeholder with the concrete test files.
- **Blocking.**

### The FR-07 coverage row is incomplete
- **Evidence:** `test/suite/agent-session-runtime.test.ts` covers runtime replacement for resume, new, fork, JSONL import, and cross-cwd session replacement, which is the hot-swap behaviour FR-07 describes. The plan names only `agent-session-runtime-events.test.ts`.
- **Artifact says:** "| FR-07 (Runtime hot-swap) | agent-session-runtime-events.test.ts |".
- **Required change:** Add `suite/agent-session-runtime.test.ts`.
- **Advisory.**

## Open questions

- None. File existence was checked directly under `packages/coding-agent/test/` and `packages/coding-agent/test/session-manager/` and `packages/coding-agent/test/suite/regressions/`.

---
title: "Session Persistence and Branching"
status: done
---

# Test Plan: Session Persistence and Branching

## Scope

Covers session format, JSONL persistence, tree-structured entries, branching, compaction, migration, export, and session lifecycle.

## Unit Tests

Test files under `packages/coding-agent/test/` cover:
- SessionManager operations (session-manager/save-entry.test.ts, session-manager/file-operations.test.ts, session-manager/build-context.test.ts, session-manager/labels.test.ts, session-manager/tree-traversal.test.ts, session-manager/migration.test.ts, session-manager/custom-session-id.test.ts)
- Session branching (agent-session-branching.test.ts)
- Session compaction (agent-session-compaction.test.ts, compaction.test.ts, compaction-serialization.test.ts, compaction-summary-reasoning.test.ts)
- Session tree navigation (agent-session-tree-navigation.test.ts, tree-selector.test.ts)
- Session file handling (session-file-invalid.test.ts, session-id-readonly.test.ts, session-info-modified-timestamp.test.ts, session-cwd.test.ts, session-selector-search.test.ts, session-selector-rename.test.ts, session-selector-path-delete.test.ts)
- Session lifecycle events (suite/agent-session-queue.test.ts)
- HTML export (export-html-whitespace.test.ts, export-html-skill-block.test.ts)
- Startup session naming (startup-session-name.test.ts)
- First-time setup fork (first-time-setup-fork.test.ts)
- Format resume command (format-resume-command.test.ts)
- Suite regressions (6324-branch-summary-ambient-auth.test.ts, 3686-session-name-event.test.ts, 3688-tree-cancel-compacting.test.ts, 5943-session-start-notify.test.ts, 5996-session-name-newlines.test.ts, 2860-replaced-session-context.test.ts, pre-prompt-compaction-no-continue.test.ts)

## Test Infrastructure

- In-memory session storage for deterministic testing
- Simulated session files for migration testing
- Tree-structured JSONL helpers

## Coverage Matrix

| Requirement | Test Files |
|---|---|
| FR-01 (JSONL tree format) | session-manager/save-entry.test.ts |
| FR-02 (Entry types) | session-manager/save-entry.test.ts |
| FR-03 (Resume/fork/clone/tree) | agent-session-branching.test.ts, agent-session-tree-navigation.test.ts |
| FR-04 (Branching) | agent-session-branching.test.ts |
| FR-05 (Compaction) | agent-session-compaction.test.ts, compaction.test.ts, compaction-serialization.test.ts |
| FR-06 (Non-destructive compaction) | compact test files |
| FR-07 (Runtime hot-swap) | agent-session-runtime-events.test.ts |
| FR-08 (Session lifecycle hooks) | (suite harness tests) |
| FR-09 (Compaction estimates) | compaction-summary-reasoning.test.ts |
| FR-10 (HTML export) | export-html-*.test.ts |
| FR-11 (Migration) | session-manager/migration.test.ts |
| NFR-01 (Non-destructive original) | compaction.test.ts |
| NFR-04 (Compaction observability) | compaction-summary-reasoning.test.ts |

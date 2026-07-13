---
title: "Extension and Skills Platform"
status: done
---

# Test Plan: Extension and Skills Platform

## Scope

Covers extension loading, hook dispatch, skills, prompt templates, package manager, and the ExtensionAPI surface.

## Unit Tests

Test files under `packages/coding-agent/test/` cover:
- Extension runner (extensions-runner.test.ts, compaction-extensions.test.ts, compaction-extensions-example.test.ts)
- Extension discovery (extensions-discovery.test.ts)
- Extension input events (extensions-input-event.test.ts)
- Skills (skills.test.ts, sdk-skills.test.ts)
- Prompt templates (prompt-templates.test.ts)
- Package manager (package-manager.test.ts, package-manager-ssh.test.ts, package-command-paths.test.ts)
- Git integration (git-update.test.ts, git-ssh-url.test.ts, git-merge-and-resolve-extension.test.ts)
- Plan mode extension (plan-mode-extension.test.ts, plan-mode-utils.test.ts)
- Trigger compact extension (trigger-compact-extension.test.ts)
- Suite regressions (extension-factory-cache.test.ts, 6162-extension-active-tools-next-turn.test.ts, 6260-inline-extension-naming.test.ts, 5433-extension-oauth-prompt-input.test.ts, 2835-tools-allowlist-filters-extension-tools.test.ts, 5080-signal-shutdown-extension-cleanup.test.ts)

## Test Infrastructure

- In-memory extension module loading with mock default exports
- Fake `ExtensionAPI` and `ExtensionUIContext` for dispatch testing
- Test extension files in `examples/extensions/`

## Coverage Matrix

| Requirement | Test Files |
|---|---|
| FR-01 (Extension loading) | extensions-runner.test.ts |
| FR-02 (Tool registration/replacement) | extensions-runner.test.ts, 2835-regression |
| FR-03 (Slash commands) | extensions-runner.test.ts |
| FR-04 (Event handlers) | extensions-runner.test.ts, extensions-input-event.test.ts |
| FR-05 (UI primitives) | (sdk docs) |
| FR-07 (Session control) | extensions-runner.test.ts |
| FR-08 (Skills loading) | skills.test.ts, sdk-skills.test.ts |
| FR-09 (Prompt templates) | prompt-templates.test.ts |
| FR-10 (Resource loading) | extensions-discovery.test.ts |
| FR-11 (Package manager) | package-manager.test.ts |
| NFR-01 (Trust-gated extensions) | (project trust tests) |
| NFR-02 (Cached module loading) | extension-factory-cache.test.ts |

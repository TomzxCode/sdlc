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
- Extension discovery and resource loading (extensions-discovery.test.ts, resource-loader.test.ts, resource-loader-theme.test.ts, trust-manager.test.ts, trust-selector.test.ts)
- Extension input events (extensions-input-event.test.ts)
- Skills (skills.test.ts, sdk-skills.test.ts)
- Prompt templates (prompt-templates.test.ts)
- Package manager (package-manager.test.ts, package-manager-ssh.test.ts, package-command-paths.test.ts, package-distribution.test.ts)
- Git integration (git-update.test.ts, git-ssh-url.test.ts, git-merge-and-resolve-extension.test.ts)
- Plan mode extension (plan-mode-extension.test.ts, plan-mode-utils.test.ts)
- Trigger compact extension (trigger-compact-extension.test.ts)
- Built-in extensions (mcp-extension.test.ts, mcp-command.test.ts, mcp-oauth-*.test.ts, llama-extension.test.ts, tool-search.test.ts, codemode-*.test.ts, branch-summary-extensions.test.ts)
- Suite regressions (test/suite/regressions/: 6162-extension-active-tools-next-turn, 6260-inline-extension-naming, 5433-extension-oauth-prompt-input, 2835-tools-allowlist-filters-extension-tools, 5080-signal-shutdown-extension-cleanup, plus extension-factory-cache coverage via loader cache tests)

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
| FR-10 (Resource loading) | extensions-discovery.test.ts, resource-loader.test.ts |
| FR-11 (Package manager) | package-manager.test.ts, package-distribution.test.ts |
| FR-12 (Custom providers) | mcp-extension.test.ts, llama-extension.test.ts |
| NFR-01 (Trust-gated extensions) | trust-manager.test.ts, (project trust tests) |
| NFR-02 (Cached module loading) | loader extensionCache (extension-factory-cache coverage) |

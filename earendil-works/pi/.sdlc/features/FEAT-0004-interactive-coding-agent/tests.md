---
title: "Interactive Coding Agent"
status: done
---

# Test Plan: Interactive Coding Agent

## Scope

Covers the `pi-coding-agent` CLI product: AgentSession, tools, modes (interactive, print, JSON, RPC), settings, resource loading, project trust, and the SDK.

## Unit Tests

Test files under `packages/coding-agent/test/` cover:
- AgentSession core (agent-session-*.test.ts files for retry, concurrent, stats, dynamic-provider, dynamic-tools, runtime-events, auto-compaction-queue)
- Bash execution (bash-close-hang-windows.test.ts, bash-execution-width.test.ts)
- Built-in tools (tools.test.ts, edit-tool-legacy-input.test.ts, edit-tool-no-full-redraw.test.ts)
- CLI args (args.test.ts)
- Config/settings (config.test.ts, settings-manager.test.ts, settings-manager-bug.test.ts, config-value-migration.test.ts)
- Resource loader (resource-loader.test.ts)
- System prompt building (system-prompt.test.ts)
- Run modes (print-mode.test.ts, rpc.test.ts, rpc-jsonl.test.ts, rpc-client-clone.test.ts, rpc-client-process-exit.test.ts, rpc-prompt-response-semantics.test.ts)
- SDK (sdk-session-manager.test.ts, sdk-skills.test.ts, sdk-stream-options.test.ts, sdk-openrouter-attribution.test.ts)
- Trust manager (trust-manager.test.ts, trust-selector.test.ts)
- Theme handling (theme-detection.test.ts, theme-export.test.ts, theme-picker.test.ts, export-html-xss.test.ts)
- Interactive mode (interactive-mode-anthropic-warning.test.ts, interactive-mode-clone-command.test.ts, interactive-mode-compaction.test.ts, interactive-mode-import-command.test.ts, interactive-mode-startup-input.test.ts, interactive-mode-status.test.ts, interactive-mode-suspend.test.ts)
- Image processing (image-process.test.ts, image-processing.test.ts, image-resize-callers.test.ts)
- Clipboard handling (clipboard.test.ts, clipboard-native.test.ts, clipboard-image.test.ts, clipboard-image-bmp-conversion.test.ts)
- Version check (version-check.test.ts, pi-user-agent.test.ts)
- Suite tests (suite/agent-session-*.test.ts) using the harness + faux provider

## Integration Tests

- Suite tests under `test/suite/` use the coding-agent test harness with a faux provider for full prompt-loop testing without real API calls
- Issue regression tests under `test/suite/regressions/` cover specific bugs and edge cases

## Test Infrastructure

- Harness (`test/suite/harness.ts`) provides a managed AgentSession + faux provider
- In-memory session manager for deterministic testing
- Controlled bash process lifecycle

## Coverage Matrix

| Requirement | Test Files |
|---|---|
| FR-01 (CLI interactive default) | args.test.ts |
| FR-02 (Built-in tools) | tools.test.ts, edit-tool-*.test.ts |
| FR-03 (AgentSession core) | agent-session-*.test.ts, suite/agent-session-*.test.ts |
| FR-04 (Model selection) | model-registry.test.ts, model-resolver.test.ts |
| FR-05 (Slash commands) | tools.test.ts, interactive-mode-*.test.ts |
| FR-06 (Run modes) | print-mode.test.ts, rpc.test.ts |
| FR-07 (Settings) | config.test.ts, settings-manager.test.ts |
| FR-08 (Project trust) | trust-manager.test.ts, trust-selector.test.ts |
| FR-09 (Resource discovery) | resource-loader.test.ts |
| FR-10 (System prompt building) | system-prompt.test.ts |
| FR-11 (Themes) | theme-detection.test.ts, theme-export.test.ts |
| FR-12 (Update/telemetry) | version-check.test.ts |
| NFR-02 (Hot-swap runtime) | agent-session-runtime-events.test.ts, suite/agent-session-runtime.test.ts |

---
title: "Command-Line Interface"
status: done
---

# Test Plan: Command-Line Interface

## Scope

Tests cover CLI command parsing, help output, configuration management commands, JSON output mode, and command routing. Does not cover CLI integration with live gateway or plugin installation.

## Unit Tests

| File | Description |
|---|---|
| `src/cli/program/command-tree.test.ts` | Command tree structure and registration |
| `src/cli/program/root-help.test.ts` | Root help output |
| `src/cli/program/build-program.test.ts` | Program builder |
| `src/cli/program/routes.test.ts` | Command routing |
| `src/cli/run-main.test.ts` | Main execution dispatcher |
| `src/cli/json-output-mode.test.ts` | JSON output formatting |
| `src/cli/config-cli.test.ts` | Config CLI commands |
| `src/cli/command-options.test.ts` | Command option parsing |
| `src/cli/skills-cli.test.ts` | Skills CLI commands |
| `src/commands/agent.test.ts` | Agent command handler |

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Missing required argument | Clear error message with usage |
| Invalid flag combination | Validation error |
| JSON output requested | Structured JSON response |
| Help requested | Formatted help text displayed |

## Test Infrastructure

- Vitest unit test runner
- Mock yargs for command parsing tests
- Captured stdout/stderr for output validation

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (Gateway start/stop) | `gateway-cli.ts` (co-located tests) |
| FR-2 (Plugin management) | `plugins-cli.ts` (co-located tests) |
| FR-4 (Config management) | `config-cli.test.ts` |
| FR-5 (Onboarding wizard) | `commands/agent.test.ts` |
| FR-6 (Doctor command) | `commands/doctor.ts` (co-located tests) |
| NFR-2 (Startup performance) | `run-main.test.ts` |

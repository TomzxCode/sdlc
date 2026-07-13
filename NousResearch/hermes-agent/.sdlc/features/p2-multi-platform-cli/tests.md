---
title: "Multi-Platform CLI"
status: done
---

# Test Plan: Multi-Platform CLI

## Scope

Tests covering HermesCLI class, slash command registry and dispatch, skin/theme system, banner rendering, autocomplete, and CLI configuration.

## Test Files

- tests/hermes_cli/ — 300+ test files covering all CLI subsystems
- tests/hermes_cli/test_commands.py — Slash command dispatch tests
- tests/hermes_cli/test_skin_engine.py — Skin/theme engine tests
- tests/hermes_cli/test_banner.py — Banner rendering tests
- tests/hermes_cli/test_completion.py — Autocomplete tests
- tests/hermes_cli/test_cli_output.py — CLI output formatting tests
- tests/hermes_cli/test_hooks_cli.py — CLI hook tests
- tests/hermes_cli/test_tools_config.py — Tool configuration tests

## Unit Tests

- CommandDef registry and resolution
- Skin config loading and merging
- Banner rendering with skin colors
- Path completion logic
- Slash command argument parsing

## Integration Tests

- Full CLI startup and command dispatch
- Skin switching via /skin command
- Configuration loading from config.yaml
- Gateway command compatibility

## End-to-End Tests

- test_cli_skin_integration.py — Skin engine integration
- test_cli_file_drop.py — File drop handling

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Unknown slash command | Help message with available commands |
| Invalid skin name | Fall back to default skin |
| Config file missing | Use DEFAULT_CONFIG defaults |
| Terminal not supporting Rich features | Graceful degradation to plain text |

## Test Infrastructure

- pytest with temp HERMES_HOME
- Mock stdin/stdout for CLI interaction testing
- Subprocess-per-test-file isolation

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (session commands) | test_commands.py |
| FR-2 (configuration commands) | test_commands.py, test_config.py |
| FR-3 (tools/skills commands) | test_commands.py, test_tools_config.py |
| FR-4 (info commands) | test_commands.py, test_debug.py |
| FR-5 (skin/theme system) | test_skin_engine.py |
| FR-6 (Rich banners and spinner) | test_banner.py, test_cli_output.py |
| FR-7 (prompt_toolkit autocomplete) | test_completion.py |
| NFR-1 (100ms dispatch) | Implicit in command dispatch tests |

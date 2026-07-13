---
title: "Configuration and Multi-Profile System"
status: done
---

# Test Plan: Configuration and Multi-Profile System

## Scope

Tests covering config.yaml loading and deep-merge, .env secrets loading, profile creation/clone/list/use, config version migration, toolset configuration, and model catalog.

## Test Files

- tests/hermes_cli/test_config.py — Config loading and merge
- tests/hermes_cli/test_config_drift.py — Config drift detection
- tests/hermes_cli/test_config_validation.py — Config validation
- tests/hermes_cli/test_config_env_expansion.py — Env var expansion in config
- tests/hermes_cli/test_config_env_refs.py — Config references to env vars
- tests/hermes_cli/test_profiles.py — Profile operations
- tests/hermes_cli/test_profile_distribution.py — Profile distribution
- tests/hermes_cli/test_profile_describer.py — Profile description
- tests/hermes_cli/test_profile_export_credentials.py — Credential export
- tests/hermes_cli/test_apply_profile_override.py — Profile override
- tests/hermes_cli/test_model_catalog.py — Model catalog tests
- tests/hermes_cli/test_tools_config.py — Toolset configuration
- tests/hermes_cli/test_toolset_validation.py — Toolset validation
- tests/hermes_cli/test_models.py — Model list and filtering
- tests/hermes_cli/test_env_loader*.py — .env loading (5+ test files)

## Unit Tests

- DEFAULT_CONFIG deep-merge with user config
- Config version migration
- Profile directory creation and isolation
- .env parsing and variable expansion
- Model catalog loading from provider registry

## Integration Tests

- Full config loading through all three loaders (CLI, tools, gateway)
- Profile-aware HERMES_HOME resolution
- Profile clone creates independent copy
- Toolset enable/disable per platform
- Config drift detection and repair

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Config yaml parse error | Graceful fallback with error message |
| Missing .env file | Continue with empty env (warn on first run) |
| Profile directory already exists | Error with existing profile message |
| Config version mismatch | Automatic migration applied |
| Unknown config key in user yaml | Ignored with warning (forward compatibility) |

## Test Infrastructure

- Temp HERMES_HOME and profile directories
- Controlled config yaml content per test
- Monkeypatched env for .env tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (config.yaml settings) | test_config.py |
| FR-2 (.env for secrets) | test_env_loader*.py |
| FR-3 (deep-merge) | test_config.py |
| FR-4 (multi-profile) | test_profiles.py |
| FR-5 (profile HERMES_HOME) | test_apply_profile_override.py |
| FR-6 (profile clone) | test_profiles.py |
| FR-7 (model catalog) | test_model_catalog.py |
| FR-8 (toolset per platform) | test_tools_config.py, test_toolset_validation.py |

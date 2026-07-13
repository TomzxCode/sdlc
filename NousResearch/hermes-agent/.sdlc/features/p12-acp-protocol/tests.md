---
title: "ACP Protocol (IDE Integration)"
status: done
---

# Test Plan: ACP Protocol (IDE Integration)

## Scope

Tests covering ACP adapter server, registry maintenance, editor protocol compatibility, and authentication.

## Test Files

- tests/hermes_cli/test_copilot_*.py — Copilot/ACP integration tests (5+ files)
- tests/acp/ — ACP-specific test directory
- tests/acp_adapter/ — ACP adapter tests
- tests/agent/test_copilot_acp_client.py — ACP client tests
- tests/agent/test_copilot_acp_deprecation.py — ACP deprecation handling

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (ACP adapter endpoint) | test_copilot_acp_client.py |
| FR-2 (code-aware context) | test_copilot_context.py |
| FR-3 (ACP registry) | test_release_acp_registry.py |

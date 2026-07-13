---
title: "Messaging Gateway"
status: done
---

# Test Plan: Messaging Gateway

## Scope

Tests covering gateway runner, platform adapters, session management, slash command dispatch, approval flow, rate limiting, and platform-specific functionality.

## Test Files

- tests/gateway/ — 80+ test files covering all gateway subsystems
- tests/hermes_cli/test_gateway*.py — Gateway CLI integration tests
- tests/plugins/platforms/ — Platform adapter-specific tests
- tests/hermes_cli/test_webhook_cli.py — Webhook adapter tests
- tests/hermes_cli/test_whatsapp_*.py — WhatsApp adapter tests
- tests/hermes_cli/test_dingtalk_auth.py — DingTalk auth tests
- tests/hermes_cli/test_slack_cli.py — Slack CLI tests

## Unit Tests

- Session management (create, resume, list, delete)
- Slash command dispatch resolution
- Approval flow state machine
- Token lock acquisition/release
- Rate limiting logic

## Integration Tests

- Adapter connection lifecycle (connect/reconnect/disconnect)
- Message processing pipeline
- Approval prompt delivery and response
- Session isolation across platforms
- Gateway restart and recovery

## End-to-End Tests

- test_approve_deny_commands.py — Approval command flow
- test_api_server.py — API server adapter
- test_background_command.py — Background command processing
- test_gateway_restart_loop.py — Gateway restart resilience
- Platform-specific adapter tests

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Platform adapter crashes | Other adapters continue unaffected |
| Rate limit exceeded | Queue messages with backoff |
| Duplicate message delivery | Deduplication before processing |
| Token lock conflict (two profiles) | Latter connection refused |
| Gateway restart mid-session | Session state recovered or gracefully reset |
| Scale-to-zero wake | Gateway resumes with session cleanup |

## Test Infrastructure

- Mock platform adapters for deterministic testing
- Async test fixtures with event loop isolation
- Temp HERMES_HOME per test
- In-memory session store for fast test execution

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (multi-platform support) | Adapter lifecycle tests |
| FR-2 (platform auth, rate limiting) | Platform-specific auth tests |
| FR-3 (slash commands bypassing agent) | test_approve_deny_commands.py |
| FR-4 (approval flow) | test_approval_prompt_redaction.py |
| FR-5 (session management) | test_async_session_db.py |
| NFR-1 (concurrent messages) | Concurrent session tests |
| NFR-2 (platform isolation) | Session isolation tests |

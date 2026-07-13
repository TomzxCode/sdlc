---
title: "Terminal and Browser Automation"
status: done
---

# Test Plan: Terminal and Browser Automation

## Scope

Tests covering terminal execution across six backends, browser automation via Playwright/CDP, file operations, security gating, background processes, and remote environment management.

## Test Files

- tests/tools/test_terminal_tool.py — Terminal tool execution
- tests/tools/test_terminal_*.py — Terminal behavior (timeout, cwd, encoding)
- tests/tools/test_browser_*.py — Browser automation (30+ test files)
- tests/tools/test_file_*.py — File operations (read, write, patch, search)
- tests/tools/test_docker_*.py — Docker environment
- tests/tools/test_ssh_environment.py — SSH environment
- tests/tools/test_local_*.py — Local environment
- tests/tools/test_threat_patterns.py — Security threat detection
- tests/tools/test_approval*.py — Command approval gating
- tests/tools/test_notify_on_complete.py — Background completion notification
- tests/tools/test_file_sync*.py — File sync with remote backends

## Unit Tests

- Environment abstraction ABC contract
- Security check (allow/block lists, threat patterns)
- Browser navigation, click, extract, screenshot
- File read/write/patch operations
- Path resolution and traversal guards

## Integration Tests

- Full command execution pipeline through each backend
- Browser page interaction sequences
- Background process with completion notification
- File sync between host and remote backends
- Docker container lifecycle

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Command timeout | Graceful timeout with partial output |
| Remote backend unreachable | Configurable retry or fallback |
| Browser dialog (alert/confirm) | Handled via dialog handler |
| Dangerous command detected | Blocked by security layer or approval prompt |
| File write to restricted path | Rejected with clear error |
| Background process in non-gateway mode | Watcher unavailable, process still runs |
| Browser anti-bot detection | CDP bypass or fallback strategy |

## Test Infrastructure

- Mock environments for deterministic testing
- Headless Chromium for browser tests (when available)
- Temp directories for file operation tests
- Process isolation for terminal tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (local terminal) | test_terminal_tool.py |
| FR-2 (remote backends) | test_docker_*, test_ssh_environment.py |
| FR-3 (background processes) | test_notify_on_complete.py |
| FR-4 (browser navigation) | test_browser_supervisor.py |
| FR-5 (browser screenshots) | test_browser_supervisor.py |
| FR-6 (browser dialogs) | test_browser_camofox*.py |
| NFR-1 (security checks) | test_threat_patterns.py, test_approval*.py |

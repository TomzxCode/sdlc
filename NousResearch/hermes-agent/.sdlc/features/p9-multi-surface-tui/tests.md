---
title: "Multi-Surface TUI and Desktop"
status: done
---

# Test Plan: Multi-Surface TUI and Desktop

## Scope

Tests covering Ink/React TUI (ui-tui/), JSON-RPC backend (tui_gateway/), Electron desktop app (apps/desktop/), web dashboard PTY bridge (web/), and dashboard SPA.

## Test Files

- tests/hermes_cli/test_tui_*.py — TUI backend tests
- tests/hermes_cli/test_dashboard_*.py — Dashboard endpoint tests
- tests/hermes_cli/test_web_server_*.py — Web server tests (20+ files)
- tests/hermes_cli/test_pty_bridge.py — PTY bridge tests
- tests/hermes_cli/test_tui_bundled.py — Bundled TUI tests
- tests/hermes_cli/test_dashboard_auth*.py — Dashboard auth tests
- tests/hermes_cli/test_dashboard_lifecycle_flags.py — Dashboard lifecycle

## JavaScript/TypeScript Tests

- ui-tui/ — Tests use vitest (npm test in ui-tui)
- apps/desktop/ — Vitest for desktop unit tests
- apps/shared/ — Vitest for shared package
- web/ — Vitest for web dashboard

## Unit Tests

- JSON-RPC method/event serialization
- Gateway client connection management
- Session picker state management
- Slash command completion logic
- Theme/skin data application

## Integration Tests

- Full TUI startup via hermes --tui
- Dashboard server boot and health check
- WebSocket PTY bridge connection lifecycle
- API server session browse and search
- Dashboard auth flow (login, token, cookies)
- Dashboard TUI back-compat mode

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| TUI backend crashes | Ink frontend shows error and offers restart |
| PTY bridge process dies | Dashboard shows disconnected state |
| Desktop app backend unresponsive | Reconnection with exponential backoff |
| WebSocket disconnection mid-stream | Reconnect and resume |
| Dashboard auth token expired | Redirect to login with return URL |

## Test Infrastructure

- JSON-RPC mock gateway for TUI backend tests
- Flask/FastAPI test client for web server
- Headless browser for dashboard SPA (when available)
- Temp ports for web server tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (TUI chat streaming) | test_tui_resume_flow.py |
| FR-2 (TUI session picker) | Session picker tests |
| FR-3 (TUI approvals) | Approval integration tests |
| FR-4 (TUI slash commands) | Slash command tests |
| FR-5 (TUI path completion) | Path completion tests |
| FR-7 (desktop WebSocket backend) | Web server tests |
| FR-8 (dashboard PTY bridge) | test_pty_bridge.py |
| NFR-1 (50ms input latency) | Performance measurement tests |

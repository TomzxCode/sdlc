---
title: "Gateway Server"
status: done
---

# Test Plan: Gateway Server

## Scope

Tests cover HTTP/WebSocket server functionality, authentication, session lifecycle, CLI backend connectivity, and gateway stability. Does not cover channel-specific or agent runtime behavior.

## Unit Tests

| File | Description |
|---|---|
| `src/gateway/gateway.test.ts` | Core gateway HTTP/WS server, auth, session management |
| `src/gateway/gateway-misc.test.ts` | Miscellaneous gateway functionality |
| `src/gateway/gateway-stability.test.ts` | Stability and error recovery scenarios |
| `src/gateway/gateway-cli-backend.connect.test.ts` | CLI backend connection handling |

## Integration Tests

| File | Description |
|---|---|
| `test/gateway.multi.e2e.test.ts` | Multi-gateway end-to-end scenarios |

## Live Tests

| File | Description |
|---|---|
| `src/gateway/gateway-cli-backend.live.test.ts` | Live CLI backend integration |
| `src/gateway/gateway-codex-harness.live.test.ts` | Codex harness live integration |
| `src/gateway/gateway-codex-bind.live.test.ts` | Codex binding live integration |
| `src/gateway/gateway-acp-bind.live.test.ts` | ACP binding live integration |
| `src/gateway/gateway-acp-spawn-defaults.live.test.ts` | Agent spawn defaults via ACP |

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Invalid auth token | Request rejected with 401 |
| Gateway crash recovery | Sessions recoverable from SQLite storage |
| Concurrent WebSocket connections | Connections handled without degradation |
| Graceful shutdown | Active sessions drained before exit |

## Test Infrastructure

- Vitest unit test runner with project matrix
- Mock HTTP and WebSocket servers for gateway testing
- SQLite in-memory database for session state tests
- Live tests require running gateway instance

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (HTTP/WS endpoints) | `gateway.test.ts` |
| FR-2 (Auth) | `gateway.test.ts` |
| FR-3 (Session management) | `gateway.test.ts`, `gateway-misc.test.ts` |
| FR-5 (Health check) | `gateway.test.ts` |
| FR-6 (Graceful shutdown) | `gateway-stability.test.ts` |
| NFR-1 (Crash recovery) | `gateway-stability.test.ts` |
| NFR-2 (No secrets in logs) | `gateway.test.ts` |

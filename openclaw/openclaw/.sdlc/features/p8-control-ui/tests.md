---
title: "Control UI"
status: done
---

# Test Plan: Control UI

## Scope

Tests cover UI components, routing, theming, gateway store interaction, agent selection, markdown rendering, and native bridge functionality. Does not cover gateway server behavior or browser compatibility.

## Unit Tests

| File | Description |
|---|---|
| `ui/src/app/app-host.test.ts` | Application host component |
| `ui/src/app/router-outlet.test.ts` | Client-side routing |
| `ui/src/app/theme.test.ts` | Theme management |
| `ui/src/app/custom-theme.test.ts` | Custom theme overrides |
| `ui/src/app/control-ui-chunking.test.ts` | UI chunking/lazy loading |
| `ui/src/app/gateway-store.test.ts` | Gateway state store |
| `ui/src/app/agent-selection.test.ts` | Agent selection UI |
| `ui/src/app/native-bridge.test.ts` | Native bridge communication |
| `ui/src/components/app-sidebar.test.ts` | Sidebar navigation |
| `ui/src/components/markdown.test.ts` | Markdown rendering |

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Gateway disconnected | UI shows connection error, auto-reconnect |
| Empty session list | Empty state displayed with create prompt |
| Large response streaming | Incremental rendering without jank |
| Invalid theme config | Graceful fallback to default theme |

## Test Infrastructure

- Vitest unit test runner
- Lit testing utilities
- Mock WebSocket for gateway store tests
- Component fixtures for rendering tests

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (Chat interface) | `gateway-store.test.ts`, `app-host.test.ts` |
| FR-2 (Streaming) | `gateway-store.test.ts` |
| FR-3 (Rich rendering) | `markdown.test.ts` |
| FR-4 (Session management) | `gateway-store.test.ts` |
| FR-5 (Gateway status) | `gateway-store.test.ts` |
| FR-7 (Config editing) | Covered by config CLI tests |
| NFR-1 (Auth enforcement) | Covered by gateway auth tests |

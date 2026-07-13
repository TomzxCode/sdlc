---
title: "Web & Desktop Apps"
status: done
---

# Test Plan: Web & Desktop Apps

## Scope

Web application frontend, Electron desktop app, shared UI components, and session UI components.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Web app component renders | Route path | Component mounted |
| TC-2 | Session UI renders messages | Message data | Markdown rendered correctly |
| TC-3 | Desktop app main process | App start | Window created |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-4 | Web app connects to server | Server running | API calls succeed |
| TC-5 | Desktop auto-updater | New version available | Update prompt shown |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-6 | Full session flow in web app | Create session, send message, view response | End-to-end success |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-03 | TC-4 |
| FR-04 | TC-5 |

## Test Files

- `packages/app/test/` (browser and unit tests)
- `packages/app/e2e/` (Playwright E2E tests)

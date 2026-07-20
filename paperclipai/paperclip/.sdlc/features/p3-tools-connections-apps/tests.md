---
title: "Tools, Connections & Apps"
status: done
---

# Test Plan: Tools, Connections & Apps

## Scope

Tests cover tool access policy validation, app gallery functionality, connection management UI, OAuth flow logic, and integration points between the tools subsystem and the rest of the Paperclip platform.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Tool access validator rejects invalid permissions | Invalid permission value | Validation error |
| TC-2 | Tool app gallery returns categorized app list | No filter | List of app definitions with categories |
| TC-3 | Human-friendly connection name formatting | Connection object | Formatted display string |
| TC-4 | App gallery search/filter works correctly | Search query | Filtered app list |

Files: `packages/shared/src/validators/tool-access.test.ts`, `packages/shared/src/tool-app-gallery.test.ts`, `packages/shared/src/humanize-connection.test.ts`

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Browse page loads and renders connections | User is authenticated, connections exist | Connection list displayed |
| TC-6 | App detail page shows app information | App ID is valid | App info with install button |
| TC-7 | Connections management page works | User has connected services | Connections displayed, can reconnect |
| TC-8 | Apps connect flow works end-to-end | User initiates connection | OAuth flow begins |
| TC-9 | Tool policies tab renders correctly | Company has tool policies | Policy list with edit capabilities |
| TC-10 | Tool runtime tab displays correctly | Company has runtime slots | Runtime slot list with status |

Files: `ui/src/pages/apps/Browse.test.tsx`, `ui/src/pages/apps/AppDetail.test.tsx`, `ui/src/pages/apps/Connections.test.tsx`, `ui/src/pages/apps/AppsConnect.test.tsx`, `ui/src/pages/tools/PoliciesTab.test.tsx`, `ui/src/pages/tools/RuntimeTab.test.tsx`

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-01 (OAuth connections) | TC-8 (UI), TC-7 (UI) |
| FR-02 (tool access policies) | TC-1 (unit), TC-9 (UI) |
| FR-04 (runtime profiles) | TC-10 (UI) |
| FR-07 (app gallery) | TC-2 (unit), TC-5 (UI), TC-6 (UI) |

---
title: "Cloud Upstreams"
status: done
---

# Test Plan: Cloud Upstreams

## Scope

Tests cover cloud upstream CLI commands and UI pages.

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-1 | CLI cloud commands work | Authenticated CLI | Cloud upstream CRUD operations succeed |
| TC-2 | UI cloud upstream page renders | Company has configured upstreams | Upstream list and detail display correctly |

Files: `cli/src/__tests__/cloud.test.ts`, `ui/src/pages/CloudUpstream.test.tsx`

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-01 through FR-09 | TC-1 (CLI), TC-2 (UI) |

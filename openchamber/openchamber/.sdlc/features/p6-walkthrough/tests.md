---
title: "Changes Walkthrough"
status: done
---

# Test Plan: Changes Walkthrough

## Scope

Tests cover the server-side walkthrough pipeline: diff parsing and hunk identity, source handling, digest construction, response normalization, caching, progress/cancellation routing, and the per-feature model settings. UI rendering of stops is covered indirectly through the store.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Parse a unified diff into files and hunks with stable ids | Unified diff string | Files + hunks with content-addressed ids |
| TC-2 | Duplicate byte-identical hunks receive -2/-3 suffixes | Diff with repeated hunks | Distinct suffixed ids |
| TC-3 | Editing a hunk changes its id | Two diffs differing in one hunk | Only that hunk's id differs |
| TC-4 | Digest construction maps hunks and aliases | Diff sections | Model-facing digest + alias/id mapping |
| TC-5 | Response schema normalization tolerates malformed JSON | Raw model output | Normalized walkthrough object |
| TC-6 | Generated/tool-produced files excluded from model input | Diff containing generated files | Files filtered out |
| TC-7 | Model settings resolve feature override vs default | Config with/without override | Correct model selected |
| TC-8 | Store caches content-addressed entries and invalidates pointers | Generate + regenerate same diff | Cache hit on unchanged diff |
| TC-9 | Language selection constrains prose languages | Selected language | Languages allowed set |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-10 | POST /api/walkthrough/generate runs the pipeline | Server running, diff present | Walkthrough generated and persisted |
| TC-11 | Progress endpoint reports in-flight generation | Generation in progress | Progress percentage returned |
| TC-12 | Cancel endpoint stops generation | Generation in progress | Status transitions to cancelled |
| TC-13 | PR diff loads through the GitHub helper | Repo with an open PR | PR walkthrough generated from merge-base diff |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-14 | Walkthrough requested with an unknown diff source | HTTP 400 INVALID_SOURCE |
| TC-15 | Small-model call fails | HTTP 500 GENERATION_FAILED, no partial stop persisted |
| TC-16 | Empty diff (no changes) | Empty walkthrough, no model call |

## Test Infrastructure

- `packages/web/server/lib/walkthrough/*.test.js` (digest, hunks, jobs, language, languages, model-settings, pull-request, routes, schema, store) — approximately 1400 lines of test code
- Mocked small-model caller; in-memory or temp-dir store
- GitHub helper mocked for PR source tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-10 |
| FR-2 | TC-1, TC-13 |
| FR-3 | TC-4, TC-5 |
| FR-4 | TC-2, TC-3 |
| FR-5 | TC-10 |
| FR-6 | TC-11, TC-12 |
| FR-7 | TC-8 |
| FR-8 | TC-7 |
| FR-9 | TC-9 |
| FR-10 | TC-13 |
| FR-11 | TC-6 |
| NFR-1 | TC-11, TC-12 |
| NFR-2 | TC-1 |
| NFR-3 | TC-3, TC-8 |

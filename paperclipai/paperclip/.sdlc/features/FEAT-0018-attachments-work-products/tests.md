---
title: "Attachments & Work Products"
status: done
session_link: "reverse-engineered during sync (no session)"
---

# Test Plan: Attachments & Work Products

## Scope

Issue attachment routes (upload, serve, delete) are covered by existing server route tests.
Docs evidence exists in doc/AGENT-ARTIFACTS.md.
Out of scope: S3-provider paths (deployment-dependent) and malware scanning (FR-08, not implemented per spec risks).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Attachment upload validates allowlist and size limits | Valid, disallowed, oversized files | Stored record or 400 INVALID_INPUT (server/src/__tests__/issue-attachment-routes.test.ts, 24 cases) |
| TC-2 | Inline content serves correct content type | Image attachment request | 200 with negotiated content type |
| TC-3 | Video byte-range requests return partial content | Range header on video asset | 206 with Content-Range and Accept-Ranges: bytes |
| TC-4 | Attachment deletion removes record | Delete request | Record removed; 404 thereafter |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-5 | Work-product creation links artifact or workspace file to issue | Existing issue and asset | issue_work_products row created; activity event emitted |

## End-to-End Tests

None automated for this feature.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Malformed Range header | 416 with Content-Range bytes */size |
| TC-7 | Cross-company attachment access | 403 UNAUTHORIZED |

## Test Infrastructure

- Existing vitest suite server/src/__tests__/issue-attachment-routes.test.ts.
- Schema tables assets and issue_work_products exist in packages/db/src/schema.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-1 |
| FR-02 | TC-2 |
| FR-03 | TC-2 (download disposition path in same serving code) |
| FR-04 | TC-3, TC-6 |
| FR-05 | TC-4 |
| FR-06 | TC-5 |
| FR-07 | Gap: S3 provider path not covered by automated tests |
| FR-08 | Gap: malware scanning not implemented |
| NFR-01 | TC-1 |
| NFR-02 | TC-3 (streaming range logic present; memory profile not asserted) |

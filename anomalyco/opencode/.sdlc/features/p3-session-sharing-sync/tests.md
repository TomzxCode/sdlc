---
title: "Session Sharing & Sync"
status: done
---

# Test Plan: Session Sharing & Sync

## Scope

Share creation/removal, host selection, debounced sync coalescing, snapshot tracking/diffing/restore/revert, and import from a share URL.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Request uses legacy share API without active org account | No account; enterprise url configured | `api.create` = `/api/share`, baseUrl = configured enterprise url, empty headers |
| TC-2 | Request uses default host when no enterprise config | No account, no enterprise url | baseUrl = `https://opncd.ai` |
| TC-3 | Request uses console API with auth headers when account active | Seeded account with org | `api.create` = `/api/shares`, headers carry bearer token and `x-org-id` |
| TC-4 | Share create posts to host and persists row | Mock HTTP client | Row in SessionShareTable with id/url/secret; one POST sent |
| TC-5 | Share remove deletes local row and calls delete endpoint | Mock HTTP client | Row gone; POST then DELETE observed |
| TC-6 | Share create fails on non-ok response without persisting | Host returns 500 | Effect fails; no row persisted |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Coalesces rapid diff events into one delayed sync with latest data | Shared session; two `Session.Event.Diff` publishes | Exactly one sync request carrying the latest (second) diff |
| TC-8 | Tracks deleted files correctly | Git worktree, tracked snapshot, file removed | `patch(before).files` contains the deleted file |
| TC-9 | Revert removes new files | Snapshot taken, new file added | After revert, new file no longer exists |
| TC-10 | Restore returns snapshot state | Files modified after snapshot | Files restored to snapshot content |
| TC-11 | Snapshot respects gitignore and size limits | Ignored, large, and binary files present | Ignored/large/binary files excluded from patches and diffs |
| TC-12 | Snapshot handles non-ASCII and long paths | Unicode and 200-char filenames | Patches and diffs computed correctly |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-13 | Import a session from a share URL | `opencode import <url>` against a live share | Session recreated locally with messages and diffs |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-14 | Sharing disabled via config or env | `SessionShare.share` throws; no host call |
| TC-15 | Sync flush fails (HTTP >= 400) | Warning logged; server continues; next event triggers another flush |
| TC-16 | Reverting a file not present in snapshot | File deleted |
| TC-17 | Revert batch crossing the 100-file boundary | Batched checkout falls back to per-file operations correctly |
| TC-18 | Non-git VCS | Snapshot tracking disabled |

## Test Infrastructure

- Mock `HttpClient.HttpClient` layers to simulate the share host.
- `provideTmpdirInstance` / `it.instance` fixtures with `{ git: true }` for snapshot tests.
- `pollWithTimeout` to wait for debounced flushes instead of fixed sleeps.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-01 | TC-4 |
| FR-02 | TC-4 |
| FR-03 | TC-7 |
| FR-04 | TC-7 |
| FR-05 | TC-14 |
| FR-06 | TC-1, TC-2, TC-3 |
| FR-07 | TC-5 |
| FR-08 | TC-8, TC-11, TC-12 |
| FR-09 | TC-9, TC-10, TC-16, TC-17 |
| FR-10 | TC-13 |
| FR-11 | TC-7 |
| NFR-01 | TC-14 |
| NFR-02 | TC-7 |
| NFR-03 | TC-15 |
| NFR-04 | TC-11 |

## Test Files

- `packages/opencode/test/share/share-next.test.ts`
- `packages/opencode/test/snapshot/snapshot.test.ts`
- `packages/enterprise/test/core/share.test.ts`
- `packages/enterprise/test/core/storage.test.ts`

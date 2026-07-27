---
title: "Session Sync & Management"
status: done
---

# Test Plan: Session Sync & Management

## Scope

Tests cover session file discovery, agent-specific parsing, sanitization, database writing, incremental and full resync, file watcher, periodic scanning, skip cache, remote sync via SSH, S3-based discovery, and SSE notification.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Engine discovers session files from configured directories | Provider config with session files | All files discovered and queued |
| TC-2 | Parser extracts messages, tool calls, usage from session files | Agent-specific session file | Structured ParsedSession output |
| TC-3 | Sanitizer clamps tokens, blanks timestamps, coerces roles | ParsedSession with edge case values | Sanitized ParsedSession |
| TC-4 | Skip cache tracks failed files by path and mtime | Failed parse result | Entry added to skip cache |
| TC-5 | File watcher detects new/changed files via fsnotify | fsnotify event stream | Changed files dispatched to parser |
| TC-6 | CWD filter correctly scopes sync to working directory | CWD config + session paths | Only matching paths synced |
| TC-7 | Periodic scan discovers new files after startup | File added between scans | File discovered on next scan |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-8 | Full sync engine integration with real directory | Session files on disk | Sessions parsed and written to DB |
| TC-9 | Incremental resync updates changed sessions | Previously synced session modified | Session re-parsed and updated |
| TC-10 | Remote sync via SSH | SSH host configured | Remote sessions synced locally |
| TC-11 | S3-compatible storage as session source | S3 bucket configured | Sessions discovered and synced from S3 |

## Test Files

- `internal/sync/engine_test.go` - Engine discovery, sync, and lifecycle tests
- `internal/sync/engine_integration_test.go` - Integration tests with real directories
- `internal/sync/watcher_test.go` - File watcher behavior tests
- `internal/sync/hash_test.go` - File hashing for change detection
- `internal/sync/parsediff_*_test.go` - Parse diff comparison tests
- `internal/sync/s3_test.go` - S3-based discovery tests
- `internal/sync/secret_*_test.go` - Secret scanning integration during sync
- `internal/parser/*_test.go` - Per-agent parser tests (50+ agents)
- `internal/parser/provider_test.go` - Provider factory tests
- `internal/parser/discovery_test.go` - Discovery path resolution tests
- `internal/sync/provider_process_test.go` - Provider processing lifecycle
- `internal/sync/cwd_filter_test.go` - CWD filter tests

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-12 | Malformed session file | Parsing error tracked, sync continues |
| TC-13 | File removed during sync | Graceful skip, no crash |
| TC-14 | Directory with thousands of files | File watcher handles volume |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-8 |
| FR-2 | TC-2 |
| FR-3 | TC-3 |
| FR-4 | TC-8 |
| FR-5 | TC-9 |
| FR-6 | TC-5 |
| FR-7 | TC-7 |
| FR-8 | TC-4 |
| FR-9 | TC-10 |
| FR-10 | TC-11 |

---
title: "Admin & Operations"
status: done
---

# Test Plan: Admin & Operations

## Scope

Tests cover secret scanning, session export (HTML, GitHub Gist), Claude.ai/ChatGPT import, self-update, remote sync via SSH, AI-generated insights, session health grades, and starring/pinning.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Secret scanning detects API key patterns | Session content with secrets | Findings recorded with redacted matches |
| TC-2 | Session export produces valid HTML | Session data | HTML output |
| TC-3 | Import from Claude.ai/ChatGPT | Export archive | Sessions imported into SQLite |
| TC-4 | Self-update check | Current version + remote | Update available/not available |
| TC-5 | Remote sync via SSH | SSH host config | Sessions synced from remote |
| TC-6 | Secret ruleset version handling | Ruleset version | Correct rule application |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-7 | Full remote sync lifecycle | SSH configured | Sessions transferred and indexed |
| TC-8 | Canonical JSON export/import | Session data | Round-trip fidelity |
| TC-9 | Insight generation from session data | Sessions with messages | Structured insights produced |

## Test Files

- `internal/secrets/secrets_test.go` - Secret scanning tests
- `internal/secrets/rules_test.go` - Ruleset tests
- `internal/secrets/bench_test.go` - Scanning performance benchmarks
- `internal/export/canonical_json_test.go` - Canonical JSON export/import
- `internal/export/pricing_test.go` - Pricing export tests
- `internal/export/project_identity_test.go` - Project identity export
- `internal/importer/importer_test.go` - Import tests
- `internal/importer/assets_test.go` - Import asset tests
- `internal/importer/zip_test.go` - Zip import tests
- `internal/update/update_test.go` - Self-update tests
- `internal/remotesync/archive_test.go` - Remote sync archive tests
- `internal/remotesync/http_test.go` - Remote sync HTTP tests
- `internal/remotesync/manifest_test.go` - Manifest tests
- `internal/remotesync/mirror_test.go` - Mirror tests
- `internal/remotesync/resolve_test.go` - Host resolution tests
- `internal/remotesync/cleanup_registry_test.go` - Cleanup registry tests
- `internal/remotesync/failure_test.go` - Failure handling tests
- `internal/remotesync/import_test.go` - Import tests
- `internal/remotesync/migration_test.go` - Migration tests
- `internal/ssh/ssh_test.go` - SSH connection tests
- `internal/ssh/classify_test.go` - SSH classification tests
- `internal/ssh/extract_test.go` - SSH path extraction tests
- `internal/ssh/resolve_test.go` - SSH resolution tests
- `internal/ssh/transfer_test.go` - SSH transfer tests
- `internal/insight/generate_test.go` - Insight generation tests
- `internal/insight/prompt_test.go` - Insight prompt tests
- `internal/insight/summary_test.go` - Insight summary tests
- `internal/db/secret_findings_test.go` - Secret findings DB tests

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-10 | SSH host unreachable | Sync fails with connect error |
| TC-11 | No new version available | Update reports up-to-date |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-6 |
| FR-2 | TC-2 |
| FR-4 | TC-3, TC-8 |
| FR-5 | TC-4 |
| FR-6 | TC-5, TC-7 |
| FR-7 | TC-9 |

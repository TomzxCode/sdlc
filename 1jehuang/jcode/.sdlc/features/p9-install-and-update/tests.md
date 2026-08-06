---
title: "Installation and Auto-Update"
status: done
---

# Test Plan: Installation and Auto-Update

## Scope

Covers installer correctness, update conversion, Windows launcher lifecycle, and Discord release posting. Out of scope: live production release flows (verified in CI release pipeline).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Update core logic | `crates/jcode-update-core` tests | Update download/stage/activate logic works |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-2 | Install conversion | `scripts/test_install_conversion.sh` | Install script converts download to working install |
| TC-3 | Windows launcher install lifecycle | `scripts/test_windows_launcher_install.ps1` | Launcher installs and runs on Windows |
| TC-4 | Release Discord posting | `scripts/test_post_discord_release.py` | Discord post generated correctly |
| TC-5 | Windows smoke in CI | `windows-smoke.yml`, `freebsd-smoke.yml` | Platform smoke tests pass |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-6 | Interrupted download | Current install stays usable; retry safe |
| TC-7 | Divergent local clone during git-pull update | Divergence handled without breaking install |
| TC-8 | Reload with open sessions | Sessions preserved; clients reconnect |

## Test Infrastructure

- CI release/smoke workflows (`release.yml`, `windows-smoke.yml`, `freebsd-smoke.yml`).
- Python and PowerShell test scripts for install/Discord flows.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-2 |
| FR-2 | TC-3 |
| FR-5 | TC-8 |
| FR-8 | TC-4 |
| NFR-1 | TC-6 |
| NFR-2 | TC-8 |

---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The requirements were reverse-engineered on 2026-10-13 (v0.96.0) and have not been updated for v0.97.0 through v0.99.0.

## Completeness

| ID | Requirement to add | Evidence |
|---|---|---|
| FR-9 | The system shall publish platform package-manager releases (Homebrew and AUR) alongside the GitHub Release. | `.github/workflows/release.yml:1033` (Homebrew formula) and `:1120` (AUR package), maintained by `scripts/update_packages.sh:1-2`. |
| FR-10 | The system shall resolve installer versions and download bases from the release metadata service, and shall publish provenance and checksum artifacts. | `scripts/install.sh:5` and `scripts/install.ps1:52-55` resolve from `https://jcode.sh/releases`; `.github/workflows/release.yml:883-912` writes `release-provenance.json` and `SHA256SUMS`. |
| FR-11 | The system shall verify a published release before and after the public installer smoke test, and shall support recovery of a failed release. | `.github/workflows/release-recovery.yml`, `scripts/apply_release_recovery.py`, `scripts/verify_public_release.py`, `tests/test_release_recovery.py`, `tests/test_public_release_builds.py`, `tests/test_verify_public_release.py`, and the smoke step at `.github/workflows/release.yml:1005`. |
| FR-12 | The system shall publish the platform runtime packages consumed by the npm launcher distribution. | `sdk/npm/{darwin-arm64,darwin-x64,linux-arm64,linux-x64,win32-arm64,win32-x64}/package.json`, `.github/workflows/publish-typescript-sdk.yml`, `scripts/prepare_sdk_runtime_packages.sh`, `scripts/sdk_publish_preflight.sh`. |

## Clarity

No requirement rewording is required.
FR-1 through FR-8 all remain accurate against the code.

## Testability

The acceptance criteria cover FR-1 through FR-8, but the coverage matrix in `tests.md` has no row for FR-3, FR-4, FR-6, FR-7, NFR-3, or NFR-4.
Each added FR needs at least one Gherkin acceptance criterion.

## Feasibility

No issues found.

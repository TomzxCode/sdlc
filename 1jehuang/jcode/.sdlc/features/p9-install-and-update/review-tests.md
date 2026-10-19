---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The test plan was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Coverage

| ID | Documented input | Reality | Correction |
|---|---|---|---|
| TC-1 | "Update core logic \| `crates/jcode-update-core` tests \| Update download/stage/activate logic works" | The crate now holds only pure helpers (checksums, divergence classification, progress bar formatting, duration estimates). It does not cover download, stage, or activate. | Reword TC-1 to "Update helper logic \| `crates/jcode-update-core` `mod tests` \| Checksum parsing and verification, divergence classification, progress formatting, and duration estimates behave as specified", and add a new entry for the engine itself over `crates/jcode-app-core/src/update_tests.rs` (resume after a dropped connection, release-versus-dev ancestry guard, channel advance). |

TC-2 through TC-8 all still exist and remain accurate.

## Missing Scenarios

Test files that exist in the repository and cover this feature but are absent from the plan:

- `crates/jcode-app-core/src/update_tests.rs` (591 lines: the actual engine tests, including resume, the ancestry guard, auto-update gating, git-pull summaries, and Termux patching via `update_termux_tests.rs`)
- `crates/jcode-build-support/src/tests.rs` (including the launcher symlink tests at `:236` and `:603`) and `crates/jcode-build-support/src/storage_helpers.rs:243-282` (Windows builds-dir resolution)
- `scripts/test_install_release_metadata.sh` (installer release-metadata resolution)
- `scripts/test_quick_release.py` (quick-release flow)
- `tests/test_release_recovery.py`, `tests/test_public_release_builds.py`, `tests/test_verify_public_release.py`, `tests/test_watch_release_run.py`, `tests/test_release_ci.py`
- `scripts/check_release_ci.py`, `scripts/verify_public_release.py`, `scripts/update_rehearsal.py`, `scripts/apply_release_recovery.py`
- `scripts/test_sdk_package.sh`, `scripts/test_sdk_e2e.sh`, `scripts/sdk_publish_preflight.sh` (SDK and npm distribution)
- `tests/test_selfdev_reload.py` (the self-dev reload path)

## Quality

The existing entries remain accurate apart from TC-1.

## Correctness

No issues found.

## Maintainability

No issues found.

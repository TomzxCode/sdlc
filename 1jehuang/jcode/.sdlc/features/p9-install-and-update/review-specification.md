---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

## Sync drift: 2026-10-19

The specification was reverse-engineered on 2026-10-13 (v0.96.0) and has not been updated for v0.97.0 through v0.99.0.

## Inconsistencies

| Location | Current wording | Code reality | Correction |
|---|---|---|---|
| Overview | "the update engine in `crates/jcode-update-core` (download from GitHub Releases, git-pull handling, divergence detection)" | The engine lives in `crates/jcode-app-core/src/update.rs` (1308 lines): `run_git_pull_ff_only` (`:134`), `fetch_latest_release_blocking` (`:203`), `prepare_update_blocking` (`:478`), `check_for_update_blocking` (`:590`), `download_and_install_blocking_with_progress` (`:970`), `check_and_maybe_update` (`:1197`). `crates/jcode-update-core` is now a helper crate with only pure functions (version comparison, asset naming, checksum parsing, divergence classification, progress formatting, duration estimates). | Reword to: "the update engine in `crates/jcode-app-core/src/update.rs` (download from GitHub Releases, git-pull handling, divergence detection, versioned install and channel repointing), with shared pure helpers in `crates/jcode-update-core`". |
| API Contracts | heading "### Update check (`jcode-update-core`)" | Same as above. | Reword the heading to `crates/jcode-app-core/src/update.rs`, with helpers in `crates/jcode-update-core`. |
| API Contracts | "Queries GitHub Releases for the configured channel (`stable`/`main`)." | The `main` channel is not a Releases query. `UpdateChannel::Main` calls `prepare_main_update_blocking` (`crates/jcode-app-core/src/update.rs:406-476`), which queries `https://api.github.com/repos/1jehuang/jcode/commits/main` (`:263`), builds from source with cargo, and installs as `main-<sha>` (`:347-361`). The enum lives at `crates/jcode-config-types/src/lib.rs:284-329`. | Reword: "On the `stable` channel, queries GitHub Releases for the latest published release. On the `main` channel, queries the GitHub API for the latest commit on `main`, rebuilds from source, and installs it as `main-<sha>`." |
| Architecture | ".github/workflows/release.yml (Linux/macOS/Windows builds, signing)" | The workflow also builds FreeBSD (`:666`, artifact at `:745`), runs a `recovery-preflight` job (`:148`), updates the Homebrew formula (`:1033`), and updates the AUR package (`:1120`). | Reword to: ".github/workflows/release.yml (Linux/macOS/Windows/FreeBSD builds, Windows signing, Homebrew and AUR publish)". |
| Architecture | "├── scripts/generate_release_notes.sh" | The script still exists, but the canonical release notes are now generated in the workflow (`.github/workflows/release.yml:117,914`). | Annotate the row: "scripts/generate_release_notes.sh (the workflow is authoritative)". |
| Data Models | a 4-row table for versions, stable, current, and shared-server | `crates/jcode-build-support/src/storage_helpers.rs:44-91` also defines `builds/canary/jcode` (`:67-70`), `builds/source/jcode` (the source-build root, `crates/jcode-app-core/src/update.rs:96-102`), `builds/manifest.json` (`:39-41`), and the marker files `builds/stable-version`, `builds/current-version`, `builds/shared-server-version` (`:78-91`). On Windows the builds root is `%LOCALAPPDATA%\jcode\builds` (`:28-33`). | Add rows for the canary channel, the source-build root, and the version marker files, and note the Windows builds root. |
| Technical Decisions | "Separate update crate \| `jcode-update-core` \| Isolates download/pull/divergence logic." | The crate has no download code path at all; the download with HTTP Range resume lives in `crates/jcode-app-core/src/update.rs:970-1091` (`download_asset_with_resume`, 120 second per-attempt budget, up to 10 attempts). | Reword to: "Separate update crate \| `jcode-app-core/src/update.rs` plus `jcode-update-core` helpers \| Keeps the engine out of the base layer while the pure helpers (checksums, divergence classification, duration estimates) stay independently testable." |
| Out of Scope | "A system package manager integration (Homebrew exists for macOS; others inferred.)" | Homebrew and AUR are both published from `release.yml`. | Reword to: "Containerized distribution of the agent runtime. (Homebrew and AUR taps are published from `release.yml` and are in scope for FR-9.)" |

## Missing Information

- The npm SDK distribution channel is not mentioned anywhere in the artifact.
- The crates.io name reservation (`packaging/crates-io-placeholder/`) is not mentioned.
- The packaged local runtime upgrade path (`crates/jcode-app-core/src/server/runtime_upgrade.rs:1-330`: ELF and Mach-O magic validation, owner and mode checks, idle-agent reservation, exec of `serve --socket` on the same socket) is distinct from the exec-based hot reload the Sequences describe.
- The stale shared-server channel repair (`crates/jcode-app-core/src/update.rs:1258`, `src/cli/hot_exec.rs:450-478`) is not described.

## Implementability

No issues found beyond the corrections above.

## Reversibility

No issues found.

## Forward Compatibility

No issues found.

## Ambiguities

No issues found.

## Incoherences

No issues found.

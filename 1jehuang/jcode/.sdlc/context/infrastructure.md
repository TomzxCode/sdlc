# Infrastructure

## Technology stack

| Component | Technology | Version |
|---|---|---|
| Language | Rust | Edition 2024, package jcode 0.99.0 |
| Client SDK | TypeScript | sdk/typescript, published to npm as `@1jehuang/jcode-sdk` 1.2.0 |
| SDK runtime packages | npm platform packages | sdk/npm, `@1jehuang/jcode-<platform>` 1.2.0, installed as optionalDependencies of the SDK |
| Mobile client | Swift | ios/ (JCodeKit plus JCodeMobile) |
| Telemetry store | SQL via Cloudflare D1 | telemetry-worker, D1 `jcode-telemetry` plus R2 and six Analytics Engine datasets, 31 migrations |
| Installers | Bash and PowerShell | scripts/install.sh and scripts/install.ps1, published at https://jcode.sh/install and https://jcode.sh/install.ps1 |
| Distribution | GitHub Releases plus package managers | 9 platform assets with SHA256SUMS and release-provenance.json, npm SDK and runtime packages, Homebrew tap, AUR |
| Workspace | Cargo workspace | 88 crates under crates/ plus root |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| justrust | Primary build and test driver (hosted build service client) | `justrust check`, `justrust test` |
| nix | Optional development shell with the pinned toolchain and native libraries | `nix develop` in the repository root |
| rustfmt | Formatting | `cargo fmt --all -- --check` |
| clippy | Linting | `cargo clippy --locked --all-targets --all-features -- -D warnings` |
| cargo test | Testing | `cargo test` (CI also runs `cargo test --locked --test e2e` and `--test provider_matrix`) |
| budget ratchets | Quality gates | `scripts/check_warning_budget.sh` (against `scripts/warning_budget.txt`), `check_code_size_budget.py` (against `scripts/code_size_budget.json`, 1200 lines per file), `check_test_size_budget.py`, `check_panic_budget.py`, `check_swallowed_error_budget.py`, `check_wildcard_reexport_budget.py`, plus the `scripts/test_check_warning_budget.sh` contract test |
| other CI gates | Quality gates | `scripts/check_module_files.py`, `scripts/check_dependency_boundaries.py`, `scripts/security_preflight.sh --strict` (Linux only) |
| npm | TypeScript SDK | `npm run check` (typecheck plus build plus `node --test`) in sdk/typescript |
| swift and xcodebuild | iOS | `swift test` in ios/, `xcodegen generate` plus a simulator `xcodebuild build`, then archive and export to App Store Connect |

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Local development | master (CI also accepts main) | Daily development and PR integration | Local daemon over a Unix socket at `$XDG_RUNTIME_DIR/jcode.sock` |
| Release channels | master, tags v<version> | GitHub Releases install, on-disk stable, current, shared-server, and canary channels, optional main self-update channel | https://jcode.sh/install |
| Telemetry production | manual deploy from telemetry-worker/ | Usage telemetry collection (D1 plus R2 plus Analytics Engine) | https://telemetry.jcode.sh (also telemetry.solosystems.dev) |

## CI/CD pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| ci.yml | Push and pull request on main and master | Ten jobs: quality (module declarations, fmt, check, clippy, Cargo.lock freshness, all six budgets, dependency boundaries, Rust and TypeScript SDK parity, unused dependencies), release automation, Linux and macOS build with provider matrix, e2e, TUI, embedding, and security preflight, Windows build and test, fmt, TypeScript SDK, setup friction, PowerShell syntax, Windows arm64, and Windows cross-check |
| release.yml | Tag push v* or manual dispatch | Builds and signs 9 platform assets, publishes the GitHub Release with checksums and provenance, verifies the public assets, smoke-tests the public Linux installer in an isolated home, updates Homebrew and AUR, and queues the Discord announcement |
| release-recovery.yml | Pull request and push on release paths, and manual | Runs the release recovery unit tests and the installer release-metadata test |
| freebsd-smoke.yml | Weekly cron, push on its own path, and manual | Builds and tests inside a real FreeBSD 15.1 QEMU guest |
| windows-smoke.yml | Manual dispatch (x64, arm64, or both) | Release build, targeted Windows validation, e2e smoke, Windows lifecycle e2e, and installer verification |
| windows-companion.yml | Pull request and push on companion paths, and manual | `justrust check` for the companion crate on x86_64 and aarch64 Windows |
| windows-transport.yml | Pull request and push on the transport and SDK paths, and manual | `justrust check` and `justrust test` for the transport and SDK crates on Windows amd64 and arm64, including native named-pipe tests |
| ios-testflight.yml | Push to master touching ios/ and manual | `swift test`, a simulator build, and an archive and App Store Connect upload (the TestFlight upload is currently blocked by signing) |
| require-issue.yml | Pull request | Enforces a linked, existing issue on every PR |
| publish-typescript-sdk.yml | Manual dispatch with a required released tag | Publishes the six `@1jehuang/jcode-<platform>` runtime packages and then `@1jehuang/jcode-sdk` to npm with provenance |
| discord-release.yml | Release published and manual | Posts the release notes to the Discord webhook |
| label-pr.yml | Check run completed and manual | Applies semantic pull request labels; failures do not redden the branch |
| update-star-history.yml | Daily cron and manual | Regenerates the star history chart |

## Deployment

- Releases are cut from master as GitHub Releases tagged v<version> following RELEASING.md quick and CI flows.
- Users install or upgrade via https://jcode.sh/install on Unix and install.ps1 on Windows. The installers resolve versions and download bases from the https://jcode.sh/releases metadata service.
- Platform runtime binaries ship as npm packages under sdk/npm (`@1jehuang/jcode-<platform>`), consumed as optionalDependencies of the SDK.
- Installed binaries are immutable under ~/.jcode/builds/versions/<version>/ (or <git-hash> for local release builds; %LOCALAPPDATA%\jcode\builds\versions\<version>\ on Windows) with channel symlinks for current, stable, shared-server, and canary.
- The long-lived local daemon runs from ~/.jcode/builds/shared-server/jcode and serves interactive and TUI clients. Headless `jcode run` executes its agent in-process and only starts a temporary server on an isolated socket when a tool requires one.
- Daemon updates require promoting the desired version onto the shared-server channel (`jcode server promote <version>`) and restarting the daemon with `jcode server reload`. `jcode self-dev --build` publishes to the current channel and repoints the launcher only.
- The telemetry worker deploys separately as a Cloudflare Worker backed by D1, from `telemetry-worker/` via `npm run deploy`. No CI workflow deploys it.

### Rollback

- Roll back the daemon with `jcode server promote <installed-version>` followed by `jcode server reload`.
- To roll back the installed release, reinstall with `JCODE_VERSION=vX.Y.Z` (scripts/install.sh) or `-Version` (scripts/install.ps1); the stable and shared-server channel symlinks then point at the restored version.

## Health checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| Daemon socket liveness | `jcode server start` succeeds or `jcode connect` attaches | The internal `has_live_listener` and `is_server_ready` probe in `crates/jcode-app-core/src/server/socket.rs` |
| http://<host>:7643/health | Server status from the remote-client gateway | Remote clients and operators, when `gateway.enabled` is true |
| https://telemetry.jcode.sh/v1/health | 200 OK with database size and prune state, or 500 if the D1 probe fails | `npm run health:size` in telemetry-worker/ (operator run); no CI job calls it |

- The daemon control plane is a Unix socket at `$XDG_RUNTIME_DIR/jcode.sock`, with no HTTP endpoint.
- The optional remote gateway is the one HTTP surface: `GET /health` and `POST /pair` over TCP on port 7643, plus the `GET /ws` WebSocket upgrade. It is off by default.

## Smoke tests

- Cross-platform smoke coverage lives in `tests/e2e` plus `freebsd-smoke.yml`, `windows-smoke.yml`, `windows-companion.yml`, and `windows-transport.yml`.
- Run the end-to-end suite with `cargo test --test e2e`; Cargo auto-discovers `tests/e2e/main.rs` as the `e2e` test target, and CI runs it per target in the build matrix.
- iOS smoke coverage runs through `ios-testflight.yml` and Xcode builds. The TestFlight upload is currently blocked by App Store Connect signing (`ios/PRODUCTION_CHECKLIST.md`).
- Feature-specific shell smoke scripts live under `scripts/` (for example `test_cloud_move_e2e.sh`, `test_install_conversion.sh`, `test_auth_e2e.sh`, `test_swarm.py`).

## Hosting

- The product is local-first with the daemon and TUI running on the user machine.
- Distribution hosting is GitHub Releases for binaries, npm for the SDK and platform runtime packages, plus Homebrew and AUR package updates.
- Installer metadata (versions, download bases, checksums) is served from `https://jcode.sh/releases`.
- Telemetry hosting is a Cloudflare Worker plus D1 at telemetry.jcode.sh.
- There is no separate staging environment and no infrastructure-as-code beyond worker config and install scripts.

## Secrets management

- Local auth state lives in owner-only files under `~/.jcode/` (`auth.json`, `openai-auth.json`, `gemini_oauth.json`, `antigravity_oauth.json`) and is never committed.
- Provider API-key environment files live in the platform config dir under `~/.config/jcode/*.env`.
- Runtime secrets are read from environment variables such as `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `CURSOR_API_KEY`, `ZAI_API_KEY`, `JCODE_BING_API_KEY`, and the Telegram, Discord, and Jade relay tokens, plus OAuth flows.
- Existing external credentials are reused from `~/.codex/auth.json`, `~/.claude/.credentials.json`, and other CLI stores (the full list is in `crates/jcode-sdk/src/launch.rs`).
- Credential files are never read through symlinks or non-regular files.
- Onboarding sandbox fixtures may contain real OAuth tokens copied from `$HOME`; they live under `/.tmp/` and must never be committed.

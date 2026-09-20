# Infrastructure

## Technology stack

| Component | Technology | Version |
|---|---|---|
| Language | Rust | Edition 2024, package jcode 0.85.0 |
| Client SDK | TypeScript | sdk/typescript, published to npm |
| Mobile client | Swift | ios/ (JCodeKit plus JCodeMobile) |
| Telemetry store | SQL via Cloudflare D1 | telemetry-worker migrations |
| Installers | Bash and PowerShell | scripts plus jcode.sh |
| Workspace | Cargo workspace | 84 crates under crates/ plus root |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| cargo fmt | Formatting | `cargo fmt` |
| clippy | Linting | `cargo clippy --all-targets --all-features -D warnings` |
| cargo test | Testing | `cargo test` |
| budget scripts | Quality gates | `scripts/` budget ratchet checks |
| npm | TypeScript SDK | `npm test` and `npm run build` in sdk/typescript |
| xcodebuild | iOS builds | Xcode TestFlight flow in ios/ |

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Local development | master | Daily development and PR integration | Local daemon over Unix socket |
| Release channels | master tags v<version> | Stable and main channel distribution | https://jcode.sh/install |
| Telemetry production | master | Usage telemetry collection | https://telemetry.jcode.sh |

## CI/CD pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| ci.yml | Push and pull request | fmt, clippy, budgets, cross-platform Linux, macOS, and Windows builds, TypeScript SDK, iOS TestFlight, and security |
| release.yml | Version tag | GitHub Releases build and channel publish |
| freebsd-smoke.yml | Scheduled and manual | FreeBSD smoke run |
| windows-smoke.yml | Scheduled and manual | Windows smoke run |
| ios-testflight.yml | Push and manual | iOS TestFlight build |
| require-issue.yml | Pull request | Enforces linked issue on every PR |
| publish-typescript-sdk.yml | Release | Publishes TypeScript SDK to npm |

## Deployment

- Releases are cut from master as GitHub Releases tagged v<version> following RELEASING.md quick and CI flows.
- Users install or upgrade via https://jcode.sh/install on Unix and install.ps1 on Windows.
- Platform launchers ship through npm launcher packages under sdk/npm.
- Installed binaries are immutable under ~/.jcode/builds/versions/<version>/ with channel symlinks for stable and main.
- The long-lived local daemon at ~/.jcode/builds/shared-server/jcode serves `jcode run` sessions.
- Daemon updates require repointing the shared-server symlink and restarting the daemon via `jcode self-dev --build`.
- Telemetry worker deploys separately as a Cloudflare Worker backed by D1.

### Rollback

- Roll back by reinstalling the prior versioned binary from GitHub Releases.
- Switch release channels to repoint stable or main away from a bad version.
- Restart the local daemon after repointing so runtime checks measure the restored binary.

## Health checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| Unix socket liveness | Daemon accepts `jcode run` on its socket | `jcode serve` supervision |
| https://telemetry.jcode.sh/v1/health | 200 OK from telemetry worker | Smoke scripts and operators |

- There is no local HTTP /health endpoint because the daemon listens on a Unix socket rather than HTTP.
- Socket liveness is confirmed by running a command against an isolated socket during self-dev testing.

## Smoke tests

- Cross-platform smoke coverage lives in tests/e2e plus freebsd-smoke.yml and windows-smoke.yml.
- Run the end-to-end suite with `cargo test` scoped to tests/e2e for post-deploy verification.
- iOS smoke coverage runs through ios-testflight.yml and Xcode builds.

## Hosting

- The product is local-first with the daemon and TUI running on the user machine.
- Distribution hosting is GitHub Releases for binaries and npm for launcher and SDK packages.
- Telemetry hosting is a Cloudflare Worker plus D1 at telemetry.jcode.sh.
- There is no separate staging environment and no infrastructure-as-code beyond worker config and install scripts.

## Secrets management

- Local auth state lives in ~/.jcode/auth and is never committed.
- Runtime secrets are read from environment variables and OAuth flows.
- Existing external credentials are reused from ~/.codex/auth.json and ~/.claude/.credentials.json where available.
- Tokens are excluded from git via .tmp/ gitignore rules and must never be committed.

# Infrastructure

## Technology stack

| Component | Technology | Version |
|---|---|---|
| Language | Go | 1.27.0 |
| Module | go.kenn.io/agentsview | N/A (version from git describe via ldflags) |
| HTTP API framework | Huma v2 (OpenAPI 3.1) | v2.39.1 |
| CLI framework | cobra | v1.10.2 |
| Primary database | SQLite via mattn/go-sqlite3, CGO, FTS5 build tag | v1.14.52 |
| Vector search bindings | sqlite-vec via go.kenn.io/kit vector package | asg017 bindings v0.1.6 (indirect) |
| PostgreSQL driver | pgx/v5 (optional push sync target, pgvector pg16 in tests) | v5.10.0 |
| DuckDB driver | duckdb-go/v2 (optional mirror and Quack reads) | v2.10505.0 |
| ClickHouse driver | clickhouse-go/v2 (optional remote mirror) | v2.48.0 |
| S3 discovery | minio-go/v7 | v7.3.0 |
| AI tool integration | MCP Go SDK | v1.7.0 |
| Frontend framework | Svelte | 5.57.0 |
| Frontend toolchain | Vite+ via vp CLI (Vite, Rolldown, Vitest, Oxlint, Oxfmt) | vite-plus 0.3.1, Node >= 24.11.0 |
| Frontend i18n | Paraglide JS with localStorage strategy | 2.20.2 |
| Frontend design system | kit-ui (commit-pinned git dependency) | 4e2d49e768d07c4ebca7da8dd37ca54f01cac28e |
| Frontend e2e | Playwright | 1.63.0 |
| Desktop wrapper | Tauri (desktop/) with macOS DMG, Windows NSIS, Linux AppImage targets | See desktop/src-tauri |
| API client generation | orval with Huma OpenAPI spec | 8.30.0 |

## Development tooling

| Tool | Purpose | Command |
|---|---|---|
| make | Build orchestration | `make build` (debug), `make build-release` (optimized) |
| go test | Backend tests, always with FTS5 tag | `go test -tags "fts5" ./...` (`make test`, `make test-short`) |
| custom-gcl (golangci-lint) | Go linting, pinned version | `make lint-golangci` (fix) / `make lint-ci` (CI, no fix) |
| NilAway | Nil-safety analysis via custom golangci plugin | `make nilaway` |
| kennlint | Shared lint config check plus SQL schema lint | `make lint-config-check`, `make lint-sql` |
| huma-check | Huma API contract check | `go run go.kenn.io/kit/cmd/huma-check@... -fix=false ./...` |
| prek | Pre-commit and pre-push hooks | `make install-hooks`, hooks defined in prek.toml |
| air | Backend live reload in development | `make dev` (pair with `make frontend-dev`) |
| vp / npm | Frontend dev, check, test, build | `vp dev`, `npm run check`, `npm run check:kit-ui`, `npm test`, `npm run build` |
| svelte-check | Frontend type checking | `npm run check` in frontend/ |
| Playwright | Frontend e2e tests | `make e2e` (full), `make e2e-duckdb` (focused smoke) |
| Docker Compose | External-service test dependencies | `make postgres-up`, `make clickhouse-up`, `make ssh-up` |
| mdformat | Markdown formatting, wrap 80 | Via prek mdformat hook |
| check-timing-budgets | Rejects unallowed sub-second polling literals | `make check-timing-budgets` |

## Environments

| Environment | Branch | Purpose | URL |
|---|---|---|---|
| Local | Any | Primary runtime, CLI binary plus embedded server on loopback | http://127.0.0.1:8080 by default |
| CI ephemeral | PR or main | Namespace runners plus macOS self-hosted runners | N/A (disposable) |
| Docs staging | docs changes | Preview deployment | Vercel preview via `make docs-deploy-staging` |
| Docs production | main | Published documentation site | Vercel production via `make docs-deploy` |

## Ci/cd pipelines

| Workflow | Trigger | What it runs |
|---|---|---|
| ci.yml | workflow_call from ci-pr.yml on pull_request, push to main, workflow_dispatch | lint, frontend checks and tests, docs check, Go tests on Linux and Windows, macOS raw-capture tests, eval-ingest tag tests, Windows SQLite package tests, DuckDB Windows tests, race tests, desktop Windows unit tests, Postgres plus ClickHouse plus SSH integration tests, Playwright e2e on Chromium and WebKit |
| ci-pr.yml | pull_request | Dispatcher that pins and calls ci.yml at main |
| ci-macos-main.yml | push to main with Go source paths | Go tests for macOS FSEvents watcher on self-hosted Apple Silicon runners |
| cjk-fts.yml | pull_request and push to main touching db, service, mcp, or sidecar build paths | Go tests with the CJK simple/cppjieba FTS sidecar |
| fuzz.yml | Weekly schedule plus workflow_dispatch | Go fuzzing of Antigravity wire-walk parsing targets, failures uploaded as artifacts |
| desktop-artifacts.yml | workflow_call, workflow_dispatch, push to main touching desktop, frontend, or go files | Tauri Windows NSIS and Linux AppImage bundles on Namespace runners |
| desktop-artifacts-pr.yml | pull_request to main touching desktop or frontend paths | Dispatcher that pins and calls desktop-artifacts.yml at main |
| desktop-macos-main.yml | push to main touching desktop or frontend paths | Tauri macOS app bundles on self-hosted macOS runners |
| msys2-update-check.yml | Weekly schedule plus workflow_dispatch | Windows CI with MSYS2 updates enabled to catch MinGW toolchain drift |

## Deployment

- Docker images publish to ghcr.io/kenn-io/agentsview with a latest tag.
- The Dockerfile is a multi-stage build that compiles the frontend with Node 24, builds the Go binary with CGO and the fts5 tag, and ships a Debian slim runtime with AGENTSVIEW_DATA_DIR set to /data.
- macOS users install via Homebrew Cask with `brew install --cask agentsview`.
- Desktop bundles are built with Tauri into a macOS DMG, a Windows NSIS installer, and a Linux AppImage.
- Release binaries embed version, commit, and build date from git describe via ldflags.
- Note: no GoReleaser configuration was found in the surveyed repo files, so the canonical automated release path beyond Docker, Homebrew, and Tauri bundles is undocumented here.
- Docs deploy via Vercel from the docs/ directory for staging and production.

### Rollback

- Docker users roll back by re-pinning to an earlier image tag instead of latest.
- Homebrew and binary users roll back by reinstalling the previous version.
- Note: no automated rollback workflow was found in the surveyed repo files.

## Health checks

| Endpoint | Expected response | Checked by |
|---|---|---|
| GET /api/ping | 200 OK with `{ok: true, healthy: bool, service, version, pid, sync}` where healthy is false when the sync engine reports stalled | Local operator or CLI polling, no load balancer or k8s probe exists |
| GET /api/openapi.json | 200 OK with the Huma OpenAPI 3.1 document | Contract tests and orval client generation |

- No /health, /ready, /livez, or /metrics endpoint exists.
- The /api/v1/health path seen in internal/server/compress_test.go is only a gzip-middleware test fixture, not a registered route.

## Smoke tests

- Run the focused Playwright smoke suite with `make e2e-duckdb` from the repo root.
- That suite covers the DuckDB backend, data-mode switching, and session-list rendering on Chromium.
- Run the full browser suite with `make e2e` or `npx playwright test` in frontend/.
- The Docker build runs `agentsview --version` as a build-time smoke check.

## Hosting

- Hosting is local-first with no project-operated cloud environment.
- The CLI binary embeds the web UI and serves it from loopback (127.0.0.1) by default.
- The Tauri desktop wrapper ships the same local stack as a macOS, Windows, or Linux app.
- The published Docker image targets self-hosting on user infrastructure.
- PostgreSQL, DuckDB, and ClickHouse mirrors are user-operated opt-in read stores, not hosted services.

## Secrets management

- API authentication uses a bearer token stored as auth_token in the config file.
- The AGENTSVIEW_AUTH_TOKEN environment variable overrides the file value at load time.
- Config.EnsureAuthToken generates and persists a token on first run when none exists.
- Protected routes require an Authorization: Bearer header with a query-param fallback on the endpoints documented in internal/server/auth.go.
- Provider API keys are referenced by environment variable name (for example AGENTSVIEW_CURSOR_ADMIN_API_KEY), and the resolved secret is never returned by config inspection paths.
- Secret scanning persists only redacted matches in the secret_findings table.
- No cloud secret manager is used.

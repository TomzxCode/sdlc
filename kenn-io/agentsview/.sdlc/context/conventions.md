# Conventions

## Naming

- **Files:** Go files use snake_case (e.g. `session_list.go`, `serve_background_unix.go`). Svelte files use PascalCase (e.g. `SessionList.svelte`, `MessageContent.svelte`). Test files append `_test.go`.
- **Variables:** Go uses camelCase for local variables, PascalCase for exported identifiers.
- **Functions / Methods:** Go uses PascalCase for exported, camelCase for unexported.
- **Types, Structs, Interfaces:** PascalCase in Go.
- **Constants:** PascalCase in Go.
- **Packages:** Lowercase, single-word package names preferred (e.g. `sync`, `parser`, `db`).
- **Directories:** Lowercase with hyphens for CLI commands (e.g. `cmd/agentsview/`), single word for internal packages (e.g. `internal/sync/`).

## Directory Structure

```
cmd/agentsview/     CLI entrypoint and commands
cmd/benchgate/      Benchmark gateway
cmd/perfsim/        Performance simulation harness
cmd/testfixture/    Test data generator
internal/           Go packages
  config/           Configuration loading
  db/               SQLite database layer
  parser/           Per-agent session parsers
  server/           HTTP handlers and API routes
  service/          Session service interface
  servicehttp/      HTTP transport for the session service
  apiclient/        Generated HTTP API client
  sync/             Sync engine and file watcher
  poller/           Polling scheduler
  sessionwatch/     Session file watcher
  postgres/         PostgreSQL store and push sync
  duckdb/           DuckDB store and push sync
  clickhouse/       ClickHouse store and push sync
  vector/           Semantic search and embeddings
  activity/         Activity aggregation engine
  insight/          AI-generated insights
  recall/           Recall context ranking
  mcp/              MCP server
  mcpdiscovery/     MCP server discovery
  remotesync/       Remote sync (SSH, HTTP)
  ssh/              SSH transport and session extraction
  secrets/          Secret scanning
  signals/          Session health signals
  skills/           Skill definitions
  pricing/          Model pricing
  pricingrefresh/   Pricing data refresh
  cursorusage/      Cursor usage API client
  money/            Decimal money arithmetic and formatting
  export/           Session export
  artifact/         Artifact export and canonical JSON
  capture/          Session capture bundles
  importer/         Claude.ai/ChatGPT import
  rawcapture/       Raw event capturer
  rawcheckpoint/    Raw sync checkpoints and acknowledgements
  rawclient/        Raw sync client
  rawderive/        Raw event derivation jobs
  rawpath/          Raw archive path layout
  rawsync/          Raw sync manifests and device auth
  rawupload/        Raw event uploader
  rawwatch/         Raw archive watcher and auditor
  usagefacts/       Usage fact records
  timeutil/         Time parsing utilities
  jsonutil/         JSON helpers
  pathutil/         Filesystem path helpers
  stringutil/       String helpers including truncation
  fsevents/         macOS filesystem event watcher
  telemetry/        Anonymous telemetry
  update/           Self-update
  web/              Embedded web assets
  assets/           Embedded binary assets
  backendbench/     Opt-in cross-backend store benchmarks
  backendcontract/  Cross-backend conformance contract
  dbtest/           Shared database test helpers
  e2e/              Go end-to-end test harness
  parsertest/       Shared parser test helpers
  testjsonl/        JSONL test fixture helpers
frontend/           Svelte 5 SPA
  src/              Application source
  e2e/              Playwright E2E tests
  messages/         i18n message catalogs
desktop/            Tauri desktop wrapper
docs/               Documentation
scripts/            Utility scripts
```

## Coding Standards

- Prefer stdlib over external dependencies.
- Use testify for test assertions (require.X for fatal, assert.X for independent).
- Table-driven tests preferred for Go code.
- Frontend tests use vitest for unit tests and Playwright for E2E tests.
- All new features and bug fixes must include unit tests.
- Error handling: check and return errors; do not panic in production code.
- Use stdlib log/slog for structured logging.
- Minimize comments; code should be self-documenting.
- Do not use emojis in code or output.
- Run go fmt and go vet (with the fts5 build tag) after changing Go code.
- Lint with golangci-lint using the repo configs, including the NilAway module plugin.
- Use mdformat --wrap 80 for Markdown files when tooling is available.

## Commit Messages

- Use Conventional Commits format with a type, an optional scope, and a short description.
- Types observed in git history include fix, feat, chore, docs, test, and refactor.
- Scopes include session, search, parser, server, db, sync, frontend, and similar areas.
- Example: `fix(sessions): include overnight activity in date filters (#1058)`.

## Branching

- Feature branches named by contributor convention (no strict pattern observed).
- PRs merge into main via GitHub pull request workflow.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff and review.
- Use sentence case for headings, not title case.
- Prefer bullet lists over prose paragraphs.
- Use tables for structured comparisons.
- Keep files focused on a single topic.

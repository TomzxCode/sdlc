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
cmd/testfixture/    Test data generator
internal/           Go packages
  config/           Configuration loading
  db/               SQLite database layer
  parser/           Per-agent session parsers
  server/           HTTP handlers and API routes
  service/          Session service interface
  sync/             Sync engine and file watcher
  postgres/         PostgreSQL store and push sync
  duckdb/           DuckDB store and push sync
  vector/           Semantic search and embeddings
  activity/         Activity aggregation engine
  insight/          AI-generated insights
  mcp/              MCP server
  remotesync/       Remote sync (SSH, HTTP)
  secrets/          Secret scanning
  signals/          Session health signals
  skills/           Skill definitions
  pricing/          Model pricing
  export/           Session export
  importer/         Claude.ai/ChatGPT import
  timeutil/         Time parsing utilities
  telemetry/        Anonymous telemetry
  update/           Self-update
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
- All new features and bug fixes must include unit tests.
- Error handling: check and return errors; do not panic in production code.
- Use structlog patterns for structured logging.
- Minimize comments; code should be self-documenting.
- Do not use emojis in code or output.
- Use mdformat --wrap 80 for Markdown files when tooling is available.

## Commit Messages

Conventional Commits format:
```
<type>(<scope>): <description>

<body>
```

Types observed in git history: fix, feat, chore, docs, test, refactor.
Scopes include session, search, parser, server, db, sync, frontend, etc.
Examples: `fix(sessions): include overnight activity in date filters (#1058)`

## Branching

Feature branches named by contributor convention (no strict pattern observed).
PRs merge into main via GitHub pull request workflow.

## SDLC Documentation Style

- One sentence per line in markdown files for easier diff and review.
- Use sentence case for headings, not title case.
- Prefer bullet lists over prose paragraphs.
- Use tables for structured comparisons.
- Keep files focused on a single topic.

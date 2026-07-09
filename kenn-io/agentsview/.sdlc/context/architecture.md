# Architecture

## System Overview

```
+-------------------+      +---------------------+      +-------------------+
| Agent Session     | ---> | Sync Engine         | ---> | SQLite Database   |
| Files (disk)      |      | (discovery, parse,  |      | (primary archive) |
|                   |      |  sanitize, write)   |      | + FTS5 indexes    |
+-------------------+      +---------------------+      +--------+----------+
                                                               |
                                                               v
+-------------------+      +---------------------+      +-------------------+
| Svelte 5 SPA      | <--- | HTTP Server (Huma)  | <--- | Service Layer     |
| (embedded binary) |      | REST API + SSE      |      | (DirectBackend)   |
+-------------------+      +---------------------+      +--------+----------+
                                                               |
                                   +---------------------------+---------------------------+
                                   |                           |                           |
                                   v                           v                           v
                           +------------------+      +------------------+      +------------------+
                           | PostgreSQL Store |      | DuckDB Store     |      | Vector DB        |
                           | (read-only push) |      | (read-only push) |      | (semantic index) |
                           +------------------+      +------------------+      +------------------+
```

## Key Components

| Component | Responsibility | Technology |
|---|---|---|
| CLI (cmd/agentsview) | Entry point, cobra commands, daemon lifecycle | Go, cobra, pflag |
| Sync Engine (internal/sync) | Session file discovery, parsing, sanitization, DB writes | Go, fsnotify |
| Parsers (internal/parser) | Per-agent session file format parsers (50+ agents) | Go |
| SQLite DB (internal/db) | Primary archive: sessions, messages, FTS5, analytics, usage | SQLite, FTS5 |
| HTTP Server (internal/server) | REST API (Huma), SPA serving, SSE, auth, CORS | Go, Huma v2 |
| Service Layer (internal/service) | Session service interface with multiple backends | Go |
| Frontend (frontend/) | SPA with session browser, analytics, usage, search UI | Svelte 5, TypeScript, Vite+ |
| PostgreSQL (internal/postgres) | Push sync from SQLite, read-only serve | Go, pgx |
| DuckDB (internal/duckdb) | Push sync from SQLite, read-only serve, Quack protocol | Go, duckdb driver |
| Vector (internal/vector) | Semantic search index, embeddings encoder, RRF hybrid search | Go, sqlite-vec |
| Config (internal/config) | TOML-based config, env vars, CLI flags | Go, BurntSushi/toml |
| File Watcher | fsnotify-based directory watching with debouncing | Go, fsnotify |

## Data Flow

1. Agent sessions are written to disk by AI coding agents (Claude, Codex, Cursor, etc.)
2. The Sync Engine discovers new/changed session files via file watcher or periodic scan
3. Each file is dispatched to the appropriate parser based on agent type
4. Parsed sessions are sanitized and written to SQLite in batches
5. The HTTP server serves the REST API from the SQLite database
6. The Svelte SPA queries the API and renders session views
7. PostgreSQL/DuckDB mirrors are populated on-demand via push commands
8. The Vector DB is built on-demand for semantic search
9. SSE streams push live updates to connected clients

## Infrastructure

| Aspect | Detail |
|---|---|
| CI/CD | GitHub Actions (see .github/workflows/) |
| Build | Makefile-based; CGO_ENABLED=1 + fts5 build tag |
| Desktop | Tauri wrapper for macOS (DMG) and Windows |
| Container | Docker image published to ghcr.io |
| Package | Homebrew cask for desktop app |
| Telemetry | Anonymous PostHog ping (opt-out), disabled in test binaries |
| Release | GitHub Releases with GoReleaser or similar |
| Linting | golangci-lint with NilAway |

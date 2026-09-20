# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| agent | An AI coding tool that produces session files (Claude, Codex, Cursor, etc.) |
| artifact | A normalized, versioned session payload exchanged between machines via artifact folder sync |
| checkpoint | A durable progress marker recording how far a sync, parse, export, or upload job has advanced |
| compaction | An agent-side summarization of conversation context to reclaim window space, tracked as a session health signal |
| embedding | A vector representation of text used for semantic search |
| FTS5 | SQLite Full-Text Search version 5, used for message content search |
| generation | A versioned batch of derived data, either one embedding index built with a specific model and dimensions or one accepted batch of raw-synced source files |
| harness | The runtime that executes an agent and persists its session files, such as DeepSeek Harness |
| insight | An AI-generated summary or analysis of session data |
| message | An individual turn in a session (user prompt, assistant response, tool result) |
| parse diff | The difference between two parser runs, used to detect incremental changes |
| parser | Code that reads an agent-specific session file format and extracts structured data |
| poller | The interval-driven background scheduler that runs periodic jobs such as sync and maintenance |
| project | A named group of sessions, typically corresponding to a code repository |
| project identity | The git remote + worktree mapping used to disambiguate projects |
| pull quote | A notable excerpt extracted from session messages, used in reports |
| Quack | DuckDB extension and remote protocol for serving a DuckDB mirror over the network to trusted clients |
| raw capture | Local preservation of original provider session files into a durable upload outbox without parsing their content |
| raw sync | Upload of original session files to an operator-managed server for later hosted processing |
| recall entry | A distilled, reusable fact extracted from session history with evidence links |
| remote sync | Syncing sessions from other machines via SSH or HTTP |
| secret finding | Detected credentials or secrets in session content, stored with redacted matches |
| session | A single conversation or interaction with an AI coding agent, typically one run/launch |
| session watch | Live polling of one session's database state and source-file mtime, shared by the SSE handler and the session watch command |
| signal | A health or outcome indicator computed from session content (success/failure, tool health, context pressure) |
| sync | The process of discovering new/changed session files and updating the database |
| tool call | An invocation of a tool/function by the AI agent during a session |
| usage event | A record of token consumption during a session or portion of a session |
| worktree | A git working tree (main or linked checkout) used with mapping rules to attribute sessions to projects |

## Technical Terms

| Term | Definition |
|---|---|
| CGO | Go's mechanism for calling C code, required for the sqlite3 driver |
| ClickHouse | Columnar analytics database supported as a remote mirror and read store |
| cobra | CLI framework for Go |
| CockroachDB | PostgreSQL-compatible distributed database supported as a shared-database target |
| CWD | Current Working Directory, used for sync path filtering |
| DuckDB | Embedded analytics database used as a local single-file mirror of the SQLite archive |
| fsnotify | Go library for filesystem event notification |
| FTS5 | SQLite virtual table module for full-text indexing and search |
| golangci-lint | Go linter aggregator |
| Huma | OpenAPI 3.1 REST framework for Go |
| kit-ui | Shared UI component library (@kenn-io/kit-ui) used in the frontend |
| LiteLLM | Open-source LLM pricing catalog used for cost estimation |
| MCP | Model Context Protocol, a protocol for AI tools to expose capabilities |
| NilAway | Go nil pointer analysis tool |
| Paraglide | i18n framework used in the Svelte frontend for message catalogs |
| pgx | PostgreSQL driver for Go |
| PostgreSQL | Relational database used as a shared sync target and read store |
| RRF | Reciprocal Rank Fusion, a method for merging FTS5 and semantic search results |
| SQLite | Embedded relational database used as the primary session archive |
| sqlite-vec | SQLite extension for vector similarity search |
| SSE | Server-Sent Events, used for real-time UI updates |
| Svelte 5 | Frontend framework using runes for reactivity |
| Tauri | Desktop application framework wrapping web UIs |
| testify | Go testing library with assertions and mocking |
| TOML | Tom's Obvious Minimal Language, used for configuration files |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| ADR | Architecture Decision Record |
| API | Application Programming Interface |
| CGO | C Go interoperability |
| CI/CD | Continuous Integration / Continuous Deployment |
| CLI | Command Line Interface |
| CORS | Cross-Origin Resource Sharing |
| CSP | Content Security Policy |
| CRUD | Create, Read, Update, Delete |
| DDL | Data Definition Language |
| DMG | Apple Disk Image |
| DSN | Data Source Name |
| FTS | Full-Text Search |
| FTS5 | Full-Text Search version 5 |
| IDE | Integrated Development Environment |
| LOTR | LLM Organized Tree of Retrievals (from internal/insight) |
| MCP | Model Context Protocol |
| OTel | OpenTelemetry |
| PG | PostgreSQL |
| REST | Representational State Transfer |
| RRF | Reciprocal Rank Fusion |
| S3 | Simple Storage Service (Amazon S3-compatible) |
| SHM | Shared Memory |
| SPA | Single Page Application |
| SSE | Server-Sent Events |
| SSH | Secure Shell |
| TUI | Terminal User Interface |
| WAL | Write-Ahead Logging |

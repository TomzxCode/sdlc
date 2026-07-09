# Vocabulary

## Domain Terms

| Term | Definition |
|---|---|
| session | A single conversation or interaction with an AI coding agent, typically one run/launch |
| message | An individual turn in a session (user prompt, assistant response, tool result) |
| tool call | An invocation of a tool/function by the AI agent during a session |
| agent | An AI coding tool that produces session files (Claude, Codex, Cursor, etc.) |
| parser | Code that reads an agent-specific session file format and extracts structured data |
| project | A named group of sessions, typically corresponding to a code repository |
| sync | The process of discovering new/changed session files and updating the database |
| FTS5 | SQLite Full-Text Search version 5, used for message content search |
| embedding | A vector representation of text used for semantic search |
| generation | A version of the semantic search embedding index (a set of embeddings with a specific model and dimensions) |
| signal | A health or outcome indicator computed from session content (success/failure, tool health, context pressure) |
| insight | An AI-generated summary or analysis of session data |
| pull quote | A notable excerpt extracted from session messages, used in reports |
| remote sync | Syncing sessions from other machines via SSH or HTTP |
| Quack | DuckDB's remote protocol for network access to DuckDB files |

## Technical Terms

| Term | Definition |
|---|---|
| SQLite | Embedded relational database used as the primary session archive |
| FTS5 | SQLite virtual table module for full-text indexing and search |
| SSE | Server-Sent Events, used for real-time UI updates |
| Huma | OpenAPI 3.1 REST framework for Go |
| Svelte 5 | Frontend framework using runes for reactivity |
| pgx | PostgreSQL driver for Go |
| RRF | Reciprocal Rank Fusion, a method for merging FTS5 and semantic search results |
| fsnotify | Go library for filesystem event notification |
| cobra | CLI framework for Go |
| testify | Go testing library with assertions and mocking |
| sqlite-vec | SQLite extension for vector similarity search |
| MCP | Model Context Protocol, a protocol for AI tools to expose capabilities |
| Tauri | Desktop application framework wrapping web UIs |
| golangci-lint | Go linter aggregator |
| NilAway | Go nil pointer analysis tool |

## Acronyms and Abbreviations

| Abbreviation | Expansion |
|---|---|
| SSE | Server-Sent Events |
| FTS | Full-Text Search |
| FTS5 | Full-Text Search version 5 |
| RRF | Reciprocal Rank Fusion |
| MCP | Model Context Protocol |
| SPA | Single Page Application |
| CLI | Command Line Interface |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| CORS | Cross-Origin Resource Sharing |
| CSP | Content Security Policy |
| DSN | Data Source Name |
| DDL | Data Definition Language |
| CRUD | Create, Read, Update, Delete |
| S3 | Simple Storage Service (Amazon S3-compatible) |
| SSH | Secure Shell |
| SSE | Server-Sent Events |
| IDE | Integrated Development Environment |
| TUI | Terminal User Interface |
| DMG | Apple Disk Image |
| CI/CD | Continuous Integration / Continuous Deployment |
| WAL | Write-Ahead Logging |
| ADR | Architecture Decision Record |
| LOTR | LLM Organized Tree of Retrievals (from internal/insight) |

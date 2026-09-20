# Project overview

## Purpose

agentsview is a local-first viewer for AI agent sessions.
It syncs session data from disk into SQLite with FTS5 full-text search.
It serves a Svelte 5 SPA via an embedded Go HTTP server.
It provides real-time updates via SSE.
The goal is to let developers browse, search, and track costs across all their AI coding agents in one place.
Everything stays local with no accounts by default, and sharing features are opt-in.

## Key stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Individual developers | End users | Browse and search past AI sessions, track token usage and costs, analyze productivity |
| Engineering managers | Evaluators | Team-wide visibility via PostgreSQL sync, analytics dashboards |
| AI agent users | End users | Review session history, find past solutions, export conversations |
| Open source contributors | Contributors | Extend parser support for new agents, fix bugs, improve performance |
| thekenn (kenn-io) | Maintainer | Project direction, architecture decisions, release management |

## Scope

**In scope:**
- Session discovery, parsing, and indexing from 70+ AI coding agents (72 AgentType values in internal/parser/types.go)
- Full-text search (FTS5) across all message content
- Semantic search (opt-in) via OpenAI-compatible embeddings
- Token usage and cost tracking with automatic pricing
- Analytics dashboard with activity heatmaps, tool usage, velocity metrics
- PostgreSQL sync for team/shared access
- ClickHouse push and read-only serve as a remote mirror backend
- DuckDB mirror and Quack remote protocol
- REST API with OpenAPI 3.1 schema
- Svelte 5 SPA frontend embedded in the Go binary
- Live updates via SSE as active sessions receive new messages
- Recall corpus of distilled knowledge with transcript evidence, CLI, MCP query_recall, and corpus browser
- Export via insight HTML, GitHub Gist publishing, session JSON/NDJSON, and raw source JSONL streaming
- Secret scanning across session content
- AI-generated Activity Insights from session data
- MCP (Model Context Protocol) server for AI tool integration (stdio and StreamableHTTP, read-only)
- Remote sync from other machines via HTTP (preferred) and SSH (deprecated, critical fixes only)
- S3-compatible object storage for session discovery (opt-in s3:// roots, dedicated handling for Claude, Codex, and Cursor)

**Out of scope:**
- Cloud-hosted version or SaaS offering
- Multi-user access control (no user accounts; optional auth via bearer token)
- Replacing the AI coding agents themselves
- Editing or modifying sessions (read-only viewer with soft-delete)
- Real-time collaboration features

## Key constraints

- CGO_ENABLED=1 and the fts5 build tag are required for the SQLite driver and FTS5 support
- Must bind to localhost by default for security (DNS rebinding protection)
- Session data must remain local by default; PostgreSQL, ClickHouse, DuckDB push, S3 ingest, and Gist publishing are opt-in
- Must support offline operation with no external dependencies
- SQLite is the primary archive; PostgreSQL, ClickHouse, and DuckDB are secondary mirrors
- Desktop app targets macOS and Windows via an experimental Tauri wrapper
- Must parse diverse session file formats from 70+ agents with varying structures

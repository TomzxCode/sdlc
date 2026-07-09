# Project Overview

## Purpose

agentsview is a local web viewer for AI agent sessions. It syncs session data from disk into SQLite with FTS5 full-text search, serves a Svelte 5 SPA via an embedded Go HTTP server, and provides real-time updates via SSE. The goal is to let developers browse, search, and track costs across all their AI coding agents in one place, with no accounts and everything local.

## Key Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Individual developers | End users | Browse and search past AI sessions, track token usage and costs, analyze productivity |
| Engineering managers | Evaluators | Team-wide visibility via PostgreSQL sync, analytics dashboards |
| AI agent users | End users | Review session history, find past solutions, export conversations |
| Open source contributors | Contributors | Extend parser support for new agents, fix bugs, improve performance |
| thekenn (kenn-io) | Maintainer | Project direction, architecture decisions, release management |

## Scope

**In scope:**
- Session discovery, parsing, and indexing from 50+ AI coding agents
- Full-text search (FTS5) across all message content
- Semantic search (opt-in) via OpenAI-compatible embeddings
- Token usage and cost tracking with automatic pricing
- Analytics dashboard with activity heatmaps, tool usage, velocity metrics
- PostgreSQL sync for team/ shared access
- DuckDB mirror and Quack remote protocol
- REST API with OpenAPI 3.1 schema
- Svelte 5 SPA frontend embedded in the Go binary
- Live updates via SSE as active sessions receive new messages
- Session export (HTML, GitHub Gist)
- Secret scanning across session content
- AI-generated insights from session data
- MCP (Model Context Protocol) server for AI tool integration
- Remote sync from other machines via SSH
- S3-compatible object storage for session discovery

**Out of scope:**
- Cloud-hosted version or SaaS offering
- Multi-user access control (no user accounts; optional auth via bearer token)
- Replacing the AI coding agents themselves
- Editing or modifying sessions (read-only viewer with soft-delete)
- Real-time collaboration features

## Key Constraints

- CGO_ENABLED=1 required for sqlite3 driver and FTS5 support
- Must bind to localhost by default for security (DNS rebinding protection)
- Session data must remain local by default; PostgreSQL sync is opt-in
- Must support offline operation with no external dependencies
- SQLite is the primary archive; DuckDB and PostgreSQL are secondary mirrors
- Desktop app targets macOS and Windows via Tauri
- Must parse diverse session file formats from 50+ agents with varying structures

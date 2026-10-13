# Use Cases

## Supported

| ID | Use case | Actor | Description |
|---|---|---|---|
| UC-1 | Sync and browse agent sessions | Developer | The developer syncs on-disk session directories from 70+ supported agents into a local SQLite archive and browses them via the CLI and web UI. |
| UC-2 | Full-text search across sessions | Developer | The developer searches all message content with FTS5, narrowing results by project, date, and CJK-aware phrase matching. |
| UC-3 | Semantic and hybrid search | Developer | The developer searches past sessions by meaning through an opt-in OpenAI-compatible embeddings index, optionally combined with full-text ranking. |
| UC-4 | Track token usage and costs | Developer | The developer reviews daily, per-model, and per-session token consumption and cost estimates computed from automatic pricing data. |
| UC-5 | Review analytics dashboards | Engineering manager | The engineering manager inspects activity heatmaps, tool usage, velocity metrics, and project breakdowns in the web UI and stats CLI. |
| UC-6 | Share sessions via PostgreSQL | Engineering manager | The engineering manager pushes the local archive to a shared PostgreSQL instance and serves read-only team dashboards from it. |
| UC-7 | Mirror the archive to DuckDB | Operator | The operator mirrors SQLite into a portable DuckDB file and serves it read-only locally or remotely over the Quack protocol. |
| UC-8 | Mirror the archive to ClickHouse | Operator | The operator pushes session data to ClickHouse and serves the web UI read-only from that remote backend. |
| UC-9 | Browse the web frontend with live updates | Developer | The developer navigates the Svelte SPA with keyboard-first controls and watches active sessions update live over SSE. |
| UC-10 | Query sessions via the REST API | Developer | The developer reads sessions, search results, usage, and analytics programmatically through the OpenAPI 3.1 REST endpoints. |
| UC-11 | Retrieve session context from an AI agent | AI agent via MCP | The agent queries past sessions, recall entries, and conversation memory through the read-only MCP server over stdio or StreamableHTTP. |
| UC-12 | Build and consult the recall corpus | Developer | The developer extracts, approves, and queries distilled knowledge entries that link back to their supporting transcript evidence. |
| UC-13 | Export and publish sessions | Developer | The developer exports sessions as HTML, JSON, or NDJSON, streams raw source JSONL, and publishes selected sessions to GitHub Gist. |
| UC-14 | Scan sessions for leaked secrets | Operator | The operator runs secret scans over session content and reviews the redacted findings list. |
| UC-15 | Generate Activity Insights | Developer | The developer generates and reviews AI-produced insight summaries derived from recorded session data. |
| UC-16 | Use the desktop app | Developer | The developer runs the macOS or Windows Tauri desktop wrapper, which shares the same local daemon, archive, and web UI. |
| UC-17 | Ingest sessions from other machines | Operator | The operator pulls session data from remote machines via HTTP remote sync, filesystem session sources, or opt-in S3 roots. |
| UC-18 | Capture one-shot CI agent runs | Developer | The developer records a single non-interactive agent execution in CI with its streams, exit outcome, and versioned usage result. |
| UC-19 | Operate the server and archive | Operator | The operator manages the daemon lifecycle, runs doctor diagnostics, and maintains the archive with compact, migrate, prune, and machine-adoption commands. |

## Wanted

| ID | Use case | Actor | Description | Signal |
|---|---|---|---|---|
| — | No wanted use cases identified | — | No not-yet-built use case with roadmap, issue, or TODO evidence was found during this pass. | None |

## Out of scope

- Cloud-hosted version or SaaS offering.
- Multi-user access control beyond the optional bearer token.
- Replacing the AI coding agents themselves.
- Editing or modifying sessions (the viewer is read-only apart from soft-delete).
- Real-time collaboration features.

---
title: "Session Sync & Management"
status: draft
---

# Specification: Session Sync & Management

## Overview

The sync engine (`internal/sync/Engine`) orchestrates session discovery, parsing, and database writing. Discovery uses provider factories or legacy path resolution. Parsing delegates to per-agent parsers in `internal/parser/`. Writing batches sessions and messages into SQLite with incremental update support.

## Architecture

```
Agent Files (disk) → Provider Factory / Legacy Resolver
                         ↓
                   Agent-specific Parser
                         ↓
                   Sanitizer
                         ↓
                   Batch Writer → SQLite DB
                         ↓
                   SSE Emitter → UI Clients
```

## Data Models

### ParsedSession

| Field | Type | Description |
|---|---|---|
| ID | string | Unique session identifier |
| AgentID | AgentType | Agent that created the session |
| Project | string | Project name |
| StartTime | time.Time | Session start timestamp |
| Messages | []ParsedMessage | Messages in the session |
| ToolCalls | []ParsedToolCall | Tool invocations |
| UsageEvents | []ParsedUsageEvent | Token usage data |

### SkipCacheEntry

| Field | Type | Description |
|---|---|---|
| Path | string | File path |
| ModTime | time.Time | Last modification time |
| Error | string | Parse error description |

## API Contracts

### POST /api/v1/sync
**Request:** Empty
**Response:** SSE stream of sync progress events

### POST /api/v1/resync
**Request:** Empty
**Response:** SSE stream of full resync progress events

### GET /api/v1/sync/status
**Response:** JSON with sync state, last sync time, pending count

## Sequences

### File Change Detection
```
fsnotify → Debounce (500ms) → Parse Changed Files → Batch Write → SSE Notify
```

### Periodic Scan
```
Timer (15min) → Discover All Paths → Diff Against Known → Parse New/Changed → Write
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Batch size | 100 sessions, 8 workers | Balances throughput and memory |
| Debounce | 500ms | Prevents thundering herd on bulk file changes |
| Skip cache | File path + mtime | Avoids re-parsing unchanged files |
| Provider factory | Per-agent pluggable discovery | Supports diverse agent directory structures |

## Risks and Unknowns

1. S3-backed discovery latency with many objects
2. File watcher scalability on directories with thousands of files

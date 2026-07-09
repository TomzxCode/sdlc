---
title: "Admin & Operations"
status: draft
---

# Specification: Admin & Operations

## Overview

Admin features are implemented across several internal packages: `internal/secrets/` for secret scanning, `internal/export/` for session export, `internal/importer/` for importing from other tools, `internal/insight/` for AI-generated insights, `internal/update/` for self-updates, `internal/signals/` for health signals, and `internal/remotesync/` for remote sync.

## Architecture

```
Session Content
  ├→ Secret Scanner (rule-based patterns)
  ├→ Exporter (HTML, Gist)
  ├→ Insight Generator (AI agent)
  └→ Health Signal Computer (heuristic rules)
```

## Data Models

### Secret Finding

| Field | Type | Description |
|---|---|---|
| id | TEXT | Finding identifier |
| session_id | TEXT | Source session |
| type | TEXT | Secret type (api_key, token, password) |
| match | TEXT | Redacted matched content |
| line | INTEGER | Line number |
| severity | TEXT | Severity level |

### Insight

| Field | Type | Description |
|---|---|---|
| id | TEXT | Insight identifier |
| type | TEXT | daily, agent_analysis, canned |
| title | TEXT | Insight title |
| content | TEXT | Generated insight body |
| model | TEXT | Model used for generation |
| created_at | TEXT | Generation timestamp |

## API Contracts

### GET /api/v1/secrets
**Response:** List of secret findings with session context

### POST /api/v1/secrets/scan
**Response:** SSE stream of scan progress

### POST /api/v1/insights/generate
**Response:** SSE stream of generation progress

### GET /api/v1/sessions/{id}/export
**Response:** HTML export of the session

## Sequences

### Secret Scanning
```
1. Walk all session messages
2. Apply regex patterns for each secret type
3. Redact matched content
4. Store findings in secrets table
5. Notify UI via SSE
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Insight generation | Uses configured agent | Leverages existing LLM infrastructure |
| Secret detection | Rule-based regex | Fast, no ML dependency |
| Export format | HTML with embedded styling | Self-contained, portable |
| Remote sync | SSH transport | Ubiquitous, no additional infrastructure |

## Risks and Unknowns

1. Insight generation cost and latency
2. False positives in secret scanning

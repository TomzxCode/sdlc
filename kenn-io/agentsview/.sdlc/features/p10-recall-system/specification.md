---
title: "Recall System"
status: done
---

# Specification: Recall System

## Overview

The recall system is implemented across `internal/recall/` and `internal/db/recall*.go`. It extracts facts from session messages, stores them in SQLite with evidence links to source messages, ranks them by query relevance using embedding similarity and keyword matching, and assembles formatted context blocks.

## Architecture

```
Session Messages
  → Extraction (distill facts into recall_entries)
  → Storage (SQLite: recall_entries, recall_evidence)
  → Ranking (query → ranked results)
  → Context Assembly (formatted prompt block)
```

## Data Models

### recall_entries

| Field | Type | Description |
|---|---|---|
| id | TEXT | Entry identifier |
| session_id | TEXT | Source session |
| content | TEXT | Distilled fact content |
| type | TEXT | Entry type (decision, convention, pattern, etc.) |
| created_at | TEXT | Creation timestamp |

### recall_evidence

| Field | Type | Description |
|---|---|---|
| entry_id | TEXT | Recall entry reference |
| message_id | TEXT | Source message reference |
| relevance | REAL | Evidence relevance score |

## API Contracts

### GET /api/v1/recall/search

**Parameters:**
- `q` - query string
- `limit` - max results

**Response:** Ranked list of recall entries with evidence

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | SQLite tables | Co-located with session data |
| Ranking | Embedding + keyword hybrid | Balances semantic and exact matching |

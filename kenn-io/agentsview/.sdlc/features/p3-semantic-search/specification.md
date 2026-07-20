---
title: "Semantic Search"
status: done
---

# Specification: Semantic Search

## Overview

Semantic search uses a separate SQLite database (`vectors.db`) with the sqlite-vec extension. A message mirror table tracks content changes for incremental updates. The encoder client sends content to an OpenAI-compatible embeddings API with configurable endpoint, model, dimensions, batch size, and concurrency.

## Architecture

```
Main SQLite DB → Message Mirror (hash-based refresh)
                     ↓
              Embeddings Encoder (HTTP client)
                     ↓
              vectors.db (sqlite-vec)
                     ↓
          Query → Encode → Similarity Search
                     ↓
              FTS5 + Semantic → RRF Merge (hybrid mode)
```

## Data Models

### vector_messages

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| message_id | TEXT | Source message ID |
| content_hash | TEXT | Hash of message content |
| session_id | TEXT | Parent session |
| ordinal | INTEGER | Message position in session |
| refreshed_at | TEXT | Last refresh timestamp |

### embedding_generations

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| model | TEXT | Embedding model name |
| dimensions | INTEGER | Vector dimensions |
| status | TEXT | building, active, retired |
| started_at | TEXT | Build start time |
| completed_at | TEXT | Build completion time |

## API Contracts

### POST /api/v1/embeddings/build
**Response:** SSE stream of build progress

### GET /api/v1/embeddings/generations
**Response:** List of generations with status

### POST /api/v1/embeddings/generations/{id}/activate
**Response:** Generation status

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Vector DB | Separate SQLite + sqlite-vec | Avoids coupling with main session DB |
| RRF merge | k=60 constant | Standard RRF parameter for hybrid search |
| Build strategy | Full scan then incremental | Balances completeness with efficiency |

## Risks and Unknowns

1. Embedding API cost for large datasets
2. sqlite-vec SQLite extension availability on all platforms

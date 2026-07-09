---
title: "Full-Text Search"
status: draft
---

# Specification: Full-Text Search

## Overview

Search uses SQLite FTS5 virtual tables created during DB migration. The indexed content covers message body text with configurable tokenization. Queries support AND, exact phrase, and prefix modes. Results include per-hit snippets built from the FTS5 snippet() function.

## Data Models

### FTS5 Virtual Table

| Column | Type | Description |
|---|---|---|
| content | TEXT | Message body text |
| session_id | TEXT | Parent session |
| agent | TEXT | Agent type |
| project | TEXT | Project name |

## API Contracts

### GET /api/v1/search

**Query Parameters**

| Field | Type | Required | Description |
|---|---|---|---|
| q | string | Yes | Search query |
| agent | string | No | Filter by agent |
| project | string | No | Filter by project |
| since | string | No | Start date (RFC3339) |
| until | string | No | End date (RFC3339) |
| limit | int | No | Results per page |
| cursor | string | No | Pagination cursor |

**Response**

| Field | Type | Description |
|---|---|---|
| results | []SearchResult | Ranked hits with snippets |
| next_cursor | string | Cursor for next page |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Tokenizer | unicode61 | Good Unicode support for multi-language content |
| Query mode | AND by default | Most intuitive for user search; exact phrase with quotes |

## Risks and Unknowns

1. FTS5 index rebuild on version migration

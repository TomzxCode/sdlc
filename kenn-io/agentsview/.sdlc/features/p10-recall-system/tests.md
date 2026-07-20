---
title: "Recall System"
status: done
---

# Test Plan: Recall System

## Scope

Tests cover the ranking algorithm, type definitions, and extraction logic. Integration tests verify SQLite persistence and query functionality.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Rank entries by query relevance | Recall entries + query | Ordered by score descending |
| TC-2 | Type definitions validate correctly | Valid/invalid entry types | Correct validation behavior |

## Test Files

- `internal/recall/rank_test.go` - Ranking algorithm tests
- `internal/recall/rank_internal_test.go` - Internal ranking helper tests
- `internal/recall/types_test.go` - Type definition tests

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-2 | TC-1 |
| FR-4 | TC-1 |

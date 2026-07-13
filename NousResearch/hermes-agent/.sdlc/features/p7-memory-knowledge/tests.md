---
title: "Memory and Cross-Session Knowledge"
status: done
---

# Test Plan: Memory and Cross-Session Knowledge

## Scope

Tests covering session store (SQLite FTS5), memory provider integration, learning graph, session search, title generation, and cross-session recall.

## Test Files

- tests/hermes_state/ — Session store tests
- tests/tools/test_memory_tool.py — Memory tool operations
- tests/tools/test_memory_tool_schema.py — Memory tool schema
- tests/tools/test_session_search.py — Session search
- tests/hermes_cli/test_memory_*.py — Memory provider setup and config
- tests/hermes_cli/test_session_*.py — Session browsing, export, filters
- tests/hermes_cli/test_journey_render.py — Learning graph journey render
- tests/plugins/memory/ — Memory provider-specific tests (honcho, retaindb, hindsight)
- tests/agent/test_memory_provider_init.py — Memory provider initialization
- tests/agent/test_memory_sync_interrupted.py — Memory sync interruption

## Unit Tests

- Session CRUD (create, read, update, delete, list)
- FTS5 full-text search query parsing and execution
- MemoryProvider ABC method signatures
- Learning graph extraction logic
- Title generation prompt construction

## Integration Tests

- Memory sync_turn() after each agent turn
- Prefetch() query during session start
- Cross-session search and recall
- Memory provider initialization from config
- Session export in HTML and Markdown formats

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Memory provider network call fails | Error logged, agent continues without memory |
| FTS5 search with special characters | Properly escaped query |
| Empty session (no messages) | Graceful handling, no sync |
| Learning graph extracts no procedures | No skill created, no error |
| Session title generation fails | Placeholder title used |
| Memory provider init fails | Fall back to no-memory mode |

## Test Infrastructure

- In-memory SQLite for fast session store tests
- Mock memory providers for ABC conformance
- Temp HERMES_HOME with controlled session data

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (SQLite FTS5 session store) | test_hermes_state.py, test_async_session_store.py |
| FR-2 (pluggable memory providers) | test_memory_providers.py |
| FR-3 (sync_turn) | test_memory_tool.py |
| FR-4 (prefetch) | test_memory_provider_init.py |
| FR-7 (session search) | test_session_search.py, test_web_server_session_search.py |
| FR-8 (title generation) | Tested via session auto-title |

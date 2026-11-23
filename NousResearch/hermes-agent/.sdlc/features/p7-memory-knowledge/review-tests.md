---
artifact: tests.md
verdict: changes-requested
reviewed_at: 2026-11-23
---

# Review: tests.md

## Sync drift: 2026-11-16

Discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run.

- **Test Files list names provider-specific tests that do not exist.** The entry for `tests/plugins/memory/` claims "Memory provider-specific tests (honcho, retaindb, hindsight)". No honcho or hindsight test file exists in `tests/plugins/memory/` or anywhere under `tests/`. The directory holds `test_byterover_provider.py`, `test_retaindb_provider.py`, and general discovery/multiplex/config tests. Honcho and Hindsight moved to the plugin catalog, so their provider-specific tests are not part of this tree.

Resync the Test Files list to the tests that exist.

## Sync drift: 2026-11-23

New discrepancies found between this artifact and the current codebase during a full `/sync-sdlc` run, beyond the 2026-11-16 drift recorded above.

- **Test Files lists `tests/hermes_state/`, which does not exist.** No such directory is present. Session store tests now live under `tests/persistence_sqlite/` (including `conversation/` and `core/`), with related coverage in `tests/agent/`, `tests/gateway/` and `tests/tools/`.

- **Coverage Matrix names three test files that do not exist.** FR-1 lists `test_hermes_state.py` and `test_async_session_store.py`, and FR-2 lists `test_memory_providers.py`. None of these files exists anywhere under `tests/`. Provider coverage lives in `tests/agent/test_memory_provider.py` and `tests/plugins/memory/`; FTS5 session-search coverage lives in `tests/persistence_sqlite/` and `tests/tools/test_session_search.py`.

Resync the Test Files entry and the FR-1 / FR-2 rows of the Coverage Matrix.

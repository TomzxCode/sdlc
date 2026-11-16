---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Tests (ACP Protocol (IDE Integration))

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Most paths in "Test Files" do not exist.** `tests/hermes_cli/test_copilot_*.py` (no matching files), `tests/acp/` (no such directory), `tests/agent/test_copilot_acp_client.py` and `tests/agent/test_copilot_acp_deprecation.py` are all absent. The only existing Copilot/ACP-named file outside the adapter suite is `tests/agent/test_copilot_acp_alias_compat.py`. The real suite lives in `tests/acp_adapter/` (over 90 test modules, e.g. `test_server.py`, `test_session.py`, `test_auth.py`, `test_tools.py`, `test_gateway_editor_wire.py`), which is the one listed path that is correct.
2. **Every row of the Coverage Matrix points at a non-existent test file.** FR-1 maps to `test_copilot_acp_client.py`, FR-2 to `test_copilot_context.py` and FR-3 to `test_release_acp_registry.py`; none of these files exist. Coverage for FR-1/FR-2/FR-3 should be remapped to actual `tests/acp_adapter/` modules (for example `test_server.py`, `test_session.py`/`test_gateway_editor_cwd.py` and `test_catalog_read_only.py`) or removed where no coverage exists.

Resync `tests.md` to list the real ACP test files and remap the coverage matrix, then re-review.

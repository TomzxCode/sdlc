---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Tests (sync drift)

## Sync drift: 2026-11-16

- The Test Files list and the Coverage Matrix cite `tests/hermes_cli/test_memory_providers.py`. No file with that name exists anywhere in the repository. Memory-provider tests live under `tests/plugins/memory/` (for example `test_discovery_sources.py`).
- The Edge Cases table records "Circular plugin dependency | Unresolved (no dependency manager yet)". Code detects cycles with `graphlib.TopologicalSorter` in `resolve_plugin_load_order()` and falls back to alphabetical order with a warning (hermes_cli/plugins_manifest.py:238-278), and `requires_plugins` dependency ordering is implemented.

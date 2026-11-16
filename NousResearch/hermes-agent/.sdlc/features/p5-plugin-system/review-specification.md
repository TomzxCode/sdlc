---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Specification (sync drift)

## Sync drift: 2026-11-16

- Discovery source list (Architecture) names the pip entry-point group `hermes_plugins`. Code reads `ENTRY_POINTS_GROUP = "hermes_agent.plugins"` (hermes_cli/plugins_discovery.py:29, also the hermes_cli/plugins.py module docstring). No group named `hermes_plugins` is read.
- Discovery source list names the in-tree directory `Plugins/<name>/`. Code scans the bundled directory `<repo>/plugins/<name>/` via `get_bundled_plugins_dir()` (hermes_cli/plugins.py:71). A `Plugins/` directory does not exist.
- Risks item 2 states there are no versioning or compatibility checks for plugins. Code defines `SUPPORTED_MANIFEST_VERSION = 2` plus `manifest_version` and `api_version` manifest fields (hermes_cli/plugins_manifest.py:36,42), and the native compatibility contract is documented in plugins/AGENTS.md.
- Risks item 3 states there is no plugin sandboxing outside of hook try/except wrapping. Code supports `plugins.isolation: host`, which runs non-bundled plugins in a separate per-profile host process (hermes_cli/plugin_isolation.py, hermes_cli/plugin_host.py).
- Out of Scope lists a plugin marketplace/server. Code ships `plugin-catalog/` as the only out-of-tree discovery system, backed by hermes_cli/plugin_catalog.py and hermes_cli/plugins_cmd_catalog.py.
- Out of Scope lists plugin version resolution and dependency management. Code implements dependency-ordered loading from `requires_plugins` via `resolve_plugin_load_order()` (hermes_cli/plugins_manifest.py:238).

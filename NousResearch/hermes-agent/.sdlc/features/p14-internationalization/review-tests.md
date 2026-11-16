---
artifact: tests.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: tests.md

## Sync drift: 2026-11-16

- "No dedicated internationalization test module identified" and "Tests for locale loading are integrated into CLI and config test suites" (tests.md:14-15) are false. Dedicated modules exist: `tests/agent/test_i18n.py`, `test_i18n_languages.py`, `test_i18n_layers.py`, `test_i18n_tui_packs.py`, plus `tests/hermes_cli/test_config_display_language.py`, `test_cli_info_i18n.py`, `test_cli_billing_i18n.py`, `test_cli_model_switch_i18n.py`, `tests/gateway/test_platform_adapter_i18n.py` and `tests/tui_gateway/test_i18n_methods.py`.
- The Coverage Matrix (tests.md:17-21) lists only FR-1 -> CLI integration tests. The code's test suite also covers language resolution and aliases, layered catalogs (packs/overlay/bundled), surface catalogs, TUI packs, `display.language` validation and CLI/gateway/TUI translation rendering, so the matrix understates tested scope.

---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-08-03
---

# Review: Tests (Terminal and Browser Automation)

## Sync drift: 2026-08-03

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Scope says "across six backends".** The codebase now ships seven terminal backends including Vercel Sandbox (`tools/environments/vercel_sandbox.py`). The scope and coverage matrix should acknowledge the seven-backend set (and Vercel Sandbox test coverage if present).

Resync `tests.md` to reflect the seven-backend set, then re-review.

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase. New items:

1. **Coverage Matrix FR-6 points at a test file that no longer exists.** The matrix maps FR-6 (browser dialogs) to `test_browser_camofox*.py`. No such file exists under `tests/tools/`; Camofox moved out of core into the `camofox` catalog plugin (`plugin-catalog/camofox.yaml`, config migration 52). The dialog end-to-end test now lives in `tests/tools/test_browser_supervisor.py::test_browser_dialog_tool_end_to_end`, against `tools/browser_dialog_tool.py`. Update the FR-6 row.

Resync `tests.md`, then re-review.

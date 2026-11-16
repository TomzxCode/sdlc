---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: Tests (Skill System)

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Coverage Matrix maps NFR-1 to "Skill injection via user message, not system prompt".** The code injects a compact skills index into the system prompt through `agent/prompt_builder.py::build_skills_system_prompt()` (called from `agent/system_prompt.py::_skills_prompt()`), built once at startup so the prefix stays byte-stable. The test plan's stated mechanism contradicts the code, and its Integration Tests list only "Skill injection into agent context" without covering the system-prompt index path. Tests for that path already exist in the codebase (`tests/agent/test_skills_index_format.py`, `tests/agent/test_prompt_builder.py`, `tests/agent/test_skill_commands.py`) but are not referenced by the plan.

Resync `tests.md` to describe the two-part injection and list the system-prompt index tests, then re-review.

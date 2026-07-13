---
title: "Skill System"
status: done
---

# Test Plan: Skill System

## Scope

Tests covering skill loading, SKILL.md parsing, skill tools (list, view, create, edit, delete), curator lifecycle, skills hub, and skill usage tracking.

## Test Files

- tests/tools/test_skill_*.py — Skill tool operations (7+ test files)
- tests/tools/test_skills_tool.py — Core skill management tool
- tests/tools/test_skills_hub.py — Skills hub download/install
- tests/tools/test_skill_manager_tool.py — Skill manager tool
- tests/tools/test_skill_usage.py — Skill usage tracking
- tests/tools/test_skill_bundle_provenance.py — Skill provenance
- tests/hermes_cli/test_skills_*.py — Skill CLI commands
- tests/hermes_cli/test_curator_*.py — Curator lifecycle tests
- tests/hermes_cli/test_skills_hub.py — Hub CLI integration
- tests/tools/test_skills_ast_audit.py — Skill AST audit
- tests/skills/ — Skill-specific functional tests

## Unit Tests

- SKILL.md frontmatter parsing
- Skill loading from filesystem paths
- Skill tool CRUD operations
- Curator state transitions (active → stale → archived)
- Skill usage tracking (increment, persist)

## Integration Tests

- Full skill lifecycle: create → use → archive → restore
- Skills hub install from remote source
- Skill injection into agent context
- Curator run with LLM review pass
- Skill discovery and listing across directories

## Edge Cases and Failure Scenarios

| Scenario | Expected Behavior |
|---|---|
| Skill with invalid frontmatter | Skipped with warning |
| Skill exceeds description length limit | Truncation or rejection |
| Curator tries to archive pinned skill | Skipped (pinned exempt) |
| Skills hub URL unreachable | Graceful failure with cached fallback |
| Duplicate skill name across directories | Last-loaded wins with dedup |

## Test Infrastructure

- Temp skill directories with controlled SKILL.md content
- Mock curator LLM review for deterministic testing
- Isolated HERMES_HOME per test

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (built-in skill loading) | test_skills_tool.py, test_skills_config.py |
| FR-2 (optional skill install) | test_skills_hub.py |
| FR-3 (agent skill creation) | test_skill_manager_tool.py |
| FR-4 (curator lifecycle) | test_curator_run.py, test_curator_archive_prune.py |
| FR-5 (skill tools) | test_skills_tool.py, test_skill_* |
| NFR-1 (system prompt size) | Skill injection via user message, not system prompt |

---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-08-03
---

# Review: Specification (Skill System)

## Sync drift: 2026-08-03

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Architecture says "~18 categories" for `skills/` and "~20 categories" for `optional-skills/`.** The codebase now ships **14** built-in categories and **21** optional categories.

Resync `specification.md` to reflect the current category counts, then re-review.

## Sync drift: 2026-11-16

Drift detected during `/sync-sdlc` reconciliation against the current codebase:

1. **Injection mechanism contradicts the code.** The Architecture section ("NOT system prompt (preserves prompt caching)"), the Technical Decisions table ("Injection method: User message, not system prompt" and "Skill loading: adds a user message with skill instructions, not a system prompt modification"), and Risks item 3 ("skills are subject to the model's context window, not the system prompt cache") all claim skills are never injected into the system prompt. The code injects a compact skills index into the system prompt: `agent/prompt_builder.py::build_skills_system_prompt()` (docstring: "Compact skill index for the system prompt") is called by `agent/system_prompt.py::_skills_prompt()`. The specification is internally inconsistent on this point: its API Contracts section describes "the system prompt injection mechanism", which matches the code. Skill slash-command *content* is still delivered as a user message, but the index is a stable, startup-built part of the system prompt.

Resync `specification.md` to describe the actual two-part injection (stable system-prompt index plus per-invocation user message), then re-review.

---
issue: ""
title: "Response Style Presets"
status: draft
---

# Existing Solutions: Response Style Presets

## Overview

The codebase already has a complete response style preset implementation. `packages/ui/src/lib/responseStyle.ts` defines 7 presets (concise, detailed, mentor, pushback, noFiller, matchEnergy, warmPeer) with full instruction text, `buildResponseStyleInstruction()` for compiling the active preset into a prompt context string, and `fetchResponseStyleInstruction()` for fetching the current setting from the server. The settings UI in `BehaviorPage.tsx` provides a selector with preview, enable/disable toggle, and custom instructions override. Presets are injected as prompt context (FR-06) and stored as local settings only (FR-07). The remaining gap is per-session preset selection: currently the setting is global via the Settings API, and FR-02 requires selection per session.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/lib/responseStyle.ts`, `packages/ui/src/components/sections/behavior/BehaviorPage.tsx`, `packages/ui/src/lib/i18n/messages/en.settings.ts`, `packages/ui/src/sync/input-store.ts`, OpenCode SDK `promptAsync` parameters |
| Open-source | Yes | Claude Code output styles spec, TavernKit preset system, Mandu prompt presets, PromptLoom multi-zone prompt compiler, RoleCall presets |
| Commercial / SaaS | Yes | Claude Code (Anthropic), OpenAI system prompt patterns |
| Standards / protocols | No | N/A |
| Reference material | Yes | Claude Code docs on output styles, system prompt customization |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing OpenChamber response style system | Internal | MIT | Mature | FR-01, FR-03, FR-04, FR-05, FR-06, FR-07 | FR-02: no per-session selection |
| Claude Code output styles | Reference pattern | Proprietary | Mature | Markdown-based style files with frontmatter, file-system storage in `~/.claude/output-styles/` | Server-side, requires Claude Code CLI, not applicable to OpenChamber |
| TavernKit preset system | Library | MIT | Mature | Complete prompt pipeline: main prompt, post-history instructions, per-chat overrides | Ruby library, roleplay-focused, not directly applicable |
| Mandu prompt presets | Reference pattern | MIT | Mature | Markdown files under `docs/prompts/`, named reference via `--preset`, versioned in git | CLI-focused, no per-session UI |
| RoleCall preset system | Reference pattern | Proprietary | Mature | Per-chat overrides without editing the preset, loadout states | Proprietary, gambling-focused infrastructure |

## Evaluation

### Existing OpenChamber Response Style System

- **Strengths:** Already implements FR-01 through FR-07 in production. 7 well-crafted presets with distinct instructions. `buildResponseStyleInstruction()` correctly compiles the preset into a prompt context string (FR-06: "inject as prompt context, not system prompts"). `fetchResponseStyleInstruction()` retrieves from `/api/config/settings` endpoint. Settings persisted as local settings only (FR-07). UI in `BehaviorPage.tsx` with Select, preview textarea, enable/disable toggle, and custom instructions override. i18n strings for all presets in all 8 supported languages.
- **Weaknesses:** The preset is global (stored in server settings). FR-02 requires per-session selection. The preset is injected on every request, but there is no per-session override mechanism in the session creation payload.
- **Integration effort:** Low for per-session support. Add a `responseStylePreset` field to the session creation payload sent to OpenCode SDK's `promptAsync()` or similar.
- **Cost:** None.
- **Risks:** None.

### Claude Code Output Styles

- **Strengths:** Reference pattern for how a production AI coding tool handles response style customization. Output styles are markdown files with frontmatter, stored in `~/.claude/output-styles/` or `.claude/output-styles/` per project. `keep-coding-instructions: true` allows layering on top of the base preset. CLI-based management (`/config`).
- **Weaknesses:** Server-side only, not applicable as a library for OpenChamber. The file-based approach is useful as inspiration for custom preset creation (FR-04).
- **Integration effort:** Not applicable (reference only).
- **Cost:** N/A.
- **Risks:** N/A.

### TavernKit Preset System

- **Strengths:** Per-chat overrides (toggling individual prompts) without cloning the preset. Loadout system for saved named configurations. Injection depth control for mid-conversation instructions. Well-designed prompt entry system with conditional activation.
- **Weaknesses:** Ruby library, roleplaying/RPG focus, complex DSL. Not directly reusable.
- **Integration effort:** Not applicable (reference only).
- **Cost:** N/A.
- **Risks:** N/A.

## Recommendation

**Direction:** Adopt and extend

The existing system is complete for global preset selection. The only remaining requirement is FR-02 (per-session selection). This can be achieved by:
- Adding a session-level `responseStylePreset` field to the session store
- Adding a preset selector to the session toolbar or chat input area (not just the Settings page)
- Passing the selected preset as a parameter when creating a session or sending the first message, so the OpenCode SDK includes it as prompt context

For FR-04 (custom presets), the Claude Code output styles pattern (markdown files with frontmatter) is a good architectural reference: users write preset content as files that are read at session start. This could be a future enhancement.

## Sources of Information

- Existing `packages/ui/src/lib/responseStyle.ts`: 7 presets, builder function, fetch function
- Existing `BehaviorPage.tsx`: Settings UI for global preset selection
- Claude Code output styles: `https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts`
- TavernKit preset system: `https://github.com/jasl/tavern_kit`
- Mandu prompt presets: `https://mandujs.com/docs/ai/prompts`

## Open Questions

1. Should the per-session preset selector be in the chat toolbar, the session sidebar, or the composer area?
2. When a session has a per-session preset, should it override or merge with the global default?
3. Should custom presets be persisted as files (Claude Code pattern) or as strings in the settings store?

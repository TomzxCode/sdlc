---
issue: ""
title: "AI-Generated Commits & PR Descriptions"
status: draft
---

# Existing Solutions: AI-Generated Commits & PR Descriptions

## Overview

AI-generated commit messages and PR descriptions are widely solved by dedicated CLI tools (aicommits, aic-commit, git-ai, commitgenius, etc.), but OpenChamber already has a substantial in-house implementation. The codebase has `generateCommitMessage` and `generatePullRequestDescription` client API functions in `gitApiHttp.ts`, Magic Prompts system for customizable generation prompts (`git.commit.generate.*` and `git.pr.generate.*`), and UI i18n strings for generated commit results and highlights. The feature requires integration with the current session's model (FR-07) and customizable prompts with server-side persistence (FR-08), which the Magic Prompts system provides. The recommended direction is to build on the existing Magic Prompts and git generation API infrastructure rather than adopting a third-party CLI.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/lib/gitApiHttp.ts` (generateCommitMessage, generatePullRequestDescription), `packages/ui/src/lib/magicPrompts.ts` (git.commit.generate.*, git.pr.generate.* prompts), `packages/ui/src/lib/i18n/messages/` (git commit and PR generation UI strings in 10 languages), `packages/web/server/lib/git/service.js` (git commit backend), `packages/ui/src/components/views/git/CommitSection.tsx`, `packages/ui/src/components/views/git/CommitInput.tsx`, `packages/ui/src/components/chat/message/parts/GeneratedJsonResultCard.tsx` |
| Open-source | Yes | npm/GitHub for AI commit message generators and PR description generators |
| Commercial / SaaS | Yes | GitHub Copilot commit message generation, Cursor AI commit messages |
| Standards / protocols | Yes | Conventional Commits specification |
| Reference material | Yes | opencommit, aicommits, aic-commit, git-ai, commitgenius, genai-pr, kilde |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber's existing git generation API + Magic Prompts | Internal | MIT | Production (v1.11.7) | FR-01 (commit messages from staged), FR-02 (PR from branch diffs), FR-03 (JSON parsing), FR-05 (highlights), FR-07 (uses session model), FR-08 (customizable prompts) | FR-04 (one-click insert into commit/PR input), FR-06 (visual result card) |
| aicommits (nutlope/aicommits) | CLI | MIT | Mature (v3.2.0, 8.9K stars) | Commit messages from staged changes, multiple providers, Conventional Commits | CLI-only, no PR descriptions (until recent versions), no UI integration, separate provider config |
| aic-commit (jhubbardsf/aic-commit) | CLI | MIT | Active (v1.0.0) | Commit messages + PR descriptions, 4 providers, --create for gh PR creation, JSON output, PR templates | CLI-only, no React UI, separate config management |
| git-ai (Malikasadjaved/git-ai) | CLI | MIT | Active | Commit + PR + code review + changelog, style learning from commit history, ticket auto-linking | CLI-only, separate provider config, opinionated workflow |
| commitgenius (Noumenon-ai/commitgenius) | CLI | MIT | Active | Commit messages via Claude, git hook integration, mixed commit detection, multiple options | Claude-only, no React UI, CLI-based |
| genai-pr | CLI | MIT | Active (npm) | PR descriptions via Claude/Cursor/Codex CLI, templates, auto-merge, multi-language | CLI-only, focused on PR creation, no commit generation |
| kilde (grunnverk/kilde) | CLI + Library | Apache 2.0 | Active (v1.5.x) | Commit + release notes, MCP integration for AI assistant, configurable | CLI/library, not React UI |
| @grunnverk/ai-service | Library | Apache 2.0 | Active (v1.5.x) | Commit/release note generation as reusable TypeScript library, agentic tool-calling | Library-only, would need UI layer, separate LLM config |

## Evaluation

### OpenChamber's existing git generation API + Magic Prompts

- **Strengths:** Generation happens server-side using the existing OpenCode session, so the user's configured model is used automatically (FR-07). Magic Prompts system allows full customization of both visible user messages and hidden instructions (FR-08) with server-side persistence via `/api/magic-prompts` endpoint. The `generateCommitMessage` and `generatePullRequestDescription` functions in `gitApiHttp.ts` already return structured JSON with subject/highlights (commit) and title/body (PR). The Magic Prompts templates enforce correct JSON output shapes.
- **Weaknesses:** FR-04 (one-click insert) and FR-06 (visual result card) may require UI work to wire the generated content into the commit input field and display it as a card. The `GeneratedJsonResultCard.tsx` component exists but may need adaptation for the git view.
- **Integration effort:** Low — generation API and prompt system are already in production. UI wiring may be a few components.
- **Cost:** None (MIT, in-house).
- **Risks:** None significant.

### aicommits / aic-commit / git-ai / commitgenius (CLIs)

- **Strengths:** Mature, well-tested. aicommits has 8.9K stars. git-ai introduces style learning from commit history. aic-commit has first-class PR support with `gh` integration. commitgenius detects mixed commits and offers multiple options.
- **Weaknesses:** CLI tools that wrap `git diff` — they cannot use the session's configured model and provider (FR-07 requirement). Running a subprocess CLI from a web/desktop app adds complexity (bundling, path resolution, output parsing). Customizable prompts (FR-08) would require each CLI's own config mechanism, not the Magic Prompts system. Would need to replicate the Magic Prompts integration on the server side regardless.
- **Integration effort:** Medium-high — would need to spawn CLI processes, parse output, handle errors, and still build the Magic Prompts integration for FR-08.
- **Cost:** Free (MIT).
- **Risks:** CLI tools have their own provider configuration (separate API keys, model selection). FR-07 requires using the current session's model, which is incompatible with a CLI's independent config. Maintenance burden of keeping CLI versions in sync.

## Recommendation

**Direction:** Adopt and extend (build on existing internal API + Magic Prompts)

The existing `generateCommitMessage` and `generatePullRequestDescription` API functions in `gitApiHttp.ts` already call the server, which uses the current OpenCode session's configured model. The Magic Prompts system provides customizable prompts with server-side persistence. The main work is FR-04 (one-click insert into commit/PR input) and FR-06 (visual result card), which are UI-only additions to `CommitSection.tsx`/`CommitInput.tsx` and possibly reusing `GeneratedJsonResultCard.tsx`. The CLI tools (aicommits, aic-commit, etc.) are excellent reference implementations for prompt engineering patterns (Conventional Commits format, highlights extraction, truncation strategies) but are not suitable for direct integration due to the FR-07 and FR-08 requirements.

## Sources of Information

- aicommits (`github.com/nutlope/aicommits`, 8.9K stars): Reference for prompt engineering and CLI patterns. Supports `conventional`, `gitmoji`, `subject+body` formats.
- aic-commit (`github.com/jhubbardsf/aic-commit`): Reference for PR description generation with `gh` integration, PR template detection from `.github/PULL_REQUEST_TEMPLATE.md`, and `--create` PR flow.
- git-ai (`github.com/Malikasadjaved/git-ai`): Style learning from last 20 commits — OpenChamber could implement similar learning from the session's git log to match the user's existing commit style.
- commitgenius (`github.com/Noumenon-ai/commitgenius`): Mixed commit detection (warning when a diff should be split into multiple commits) is an interesting UX pattern to consider.
- Conventional Commits (`conventionalcommits.org`): Standard format used by the existing Magic Prompts templates.
- Magic Prompts (`packages/ui/src/lib/magicPrompts.ts`): The `git.commit.generate.*` and `git.pr.generate.*` prompt IDs with their visible/instructions templates and placeholders are the foundation for FR-08.

## Open Questions

1. For FR-04 (one-click insert): Should the generated commit message be inserted into the existing commit input, or should it auto-fill and immediately show a diff preview? The "one-click" wording suggests auto-fill without confirmation, but best practice is to show the generated message for review.
2. For FR-06 (visual result card): Should `GeneratedJsonResultCard.tsx` be reused as-is, or does the git view need a specialized card? The existing card shows generated JSON results in chat messages; the git view may need its own layout.

---
issue: ""
title: "Magic Prompts"
status: draft
---

# Existing Solutions: Magic Prompts

## Overview

The magic prompts feature is fully implemented across the codebase. A server-side runtime (`packages/web/server/lib/magic-prompts/runtime.js`) manages a JSON file (`magic-prompts.json`) in the OpenChamber data directory, providing CRUD for prompt overrides. REST API routes (`packages/web/server/lib/magic-prompts/routes.js`) expose GET/put/delete endpoints for managing individual prompts and bulk reset. The VS Code extension has full bridge support for magic prompts via `bridge-settings-runtime.ts` and `bridge-config-runtime.ts`. The feature was released in v1.9.4 with a dedicated settings page. Default templates ship with each release and user overrides are layered on top. The existing solution covers all functional requirements.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/magic-prompts/runtime.js`, `packages/web/server/lib/magic-prompts/routes.js`, `packages/web/server/lib/opencode/core-routes.js`, `packages/web/server/lib/opencode/feature-routes-runtime.js`, `packages/vscode/src/bridge-settings-runtime.ts`, `packages/vscode/src/bridge-config-runtime.ts`, `packages/vscode/webview/main.tsx` |
| Open-source | Yes | Prompt template systems, OpenCode SDK prompt handling, AGENTS.md conventions |
| Commercial / SaaS | No | N/A — feature is internal prompt template management |
| Standards / protocols | No | N/A |
| Reference material | Yes | OpenChamber docs for Magic Prompts, CHANGELOG.md for v1.9.4 release notes |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Internal magic-prompts runtime + routes | Internal | MIT | Production | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-08, FR-09 | None |
| OpenCode AGENTS.md prompt system | External | MIT | Mature | Reference pattern for prompt templates | Not a replacement — complementary |
| CortexKit Magic Context | Plugin | MIT | Active | Not applicable — different purpose (context management vs prompt library) | N/A |

## Evaluation

### Internal magic-prompts runtime + routes

- **Strengths:** Fully implemented with server-side persistence using atomic JSON file writes.
  Override system with `setOverride`, `resetOverride`, `resetAllOverrides` methods.
  Prompt ID validation with strict regex pattern (`/^[a-z0-9._-]{1,160}$/`).
  Maximum text length enforcement (200KB).
  Write-lock serialization prevents concurrent write corruption.
  REST API with proper error handling and HTTP status codes.
  VS Code bridge provides same API surface for the extension runtime.
  Supports visibility toggling per prompt (prompts ending in `.visible`).
  Layered approach: defaults ship with release, user overrides are stored separately and merged.
  Released in v1.9.4 with dedicated settings page (confirmed in CHANGELOG.md).
- **Weaknesses:** No support for creating entirely new prompt IDs — only overrides of hardcoded IDs (by design per FR-08).
  The default prompt templates are hardcoded in the codebase rather than loaded from external files (may make customization harder for power users).
- **Integration effort:** Already done.
- **Cost:** Free.
- **Risks:** None — the solution is in production.

### OpenCode AGENTS.md prompt system

- **Strengths:** OpenCode's native system for customizing agent behavior through markdown files.
  Allows per-agent prompt customization.
- **Weaknesses:** This is the underlying system that OpenChamber's Magic Prompts work with, not an alternative.
  Lower-level than the Magic Prompts UI — requires editing markdown files directly.
- **Integration effort:** N/A — complementary system.
- **Cost:** Free (MIT).
- **Risks:** None.

## Recommendation

**Direction: Adopt**

The magic prompts feature is fully implemented and in production since v1.9.4.
The design of hardcoded prompt IDs with user override layering (FR-08, FR-09) is correctly implemented.
The JSON file persistence via atomic writes is appropriate for the infrequent write pattern (user edits prompts occasionally).
No external libraries are needed — the implementation is self-contained and uses only standard Node.js `fs` APIs.
The existing solution should be adopted as-is.

## Sources of Information

- `packages/web/server/lib/magic-prompts/runtime.js`: Core runtime with read/write lock, override CRUD, prompt ID validation.
- `packages/web/server/lib/magic-prompts/routes.js`: Express routes for GET/put/DELETE /api/magic-prompts endpoints.
- `packages/web/server/lib/opencode/feature-routes-runtime.js`: Registers magic prompt routes.
- `packages/vscode/src/bridge-settings-runtime.ts`: VS Code bridge implementation for magic prompts with OPENCHAMBER_MAGIC_PROMPTS_PATH constant.
- `packages/vscode/src/bridge-config-runtime.ts`: IPC handlers for `api:magic-prompts:*` operations.
- `packages/vscode/webview/main.tsx`: Webview handler for magic prompts API calls.
- `CHANGELOG.md`: v1.9.4 release notes confirming Magic Prompts settings page launch.
- OpenChamber docs at `https://docs.openchamber.dev/magic-prompts/`: Feature documentation.

## Open Questions

1. Should the default prompt templates be moved from hardcoded constants to loadable files for easier customization?
2. Is the 200KB max prompt text length sufficient for all use cases (commit generation, PR generation, session summaries)?

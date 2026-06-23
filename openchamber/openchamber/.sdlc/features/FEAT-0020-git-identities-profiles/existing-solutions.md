---
issue: ""
title: "Git Identities / Profiles"
status: draft
---

# Existing Solutions: Git Identities / Profiles

## Overview

OpenChamber has a substantial git identities implementation with a settings page (GitPage), an editor dialog (GitIdentityEditorDialog), a Zustand store (useGitIdentitiesStore), server-side API routes for CRUD and credential discovery, git config integration, SSH key support, gitmoji caching and picker, and per-project identity application. The requirements are mostly covered. Gaps include: credential discovery from SSH config (FR-03 is partially implemented with git credential discovery, not SSH), per-project identity selection UI in project settings (FR-02), and switching identity via git includeIf config. The recommendation is to extend the existing implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | packages/ui/src/components/sections/git-identities/; packages/ui/src/stores/useGitIdentitiesStore.ts; packages/web/server/lib/git/routes.js; packages/web/server/lib/git/service.js; GitView.tsx (gitmoji); GitSettings.tsx |
| Open-source | Yes | npm for git identity/profile management libraries, gitmoji libraries |
| Commercial / SaaS | No | Not applicable |
| Standards / protocols | No | Git config includeIf is the relevant standard |
| Reference material | Yes | git-profile-switch, gitprofile, gitrole, gitswitch, gitmojis npm |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal implementation | Internal | MIT | Mature | FR-01, FR-03 (partial), FR-04, FR-05, FR-06, FR-07 | FR-02 (per-project selection UI), FR-03 (SSH config discovery) |
| git-profile-switch (CLI) | CLI | ISC | Early (0.1.x) | FR-01, FR-02 | No UI, no gitmoji, no SSH key management, CLI only |
| gitprofile (Go CLI) | CLI | MIT | Active | FR-01, FR-02, FR-05 | No UI, no gitmoji, separate Go binary, no credential discovery |
| gitrole (CLI) | CLI | MIT | Active (0.7.x) | FR-01, FR-02, FR-05 | No UI, no gitmoji, no credential discovery |
| gitmojis (npm package) | Library | MIT | Mature (3.15.0, 92K weekly) | FR-04, FR-06 | No identity management — gitmoji data only |

## Evaluation

### Existing Internal Implementation

- **Strengths:** Full identity CRUD with name/email/SSH key/token auth type, color and icon customization, global identity display, credential discovery from git config (host+username), default identity per project, gitmoji picker with local caching (TTL), server-side git config apply (user.name, user.email, core.sshCommand), SSH agent integration, VS Code bridge for identity operations, i18n translations
- **Weaknesses:** Per-project identity selection is tracked via a `defaultGitIdentityId` config key but there is no per-repository UI dropdown in project settings to switch identities. Credential discovery only checks git config, not SSH config (~/.ssh/config). SSH key paths use a simple text input with no file browser. No support for git `includeIf` conditional configs for automatic identity switching per directory.
- **Integration effort:** Low — all changes are additive to existing stores and routes
- **Cost:** Already maintained
- **Risks:** None significant

### External git identity CLI tools

- **Strengths:** Each offers a focused CLI for switching git identities using git config modifications, often including includeIf support
- **Weaknesses:** CLI-only, no React components, no integration with OpenChamber's session/permission model, no gitmoji support, no credential discovery from existing config, each is early-stage with low adoption
- **Integration effort:** High — would need to shell out to CLI or rewrite the tool's logic
- **Cost:** Free
- **Risks:** Low adoption, early stage, may be abandoned

### gitmojis (npm package)

- **Strengths:** Official gitmoji dataset as an npm package (zero dependencies, 92K weekly downloads), includes all emoji characters with semver metadata, can replace the current manual HTTP fetch from gitmoji.dev
- **Weaknesses:** Only provides the emoji data — no identity management
- **Integration effort:** Low — swap the current `fetch`-based gitmoji loading with a direct import from `gitmojis`
- **Cost:** Free
- **Risks:** None — mature, official package from the gitmoji project

## Recommendation

**Direction:** Build (extend existing internal implementation)

The existing identity system is comprehensive and production-used. The gaps are modest: per-project identity selection UI (add a dropdown to project settings), SSH config file discovery (parse ~/.ssh/config for Host entries), and optionally adopt the `gitmojis` npm package to replace the current HTTP fetch pattern for reliability and offline support. External CLI tools offer no UI integration and are too early-stage to adopt.

## Sources of Information

- `packages/ui/src/components/sections/git-identities/GitPage.tsx`: Identity profiles page with list, CRUD, credential discovery
- `packages/ui/src/components/sections/git-identities/GitIdentityEditorDialog.tsx`: Identity editor dialog with name, email, SSH, token, icon, color
- `packages/ui/src/stores/useGitIdentitiesStore.ts`: Zustand store with profiles, discovery, default identity
- `packages/web/server/lib/git/routes.js`: REST routes for identity CRUD, credential discovery, global identity
- `packages/web/server/lib/git/service.js`: Server-side identity operations (SSH command building, git config apply)
- `packages/ui/src/components/views/git/CommitSection.tsx`: Gitmoji integration in commit UI
- `packages/ui/src/components/views/GitView.tsx`: Gitmoji picker with caching, commit view
- `packages/ui/src/components/sections/openchamber/GitSettings.tsx`: Git settings with gitmoji toggle
- `packages/web/server/lib/opencode/skill-routes.js`: Identity resolution in skill context
- `gitmojis` on npm: <https://www.npmjs.com/package/gitmojis> — Official dataset package
- `git-profile-switch` on npm: <https://github.com/prateekmaheshwari/git-profile-switch> — Reference for includeIf pattern
- `gitprofile` on GitHub: <https://github.com/hapiio/git-profile> — Reference for profile management patterns

## Open Questions

1. Should per-project identity selection be in the existing project settings or in the Git identities settings page with a project selector?
2. Should we adopt the `gitmojis` npm package (removing the fetch dependency) or keep the HTTP cache approach for smaller bundle size?
3. Does the SSH config discovery need to parse all possible SSH config formats (Include directives, Match blocks, Host wildcards) or just simple Host entries?

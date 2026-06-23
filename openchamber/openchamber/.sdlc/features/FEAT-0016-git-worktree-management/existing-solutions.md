---
issue: ""
title: "Git Worktree Management"
status: draft
---

# Existing Solutions: Git Worktree Management

## Overview

OpenChamber already has an extensive worktree implementation in both the server (simple-git wrapper, routes, bootstrap state) and UI (worktreeManager, worktreeCreate, worktreeStatus, WorktreeSectionContent). The requirements build on this foundation by adding branch renaming/deletion, PR-based worktree creation, agent group views, and draft-first creation. No external library covers these gaps; the recommendation is to extend the existing internal implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | packages/web/server/lib/git/service.js, routes.js; packages/ui/src/lib/worktrees/; packages/ui/src/components/sections/openchamber/WorktreeSectionContent.tsx |
| Open-source | Yes | npm/github for worktree management CLI and GUI tools |
| Commercial / SaaS | No | Not applicable |
| Standards / protocols | No | Git worktree protocol is stable |
| Reference material | Yes | git-worktree documentation, worktreeHQ, git-worktree-toolbox |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal implementation (simple-git wrapper) | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-07 | FR-05, FR-06, FR-08, FR-09 |
| git-worktree-toolbox (MCP server + CLI) | CLI/MCP | MIT | Early (0.5.x) | FR-01, FR-03 | FR-02, FR-04, FR-05, FR-06, FR-08, FR-09, architecture mismatch (MCP) |
| WorktreeHQ (Tauri desktop app) | Desktop | Other | Early (0.x) | FR-01, FR-03, FR-06 | FR-02, FR-04, FR-05, FR-07, FR-08, FR-09, separate app not embeddable |
| worktree-mcp-manager (Tauri + MCP) | Desktop/MCP | MIT | Early (0.x) | FR-01, FR-03 | FR-02, FR-04, FR-05, FR-07, FR-08, separate app not embeddable |
| worktree-manager (Tauri) | Desktop | MIT | Active (50 releases) | FR-01, FR-03 | Separates app, not embeddable, Chinese docs |

## Evaluation

### Existing Internal Implementation

- **Strengths:** Comprehensive server-side worktree CRUD (create, validate, list, delete, bootstrap status), porcelain parsing, branch tracking fallback, setup commands, worktree metadata linking to sessions, UI for listing/deletion
- **Weaknesses:** No branch renaming or deletion from worktree UI, no PR-based worktree creation, no Agent Group view, no stash management integration, no draft-first creation flow
- **Integration effort:** Low — all changes are additions to existing server routes and UI components
- **Cost:** Already maintained; incremental cost only
- **Risks:** Simple-git is already a dependency with known contract

### git-worktree-toolbox

- **Strengths:** Pure CLI and MCP server approach, MIT licensed, covers create/list/remove/archive/clean workflows
- **Weaknesses:** MCP architecture mismatch (OpenChamber is Express + REST, not MCP), no session association, no UI components, early-stage (0.5.x)
- **Integration effort:** High — would need to wrap MCP tools with HTTP routes or run sidecar process
- **Cost:** Free
- **Risks:** Immature, architecture incompatible

### WorktreeHQ

- **Strengths:** Beautiful worktree dashboard with live cards, dirty state detection, squash-merge detection, per-worktree notepad, Claude session awareness
- **Weaknesses:** Separate desktop app (Tauri), read-only except create/remove, one repo at a time, build-from-source only, architecture incompatible
- **Integration effort:** Very high — separate app cannot be embedded
- **Cost:** Free
- **Risks:** Pre-v1, build from source only, no installers

## Recommendation

**Direction:** Build (extend existing internal implementation)

The codebase already has production-grade worktree management on the server side (simple-git wrapper with porcelain parsing, bootstrap state, validation) and a functional UI section. The requirements (branch renaming, PR-based creation, agent group view, draft-first, stash management, dirty-change warnings) are additive features on top of this foundation. None of the external solutions are embeddable into OpenChamber's Express + React architecture, nor do they cover OpenChamber-specific concerns like session association and setup commands.

## Sources of Information

- `packages/web/server/lib/git/service.js`: Core worktree operations (create, remove, list, validate, bootstrap)
- `packages/ui/src/lib/worktrees/`: Client-side worktree API (worktreeCreate, worktreeManager, worktreeStatus, worktreeBootstrap)
- `packages/ui/src/components/sections/openchamber/WorktreeSectionContent.tsx`: Worktree listing and deletion UI
- `packages/ui/src/lib/worktrees/pendingDraftWorktree.ts`: Draft-first worktree creation pattern
- `packages/web/server/lib/git/routes.js`: REST routes for worktree operations
- `git-worktree-toolbox` on npm: MCP-based CLI worktree manager (reference for PR+branch operations)
- WorktreeHQ on GitHub: Desktop worktree dashboard (reference for UI patterns like dirty state cards, stash display)

## Open Questions

1. Should branch renaming/deletion be a server-only operation (git branch -m/-d) or include UI-level session metadata updates?
2. Should the Agent Group view be a new page/section or an embedded panel in the existing settings area?
3. For PR-based creation, should we use the GitHub API (Octokit) to discover PR branches, or rely on git remote refs?

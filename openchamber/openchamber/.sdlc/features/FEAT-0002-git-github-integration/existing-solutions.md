---
issue: ""
title: "Git & GitHub Integration"
status: draft
---

# Existing Solutions: Git & GitHub Integration

## Overview

OpenChamber's Git and GitHub integration is already largely implemented using `simple-git` for server-side Git operations (status, diff, branches, commits, push/pull, stash, worktrees, merge/rebase) and `@octokit/rest` for GitHub API access (OAuth device flow, PR creation, PR status checks, issue/PR picker). The recommendation is to continue using both libraries, which are well-established and appropriate for the project's architecture, while filling remaining feature gaps (multi-remote push, fork-aware PR, rebase UI, conflict resolution UI) within the existing module structure.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/git/` (service.js, routes.js, credentials.js, identity-storage.js), `packages/web/server/lib/github/` (auth.js, octokit.js, device-flow.js, pr-status.js, repo/), `packages/ui/src/stores/` (useGitStore, useGitHubAuthStore, useGitHubPrStatusStore, useGitIdentitiesStore), `packages/ui/src/lib/` (gitApi.ts, gitApiHttp.ts), `packages/ui/src/components/views/GitView.tsx` (2613 lines), `packages/ui/src/components/views/git/` (10+ sub-components), `packages/ui/src/components/session/` (BranchPickerDialog, GitHubIssuePickerDialog, GitHubPrPickerDialog) |
| Open-source | Yes | simple-git, isomorphic-git, nodegit, Dugite, @octokit/rest, octokit-plugin-create-pull-request |
| Commercial / SaaS | Yes | GitHub (PRs, issues, code review), GitLab, Bitbucket, SourceHut |
| Standards / protocols | Yes | Git protocol, GitHub REST API v3, Git worktree protocol |
| Reference material | Yes | simple-git documentation, Octokit REST.js docs, Pro Git book, Git worktree patterns |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| simple-git (current) | Library | MIT | Mature (10.8M/week) | FR-01, FR-02, FR-03 (via git binary wrapper), FR-07, FR-08, FR-09, FR-11 (basic) | FR-04 (PR creation), FR-05 (PR status), FR-10 (multi-remote + fork), FR-06 (issue/PR session start) |
| @octokit/rest (current) | Library | MIT | Mature (15.4M/week) | FR-04 (PR create via REST), FR-05 (PR status checks), FR-06 (issue/PR fetch), FR-10 (fork-aware) | FR-01, FR-02, FR-03, FR-07, FR-08, FR-11 (Git-only operations) |
| internal Git module (`packages/web/server/lib/git/`) | Internal | MIT | Ship-ready | FR-01 through FR-03, FR-07, FR-08 (basic worktree), FR-09 (identities) | FR-04 (no AI PR description generator), FR-05 (no PR status inline), FR-10 (multi-remote), FR-11 (rebase UI) |
| internal GitHub module (`packages/web/server/lib/github/`) | Internal | MIT | Ship-ready | FR-04 (raw PR create), FR-05 (PR status), FR-06 (issue/PR fetch) | FR-04 (AI description not integrated, needs opencode SDK) |
| octokit-plugin-create-pull-request | Plugin | MIT | Mature (110K/week) | FR-04 (multi-file PR with forks, auto-fork when no write access) | Plugin for Octokit - covers fork-aware PR creation |
| isomorphic-git | Library | MIT | Mature (1.1M/week) | Pure JS git, browser support | No SSH support, slower than native git, poor Bun compatibility |

## Evaluation

### simple-git (current)

- **Strengths:** Most popular Node.js Git library (3.8K GitHub stars, 10.8M npm weekly). Promise-based API covering all common Git operations. Wraps the git binary so full git feature set is accessible via `.raw()`. Excellent TypeScript support. Actively maintained. Works well with Bun.
- **Weaknesses:** Still a git binary wrapper (requires git installed). Authentication relies on system git config. Two-phase polling (NFR-01) must be implemented on top. Sparse checkout requires `.raw()`.
- **Integration effort:** Already integrated. All core Git operations already use simple-git.
- **Cost:** MIT (free).
- **Risks:** Low. simple-git is well-maintained. No Bun compatibility issues.

### @octokit/rest (current)

- **Strengths:** Official GitHub REST API client (652 GitHub stars, 15.4M npm weekly). Full coverage of all GitHub REST endpoints. TypeScript types. Multiple auth strategies (token, OAuth, GitHub App). Actively maintained by Octokit team.
- **Weaknesses:** REST API only (GraphQL via separate package). Requires network access. Rate limits apply. OAuth token management is additional complexity.
- **Integration effort:** Already integrated. OAuth device flow, Octokit factory, and PR status resolution already implemented.
- **Cost:** MIT (free).
- **Risks:** Low. GitHub API deprecations are well-communicated. Octokit team maintains backward compatibility.

### octokit-plugin-create-pull-request

- **Strengths:** Handles fork creation when user lacks write access. Multiple file changes in single commit. Can update existing PRs. Auto-resolves default branch.
- **Weaknesses:** Plugin adds complexity. The existing PR creation flow is already functional.
- **Integration effort:** Low. Simple plugin registration on Octokit instance.
- **Cost:** MIT (free).
- **Risks:** Low. Well-maintained by Octokit community member.

## Recommendation

**Direction:** Adopt and extend

Continue using simple-git and @octokit/rest, which are already deeply integrated and well-suited to the project's server-side architecture. For the remaining feature gaps:

- **FR-04 (AI-generated PR descriptions):** Already partially addressed by the `generateCommitMessage` function in `gitApi.ts` which calls the OpenCode SDK. Extend this to generate PR descriptions as well.
- **FR-10 (fork-aware PR creation):** Adopt `octokit-plugin-create-pull-request` as a lightweight plugin injection into the existing Octokit factory (`packages/web/server/lib/github/octokit.js`). It handles fork auto-creation when the user lacks write access - the key gap in the current PR flow.
- **FR-11 (rebase + conflict UI):** Both simple-git's `.raw()` method and the existing `service.js` merge/rebase support can be extended. No alternative library provides a meaningful advantage here.
- **NFR-01 (two-phase polling):** The architecture doc already specifies lightweight change detection before heavy status fetches. This is an implementation detail within the existing `useGitStore`.

## Sources of Information

- simple-git npm/docs: `npmjs.com/package/simple-git` — lightweight git binary wrapper with promise API
- @octokit/rest GitHub: `github.com/octokit/rest.js` — official GitHub REST API client
- octokit-plugin-create-pull-request: `github.com/gr2m/octokit-plugin-create-pull-request` — multi-file PR with auto-fork
- isomorphic-git comparison: `github.com/dexhorthy/kustomark-ralph-bash/blob/main/GIT_LIBRARIES_COMPARISON.md` — detailed comparison of simple-git vs isomorphic-git vs nodegit
- Git worktree docs: `git-scm.com/docs/git-worktree` — worktree protocol reference
- Existing `packages/web/server/lib/git/DOCUMENTATION.md` — comprehensive API documentation for the internal Git module

## Open Questions

1. Should `octokit-plugin-create-pull-request` be adopted for fork-aware PR creation, or should fork detection remain custom (current state in `packages/web/server/lib/github/repo/fork-detection.js`)?
2. Does the two-phase polling (NFR-01) need a new file-watcher-based approach, or is polling with change detection sufficient?

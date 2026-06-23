---
issue: ""
title: "GitHub Issue / PR Starters"
status: draft
---

# Existing Solutions: GitHub Issue / PR Starters

## Overview

The codebase already has a complete implementation. `@octokit/rest` is the GitHub SDK, server routes (`packages/web/server/lib/github/routes.js`) provide REST endpoints for listing/fetching issues and PRs with fork-aware network resolution, and UI dialogs (`GitHubIssuePickerDialog.tsx`, `GitHubPrPickerDialog.tsx`) provide the picker UX. The recommended direction is to adopt the existing implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/github/`, `packages/ui/src/components/session/GitHub*PickerDialog.tsx`, `packages/web/src/api/github.ts`, `packages/vscode/src/github*.ts` |
| Open-source | Yes | Octokit SDK ecosystem, GitHub REST API |
| Commercial / SaaS | Yes | GitHub.com, GitHub Enterprise |
| Standards / protocols | Yes | GitHub REST API v3, GitHub Search API |
| Reference material | Yes | Octokit docs, GitHub API docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| @octokit/rest (current) | Library | MIT | Mature | All FRs, all GitHub REST endpoints | None for this feature |
| GitHubIssuePickerDialog.tsx | Internal | MIT | Active | FR-01, FR-05, FR-07, FR-08 | None |
| GitHubPrPickerDialog.tsx | Internal | MIT | Active | FR-02, FR-06, FR-07, FR-08 | None |
| Server routes (routes.js) | Internal | MIT | Active | FR-03, FR-04, FR-06, NFR-01 | None |
| octokit.rest.search.issuesAndPullRequests | Library | MIT | Mature | Server-side search with pagination | Not yet used in all picker paths (recently added) |

## Evaluation

### @octokit/rest

- **Strengths:** Complete GitHub REST API coverage; TypeScript types; used extensively in the codebase for auth, PR status, repo resolution, issue listing, PR creation/merge
- **Weaknesses:** Rate limited to 5,000 req/hr for authenticated users (NFR-01 explicitly acknowledges this as acceptable)
- **Integration effort:** Already fully integrated at `packages/web/package.json:27` and `package.json:100`
- **Cost:** Free (MIT); GitHub API rate limits apply
- **Risks:** Low; well-maintained by GitHub

### GitHubIssuePickerDialog.tsx

- **Strengths:** Supports browse listing, URL/number input, fork-network aware search, debounced server-side search. Icons, labels, author avatars rendered. "Start session" creates new session or worktree session with issue context.
- **Weaknesses:** Search API recently added; direct-number path guard issue identified in PR feedback
- **Integration effort:** Already exists at `packages/ui/src/components/session/GitHubIssuePickerDialog.tsx`
- **Cost:** Free
- **Risks:** Low; recently updated with server-side search

### GitHubPrPickerDialog.tsx

- **Strengths:** Same structure as issue picker. Shows PR state (open/closed/merged), draft status, head repo, base branch. Loads PR description, comments, and check status as context.
- **Weaknesses:** Same direct-number guard issue as issue picker
- **Integration effort:** Already exists at `packages/ui/src/components/session/GitHubPrPickerDialog.tsx`
- **Cost:** Free
- **Risks:** Low

### Server-side routes (routes.js)

- **Strengths:** Comprehensive implementation covering issue list, issue get, issue comments, PR list, PR context (description + comments + review comments + files + diff + checks), PR create/update/merge/ready, upstream detection, branch listing. Fork-network aware via `resolveRepoNetwork`. Caching for PR status with 90s TTL.
- **Weaknesses:** PR search hydration bug identified (page-1-only when rehydrating PR details from Search API results)
- **Integration effort:** Already exists at `packages/web/server/lib/github/routes.js` (1200+ lines)
- **Cost:** Free
- **Risks:** Low; considered production code

## Recommendation

**Direction:** Adopt and extend

All requirements are already implemented:
- FR-01: `GitHubIssuePickerDialog.tsx` with server-side issue list/search (`routes.js:946-1019`)
- FR-02: `GitHubPrPickerDialog.tsx` with server-side PR list/search (`routes.js:1127-1215`)
- FR-03: Session creation with issue/PR context pre-loaded (dialog `onStartSession` handlers)
- FR-04: Worktree creation from selected issue/PR branch (new worktree dialog integration in picker dialogs)
- FR-05: URL/number input in both pickers
- FR-06: PR context loaded via `GET /api/github/pulls/context` (`routes.js:1217-1400`) including description, comments, review comments, files, checks, diff
- FR-07: Fork-aware listing via `resolveRepoNetwork` (`routes.js:963-964`)
- FR-08: Scoped to directory's git remote and fork network via `resolveGitHubRepoFromDirectory`
- NFR-01: Uses authenticated Octokit with per_page:50; no client-side rate limiting added

Remaining work: Fix the PR search hydration bug (page-1-only) and the direct-number guard issue identified in the latest PR feedback.

## Sources of Information

- Octokit REST API client: https://github.com/octokit/octokit.js
- GitHub REST API issues docs: https://docs.github.com/en/rest/issues
- GitHub REST API pulls docs: https://docs.github.com/en/rest/pulls
- GitHub Search API: https://docs.github.com/en/rest/search
- GitHub Module Documentation: `packages/web/server/lib/github/DOCUMENTATION.md`

## Open Questions

1. Should the PR search hydration bug be fixed by iterating multiple pages of `pulls.list` or by using individual `pulls.get` calls for each matched PR number?
2. Should the direct-number guard in picker dialogs suppress the debounced Search API call when `directNumber` is set?
3. Is cross-repository issue linking (out of scope by spec) commonly requested enough to warrant future consideration?

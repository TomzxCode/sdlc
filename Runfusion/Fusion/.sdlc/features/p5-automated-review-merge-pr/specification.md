---
title: "Automated Code Review, Merge & PR Automation"
status: done
---

# Specification: Automated Code Review, Merge & PR

## Overview

Review runs as a workflow-graph node (`review`), then the merger lands finished branches: squash by default, with rebase/PR paths, conflict resolution, smart-pull/auto-prerebase, and a stack of guards (file-scope, overlap, diff-volume, lineage). PR automation drives GitHub/GitLab create/monitor/respond/finalize.

## Architecture

```
workflow graph ── review node (workflow-review-service) ──► verdict
      │
      ▼
merger (merger.ts + merge/) ── squash/rebase/PR
      │   guards: file-scope, overlap, diff-volume, lineage, post-squash audit
      ▼
default branch / PR (GitHub | GitLab) ── pr-monitor, pr-nodes, pr-response-run
```

## Data Models

### Merge Plan / Branch Group

| Field | Type | Constraints | Description |
|---|---|---|---|
| taskId | int | PK | Task being merged |
| branchName | string | not null | Working branch / shared-branch-group |
| strategy | enum | not null | always-squash / auto / always-rebase |
| landedSha | string | — | Commit SHA after landing |

## Sequences

### Merge

```
approval → merge-active → pre-merge review node
   → guard checks (file-scope overlap diff-volume)
   → auto-prerebase/smart-pull on divergence
   → squash commit (default) → post-squash audit (warn/block/off)
   → push → verify → in-review/done
```

### PR lifecycle

```
pr-create node → PR monitor → PR checks → response-run → finalize → merge
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Squash default | `directMergeCommitStrategy="always-squash"` | Clean history; opt-in for multi-commit |
| File-scope invariant | `FileScopeViolationError` | Prevents out-of-scope changes landing |
| Smart prefer-main overlap | overlap-guard flip | Recent main overlap can favor branch |
| Post-squash audit | warn/block/off modes | Prevents suspicious shrinkage |

## Risks and Unknowns

1. Divergent push races are handled by recovery-branch safety refs and push:origin aborted outcomes.

## Out of Scope

- Planner oversight gates (FEAT-p3) and the board surface (FEAT-p1)
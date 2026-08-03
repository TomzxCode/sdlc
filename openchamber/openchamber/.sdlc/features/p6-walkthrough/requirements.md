---
title: "Changes Walkthrough"
status: done
---

# Requirements: Changes Walkthrough

## Overview

The Changes Walkthrough turns a large diff into an AI-guided tour of the change. It groups related hunks into ordered stops and chapters, explains what each group does, and renders the explanation interleaved with the code it describes. Generation is always user-initiated because it spends tokens; nothing runs on a timer or as a side effect of opening a panel. The walkthrough can cover the working tree, a branch, or an open pull request.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users (developers) | Understand a large or unfamiliar diff without reading every hunk |
| Reviewers | Get an ordered, explained tour of a change before reviewing it |
| Session goal / review workflows | Reuse the small model to summarize changes on demand |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall generate a walkthrough only when the user explicitly requests it. |
| FR-2 | Must | The system shall accept a diff source of type working-tree (all, staged, or working), branch, or pull request. |
| FR-3 | Must | The system shall group related hunks into stops and chapters in a meaningful order using the small model. |
| FR-4 | Must | The system shall assign each hunk a stable, content-addressed id so anchors stay valid and stale stops are provable. |
| FR-5 | Must | The system shall render stops interleaved with the code they describe in the UI. |
| FR-6 | Must | The system shall report generation progress and allow cancelling an in-progress generation. |
| FR-7 | Should | The system shall cache walkthrough results keyed by the generated content so regenerating an unchanged diff is cheap. |
| FR-8 | Should | The system shall support a per-feature model override distinct from the general small-model setting. |
| FR-9 | Should | The system shall generate walkthrough prose in the user's selected language. |
| FR-10 | Should | The system shall load a pull request's diff through the shared GitHub helper for walkthroughs of PRs. |
| FR-11 | Must | The system shall keep tool-produced files (e.g. lockfiles, build artifacts) out of the model input. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Walkthrough generation shall report progress and respond to cancellation without blocking the server. |
| NFR-2 | Should | Cost | Token use shall be proportional to the requested diff; the user triggers generation explicitly. |
| NFR-3 | Should | Reliability | Cached walkthroughs shall be content-addressed so stale or invalidated entries do not mis-anchor stops. |

## Constraints

- Uses the small model (`packages/web/server/lib/small-model/`) and the user's configured provider
- Hunk identity is decided only in `hunks.js`; the client never recomputes hunk ids
- PR diffs come from the shared GitHub octokit helper

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a session with an unviewed walkthrough panel
    - **When** the user has not clicked generate
    - **Then** no walkthrough is generated and no tokens are spent
- [ ] **FR-2**
    - **Given** a diff source
    - **When** the user requests a walkthrough of working-tree, branch, or PR changes
    - **Then** the walkthrough is generated from that source
- [ ] **FR-3**
    - **Given** a large diff
    - **When** the walkthrough is generated
    - **Then** related hunks appear grouped into ordered stops and chapters
- [ ] **FR-4**
    - **Given** a hunk that later changes
    - **When** the walkthrough is re-validated
    - **Then** the stale stop is provable by the changed hunk id
- [ ] **FR-5**
    - **Given** a generated walkthrough
    - **When** the user opens it
    - **Then** explanations render next to the code they describe
- [ ] **FR-6**
    - **Given** an in-progress generation
    - **When** the user cancels
    - **Then** the generation stops and the UI reflects the cancelled state
- [ ] **FR-11**
    - **Given** a diff containing generated files
    - **When** the walkthrough is generated
    - **Then** the generated files are excluded from the model input

## Conflicts

None identified yet.

## Open Questions

1. What token budget should guide stop granularity for very large PR diffs?

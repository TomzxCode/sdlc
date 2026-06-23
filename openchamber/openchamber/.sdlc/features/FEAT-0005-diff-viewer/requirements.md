---
title: "Diff Viewer"
status: draft
---

# Requirements: Diff Viewer

## Overview

OpenChamber provides a full-screen diff viewer for inspecting code changes. It supports side-by-side and stacked layouts, file tree navigation for multi-file changesets, per-file diff expansion for large files, image diffs, and actions like copy and delete. The diff viewer is used both standalone and inline in chat tool output.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Review AI-generated code changes before accepting |
| Code reviewers | Inspect diffs from pull requests and commits |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display file diffs in side-by-side and stacked (unified) modes. |
| FR-02 | Must | The system shall show a file tree for multi-file changesets with navigation. |
| FR-03 | Must | The system shall support expanding/collapsing per-file diff sections for large changesets. |
| FR-04 | Must | The system shall render syntax-highlighted diffs with added/removed line indicators. |
| FR-05 | Must | The system shall support inline diff rendering within chat tool output messages. |
| FR-06 | Should | The system shall display image diffs (before/after comparison). |
| FR-07 | Should | The system shall support inline comment drafts on diff lines. |
| FR-08 | Should | The system shall handle multi-file tool diffs with mixed line endings safely. |
| FR-09 | May | The system shall support copy/delete actions on diffed files. |
| FR-10 | Should | The system shall support standard two-parent diffs; three-way merge diff visualization is not supported. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Large changesets (100+ files) shall display reliably without UI freeze. |
| NFR-02 | Should | Performance | Lazy loading of per-file diff content for large changesets. |

## Constraints

- Uses `@pierre/diffs` library for diff rendering
- Diffs are computed server-side and streamed to the UI
- Inline diffs in chat must handle mixed line endings (CRLF/LF)

## Acceptance Criteria

- [ ] FR-01: Given a diff, the user can toggle between side-by-side and stacked modes
- [ ] FR-02: Given a multi-file changeset, the file tree shows all changed files with navigation
- [ ] FR-04: Given a diff with syntax-highlighted code, added lines show green and removed lines show red
- [ ] FR-05: Given an assistant tool call with a file diff, the diff renders inline in the chat message
- [ ] FR-08: Given a diff with mixed CRLF/LF line endings, it renders without errors
- [ ] FR-10: Given a merge conflict diff, the system shows standard two-parent diff only; three-way visualization is not available
- [ ] FR-03: Given a large changeset with many files, individual file diffs can be expanded and collapsed
- [ ] FR-06: Given an image diff (before/after), the viewer shows a side-by-side comparison
- [ ] FR-07: Given a diff view, the user can add inline comment drafts on specific lines
- [ ] FR-09: Given a diffed file, the user can copy the file contents or delete the file from the diff view
- [ ] NFR-01: Given a changeset with 100+ files, the diff viewer renders without UI freeze
- [ ] NFR-02: Given a changeset with 100+ files, per-file diff content loads lazily as the user scrolls

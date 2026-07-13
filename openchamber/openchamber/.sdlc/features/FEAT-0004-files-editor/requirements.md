---
title: "Files & Editor"
status: done
---

# Requirements: Files & Editor

## Overview

OpenChamber provides a full file explorer and inline editor within the app. Users can browse the workspace file tree, open files with syntax highlighting via CodeMirror, edit and save, preview markdown, inspect JSON trees, view images, navigate with Go To Line, and perform CRUD operations (create, rename, delete files and folders). File paths in chat messages are clickable and jump to exact line locations.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Browse and edit project files without leaving the app |
| Code reviewers | Inspect files referenced in AI tool output |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display a workspace file tree with folder expansion, file type icons, and git status indicators. |
| FR-02 | Must | The system shall open files in a CodeMirror editor with syntax highlighting for 15+ languages. |
| FR-03 | Must | The system shall support creating, renaming, and deleting files and folders. |
| FR-04 | Must | The system shall support file search within the tree. |
| FR-05 | Must | The system shall support Go To Line navigation. |
| FR-06 | Must | The system shall render markdown files with preview mode. |
| FR-07 | Must | The system shall render JSON files with a collapsible tree view. |
| FR-08 | Must | The system shall display image files inline. |
| FR-09 | Should | The system shall support inline comment drafts on files that can be sent to the agent. |
| FR-10 | Should | The system shall support clickable file paths in chat messages that open the file at the referenced line. |
| FR-11 | Should | The system shall preserve pending navigation and ignore stale file loads. |
| FR-12 | May | The system shall support file diff preview from the file tree when git changes exist. |
| FR-13 | Must | The system shall truncate files exceeding 200,000 characters in inline editing/viewing. |
| FR-14 | Should | The system shall display a warning when previewing files over 500KB. |
| FR-15 | Must | The system shall cap file attachment size at 50MB. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | File save failures shall not silently discard edits. |
| NFR-02 | Should | Performance | Large files (10k+ lines) shall open and scroll without lag via CodeMirror virtualization. |
| NFR-03 | Should | Reliability | Switching files while a save is pending shall guard against data loss. |

## Constraints

- File operations are server-side via `/api/fs/` endpoints
- CodeMirror handles all text editing with language-specific modes
- File-type icons come from the shared SVG sprite system

## Acceptance Criteria

- [ ] FR-01: Given a project directory, the file tree shows all files and folders with icons and git status
- [ ] FR-02: Given a `.ts` file opened, syntax highlighting renders correctly
- [ ] FR-03: Given the file tree, the user can create a new file, rename it, and delete it
- [ ] FR-04: Given a project with many files, typing in search filters the tree
- [ ] FR-05: Given an open file, Go To Line navigates to the specified line
- [ ] FR-06: Given a `.md` file, preview mode renders formatted markdown
- [ ] FR-10: Given a chat message with `src/foo.ts:42`, clicking it opens the file at line 42
- [ ] FR-13: Given a file exceeding 200,000 characters, when opened inline, the content is truncated
- [ ] FR-14: Given a file over 500KB, when previewed, a "large file preview limited" warning is displayed
- [ ] FR-15: Given a file attachment exceeding 50MB, when attached, the upload is rejected
- [ ] FR-07: Given a JSON file opened, its contents are displayed in a collapsible tree view
- [ ] FR-08: Given an image file (PNG, JPG, SVG, GIF) selected, it renders inline in the editor pane
- [ ] FR-09: Given an open file, the user can add inline comment drafts and send them to the agent
- [ ] FR-11: Given a file is loading, when the user navigates to a different file, the stale load is ignored and the new file opens
- [ ] FR-12: Given the file tree with git changes, files with diffs show a preview option that opens the diff
- [ ] NFR-01: Given a file save that fails (disk full, permissions), the user is shown an error and the edit content is not discarded
- [ ] NFR-02: Given a file with 10,000+ lines, opening and scrolling is responsive without noticeable lag
- [ ] NFR-03: Given a save is in progress, when the user switches to another file, the save completes and the user is notified before the switch

---
title: "Session Folders"
status: done
---

# Requirements: Session Folders

## Overview

Users can organize sessions into named, nested folders per project. Folders support create/rename/delete, drag-and-drop reordering, add/remove sessions, collapse/expand, and automatic cleanup of deleted sessions.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | Organize sessions into meaningful groups |
| Project leads | Group sessions by feature or sprint |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating named folders for organizing sessions. |
| FR-02 | Must | The system shall support nested subfolders. |
| FR-03 | Must | The system shall support drag-and-drop reordering of sessions and folders. |
| FR-04 | Must | The system shall support rename and delete of folders with confirmation. |
| FR-05 | Should | The system shall support collapse/expand of folders. |
| FR-06 | Should | The system shall automatically clean up folders when sessions are deleted. |

## Acceptance Criteria

- [ ] FR-01: Given the session sidebar, the user creates a named folder
- [ ] FR-02: Given a folder, the user creates a subfolder inside it
- [ ] FR-03: Given sessions and folders, the user can drag to reorder them
- [ ] FR-04: Given a folder, the user can rename or delete it with confirmation
- [ ] FR-05: Given a folder with nested items, the user can collapse or expand it
- [ ] FR-06: Given a folder whose sessions are all deleted, it is cleaned up


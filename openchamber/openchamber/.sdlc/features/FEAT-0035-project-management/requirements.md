---
title: "Project Management (Multi-Project)"
status: done
---

# Requirements: Project Management

## Overview

A multi-project workspace system where users add, rename, reorder, and customize projects with icons, colors, and custom images. Each project has its own directory, sessions, git identity, and configuration. Projects appear in the sidebar with visual indicators and can be switched between instantly.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers with multiple repos | Switch between projects without restarting |
| Teams | Organize work by project with distinct configurations |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support adding projects by selecting a directory. |
| FR-02 | Must | The system shall support per-project sessions, git identity, and configuration. |
| FR-03 | Must | The system shall support renaming, reordering, and deleting projects. |
| FR-04 | Must | The system shall display projects with visual indicators (icons, colors) in the sidebar. |
| FR-05 | Should | The system shall support custom project icons with upload and favicon discovery. |
| FR-06 | Should | The system shall support cloning repositories as part of project setup. |
| FR-07 | Should | The system shall support drag-to-reorder of projects. |

## Acceptance Criteria

- [ ] FR-01: Given the project list, the user adds a project by selecting a directory
- [ ] FR-02: Given multiple projects, each has its own session list and git state
- [ ] FR-03: Given an existing project, the user can rename, reorder, or delete it
- [ ] FR-04: Given a project with an icon, the sidebar shows the icon
- [ ] FR-05: Given a project, the user can upload a custom icon or the system discovers one from the project's favicon
- [ ] FR-06: Given a repository URL, the user can clone it as a new project
- [ ] FR-07: Given multiple projects, the user can drag to reorder them


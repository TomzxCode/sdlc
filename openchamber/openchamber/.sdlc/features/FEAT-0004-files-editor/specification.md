---
title: "Files & Editor"
status: draft
---

# Specification: Files & Editor

## Overview

The files view is implemented in `packages/ui/src/components/views/FilesView.tsx` (3466 lines). It integrates a file tree, CodeMirror editor, markdown previewer, JSON tree viewer, and image viewer into a single panel. File operations go through REST endpoints on the Express server.

## Architecture

```
FilesView (packages/ui/src/components/views/FilesView.tsx)
    |
    +---> FileTree (search, CRUD, git status icons)
    +---> CodeMirror Editor (syntax highlighting, Go To Line)
    +---> Markdown Preview (rendered HTML)
    +---> JSON Tree Viewer (collapsible nodes)
    +---> Image Viewer (inline display)
    |
    v  REST calls
Express Server (/api/fs/* endpoints)
    |
    v
Local filesystem
```

## Data Models

### FileEntry

| Field | Type | Constraints | Description |
|---|---|---|---|
| path | string | PK | Absolute file path |
| name | string | not null | Filename |
| type | enum | not null | file, directory |
| size | number | nullable | File size in bytes |
| modified | timestamp | nullable | Last modified time |
| gitStatus | enum | nullable | modified, added, deleted, untracked |

## API Contracts

### GET /api/fs/tree?dir=<path>

Returns recursive file tree for a directory.

### GET /api/fs/file?path=<path>

Returns file content as text or binary.

### PUT /api/fs/file

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| path | string | yes | File path |
| content | string | yes | File content |

### POST /api/fs/rename

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| oldPath | string | yes | Current path |
| newPath | string | yes | New path |

### DELETE /api/fs/file?path=<path>

Deletes a file or empty directory.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Editor | CodeMirror 6 | Best-in-class code editor with language support, extensible, performant |
| File tree | Custom component with virtualization | Handles large projects without DOM bloat |
| Language support | @codemirror/lang-* packages | Official language modes for 15+ languages |

## Risks and Unknowns

1. Very large binary files may cause memory issues if loaded inline
2. File watcher latency may cause stale tree after external changes

## Out of Scope

- Collaborative editing
- Terminal-integrated file operations
- Version control diffing (handled by Diff View feature)

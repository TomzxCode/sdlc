---
title: "Diagram Editor"
status: done
---

# Requirements: Diagram Editor

## Overview

The Diagram Editor embeds a DrawIO-based editor in OpenChamber for viewing and editing `.drawio` (and `.xml`) diagram files within a session. Users open a diagram file from the file tree, edit it visually in a rich canvas, and save the resulting XML back to disk. A dedicated Diagram View renders the editor for a pending diagram file, and the editor supports read-only mode and dark-theme matching.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users (developers) | Edit architecture diagrams and flowcharts without leaving OpenChamber |
| Architects | Visually capture designs next to the agent session that produced them |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall open a `.drawio`/`.xml` diagram file from the file tree in an embedded editor. |
| FR-2 | Must | The system shall edit diagram XML in a DrawIO-based canvas and produce updated XML on save. |
| FR-3 | Must | The system shall save edited diagram XML back to the file system. |
| FR-4 | Must | The system shall support read-only mode for diagrams opened without edit intent. |
| FR-5 | Should | The system shall provide a blank diagram template when opening a new/empty diagram. |
| FR-6 | Should | The system shall match the editor's color scheme to the app theme (dark/light). |
| FR-7 | Should | The system shall expose the editor XML to callers through a stable handle so the view can serialize on demand. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Should | Compatibility | Saved files shall remain valid DrawIO/mxGraph XML readable by external DrawIO tools. |

## Constraints

- Uses the `react-drawio` embedded editor
- Diagram format is mxGraph XML (`<mxfile>` / `<mxGraphModel>`)
- File access goes through the shared files runtime API

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a `.drawio` file selected in the file tree
    - **When** the user opens it
    - **Then** the embedded editor loads with the file's XML
- [ ] **FR-2**
    - **Given** an open diagram
    - **When** the user edits the canvas
    - **Then** the editor produces updated XML reflecting the edits
- [ ] **FR-3**
    - **Given** an edited diagram
    - **When** the user saves
    - **Then** the XML is written to the original file path
- [ ] **FR-4**
    - **Given** a diagram opened read-only
    - **When** the user attempts edits
    - **Then** editing is disabled
- [ ] **FR-6**
    - **Given** the app theme is dark
    - **When** the diagram editor opens
    - **Then** the editor renders in dark colors

## Conflicts

None identified yet.

## Open Questions

1. Should diagrams opened from agent output (not the file tree) support saving to an arbitrary path?

---
title: "Session Export"
status: done
---

# Requirements: Session Export

## Overview

Export any chat session (including sub-agent sessions) as a structured Markdown file with timestamps, model info, and nested sub-agent sections. Supports browser download, desktop native save dialog, and file reveal after saving.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | Save session transcripts for documentation or sharing |
| Desktop users | Save to disk with native file dialog |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall export sessions as structured Markdown files. |
| FR-02 | Must | The system shall include timestamps, model info, and role indicators. |
| FR-03 | Must | The system shall include nested sub-agent session sections. |
| FR-04 | Must | The system shall support browser download and desktop native save dialog. |
| FR-05 | Should | The system shall support file reveal after saving (desktop). |
| FR-06 | Should | The system shall work across web, desktop, and VS Code runtimes. |

## Acceptance Criteria

- [ ] FR-01: Given an active session, the user exports it as a Markdown file
- [ ] FR-02: Given an exported file, timestamps and model info are present
- [ ] FR-03: Given a session with sub-agents, the export includes their messages nested
- [ ] FR-04: Given desktop, the native save dialog opens; given web, the file downloads
- [ ] FR-05: Given the file is saved on desktop, clicking "Reveal" opens the file manager to its location
- [ ] FR-06: Given web, desktop, and VS Code runtimes, the export dialog is accessible and functional in each

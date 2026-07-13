---
title: "AI-Generated Commits & PR Descriptions"
status: done
---

# Requirements: AI-Generated Commits & PR Descriptions

## Overview

AI-powered generation of commit messages (subject + highlights) and PR descriptions (title + body) with structured JSON parsing, one-click copy/insert into commit input or PR form, and visual result cards. The AI generates these from staged changes or branch diffs.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Generate meaningful commit messages and PR descriptions from code changes |
| Teams | Consistent, descriptive commit and PR documentation |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall generate commit messages from staged changes via AI. |
| FR-02 | Must | The system shall generate PR descriptions from branch diffs via AI. |
| FR-03 | Must | The system shall parse structured JSON output for subject + body separation. |
| FR-04 | Must | The system shall support one-click insert of generated content into commit input or PR form. |
| FR-05 | Should | The system shall display AI-generated highlights alongside commit messages. |
| FR-06 | Should | The system shall show a visual result card for generated content. |
| FR-07 | Must | The system shall use the current session's configured model for generation without a dedicated hardcoded model. |
| FR-08 | Should | The system shall allow full customization of generation prompts via Settings with server-side persistence. |

## Acceptance Criteria

- [ ] FR-01: Given staged changes, clicking "Generate" produces a commit message
- [ ] FR-02: Given a branch with commits ahead, clicking "Generate" produces a PR description
- [ ] FR-03: Given generated content, the system parses structured JSON into subject and body
- [ ] FR-04: Given generated content, clicking "Insert" fills the commit input or PR form
- [ ] FR-05: Given a generated commit message, highlights are displayed alongside it
- [ ] FR-06: Given generated content, a visual result card is shown
- [ ] FR-07: Given a session with a configured model, generation uses that model without a dedicated hardcoded model
- [ ] FR-08: Given Settings > Magic Prompts, the user can customize generation prompts and overrides are persisted server-side

## Constraints

_No technical constraints remaining._

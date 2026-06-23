---
title: "Question Cards"
status: draft
---

# Requirements: Question Cards

## Overview

Interactive question cards rendered in the chat when the AI needs user input. Supports multiple question types: free text, multiple choice (radio/checkbox), and file paths. Includes copy-as-JSON/Markdown export and inline response submission.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | Respond to structured AI questions without typing raw text |
| Users sharing context | Export question/response pairs for documentation |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall render question cards with multiple input types (text, radio, checkbox). |
| FR-02 | Must | The system shall support inline response submission from the card. |
| FR-03 | Must | The system shall support copy-as-Markdown and copy-as-JSON for question content. |
| FR-04 | Should | The system shall support single-select radio buttons for choice questions. |
| FR-05 | Should | The system shall preserve pending questions across session switches. |
| FR-06 | Must | The system shall support question types: text, radio (single choice), checkbox (multi-choice), and file paths. |

## Acceptance Criteria

- [ ] FR-01: Given an AI question with choices, radio buttons or checkboxes render correctly
- [ ] FR-02: Given a question card, submitting a response sends it to the AI
- [ ] FR-03: Given a question card, copy buttons produce Markdown and JSON output
- [ ] FR-04: Given a single-choice question, only one option can be selected
- [ ] FR-05: Given a pending question card, switching to another session and back preserves the question and the draft response
- [ ] FR-06: Given a question of each type (text, radio, checkbox, file path), the correct input widget is rendered and submission works

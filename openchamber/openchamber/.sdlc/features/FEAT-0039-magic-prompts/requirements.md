---
title: "Magic Prompts"
status: done
---

# Requirements: Magic Prompts

## Overview

A library of pre-built, customizable AI prompt templates organized by group (Git, GitHub, Planning, Session) covering commit generation, PR generation, conflict resolution, plan creation/improvement/implementation, session summaries/reviews, and session fusion. Users can override visible prompts and instruction templates via a dedicated settings page.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | One-click AI-powered actions (commit, PR, summarize) |
| Power users | Customize prompt templates for their workflow |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide 30+ pre-built prompt templates organized by group. |
| FR-02 | Must | The system shall support customizing instruction templates per prompt. |
| FR-03 | Must | The system shall support hiding/showing specific prompts. |
| FR-04 | Must | The system shall provide a dedicated settings page for prompt management. |
| FR-05 | Should | The system shall support configurable planning prompts. |
| FR-06 | Should | The system shall power git commit and PR generation via magic prompts. |
| FR-08 | Must | The system shall allow overriding existing prompt templates without supporting creation of entirely new prompt IDs. |
| FR-09 | Must | The system shall ship default templates with each release and layer user overrides on top. |

## Acceptance Criteria

- [ ] FR-01: Given the magic prompts settings, 30+ prompts are available in groups
- [ ] FR-02: Given a prompt, the user can edit its instruction template
- [ ] FR-03: Given the settings, the user can hide prompts from quick actions
- [ ] FR-04: Given the settings page, all prompt templates are listed organized by group
- [ ] FR-05: Given a planning prompt, the user can configure its behavior
- [ ] FR-06: Given staged changes, commit generation uses a magic prompt template
- [ ] FR-08: Given an existing prompt template, the user can override it; creating entirely new prompt IDs is not supported
- [ ] FR-09: Given a new app release, default templates are shipped and user overrides are layered on top

## Constraints

- Prompt IDs are hardcoded

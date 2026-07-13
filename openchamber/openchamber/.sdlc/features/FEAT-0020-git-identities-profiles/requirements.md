---
title: "Git Identities / Profiles"
status: done
---

# Requirements: Git Identities / Profiles

## Overview

Multiple git identity profiles (name + email + auth type + SSH key) that users can switch between per-project or globally. Includes credential discovery from existing git/SSH config, gitmoji support, and a dedicated settings page.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers with work/personal repos | Switch git identities per project |
| Open-source contributors | Use different identities for different forges |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support multiple git identity profiles with name and email. |
| FR-02 | Must | The system shall support per-project identity selection. |
| FR-03 | Must | The system shall support credential discovery from existing git and SSH config. |
| FR-04 | Must | The system shall support gitmoji in commit messages. |
| FR-05 | Should | The system shall support SSH key selection per identity. |
| FR-06 | Should | The system shall cache gitmojis locally with TTL. |
| FR-07 | Must | The system shall store identity profiles centrally and support applying them globally or per-project. |

## Acceptance Criteria

- [ ] FR-01: Given the Git Identities settings, the user creates multiple profiles
- [ ] FR-02: Given a project, the user selects a specific git identity for it
- [ ] FR-03: Given existing git config, the system discovers and offers existing credentials
- [ ] FR-04: Given gitmoji enabled, the commit input shows a gitmoji picker
- [ ] FR-05: Given an identity profile, the user can select an SSH key to associate with it
- [ ] FR-06: Given gitmoji data fetched from the remote API, subsequent loads use the cached version within the TTL
- [ ] FR-07: Given an identity profile, the user can apply it globally or select it for a specific project

## Constraints

- Identity profiles are stored in OpenCode config layers

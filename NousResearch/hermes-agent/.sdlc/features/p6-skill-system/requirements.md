---
title: "Skill System"
status: draft
---

# Requirements: Skill System

## Overview

Skills are markdown documents (SKILL.md) that guide the agent on how to perform specific tasks. Hermes ships ~18 categories of built-in skills and ~20 categories of optional skills (loaded only on demand). The agent can autonomously create and improve skills from its own experience via the learning graph and curator system. Skills provide specialized instructions and workflows that are injected into the system prompt per-session.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Users | Want the agent to be able to perform specialized tasks (GitHub workflows, DevOps, creative writing, etc.) |
| Agents (self) | The agent creates skills autonomously from its own experience and improves them over time |
| Skill authors | Want to write and share skills that guide the agent through domain-specific tasks |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | Built-in skills shall be loadable by default and injected into the system prompt |
| FR-2 | Must | Optional skills shall be installable via hermes skills install command |
| FR-3 | Must | The agent shall be able to create skills from its own experience (learning graph) |
| FR-4 | Must | The curator shall track skill usage and auto-archive stale agent-created skills |
| FR-5 | Must | The agent shall have tools to list, view, create, edit, and delete skills |
| FR-6 | Should | Skills shall be organized by category in the file system |
| FR-7 | Should | Pinned skills shall be exempt from curator auto-archiving |
| FR-8 | Weather | Skills should support a hub mechanism for community distribution |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Loading many skills shall not significantly increase system prompt size (skills are stored as references, not inline content) |
| NFR-2 | Must | Safety | Agent-created skills must be reviewed before activation (optional guard) |

## Constraints

- Skills must follow the SKILL.md format with standardized frontmatter (name, description, version, platforms, etc.)
- Skill descriptions are limited to 60 characters
- Curator only touches skills with created_by: agent provenance — bundled and hub-installed skills are off-limits

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a built-in skill exists in skills/github/
    - **When** the agent loads
    - **Then** the skill is available and its instructions are injected into the system prompt
- [ ] **FR-3**
    - **Given** the agent has performed a multi-step task
    - **When** the agent decides to create a skill from the procedure
    - **Then** a new SKILL.md is created in the skills directory with the extracted steps
- [ ] **FR-4**
    - **Given** an agent-created skill has not been used for stale_after_days
    - **When** the curator runs
    - **Then** the skill is archived to ~/.hermes/skills/.archive/

## Conflicts

None identified yet.

## Open Questions

1. How should skill versioning work for agent-created skills that get improved over time?
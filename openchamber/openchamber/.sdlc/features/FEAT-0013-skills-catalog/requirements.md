---
title: "Skills Catalog"
status: done
---

# Requirements: Skills Catalog

## Overview

OpenChamber includes a skills catalog for discovering, installing, and managing reusable automation packages (skills) that extend agent behavior. Skills are loaded from remote catalogs and managed locally per project.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Extend agent capabilities with reusable automation packages |
| Skill authors | Publish and share skills via catalogs |
| Teams | Maintain project-specific skills for consistent agent behavior |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display a skills catalog UI for browsing and searching available skills. |
| FR-02 | Must | The system shall support installing skills from remote catalogs. |
| FR-03 | Must | The system shall support local skill management (enable, disable, configure). |
| FR-04 | Must | The system shall display installed skills that match OpenCode's own skill list. |
| FR-05 | Should | The system shall support multiple skill sources/registries. |
| FR-06 | Should | The system shall sync installed skills with the OpenCode server. |
| FR-09 | Must | The system shall define skills as SKILL.md files with YAML frontmatter and markdown body; skill names shall be 1-64 lowercase alphanumeric characters with hyphens. |
| FR-10 | Must | The system shall version skills via the ClawdHub API with manual re-installation for updates, supporting conflict resolution (skip or overwrite). |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Skills catalog scans shall ignore stale or outdated results. |
| NFR-02 | Should | Performance | Catalog loading shall not block the main UI thread. |

## Constraints

- Skills are defined by OpenCode's skill specification; OpenChamber is a management UI
- Skills are stored on disk in the project's `.opencode/skills/` directory
- Remote catalogs are fetched via HTTP
- Skills use SKILL.md file format with YAML frontmatter followed by markdown body
- Skills are versioned via the ClawdHub API

## Acceptance Criteria

- [ ] FR-01: Given the skills settings section, the user can browse and search available skills
- [ ] FR-02: Given a skill in the catalog, the user can install it with one click
- [ ] FR-03: Given installed skills, the user can enable, disable, or configure them
- [ ] FR-04: Given OpenCode skills, the installed list matches what OpenCode reports
- [ ] FR-05: Given the skills catalog, the user can configure multiple remote registries as skill sources
- [ ] FR-06: Given an installed skill, the system syncs its status to the OpenCode server
- [ ] FR-09: Given a skill definition, it is a SKILL.md file with YAML frontmatter and a valid name (1-64 lowercase alphanumeric with hyphens)
- [ ] FR-10: Given an installed skill with a newer version available, re-installing offers conflict resolution (skip or overwrite)
- [ ] NFR-01: Given a skills catalog scan, stale or outdated results are ignored and not shown in the UI
- [ ] NFR-02: Given catalog loading, the UI remains responsive and does not block during the fetch

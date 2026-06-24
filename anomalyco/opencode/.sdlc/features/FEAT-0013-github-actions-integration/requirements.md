---
title: "GitHub Actions Integration"
status: draft
---

# Requirements: GitHub Actions Integration

## Overview

The GitHub Actions Integration packages OpenCode as a reusable composite GitHub Action (`github/action.yml`), enabling AI-powered code review, PR analysis, and automated engineering tasks directly within GitHub CI/CD pipelines.
Users can invoke OpenCode in workflows without manual installation or configuration.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| CI/CD users | Run OpenCode in GitHub Actions without manual setup |
| Repository maintainers | Automate PR review, code analysis, and task execution in CI |
| Core team | Maintain the action definition and publish lifecycle |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a GitHub composite action that installs and runs OpenCode in CI. |
| FR-02 | Must | The action shall accept configurable inputs for the working directory, prompt, and agent selection. |
| FR-03 | Must | The action shall support running OpenCode in headless mode for automated PR analysis. |
| FR-04 | Should | The action shall preserve session output as CI artifacts for inspection. |
| FR-05 | Should | The action shall be published to the GitHub Marketplace. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Usability | The action shall require minimal YAML configuration (one step). |
| NFR-02 | Should | Compatibility | The action shall work on ubuntu-latest, macos-latest, and windows-latest runners. |

## Constraints

- The action definition lives in `github/action.yml` as a composite action.
- The action wraps the existing `install` script and CLI binary.
- Publishing workflows for the action live in `.github/workflows/publish-github-action.yml`.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a workflow using `anomalyco/opencode`
    - **When** the workflow runs
    - **Then** OpenCode is installed and executes the provided prompt
- [ ] **FR-03**
    - **Given** a PR is opened
    - **When** the action triggers on `pull_request`
    - **Then** OpenCode analyzes the PR diff and posts results as a check run
- [ ] **NFR-01**
    - **Given** a minimal workflow setup
    - **When** the action is configured with a prompt and directory
    - **Then** it runs without additional setup steps

## Conflicts

None identified yet.

## Open Questions

1. Should the GitHub Action support persistent sessions across multiple workflow runs?
2. How should API keys for LLM providers be securely passed to the action (GitHub secrets)?

---
title: "Multi-Agent / Multi-Run Sessions"
status: done
---

# Requirements: Multi-Agent / Multi-Run Sessions

## Overview

OpenChamber supports running multiple AI agents in parallel from a single prompt, using isolated Git worktrees for safe side-by-side comparisons. This enables users to explore different approaches simultaneously and merge the best results.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers exploring approaches | Compare multiple AI-generated solutions side by side |
| Team leads | Review multiple agent outputs before committing to one |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support launching multiple AI agents from a single prompt, each in its own isolated worktree. |
| FR-02 | Must | The system shall display each agent's progress independently in the UI. |
| FR-03 | Must | The system shall support fusion of multi-run session results into a unified view. |
| FR-04 | Must | The system shall support optional isolation per agent run. |
| FR-05 | Should | The system shall support multi-run on non-Git projects (without worktree isolation). |
| FR-06 | Should | The system shall display the Agent Manager UI for parallel multi-model runs. |
| FR-07 | May | The system shall support model limits per multi-run to control costs. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Each agent run shall be independent; failure of one shall not affect others. |
| NFR-02 | Should | Performance | UI shall handle concurrent streaming from multiple agents without jank. |
| NFR-03 | Must | Capacity | The system shall support up to 5 models per run group, each with its own isolated session and worktree if Git is available. |

## Constraints

- Worktree-based isolation requires a Git repository
- Non-Git projects use directory-level isolation instead
- Each agent run consumes its own OpenCode session and API tokens

## Acceptance Criteria

- [ ] FR-01: Given a prompt and 3 agents, the system creates 3 worktrees and starts 3 parallel sessions
- [ ] FR-02: Given 3 running agents, each agent's streaming output is visible independently
- [ ] FR-03: Given completed multi-run results, the fusion view shows a unified comparison
- [ ] FR-04: Given optional isolation is disabled, agents share the same working directory
- [ ] FR-05: Given a non-Git project, multi-run uses directory-level isolation instead of worktrees
- [ ] FR-06: Given the Agent Manager UI, the user can select multiple models for a parallel multi-run
- [ ] FR-07: Given a multi-run configuration, the user can set a model limit to cap costs per run
- [ ] NFR-01: Given 3 concurrent agent runs, one agent failing does not interrupt or affect the other two
- [ ] NFR-02: Given 3 agents streaming output concurrently, the UI scrolls and updates without noticeable jank or stutter
- [ ] NFR-03: Given a run group with 5 models, each gets its own isolated session and worktree; given a 6th model, the system rejects the run

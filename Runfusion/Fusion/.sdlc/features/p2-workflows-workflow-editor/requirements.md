---
title: "Selectable Workflows & Visual Workflow Editor"
status: done
---

# Requirements: Selectable Workflows & Visual Workflow Editor

## Overview

Fusion replaces the fixed legacy lifecycle with a graph-of-nodes workflow: each task runs through a user-selectable workflow composed of plan/code/review/gate/merge (and exit-gate) nodes. Operators pick a built-in workflow or author a custom one visually in a workflow editor, and the engine executes the graph with a single review authority per concern.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Selects or authora workflows, tunes nodes, validates and imports/exports workflow definitions |
| Engine | Executes the selected workflow graph against each task |
| Power user / workflow author | Uses the visual editor to author custom workflows |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide built-in workflows (e.g. six-column, coding, brainstorming, coding-ideas, lead-generation, custom v1) |
| FR-2 | Must | The system shall execute a task through the selected workflow graph via a graph executor and per-node runners (code, gate, merge, exit-gate, review) |
| FR-3 | Must | The system shall let operators select a workflow per task and resolve a default workflow |
| FR-4 | Must | The system shall render the workflow editor: view, author, validate, import/export, and tune nodes/settings |
| FR-5 | Must | The system shall define a workflow IR and transition policy governing node transitions and gates |
| FR-6 | Should | The system shall support workflow graphs with foreach and loop constructs for repeated subgraphs |
| FR-7 | Should | The system shall expose workflows through dashboard API routes and validate user-authored definitions |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Consistency | Graph execution shall preserve workflow/node state across restarts (durable execution results) |
| NFR-2 | Must | Correctness | Exactly one authority (the graph) owns review of plan/code/browser concerns |
| NFR-3 | Should | Reliability | Custom workflows shall meet the end-to-end reliability acceptance map |

## Constraints

- Plan/code/browser review is owned exclusively by workflow-graph nodes; do not reintroduce a second review authority inside implementation sessions
- `task.status === "needs-review"` / `needs-replan` are graph signals, not legacy; their writers must remain

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a fresh task
    - **When** workflow resolution runs
    - **Then** a built-in or user-selected workflow is assigned
- [ ] **FR-2**
    - **Given** an in-progress task
    - **When** the graph executor runs
    - **Then** the graph advances through the selected nodes via their runners
- [ ] **FR-3**
    - **Given** operator input and no selection
    - **When** a default workflow is needed
    - **Then** a sensible default (no-selection default) applies
- [ ] **FR-4**
    - **Given** a workflow definition
    - **When** opened in the editor
    - **Then** it can be validated, edited, imported, and exported
- [ ] **FR-5**
    - **Given** a graph with gates
    - **When** a gate fails
    - **Then** the graph halts or routes per transition policy
- [ ] **NFR-1**
    - **Given** a restart mid-graph
    - **When** the task resumes
    - **Then** graph execution state is preserved, not reset

## Conflicts

None identified yet.

## Open Questions

1. How many built-in workflows are considered a supported face-public contract, and where is the canonically catalogued?
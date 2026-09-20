---
title: "Knowledge Graph & Memory"
status: done
---

# Requirements: Knowledge Graph & Memory

## Overview

Fusion maintains a deterministic LLM-free knowledge graph over its own source, docs, and FNXC rationale comments so agents and operators can query code structure without invoking a model.
The graph lives in packages/core/src/knowledge-graph/ with a memory backend in packages/core/src/memory/ and the Memory Keeper epic FN-8920 layered on top for provenance-tagged inferred semantics.
The runtime artifact at .fusion-knowledge/graph is regenerable via `fn knowledge-graph build` and stays gitignored.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Operator | Rebuilds the graph explicitly and browses it in the dashboard Memory tab |
| Agent executor | Queries structure and rationale in process without model calls |
| Memory Keeper | Adds inferred semantic edges with provenance tags on top of deterministic extraction |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall extract file, module, symbol, doc-concept, and rationale nodes with structural edges using only deterministic parsers and no LLM calls. |
| FR-2 | Must | The system shall rebuild incrementally by re-extracting only files whose SHA-256 fingerprints changed and pruning ownership of deleted files. |
| FR-3 | Must | The system shall expose an in-process query API with queryNodes, neighbors, and shortestPath that retains complete edge provenance. |
| FR-4 | Must | The system shall let Memory Keeper add inferred relates-to and rationale-supports edges that are always stamped with inferred provenance. |
| FR-5 | Must | The system shall extract FNXC rationale nodes from TypeScript parser comment ranges and markdown HTML comments outside fenced code. |
| FR-6 | Must | The system shall provide the `fn knowledge-graph build` CLI command and keep the regenerable artifact gitignored with rebuild documented. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Determinism | The system shall produce byte-identical artifacts for identical source on rebuild. |
| NFR-2 | Must | Maintainability | The system shall keep the roughly 85MB runtime artifact untracked so clones never carry compounding graph history. |
| NFR-3 | Must | Portability | The system shall parse TypeScript and TSX with a parser only and never require a type checker. |
| NFR-4 | Should | Reliability | The system shall write artifacts as sorted LF JSON with nodes and edges before the manifest so torn writes trigger full rebuild. |

## Constraints

- TypeScript and TSX are the only languages with symbol extraction.
- Relative import resolution covers lexical ts, tsx, and index candidates without package or alias resolution.
- Export star records a re-export relationship without expanding names.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [x] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Parser-only build over the repo
      Given a checkout of the Fusion source tree
      When the operator runs `fn knowledge-graph build --force`
      Then nodes and edges are produced with no model call and every edge carries extracted provenance
    ```

- [x] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Incremental rebuild after one file change
      Given a built graph with a recorded manifest
      When one source file changes and the build runs again
      Then only that file is re-extracted while unchanged files are reused from fingerprints
    ```

- [x] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Query API round trip
      Given a built graph artifact
      When a caller invokes queryNodes, neighbors, and shortestPath
      Then results return deterministic node and edge objects with source, owner, and provenance intact
    ```

- [x] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Inferred edges stay labeled
      Given the deterministic extracted graph
      When Memory Keeper writes semantic relationships
      Then every new edge is stamped inferred and model output can never appear as extracted
    ```

- [x] **FR-5**

    ```gherkin
    @FR-5
    Scenario: FNXC rationale extraction
      Given source and markdown files with stamped FNXC headers
      When the build runs
      Then each stamped header yields a rationale node linked by rationale-supports
    ```

- [x] **FR-6**

    ```gherkin
    @FR-6
    Scenario: CLI rebuild replaces the artifact
      Given a missing or stale .fusion-knowledge/graph directory
      When the operator runs `fn knowledge-graph build`
      Then nodes, edges, and manifest are regenerated without requiring a git pull of the artifact
    ```

- [x] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Rebuild stability
      Given identical source input
      When the build runs twice in a row
      Then the resulting artifact bytes are identical with no timestamps or host metadata
    ```

- [x] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Artifact stays untracked
      Given a fresh clone of the repository
      When the operator checks git status after a graph build
      Then .fusion-knowledge/graph remains ignored and no graph payload is staged
    ```

- [x] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: No checker dependency
      Given TypeScript sources with unresolvable imports
      When the build runs
      Then extraction completes best-effort without loading a type checker
    ```

- [x] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: Torn write recovery
      Given an interrupted build that wrote nodes but no manifest
      When the next build starts
      Then the incomplete artifact is discarded and a full rebuild runs
    ```

## Conflicts

None identified yet.

## Open Questions

1. Should the dashboard Memory tab ever trigger an automatic rebuild on missing artifacts instead of reporting a recoverable status.
2. Should symbol extraction expand beyond TypeScript and TSX to additional languages.
3. Should the deferred FR-29 and FR-34 bundle format be revived for capability-fabric integration.

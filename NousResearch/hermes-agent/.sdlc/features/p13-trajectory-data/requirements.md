---
title: "Trajectory and Data Generation"
status: done
---

# Requirements: Trajectory and Data Generation

## Overview

Hermes includes a research-ready data generation pipeline for producing training trajectories from agent runs. The system comprises batch_runner.py for parallel agent execution, trajectory_compressor.py for compressing tool-calling trajectories, mini_swe_runner.py for SWE-bench style evaluation, and datagen-config-examples/ for configuration templates. This enables researchers to generate training data for tool-calling models at scale.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| AI researchers | Generate training trajectories for tool-calling model fine-tuning |
| Evaluators | Run SWE-bench-style evaluations on the agent |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The batch runner shall execute multiple agent instances in parallel across a dataset |
| FR-2 | Must | The batch runner shall support checkpointing for resumable runs |
| FR-3 | Must | The trajectory compressor shall compress tool-calling agent trajectories |
| FR-4 | Must | The trajectory compressor shall support configurable compression strategies |
| FR-5 | Should | The mini SWE runner shall execute SWE-bench style evaluations |
| FR-6 | Should | The system shall provide configuration examples for common data generation setups |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | Batch runner shall scale to hundreds of parallel agent runs |
| NFR-2 | Should | Reliability | Checkpoint system shall survive process restarts |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a dataset of prompts
    - **When** batch_runner.py is invoked
    - **Then** agents run in parallel across the dataset and results are collected
- [ ] **FR-3**
    - **Given** a raw agent trajectory
    - **When** trajectory_compressor.py processes it
    - **Then** the compressed trajectory preserves essential tool-calling structure

## Conflicts

None identified yet.

## Open Questions

1. Should compressed trajectories support round-trip reconstruction?

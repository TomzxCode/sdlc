---
title: "Trajectory and Data Generation"
status: done
---

# Specification: Trajectory and Data Generation

## Architecture

```
Data Generation Pipeline
    │
    ├── Batch Runner (batch_runner.py)
    │   ├── Parallel agent execution
    │   ├── Checkpoint system
    │   └── Result collection
    │
    ├── Trajectory Compressor (trajectory_compressor.py)
    │   ├── Configurable compression levels
    │   ├── Tool-call structure preservation
    │   └── Token optimization
    │
    ├── SWE-bench Runner (mini_swe_runner.py)
    │   └── SWE-bench evaluation harness
    │
    └── Configuration (datagen-config-examples/)
        └── Example configs for common setups
```

## Data Models

### Batch Config

| Field | Type | Description |
|---|---|---|
| dataset_path | string | Path to input dataset |
| model | string | Model to use for runs |
| max_concurrent | int | Parallelism limit |
| checkpoint_path | string | Resume checkpoint location |
| output_format | string | JSON, JSONL, or Parquet |

### Compressed Trajectory

| Field | Type | Description |
|---|---|---|
| messages | array | Compressed message sequence |
| tool_calls | array | Extracted tool call data |
| metadata | object | Run config, duration, token counts |

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Compression | Tool-call-structure-aware | Preserves training-relevant structure while reducing token count |
| Checkpointing | Periodic state dump | Enables long-running batch jobs to survive crashes |
| Output format | JSONL | Standard for ML training pipelines |

## Risks and Unknowns

1. Batch runner with hundreds of parallel agents requires significant API budget
2. Trajectory compression quality varies by conversation length and complexity
3. SWE-bench evaluation requires code execution sandbox

## Out of Scope

- Training model weights from generated data
- Dataset hosting or distribution

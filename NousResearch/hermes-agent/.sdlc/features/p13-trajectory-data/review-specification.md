---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: specification.md

## Sync drift: 2026-11-16

- Architecture lists a "SWE-bench Runner (mini_swe_runner.py)" component, but no `mini_swe_runner.py` exists in the repository.
- Architecture lists a "Configuration (datagen-config-examples/)" component, but no `datagen-config-examples/` directory exists.
- Batch Config data model fields do not match `batch_runner.py`: the spec says `dataset_path` (code uses `dataset_file`), `max_concurrent` (code uses `num_workers`), and `checkpoint_path` (code derives `checkpoint_file` under `data/<run_name>/`, not configurable). The spec's `output_format` field ("JSON, JSONL, or Parquet") has no counterpart in the code, which always writes JSONL.
- Compressed Trajectory data model fields do not match `trajectory_compressor.py`: the spec says `messages`, `tool_calls`, and `metadata` (run config, duration, token counts), while the compressor emits `conversations` (from/value turns with embedded tool calls) plus an optional `compression_metrics` object.

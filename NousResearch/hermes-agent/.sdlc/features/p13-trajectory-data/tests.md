---
title: "Trajectory and Data Generation"
status: done
---

# Test Plan: Trajectory and Data Generation

## Scope

Tests covering batch runner, trajectory compression, and checkpointing functionality.

## Test Files

- tests/test_batch_runner_checkpoint.py — Batch runner checkpointing
- tests/run_agent/test_codex_app_server_compaction.py — Trajectory compression

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 (batch execution) | test_batch_runner_checkpoint.py |
| FR-2 (checkpointing) | test_batch_runner_checkpoint.py |

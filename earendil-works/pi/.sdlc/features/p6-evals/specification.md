---
title: "Evals"
status: done
---

# Specification: Evals

## Overview

`pi-evals` turns real Pi agent runs into behavioral evals.
A `pi-harness.ts` adapter exposes a real `AgentSession` to the `vitest-evals` harness, running it inside isolated temporary project and agent directories.
Core evals (smoke, extensions) plus harness-table, artifacts, and summary utilities support measuring and comparing workflow behavior.

## Architecture

```
npm run eval (scripts/run-evals.mjs)
        |
        v
+---------------------+
|  vitest-evals        |
|  (harness runner)    |
+----------+----------+
           | adapts a real AgentSession
           v
+---------------------+
|  src/pi-harness.ts  |
|  (isolated temp     |
|   project + agent)  |
+----------+----------+
           |
           v
+---------------------+
|  AgentSession       |
|  (real pi agent)    |
+---------------------+
```

`src/extensions.eval.ts` and `src/smoke.eval.ts` are core evals; `src/vitest-evals/` provides the harness primitives (harness-table, artifacts, summary).

## Data Models

### Eval artifact

| Field | Type | Constraints | Description |
|---|---|---|---|
| session | native pi session | attached | The AgentSession transcript/artifacts from the run |
| result | vitest-evals result | — | Harness verdict and observations |

## API Contracts

### `npm run eval [-- --provider <p> --model <m>]`

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| provider | string | yes* | Default provider (`*` unless every harness sets its own model) |
| model | string | yes* | Default model |

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| exit code | number | Vitest exit code for the eval run |

## Sequences

### Run an eval

```
npm run eval → run-evals.mjs → vitest-evals → pi-harness
→ create temp project + agent dirs → adapt AgentSession
→ run workflow → attach session artifacts → record result
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Harness | `vitest-evals` | Reuses Vitest runner, filtering, and reporting |
| Isolation | temp project + agent dirs per eval | No side effects on the real workspace |
| Model defaults | CLI args or `PI_PROVIDER`/`PI_MODEL` | CLI wins; harnesses may override per eval |
| Auth | normal `ModelRuntime` | Subscription + env API keys, no new secret handling |

## Risks and Unknowns

1. Model-backed evals are non-deterministic and cost tokens; thresholds need care.
2. Auth availability (subscription vs. API key) affects whether evals can run locally.

## Out of Scope

- The remote-session stack (protocol/client/server).
- SQLite session storage.
- The interactive coding agent itself (covered by other features).

---
title: "Evals"
status: done
---

# Specification: Evals

## Overview

`pi-evals` turns real Pi agent runs into behavioral evals.
A `harness.ts` adapter exposes a real `AgentSession` to the `vitest-evals` harness, running it inside isolated temporary project and agent directories.
Core evals (smoke, documentation-audit, `*.docs.eval.ts`) plus the docs-comparison runner (`cli.ts`, `docker.ts`, `plan.ts`, `report.ts`) and container images (`docker/`) support measuring and comparing workflow behavior.

## Architecture

```
npm run eval (root forwards to packages/evals: eval:host + eval:docs via src/cli.ts)
        |
        v
+---------------------+
|  vitest-evals        |
|  (harness runner;    |
|   host + docs       |
|   projects)          |
+----------+----------+
           | adapts a real AgentSession
           v
+---------------------+
|  src/harness.ts     |
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

`evals/smoke.eval.ts` and `evals/documentation-audit.eval.ts` are host evals; `evals/*.docs.eval.ts` are documentation-lift evals run as paired `(case, variant, run)` arms in containers. `src/cli.ts` orchestrates the comparison, `src/docker.ts` builds images and runs arms, `src/plan.ts` expands cases into tasks, `src/report.ts` pairs arms and computes lift, and `src/harness.ts` is the vitest-evals adapter. Unit tests live in `test/` (`harness`, `plan`, `report`, `comparison`, `configured-runtime`, `acme-server`).

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
npm run eval → packages/evals (eval:host via vitest.evals.config.ts host project; eval:docs via src/cli.ts) → vitest-evals → src/harness.ts
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

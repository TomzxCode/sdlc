---
title: "Insights: Project Learning Extraction"
status: done
---

# Specification: Insights: Project Learning Extraction

## Overview

The feature stores normalized insights in a project-scoped store, runs a model-assisted extraction over the project working memory, and tracks every extraction as a run with a status, a retry policy, and an ordered event trail.
The dashboard exposes the insights and the runs over HTTP, renders them in a category-grouped view, and lets the operator turn an insight into a board task.
The same store is reachable from the CLI tool surface so agents can read the insights a project has produced.

## Architecture

```
                       +-------------------------------------------+
                       |  Project working memory                  |
                       |  .fusion/memory/MEMORY.md                 |
                       +------------------+------------------------+
                                          |
                                          | readWorkingMemory
                                          v
+-------------+   POST /api/insights/run   +------------------+   prompt   +------------------+
|  Dashboard  | ------------------------> |  Insights route  | ---------> |  Model session   |
|  Insights   | <------------------------- |  insights-       | <-------- |  (read-only      |
|  view       |   run + insight records    |  routes.ts       |  insights |  tools)          |
+-------------+                            +--------+---------+            +------------------+
                                             |        |
                       list / read / update  |        |  run lifecycle
                       dismiss / archive     |        v
                       unarchive / delete    |  +---------------------+
                       create-task draft     |  | Insight run        |
                                             |  | executor           |
                                             |  | insight-run-       |
                                             |  | executor.ts        |
                                             |  +----------+----------+
                                             |             |
                                             |             |  store calls
                                             |             v
                                             |  +---------------------------+
                                             |  | Insight store            |
                                             |  | - SQLite InsightStore    |
                                             |  | - AsyncInsightStore (PG) |
                                             |  +-------------+-------------+
                                             |                |
                                             |                v
                                             |  +---------------------------+
                                             |  | project_insights         |
                                             |  | project_insight_runs     |
                                             |  | project_insight_run_     |
                                             |  |   events                 |
                                             |  +---------------------------+
                                             |
                                             |  mergeInsights
                                             |  writeInsightsMemory
                                             |                |
                                             |                v
                                             |  +---------------------------+
                                             |  | .fusion/memory/           |
                                             |  |   memory-insights.md      |
                                             |  +---------------------------+

  +---------------------------+        +---------------------------+
  | Insight run sweeper      |        | CLI agent session          |
  | insight-run-sweeper.ts   |        | fn_insight_list / _show    |
  | startup / periodic /     |        | fn_insight_run_list /_show |
  | drive-by sweep           |        +-------------+-------------+
  +-------------+-------------+                      |
                |                                    |
                +----------------------+-------------+
                                       |
                                       v
                            +---------------------------+
                            | Insight store             |
                            +---------------------------+

  Engine scheduler  --->  backlog pressure reporter
                        unlinked missions advisory reporter   ---->  Insight store
```

The dashboard reads and writes the insights through the HTTP router.
The router resolves the store once per request through the request-scoped store, so the same handler serves the SQLite-backed store and the PostgreSQL-backed store.
The run executor drives the run state machine and the sweeper recovers runs whose owner disappeared.

## Data Models

### Insight

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK, not null | Store-assigned identifier with the `INS-` prefix. Stable across upserts. |
| projectId | string | not null | Project the insight belongs to. |
| title | string | not null | Short summary, derived from the extracted content and truncated to one hundred characters. |
| content | string | nullable | Full body of the insight. Nullable for a title-only insight. |
| category | enum | not null | One of fifteen insight categories. |
| status | enum | not null | One of generated, confirmed, stale, dismissed, archived. |
| fingerprint | string | not null | Deterministic dedupe key derived from the normalized title and category. |
| provenance | object | nullable | Trigger, description, related entity ids, token estimate, and free-form metadata. |
| lastRunId | string | nullable | Id of the most recent run that produced or updated the insight. |
| createdAt | string | not null | ISO-8601 creation timestamp, preserved on upsert. |
| updatedAt | string | not null | ISO-8601 timestamp of the last change. |

### InsightRun

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK, not null | Store-assigned identifier with the `INSR-` prefix. |
| projectId | string | not null | Project the run belongs to. |
| trigger | enum | not null | One of schedule, manual, task completion, merge event, api. |
| status | enum | not null | One of pending, running, completed, failed, cancelled. Terminal states are immutable. |
| summary | string | nullable | Human-readable outcome written on completion. |
| error | string | nullable | Error message written on failure or cancellation. |
| insightsCreated | integer | not null, default 0 | Insights inserted by the run. |
| insightsUpdated | integer | not null, default 0 | Existing insights updated by the run. |
| inputMetadata | object | nullable | Snapshot of what was analyzed, including the model provider, model id, and reasoning effort. |
| outputMetadata | object | nullable | Snapshot of what was produced, including insight ids and token counts. |
| lifecycle | object | nullable | Terminal reason and cause, failure class, retryable flag, attempt and max attempts, and the retry and root run links. |
| createdAt | string | not null | ISO-8601 timestamp of run creation. |
| startedAt | string | nullable | ISO-8601 timestamp of the first attempt. |
| completedAt | string | nullable | ISO-8601 timestamp of the terminal transition, set automatically. |
| cancelledAt | string | nullable | ISO-8601 timestamp of cancellation, set automatically. |

### InsightRunEvent

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | PK, not null | Store-assigned identifier with the `INSEVT-` prefix. |
| runId | string | FK to run, not null, cascade delete | Run the event belongs to. |
| seq | integer | not null | Per-run sequence number, allocated as the current maximum plus one. |
| type | enum | not null | One of status changed, retry scheduled, cancel requested, timeout, info, warning, error. |
| message | string | not null | Human-readable event text. |
| status | enum | nullable | Run status at the time of the event. |
| classification | enum | nullable | One of cancelled, timed out, retryable transient, non-retryable. |
| metadata | object | nullable | Free-form event metadata, including the recovery marker and source. |
| createdAt | string | not null | ISO-8601 timestamp of the event. |

### Memory artifacts

| Path | Format | Description |
|---|---|---|
| `.fusion/memory/MEMORY.md` | Markdown | Working memory read as the extraction input. |
| `.fusion/memory/memory-insights.md` | Markdown | Insights memory merged with every extraction result. |

## API Contracts

The normative contract is in [`api.yaml`](api.yaml) (OpenAPI 3.1), written alongside this document.
The table below is a summary; request and response schemas, error response bodies, and status codes are in `api.yaml`.

| Method | Path | Purpose |
|---|---|---|
| GET | /api/insights | List insights with optional category, status, run, and pagination filters. |
| POST | /api/insights/run | Trigger an extraction run and execute it. |
| GET | /api/insights/runs | List runs with optional status, trigger, and pagination filters. |
| GET | /api/insights/runs/:id | Read one run. |
| GET | /api/insights/runs/:id/events | List the event trail of one run. |
| POST | /api/insights/runs/:id/cancel | Cancel a pending or running run. |
| POST | /api/insights/runs/:id/retry | Retry a failed run whose failure class is retryable transient. |
| GET | /api/insights/:id | Read one insight. |
| PATCH | /api/insights/:id | Update the title, body, category, or status of one insight. |
| DELETE | /api/insights/:id | Delete one insight. |
| POST | /api/insights/:id/dismiss | Move one insight to the dismissed state. |
| POST | /api/insights/:id/archive | Move one insight to the archived state. |
| POST | /api/insights/:id/unarchive | Move one archived insight back to the confirmed state. |
| POST | /api/insights/:id/create-task | Return a task payload draft built from one insight. |

Error codes shared across endpoints:

| Status | Code | Description |
|---|---|---|
| 400 | INVALID_INPUT | A filter, pagination value, trigger, or reasoning effort is not accepted. |
| 404 | NOT_FOUND | The requested insight or run does not exist. |
| 409 | ACTIVE_RUN_CONFLICT | A run for the same project and trigger is already active. The details carry the active run id and status. |
| 409 | RUN_TERMINAL | The run already reached a terminal state and cannot be cancelled. |
| 409 | RUN_NOT_RETRYABLE | The run is not failed, or its failure class is not retryable transient. |
| 500 | INTERNAL_ERROR | The store could not be resolved or the request failed unexpectedly. |

## Sequences

### Manual extraction run

```
Client            Route             Executor           Store             Model
  |                  |                  |                 |                 |
  |-- POST /run ---->|                  |                 |                 |
  |                  |-- find active --->|                 |                 |
  |                  |<-- none ---------|                 |                 |
  |                  |-- create run ---->|-- insert ------>|                 |
  |                  |                  |<-- pending -----|                 |
  |                  |<-- run id -------|                 |                 |
  |                  |                  |-- set running -->|                 |
  |                  |                  |-- read memory ->|                 |
  |                  |                  |                 |-- prompt ----->|
  |                  |                  |                 |<-- json -------|
  |                  |                  |-- parse + merge ->|                 |
  |                  |                  |-- upsert ------->|                 |
  |                  |                  |-- set completed ->|                |
  |                  |<-- 201 run -------|                 |                 |
  |<-- 201 run -------|                  |                 |                 |
```

### Orphan recovery sweep

```
Sweeper           Store              Events             Run
  |                  |                 |                 |
  |-- list stale ---->|                 |                 |
  |<-- pending/running rows            |                 |
  |                  |                 |                 |
  |-- append warning ->|-------------->|                 |
  |                  |                 |                 |
  |-- set failed ---->|                 |                 |
  |                  |--- update ----->|----------------->|
  |                  |                 |                 |
  |-- append status_changed ->|-------->|                 |
  |                  |                 |                 |
```

The sweeper skips a run whose id is registered in the live controller map.
A run inside the grace window is skipped.
A recovered run is marked failed with a non-retryable cause and the recovery source recorded in the event metadata.

### Insight to board task

```
Operator          View              Route              Store            Board
  |                  |                 |                  |                 |
  |--- create task -->|                 |                  |                 |
  |                  |-- draft ----->|                  |                 |
  |                  |               |-- get insight --->|                 |
  |                  |               |<-- insight -------|                 |
  |                  |               |-- archive ------>|                 |
  |                  |<-- draft -----|                  |                 |
  |                  |-- createTask -------------------------->|          |
  |                  |<-- task id ---------------------------------------->|
```

The draft endpoint does not create a task.
The view archives the insight and then creates the task through the normal intake path, which resolves the landing column from the selected or project-default workflow.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Dedupe key | Hash of the normalized title and category | Keeps a repeated observation on one row without needing an embedding store. |
| Upsert behavior | Update the matching row and keep the original id and creation timestamp | Preserves the identity an operator already acted on. |
| Run immutability | Terminal runs reject every field write | A completed or failed run is an audit record, not a scratch pad. |
| Event trail | Append-only rows with a per-run sequence number | Lets an operator rebuild a run's history without parsing log output. |
| Run execution | Synchronous inside the request with a per-attempt timeout | The dashboard shows a finished run immediately and the request is bounded. |
| Failure classification | Regex on the error message split into four classes | Keeps the executor free of provider-specific error handling while still separating transient from permanent failures. |
| Cancellation | An abort controller registered per run id | The sweeper can tell a live run from an orphan, and cancellation reaches the model call. |
| Orphan recovery | Startup sweep, five-minute interval, and a sweep before listing runs | Covers a crash, a slow run, and a stale row regardless of when it appeared. |
| Backend portability | One method surface over SQLite and PostgreSQL stores | The dashboard, the CLI, and the engine all call the same names. |
| Presentation order | Reversed in the dashboard hook, not in the store | The store keeps ascending order for stable pagination and dedupe. |
| Model selection | Stored in the run input metadata | A retry must reproduce the original provider and reasoning effort without new schema columns. |
| Extraction tool scope | Read-only tools for the extraction session | An extraction reads the project, it never changes the project. |
| Task creation | The endpoint returns a draft and the view creates the task | Task creation follows the normal intake path, including duplicate checks and the workflow landing column. |

## Risks and Unknowns

1. The route validates insight categories against eleven values while the type, the CLI, and the dashboard use fifteen, so four categories cannot be filtered or set over HTTP.
2. The fingerprint is a 32-bit hash, so two different titles in the same category can collide and merge two distinct insights.
3. The extraction runs inside the HTTP request, so a proxy or client timeout can cut the request while the run continues in the store.
4. The run event metadata carries the raw error message, so provider error text can reach the event trail.
5. The dashboard caches the insight list in browser storage, so a stale cache can show insights that were dismissed on another surface.
6. The insight body is written to the insights memory file as well as to the store, so the two copies can drift when one write fails.
7. The run trigger list offers schedule, task completion, and merge event, and the route accepts all of them, but no scheduler, task completion hook, or merge hook starts a run today, so the manual trigger is the one in use.
8. The engine publishes workflow insights such as backlog health and unlinked-mission advisories into the same store, so those rows share the extraction lifecycle even though no extraction produced them.

## Out of Scope

- Scheduled memory insight extraction and working memory pruning, which the memory subsystem owns.
- The task recommendations section of the insights view, which aggregates follow-up suggestions from completed tasks.
- The backlog pressure reporter and the unlinked missions advisory reporter, which publish into the store but define their own content.
- Cross-project insight queries, insight sharing between projects, and insight export.
- Embedding-based or semantic similarity dedupe.
- The run list and run detail surfaces of the CLI, beyond the read-only tools they call.

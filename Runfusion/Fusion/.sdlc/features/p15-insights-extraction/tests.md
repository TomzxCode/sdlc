---
title: "Insights: Project Learning Extraction"
status: done
---

# Test Plan: Insights: Project Learning Extraction

## Scope

This plan covers the insight store contract, the run executor and its retry classification, the run event trail, the orphan sweeper, the HTTP surface of the insights router, the dashboard insights view and its hook, the model and reasoning-effort selection, and the CLI insight tools.

Out of scope are the scheduled memory extraction automation and the working memory pruning, which the memory subsystem owns and which `packages/core/src/__tests__/memory-insights.test.ts` covers, and the content of the workflow insights published by the engine reporters.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Store resolution in PostgreSQL backend mode | `packages/core/src/__tests__/postgres/insight-store.pg.test.ts` | The store resolves without throwing and returns the async store. |
| TC-2 | Fingerprint dedupe on upsert | `packages/core/src/__tests__/postgres/insight-store.pg.test.ts` | A repeated fingerprint keeps the original id and creation timestamp and holds the new content. |
| TC-3 | Count agrees with the filtered list | `packages/core/src/__tests__/postgres/insight-store.pg.test.ts` | The count matches the number of listed insights for the same filter. |
| TC-4 | Terminal run immutability | `packages/core/src/__tests__/postgres/insight-store.pg.test.ts` | Updating a completed run throws the terminal immutability error. |
| TC-5 | Invalid run status transition | `packages/core/src/__tests__/postgres/insight-store.pg.test.ts` | A transition the run state machine forbids throws the invalid transition error. |
| TC-6 | Recall capture at the store factory | `packages/core/src/__tests__/postgres/insight-store.pg.test.ts` | A new insight writes a recall record through the live recall writer. |
| TC-7 | Run creation, event sequencing, and completion | `packages/core/src/__tests__/postgres/insight-store.pg.test.ts` | Events come back in sequence order and the terminal update sets the completion timestamp. |
| TC-8 | Full run lifecycle against the async store | `packages/core/src/__tests__/postgres/insight-run-execution.pg.test.ts` | A run moves from pending to running to completed with the summary and the insight counts. |
| TC-9 | Failed attempt against the async store | `packages/core/src/__tests__/postgres/insight-run-execution.pg.test.ts` | A thrown attempt leaves a failed run with the error text. |
| TC-10 | Retry of a retryable transient failure | `packages/core/src/__tests__/postgres/insight-run-execution.pg.test.ts` | The retry runs a new attempt that reaches completion. |
| TC-11 | Insight grouping by category | `packages/dashboard/app/hooks/__tests__/useInsights.test.ts` | Insights land in the section of their category and empty sections carry no item. |
| TC-12 | Newest-first presentation order | `packages/dashboard/app/hooks/__tests__/useInsights.test.ts` | The list is ordered newest first and equal timestamps break by descending id, with malformed timestamps last. |
| TC-13 | Dismissed insights are filtered out | `packages/dashboard/app/hooks/__tests__/useInsights.test.ts` | Insights with the dismissed status are not shown. |
| TC-14 | Cached insight hydration | `packages/dashboard/app/hooks/__tests__/useInsights.test.ts` | Cached insights render without a loading state and the cache is capped at five hundred entries and isolated per project. |
| TC-15 | Manual run trigger and refresh | `packages/dashboard/app/hooks/__tests__/useInsights.test.ts` | A completed run triggers a refresh and the latest run is shown. |
| TC-16 | Active run conflict handling | `packages/dashboard/app/hooks/__tests__/useInsights.test.ts` | A conflict response hydrates the active run and raises a friendly error, and the in-flight state is always cleared. |
| TC-17 | Dismiss, archive, and unarchive actions | `packages/dashboard/app/hooks/__tests__/useInsights.test.ts` | Each action updates the local record and a failure records the error. |
| TC-18 | Model and reasoning-effort selection | `packages/dashboard/app/__tests__/insight-model-selector.test.tsx` | The selection persists in browser storage, restores on mount, shows an indicator, and is forwarded when a run starts. |
| TC-19 | Category sections and status badges | `packages/dashboard/app/components/__tests__/InsightsView.test.tsx` | The populated sections render with the expected order and each insight carries the status badge of its status. |
| TC-20 | View action wiring | `packages/dashboard/app/components/__tests__/InsightsView.test.tsx` | The dismiss and create-task actions fire, the run button is disabled while a run is in flight, and failures show an inline error without a success toast. |
| TC-21 | View states | `packages/dashboard/app/components/__tests__/InsightsView.test.tsx` | The loading, top-level error, run-level error, and global empty states each render. |
| TC-22 | Backlog health filter and archived insights | `packages/dashboard/app/components/__tests__/InsightsView.test.tsx` | The backlog health toggle filters the list and archived insights render with the archived class and an unarchive button. |
| TC-23 | View layout tiers | `packages/dashboard/app/components/__tests__/InsightsView.test.tsx` | The header action cluster keeps the title and controls on desktop, stacks the title on mobile, and reflows on tablet. |
| TC-24 | CLI insight tools | `packages/cli/src/__tests__/extension-insights.test.ts` | The four insight tools register, list and show insights and runs, and report invalid pagination and missing ids. |
| TC-25 | Extraction MCP forwarding | `packages/dashboard/src/__tests__/mcp-helper-forwarding.test.ts` | A manual run forwards the scoped MCP server set to a read-only session and answers with a created status. |
| TC-26 | Memory extraction helpers | `packages/core/src/__tests__/memory-insights.test.ts` | The prompt includes the working memory and the existing insights, the response parser accepts fenced and prefixed JSON, the merge skips duplicates, and the trigger honors the time and growth thresholds. |
| TC-27 | Engine workflow insight publishers | `packages/engine/src/__tests__/backlog-pressure-reporter.test.ts` and `packages/engine/src/__tests__/unlinked-missions-advisory-reporter.test.ts` | Each reporter upserts one deduplicated workflow insight and falls back to a log entry when the insight store is unavailable. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-28 | Route mounting and lazy view registration | `packages/dashboard/src/routes/register-integrated-routers.ts` and `packages/dashboard/app/__tests__/lazy-loaded-views-docs.test.ts` | The insights router is mounted at `/api/insights` and the insights view stays a lazy-loaded chunk listed in the documentation inventory. |
| TC-29 | Dashboard guide coverage | `packages/dashboard/src/__tests__/dashboard-guide.test.ts` | The Insights View section is present in the dashboard guide. |
| TC-30 | Run execution against the async store | `packages/core/src/__tests__/postgres/insight-run-execution.pg.test.ts` | A create, run, and complete cycle persists through the store with ordered status and info events. |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-31 | Manual extraction through the HTTP surface | Start the dashboard against a project with working memory, then call `POST /api/insights/run` | The run completes, the insights are listed by `GET /api/insights`, and the run events are listed by `GET /api/insights/runs/{id}/events`. |
| TC-32 | Insight to board task | Select an insight in the dashboard view and use the create-task action | The insight is archived, a task payload draft is returned, and the task is created through the normal intake path. |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-33 | Model returns output that is not JSON | The extraction fails, the run is recorded as failed, and the insights memory file keeps its prior content. |
| TC-34 | A run is still active when a new run is requested | The request is answered with a conflict status that names the active run, and no second run row is created. |
| TC-35 | A run has no live owner after the grace window | The sweep marks the run failed with a non-retryable cause and appends a warning event and a status event. |
| TC-36 | A run is cancelled while it is pending | The run moves to cancelled with a cancellation timestamp and no execution is started. |
| TC-37 | A failed run is not classified as retryable transient | The retry request is answered with a conflict status and no new run is created. |
| TC-38 | An unknown insight or run id is requested | The request is answered with a not found status. |
| TC-39 | A bad pagination or filter value is sent | The request is answered with a bad request status. |
| TC-40 | The insight store cannot be resolved | The request is answered with an internal error status. |
| TC-41 | Two insights in one category produce the same fingerprint | The second upsert updates the first row instead of inserting a second one. |

## Test Infrastructure

- The shared embedded PostgreSQL harness from `packages/core/src/__test-utils__/pg-test-harness.ts`, which provides a project-scoped store for the store and executor tests.
- A stubbed `executeAttempt` callback for the run executor tests, so no model provider is called.
- An Express app with a fake task store for the router tests, with the core memory helpers spied on.
- A mocked `useInsights` hook and a mocked `useTaskRecommendations` hook for the view tests, plus a CSS fixture loader for the layout tier tests.
- A mocked dashboard API module for the hook tests, including a fake `ApiRequestError` that carries a status and a details object.
- Browser storage stubs for the model and reasoning-effort persistence tests.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-2, TC-7, TC-11 |
| FR-2 | TC-19, TC-24 |
| FR-3 | TC-17, TC-22 |
| FR-4 | TC-2, TC-41, TC-26 |
| FR-5 | TC-7, TC-8 |
| FR-6 | TC-4, TC-5 |
| FR-7 | TC-7, TC-10, TC-30 |
| FR-8 | TC-25, TC-26, TC-31 |
| FR-9 | TC-9, TC-10, TC-33 |
| FR-10 | TC-16, TC-34 |
| FR-11 | TC-36 |
| FR-12 | TC-10, TC-18 |
| FR-13 | TC-35 |
| FR-14 | TC-19, TC-38, TC-39 |
| FR-15 | TC-24, TC-30, TC-31 |
| FR-16 | TC-20, TC-32 |
| FR-17 | TC-19, TC-20, TC-21, TC-22, TC-23 |
| FR-18 | TC-15, TC-18 |
| FR-19 | TC-12 |
| FR-20 | TC-24, TC-39 |
| FR-21 | TC-24 |
| FR-22 | TC-34, TC-35 |
| NFR-1 | TC-35 |
| NFR-2 | TC-33, TC-36 |
| NFR-3 | TC-2, TC-41 |
| NFR-4 | TC-34 |
| NFR-5 | TC-7, TC-30, TC-35 |
| NFR-6 | TC-35 |
| NFR-7 | TC-18 |
| NFR-8 | TC-1, TC-8, TC-30 |
| NFR-9 | TC-25 |
| NFR-10 | TC-14 |

## Key Test Files

- `packages/core/src/__tests__/postgres/insight-store.pg.test.ts`
- `packages/core/src/__tests__/postgres/insight-run-execution.pg.test.ts`
- `packages/dashboard/app/hooks/__tests__/useInsights.test.ts`
- `packages/dashboard/app/components/__tests__/InsightsView.test.tsx`
- `packages/dashboard/app/__tests__/insight-model-selector.test.tsx`
- `packages/dashboard/src/__tests__/mcp-helper-forwarding.test.ts`
- `packages/cli/src/__tests__/extension-insights.test.ts`
- `packages/core/src/__tests__/memory-insights.test.ts`
- `packages/engine/src/__tests__/backlog-pressure-reporter.test.ts`
- `packages/engine/src/__tests__/unlinked-missions-advisory-reporter.test.ts`
- `packages/dashboard/app/__tests__/lazy-loaded-views-docs.test.ts`
- `packages/dashboard/src/__tests__/dashboard-guide.test.ts`

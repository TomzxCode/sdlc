---
title: "Company/task search"
status: done
---

# Requirements: Company/task search

## Overview

Operators and agents need one company-scoped search that finds tasks and their surrounding context (comments, documents, artifacts, agents, projects) with relevance-ranked results, focused extract output for machines, and a full Search UI page for navigation.
This feature documents already-implemented functionality grounded in `server/src/services/company-search.ts`, `server/src/services/company-search-extract.ts`, `server/src/services/company-search-rate-limit.ts`, `server/src/services/task-search.ts`, `GET /companies/:companyId/search` and `/search/extract` in `server/src/routes/issues.ts`, `ui/src/pages/Search.tsx`, and OpenAPI entries in `server/src/routes/openapi.ts`.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Board operator | Find tasks, comments, documents, artifacts, agents, and projects from one Search page with filters, scopes, and sorts |
| Agent | Query company search and extract endpoints for task discovery and focused context snippets within its company |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide company-scoped cross-entity search across issues, comments, documents, artifacts, agents, and projects with company access checks. |
| FR-2 | Must | The system shall provide an extract endpoint that returns focused per-issue context matches with excerpts and source references. |
| FR-3 | Must | The system shall enforce per-company per-actor rate limiting on search and extract endpoints. |
| FR-4 | Must | The system shall rank task results by relevance and quality using disjoint score bands with identifier, phrase, coverage, and fuzzy handling. |
| FR-5 | Must | The system shall provide a Search UI page with result navigation to tasks and their evidence anchors. |
| FR-6 | Should | The system shall support faceted issue filters with option counts and zero-result loosen suggestions. |
| FR-7 | Should | The system shall support result scopes, sort orders, and limit/offset pagination with a has-more signal. |
| FR-8 | Should | The system shall surface Search UI states for loading, errors with retry, no-results recovery, debounced input, recent searches, and filter/sort controls. |
| FR-9 | May | The system shall return markdown-aware snippets with highlight ranges and preview images where available. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | All search and extract operations shall enforce company scoping, actor authorization boundaries, and issue visibility rules. |
| NFR-2 | Must | Performance | Issue-side search shall compute ranked pages and aggregates efficiently using shared CTEs, page-window snippet enrichment, and trigram-backed matching. |
| NFR-3 | Should | Availability | Rate limiting shall cap search demand per actor key per window and fail with retry metadata before invoking search. |

## Constraints

- Search never crosses company boundaries.
- Extract `contains` has a minimum length and rejects regex input (literal and URL kinds only).
- Query text is truncated to `COMPANY_SEARCH_MAX_QUERY_LENGTH` and tokens to `COMPANY_SEARCH_MAX_TOKENS`.
- Pagination is bounded by `COMPANY_SEARCH_MAX_LIMIT` and `COMPANY_SEARCH_MAX_OFFSET`.
- Deleted comments are excluded from search and extract evidence.

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Company-scoped cross-entity search
      Given a company with issues, comments, documents, artifacts, agents, and projects
      When an authorized actor searches within that company
      Then results contain only that company's visible rows with type counts per entity
    ```

    ```gherkin
    @FR-1
    Scenario: Cross-company access denied
      Given an actor without access to company B
      When they request company B search or extract
      Then the API denies access before invoking the service
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Extract focused matches
      Given issues with matching titles, comments, or documents
      When a client calls the extract endpoint with a contains string, kind, and scope
      Then each issue returns deduplicated matches with excerpts, truncation flags, and comment or document source references
    ```

    ```gherkin
    @FR-2
    Scenario: Extract URL kind
      Given comments containing URLs
      When a client extracts with kind url
      Then URL occurrences are expanded, deduplicated, and scheme-less queries still select URL sources
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Rate limit enforced
      Given an actor exceeding the per-window request budget
      When they call search or extract again
      Then the API returns 429 with Retry-After and rate-limit headers without invoking search
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Identifier outranks weak title matches
      Given a task with an exact identifier and another with a weak title resemblance
      When searching by the identifier
      Then the exact identifier result ranks first
    ```

    ```gherkin
    @FR-4
    Scenario: Aggregate relevance gates hold
      Given the task-search corpus and quality cases
      When full and quick engines are evaluated
      Then mean reciprocal rank meets 0.95 and NDCG@5 meets 0.90
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Navigate from results to evidence
      Given search results with comment or document evidence
      When the operator opens a context result
      Then the link targets the exact comment or document anchor on the issue
    ```

    ```gherkin
    @FR-5
    Scenario: Exact identifier auto-redirects
      Given an exact identifier match in the results
      When the Search page resolves it
      Then it redirects to the issue root without a deep-link suffix
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Filtered search with facets
      Given active status, priority, assignee, project, label, or updated-window filters
      When searching
      Then only matching issues are returned with per-option facet counts
    ```

    ```gherkin
    @FR-6
    Scenario: Zero-result recovery
      Given filters that empty the result page
      When the response contains zeroResults
      Then it reports the unfiltered total and per-filter loosen suggestions ordered by additional results
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Scope, sort, and paginate
      Given a scope, sort order, limit, and offset
      When searching
      Then the response echoes scope and sort, pages merged cross-type results, and reports hasMore
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Search UI states
      Given a slow, failing, or empty search
      When the operator uses the Search page
      Then loading, error-with-retry, and no-results states render with recovery actions
    ```

    ```gherkin
    @FR-8
    Scenario: Debounced input with operator filters
      Given typed text with operator tokens and filter chips
      When the operator edits or removes a token or chip
      Then the request dispatches after the debounce window with updated filters in the URL and query
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Snippet highlights and previews
      Given a result with markdown content or images
      When snippets are built
      Then snippet text is markdown-stripped with highlight ranges and a preview image URL when present
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Hidden and foreign rows excluded
      Given hidden issues and another company's data
      When searching or extracting
      Then hidden and foreign rows are excluded from results and counts
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Efficient issue aggregation
      Given many matching issues
      When searching
      Then one statement computes the ranked page plus type, facet, and total aggregates with snippet enrichment limited to the page window
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Rate-limit headers present
      Given any search or extract call
      When the response is returned
      Then X-RateLimit-Limit and X-RateLimit-Remaining headers are set with Retry-After on 429
    ```

## Conflicts

None identified yet.

## Open Questions

1. Is the absence of a goals entity scope in company search intentional, or should goals become a searchable entity later?

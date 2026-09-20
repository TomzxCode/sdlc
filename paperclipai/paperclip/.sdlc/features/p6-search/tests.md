---
title: "Company/task search"
status: done
---

# Test Plan: Company/task search

## Scope

Tests cover search query validation, ranked cross-entity retrieval, extract matching, route rate limiting and access checks, relevance and quality gates, query-intent parsing, and the Search UI page.
Out of scope: goals entity search (not implemented), cross-instance rate-limit coordination, and release smoke coverage.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Search query validation truncates long text and rejects invalid filters, sort, and pagination | Overlong `q` plus invalid limit, offset, scope, status, priority, sort, updatedWithin, projectId | Truncated valid parse; throws on each invalid field (`server/src/__tests__/company-search-service.test.ts:37`) |
| TC-2 | Per-branch fetch window includes offset up to the branch cap | Limit 50 with offsets 0 and 200 | 51 and `COMPANY_SEARCH_BRANCH_FETCH_LIMIT` (`server/src/__tests__/company-search-service.test.ts:64`) |
| TC-3 | Extract query validation accepts supported filters and rejects unsafe or ambiguous input | URL contains with kind, scope, status, limits; then regex kind, short contains, over-limit, and conflicting update filters | Accepted parse with capped matchesPerIssue; throws on regex, short, over-limit, and conflicting inputs (`server/src/__tests__/company-search-extract-service.test.ts:32`) |
| TC-4 | Query intent keeps negation, short domain terms, and quoted filler | Task-search intent strings | Filler dropped only in multi-term unquoted queries (`server/src/__tests__/task-search-query.test.ts:5`) |
| TC-5 | Query intent retains strictest intent for repeated terms | Repeated terms with mixed quoting | Strictest (quoted) intent wins (`server/src/__tests__/task-search-query.test.ts:10`) |
| TC-6 | Query intent normalizes identifiers without guessing numbers | Identifier-like strings | Normalized `letters-digits` form (`server/src/__tests__/task-search-query.test.ts:14`) |
| TC-7 | URL building writes q and scope, clears empty q and all scope, and preserves path plus hash | Search URL inputs | Correct params with preserved pathname and hash (`ui/src/pages/Search.test.tsx:143`, `:149`, `:153`) |

Files: `server/src/__tests__/company-search-service.test.ts`, `server/src/__tests__/company-search-extract-service.test.ts`, `server/src/__tests__/task-search-query.test.ts`, `ui/src/pages/Search.test.tsx`.

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-8 | Exact entity names outrank speculative typos and empty quotes return nothing | Seeded issues, agents, and projects | Exact names first; `""` yields no rows (`server/src/__tests__/company-search-service.test.ts:166`) |
| TC-9 | Exact issue identifiers rank before weaker title matches | Seeded identifier and title rows | Identifier row first (`server/src/__tests__/company-search-service.test.ts:179`) |
| TC-10 | Phrase outranks reordered title words and partial matches are rejected | Seeded phrase and reordered rows | Phrase first; partial unmatched (`server/src/__tests__/company-search-service.test.ts:196`) |
| TC-11 | Multi-token thread matches return comment snippets | Issue with matching comments | Same-issue match with comment snippet (`server/src/__tests__/company-search-service.test.ts:221`) |
| TC-12 | Document search returns document metadata for snippets | Issue with linked matching document | Document snippet with title, key, and anchor data (`server/src/__tests__/company-search-service.test.ts:247`) |
| TC-13 | Artifact scope searches artifact projections | Seeded document, work-product, and attachment artifacts | Artifact rows in artifacts scope (`server/src/__tests__/company-search-service.test.ts:280`) |
| TC-14 | High-offset fetch windows are not passed to artifact query validation | High offset search | Artifact listing still succeeds (`server/src/__tests__/company-search-service.test.ts:319`) |
| TC-15 | Issue filters apply before sorting and pagination | Seeded filtered issues | Filtered, sorted, paged rows (`server/src/__tests__/company-search-service.test.ts:333`) |
| TC-16 | Filter-only searches return issue rows | Filters without search text | Issue rows without requiring `q` (`server/src/__tests__/company-search-service.test.ts:394`) |
| TC-17 | Zero-result filters return loosen data and suppress agent/project rows | Filters emptying the page | zeroResults with suggestions; no agent or project rows (`server/src/__tests__/company-search-service.test.ts:425`) |
| TC-18 | Hidden issue-backed artifacts are not leaked | Hidden issues with artifacts | Artifacts excluded (`server/src/__tests__/company-search-service.test.ts:443`) |
| TC-19 | Hidden issues and other companies' data are excluded | Hidden and foreign rows | Only visible same-company rows (`server/src/__tests__/company-search-service.test.ts:486`) |
| TC-20 | Bare SQL wildcards are treated as literals | Queries with `%`, `_`, `\` | Literal matching, no match-all (`server/src/__tests__/company-search-service.test.ts:513`) |
| TC-21 | Percent characters match literally across entities | Rows containing `%` | Literal percent matches in issues, comments, documents, agents, projects (`server/src/__tests__/company-search-service.test.ts:555`) |
| TC-22 | Offset applies after merged cross-type ranking | Mixed entity rows | Correct offset window (`server/src/__tests__/company-search-service.test.ts:659`) |
| TC-23 | Underscore and backslash escaping in phrase and token patterns | Special-character queries | Escaped patterns match literally (`server/src/__tests__/company-search-service.test.ts:680`) |
| TC-24 | Short UI terms do not match inside unrelated words | Short terms | Word-boundary matching only (`server/src/__tests__/company-search-service.test.ts:699`) |
| TC-25 | Typo fallback stays inside requested filters | Filtered fuzzy query | Fuzzy rows respect filters (`server/src/__tests__/company-search-service.test.ts:707`) |
| TC-26 | Exact title hits stay on the task with best context evidence | Title plus context rows | Exact task first with most complete evidence (`server/src/__tests__/company-search-service.test.ts:715`) |
| TC-27 | Edits, deleted comments, and document updates reflect immediately | Mutated rows | Fresh results without stale evidence (`server/src/__tests__/company-search-service.test.ts:756`) |
| TC-28 | Conservative fuzzy title matches use pg_trgm | Typo queries | Near titles matched (`server/src/__tests__/company-search-service.test.ts:776`) |
| TC-29 | Transposition typos match multi-word titles | Transposed queries | Multi-word titles matched (`server/src/__tests__/company-search-service.test.ts:789`) |
| TC-30 | Extract expands and deduplicates URLs across sources | Issues, comments, documents with URLs | Deduplicated URL matches (`server/src/__tests__/company-search-extract-service.test.ts:109`) |
| TC-31 | Scheme-less queries keep URL sources selected | Scheme-less contains | URL sources still selected (`server/src/__tests__/company-search-extract-service.test.ts:152`) |
| TC-32 | Extract filters by update window and status | Status and update filters | Only matching issues (`server/src/__tests__/company-search-extract-service.test.ts:190`) |
| TC-33 | Extract default distinct-match cap marks truncation explicitly | Many matches | Capped matches with truncation flags (`server/src/__tests__/company-search-extract-service.test.ts:221`) |
| TC-34 | Bounded per-issue match cap supports machine extraction | High matchesPerIssue | Complete bounded extraction (`server/src/__tests__/company-search-extract-service.test.ts:240`) |
| TC-35 | Extract does not return another company's issues | Foreign company rows | Empty same-company result (`server/src/__tests__/company-search-extract-service.test.ts:260`) |
| TC-36 | Relevance cases pass per-query first-result, absence, and grade gates | Task-search corpus | First, absent, and grade-3 top-5 assertions (`server/src/__tests__/task-search-quality.test.ts:68`) |
| TC-37 | Aggregate relevance gates hold for both engines | Full and quick engine reports | MRR at least 0.95 and NDCG@5 at least 0.90 (`server/src/__tests__/task-search-quality.test.ts:83`) |
| TC-38 | Empty quotes, punctuation, and oversized words do not error | Edge queries | Empty or safe results (`server/src/__tests__/task-search-quality.test.ts:93`) |
| TC-39 | Repeated same-actor search is rejected before invoking search | Rate limiter with max 1 | Second call 429 with retry metadata; service called once (`server/src/__tests__/company-search-rate-limit-routes.test.ts:33`) |
| TC-40 | assigneeUserId=me resolves for board actors before search | Board actor with userId | Service receives resolved user id (`server/src/__tests__/company-search-rate-limit-routes.test.ts:65`) |
| TC-41 | Invalid filter and sort params are rejected before search | Invalid query params | 400 without service call (`server/src/__tests__/company-search-rate-limit-routes.test.ts:93`) |
| TC-42 | Extract route parses query and invokes the service | Valid extract query | Service called with parsed fields (`server/src/__tests__/company-search-extract-routes.test.ts:55`) |
| TC-43 | Extract route denies cross-company access before service | Foreign company id | 403 or 404 without service call (`server/src/__tests__/company-search-extract-routes.test.ts:80`) |
| TC-44 | Extract route shares the company-search rate limiter | Rate limiter with max 1 | Second extract call 429 (`server/src/__tests__/company-search-extract-routes.test.ts:91`) |

Files: `server/src/__tests__/company-search-service.test.ts`, `server/src/__tests__/company-search-extract-service.test.ts`, `server/src/__tests__/task-search-quality.test.ts`, `server/src/__tests__/company-search-rate-limit-routes.test.ts`, `server/src/__tests__/company-search-extract-routes.test.ts`.

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-45 | Search request renders the result from `?q` | Open Search with `?q`, await query | Result row rendered (`ui/src/pages/Search.test.tsx:185`) |
| TC-46 | Artifact results render in the search surface | Search with artifact rows | Artifact rows rendered (`ui/src/pages/Search.test.tsx:290`) |
| TC-47 | Comment and document rows render anchors, chips, and highlights | Search with context evidence | Exact anchors, source chips, highlights (`ui/src/pages/Search.test.tsx:366`) |
| TC-48 | Loading state renders while search is pending | Trigger search with deferred response | Loading state visible (`ui/src/pages/Search.test.tsx:467`) |
| TC-49 | Error state renders retry and fallback actions | Fail the search request | Error with retry and fallbacks (`ui/src/pages/Search.test.tsx:481`) |
| TC-50 | Typing debounces before dispatching search | Type then advance timers | One search after the debounce window (`ui/src/pages/Search.test.tsx:498`) |
| TC-51 | Exact identifier match auto-redirects to issue root | Return exact identifier result | Redirect without deep-link suffix (`ui/src/pages/Search.test.tsx:553`) |
| TC-52 | Non-default scope no-results renders Search-all action | Empty scoped search | No-results with Search-all (`ui/src/pages/Search.test.tsx:618`) |
| TC-53 | URL filters parse into params and operator pills | Load URL with filters | Params and pills match (`ui/src/pages/Search.test.tsx:654`) |
| TC-54 | Typed operators dispatch as search filters | Type operator tokens | Request carries parsed filters (`ui/src/pages/Search.test.tsx:699`) |
| TC-55 | Deleted operator tokens drop filters from requests | Delete committed token | Request omits the filter (`ui/src/pages/Search.test.tsx:751`) |
| TC-56 | Removed filter chips strip tokens from the query | Remove operator-derived chip | Token stripped and re-query issued (`ui/src/pages/Search.test.tsx:790`) |
| TC-57 | Operator autocomplete applies a suggestion to the token | Open suggestions and select one | Token updated with suggestion (`ui/src/pages/Search.test.tsx:838`) |
| TC-58 | Sort param round-trips through URL into requests | Change sort | URL and request carry sort (`ui/src/pages/Search.test.tsx:922`) |
| TC-59 | Removable filter chips re-query without the filter | Remove chip | Re-query without that filter (`ui/src/pages/Search.test.tsx:946`) |
| TC-60 | Zero-results recovery renders loosen suggestions | Filters emptying the page | Recovery with loosen suggestions (`ui/src/pages/Search.test.tsx:986`) |

Files: `ui/src/pages/Search.test.tsx`.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-61 | Overlong query text | Truncated to max length before parsing |
| TC-62 | Invalid scope, status, priority, sort, pagination, or project id | 400 before service invocation |
| TC-63 | Regex extract kind or too-short contains | 400 rejected as unsafe or ambiguous |
| TC-64 | Conflicting extract update filters | 400 when both updatedWithin and updatedAfter are set |
| TC-65 | Rate budget exceeded | 429 with Retry-After and rate-limit headers |
| TC-66 | Foreign company or hidden rows | Excluded from results, counts, and extracts |
| TC-67 | Empty quotes or literal-only punctuation queries | Empty safe result without errors |

## Test Infrastructure

- Embedded Postgres test databases with `pg_trgm` for service, extract, and quality suites.
- Supertest plus express route harness with mocked search services for route tests.
- jsdom Search page harness with mocked search, agents, projects, labels, auth, router, and sidebar contexts.
- Task-search corpus fixture in `server/src/__tests__/fixtures/task-search-corpus.ts` with per-case relevance grades.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-8, TC-11, TC-12, TC-13, TC-18, TC-19, TC-43, TC-45 |
| FR-2 | TC-3, TC-30, TC-31, TC-32, TC-33, TC-34, TC-35, TC-42, TC-43 |
| FR-3 | TC-39, TC-41, TC-44, TC-65 |
| FR-4 | TC-4, TC-5, TC-6, TC-8, TC-9, TC-10, TC-24, TC-25, TC-26, TC-28, TC-29, TC-36, TC-37, TC-38 |
| FR-5 | TC-46, TC-47, TC-51 |
| FR-6 | TC-15, TC-16, TC-17, TC-53, TC-54, TC-55, TC-56, TC-59, TC-60 |
| FR-7 | TC-2, TC-7, TC-14, TC-22, TC-58 |
| FR-8 | TC-7, TC-48, TC-49, TC-50, TC-52, TC-53, TC-54, TC-57, TC-60 |
| FR-9 | TC-11, TC-12, TC-47 |
| NFR-1 | TC-18, TC-19, TC-35, TC-40, TC-43, TC-66 |
| NFR-2 | TC-2, TC-11, TC-12, TC-14 |
| NFR-3 | TC-39, TC-44, TC-65 |

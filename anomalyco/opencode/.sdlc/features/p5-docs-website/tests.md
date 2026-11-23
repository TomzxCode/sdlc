---
title: "Docs website"
status: done
session_link: http://localhost:10000/?session=ses_df5cc15baffea6HFTvAOmQ6bxA
---

# Test Plan: Docs website

## Scope

This plan covers the docs website that now lives under `services/site/src/docs` as the V2 set at `/docs` and the V1 set at `/v1/docs`.
The tests cover routing, Markdown rendering, V1 locale parity, the sitemap, and the changelog pages that share the site's rendering and navigation.
Automation described in the original requirements, including the scheduled docs update workflow and the locale sync workflow, is out of scope because those workflows no longer exist.
Visual and responsive layout checks are manual, as described in `services/site/src/docs/AGENTS.md`.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | V2 and V1 page routing, Markdown twins, redirects and reserved files are resolved correctly | URLs and `Accept` headers in `services/site/test/docs-route.test.ts` | Page, file, redirect or missing result for each URL |
| TC-2 | Fenced code blocks become the right code frames with correct copy text | Shell, titled, tree, plain and diff fences in `services/site/test/docs-rehype.test.ts` | `CodeFrame` and `FileTree` components with the expected attributes |
| TC-3 | Headings keep ids and gain copy links, and heading data is collected | `h2` and `h4` nodes in `services/site/test/docs-rehype.test.ts` | `HeadingLink` on `h2` and `h3`, with heading metadata |
| TC-4 | Legacy Starlight directives, tabs and steps compile into site components | MDX sources in `services/site/test/docs-rehype.test.ts` | Callouts, tabs with slots and a steps list, with no Starlight imports |
| TC-5 | Every V1 locale mirrors the English pages and translates the docs chrome | Locale folders and i18n dictionaries in `services/site/test/docs-i18n.test.ts` | Matching page sets, sidebar slugs and translated strings |
| TC-6 | Sitemap index, page coverage, locale alternates and size limits hold | Route manifest and release fixtures in `services/site/test/sitemap.test.ts` | A valid index listing pages and `/docs/sitemap.xml` within limits |
| TC-7 | Changelog highlights are parsed, grouped by area and counted | Release notes in `services/site/test/changelog-highlights.test.ts` | All highlights shown with correct area filters and hidden counts |
| TC-8 | Changelog entry status distinguishes live, stand-in and missing releases | Release lists in `services/site/test/changelog-status.test.ts` | Status 200, 404 or 503 as expected |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-9 | The docs build prerenders every page and validates links and asset boundaries | Run `bun src/docs/script/build.ts --out "$RUNNER_TEMP/docs"` from `services/site` after `bun run generate` | Every page renders, all links resolve, all assets stay under `/docs`, and script and stylesheet stay within gzip budgets |
| TC-10 | Pull requests that touch the site run the same docs build | A pull request changes `services/site/**`, protocol OpenAPI or CLI config | `.github/workflows/check-docs.yml` builds the docs and fails the check on broken pages or links |
| TC-11 | The site build and deploy produce the Worker that serves the docs | Pushes to `dev` or `production` | `.github/workflows/deploy-site.yml` builds and deploys `services/site`, including the prerendered docs |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-12 | No automated browser test exists for the docs | Inspect `services/site/test` and the workflows | Routing and rendering are covered by unit tests and the docs build; layout checks are manual |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | A V2 URL has no page, for example `/docs/ja/agents/` | Redirect to the same path under `/v1/docs` with status 302 |
| TC-14 | A page moved between URLs | Redirect to its new URL with status 301 |
| TC-15 | A request asks for Markdown or uses a `.md` URL | Serve the page's Markdown twin |
| TC-16 | A page takes a reserved file name or loads an asset from outside the docs sets | The docs build fails |
| TC-17 | A link points at a missing page or anchor | `validate-links.ts` reports the path and fails the build |
| TC-18 | A tag is missing from GitHub's release list | The changelog answers with 404 or 503 according to the release source |
| TC-19 | `docs.opencode.ai` is requested | Redirect to the same path under `/docs` on the main site |

## Test Infrastructure

- Run all tests from `services/site` with `bun test`.
- The docs build requires `bun run generate` to place `openapi.json`, `config.json` and `v2/cli.json` in `public`.
- `pagefind` builds one search index per docs set, and the build uses the site's CSS and fold settings plugins.
- The route tests use `services/site/src/docs/vite.ts` slug lists through `virtual:docs-pages`; no browser is required.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-9, TC-10, TC-11 |
| FR-2 | TC-5, TC-9 |
| FR-3 | TC-1, TC-9 |
| FR-4 | TC-5 |
| FR-5 | TC-5 |
| FR-6 | Not covered, the scheduled update workflow is absent |
| FR-7 | Not covered, the locale sync workflow is absent |
| FR-8 | TC-3, TC-6, TC-9, TC-10 |
| FR-9 | TC-11 |
| FR-10 | TC-9 |
| NFR-1 | TC-11 |
| NFR-2 | Not covered, RTL is rendered from the V1 Arabic locale but has no test |
| NFR-3 | TC-1, TC-5, TC-9, TC-10 |

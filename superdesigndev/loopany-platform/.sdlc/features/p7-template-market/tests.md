---
title: "Template Market & Bundles"
status: done
---

# Test Plan: Template Market & Bundles

## Scope

Testing the template/bundle registries, the shape and editorial-rating guards, the public market/detail SSR routes, the shared card, the flow-spec derivation, the reference.md serving, and the compose deep-link. Out of scope: dashboard card fan geometry (owned by the dashboard feature) and the daemon skill whitelist (owned by daemon packaging).

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Registry builds TEMPLATES from the folder glob | Folder list under `skill/templates/` | `templates.test.ts` pins the full name list; each template's defining behaviors stay in its `description` |
| TC-2 | Every template belongs to exactly one bundle | Template ↔ bundle map | `bundles.test.ts` passes; no template invisible, none duplicated |
| TC-3 | Editorial ratings complete and consistent | Template with no rating or misclassified open/closed | `templateRatings.test.ts` fails |
| TC-4 | Detail resolves by slug with real 404 | Unknown slug | `notFound()` throws for a real HTTP 404 |
| TC-5 | Flow spec is single-sourced | A template with a `FlowSpec` | Compose preview and `TemplateFlowDiagram` both derive from the same spec |
| TC-6 | Reference route is a static map of ONLY reference.md | Request `meta.json`/`thumb.svg` | 404; only the exact name resolves (pinned by `-api.skill.references.test.ts`) |
| TC-7 | Detail page is hook-free and measurement-free | SSR pass over the detail route | Guard test pins the route stays hook-free (crawler-safe) |
| TC-8 | Public payloads carry no thumbnails | `listPublicBundles`/`getPublicTemplate` | No inlined `thumb.svg` on list or detail payloads |
| TC-9 | Card is one shared component | Dashboard teaser, market, landing | All three render the same `TemplateCard` with the rating-fed `FlowStrip` |
| TC-10 | Story media rewrites resolve | `templateStory` with `assets/<file>` refs | Rewritten to `/template-assets/<name>/…`; nitro serves `public/` verbatim |
| TC-11 | Template shape pins | New/renamed/removed folder | Shape tests (`templates.test.ts`, `bundles.test.ts`) cover the change automatically |
| TC-12 | Bundle-name stability | Label/tagline changes only | Tests key on names, so label/tagline edits pass |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-13 | Template in no bundle | Invisible on every surface; shape test fails loudly |
| TC-14 | Accent declared only in `:root` | Tailwind v4 doesn't tree-shake the var used in a runtime inline style |
| TC-15 | Folder renamed | Old `/templates/<old>` share link and `/?template=<old>` permanently 404 (documented, Should) |
| TC-16 | Markdown detail under SSR | Renders through marked without DOMPurify (trusted repo content) |

## Test Infrastructure

- vitest unit + route tests; `templates.test.ts`/`bundles.test.ts`/`templateRatings.test.ts` read source via the VARIABLE-path `readFileSync` guard form.
- Public routes verified for SSR HTML and the zero-auth contract.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-11 |
| FR-2 | TC-2, TC-13 |
| FR-3 | public-route SSR + zero-auth contract |
| FR-4 | TC-5 (diagram), TC-10 (story media) |
| FR-5 | compose deep-link + OAuth-forward integration |
| FR-6 | TC-9 |
| FR-7 | TC-5 |
| FR-8 | TC-4 |
| FR-9 | TC-6 |
| FR-10 | TC-1 |
| FR-11 | TC-15 |
| NFR-1 | TC-6 |
| NFR-2 | TC-16 |
| NFR-3 | reduced-motion contract (carousel + typed hero) |
| NFR-4 | TC-8 |
| NFR-5 | deploy paths-ignore (CI contract) |

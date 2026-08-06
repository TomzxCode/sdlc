---
title: "Template Market & Bundles"
status: done
---

# Requirements: Template Market & Bundles

## Overview

The template market is a curated catalog of ready-to-run loops. A template is a folder under `src/skill/templates/<name>/` carrying a static `meta.json` (whose `description` is the guided paste-prompt the user copies into their coding agent) plus optional `reference.md`, `thumb.svg`, `story.md`, and a flow spec. Bundles group templates into curated categories shown on the dashboard carousel and the public market at `/templates`. The market renders zero-auth public pages that SSR for crawlers and unfurlers, and the compose modal consumes the same template intent, so there is exactly one creation path.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Discover ready-to-run loops, compare mechanisms, and start a loop with one paste. |
| Content editor | Add a template by writing content (meta.json + optional assets) plus one bundle line; shape tests cover it automatically. |
| Product | A public, shareable catalog that deep-links into the existing single-template compose path. |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | A template shall be a folder under `skill/templates/<name>/` with a static `meta.json`; the registry builds `TEMPLATES` from an `import.meta.glob` over `meta.json`. |
| FR-2 | Must | Every template shall belong to exactly one bundle, and a template in no bundle shall be invisible to every user-facing surface. |
| FR-3 | Must | The market pages (`/templates`, `/templates/<slug>`) shall do zero auth checks, render logged out, and SSR real HTML for crawlers. |
| FR-4 | Must | The detail page shall render a split layout: left = flow diagram + mechanism facts + optional field notes; right = sticky verbatim prompt + Copy. |
| FR-5 | Must | The detail CTA shall deep-link `/?template=<name>`, forwarded through the gated `/t/<team>` redirect and preserved across OAuth, reusing the existing single-template compose. |
| FR-6 | Must | The market card shall be one shared component (with a body fed by editorial ratings) rendered by `/templates`, the dashboard teaser, and the pre-login landing. |
| FR-7 | Must | The flow spec in `lib/templateFlow.tsx` shall be ONE source drawn by both the compose modal's animated preview and the public detail page's static diagram. |
| FR-8 | Must | An unknown template slug shall throw `notFound()` for a real HTTP 404. |
| FR-9 | Should | On-demand `reference.md` (artifact contracts, dashboard markup, state schemas) shall be served at `/api/skill/references/templates/<name>/reference.md` only; `meta.json`/`thumb.svg` stay off that route. |
| FR-10 | Should | A template's `description` shall spell out the specifics (per-run workflow, hard rules, boundaries, quality gates) as a guided multi-step setup conversation, optionally embedding the task-file skeleton. |
| FR-11 | Should | The slug shall be stable: renaming a folder permanently 404s old share links and deep links. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | `reference.md` serving is a static map of only the four exact names; `meta.json`/`thumb.svg` never resolve. |
| NFR-2 | Must | Reliability | Field notes render through marked WITHOUT DOMPurify only because the content is trusted repo content (SSR has no DOM). |
| NFR-3 | Must | Accessibility | Carousel auto-play and the typed hero are off under `prefers-reduced-motion`. |
| NFR-4 | Should | Performance | Thumbnails are stripped from public list payloads (the market draws no illustration). |
| NFR-5 | Should | Availability | A change to a prompt-only `.md` compiles into the server bundle and must deploy (explicit paths-ignore, not `**/*.md`). |

## Constraints

- Template/flow/dashboard content lives under `src/skill/` and is compiled into the bundle via `?raw` imports.
- `sync-skill.mjs` stays selective: neither `skill/templates/` nor `skill/bundles/` ever ships in the daemon npm tarball.
- A new template needs a `meta.json` (paste-prompt), membership in exactly one bundle meta, and a `templateRatings.ts` entry, or it fails its shape tests.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

- [ ] **FR-1**
    - **Given** a new template folder with `meta.json`
    - **When** the registry builds
    - **Then** the template appears in `TEMPLATES` and the shape tests cover it automatically
- [ ] **FR-2**
    - **Given** a template named in no bundle meta
    - **When** the market renders
    - **Then** it is invisible; `bundles.test.ts` fails the shape guard
- [ ] **FR-3**
    - **Given** a logged-out visitor on `/templates`
    - **When** the page loads
    - **Then** real SSR HTML renders without any auth redirect
- [ ] **FR-4**
    - **Given** the detail page for a template with a flow spec and story
    - **When** it renders
    - **Then** the left shows the derived diagram + mechanism facts + field notes and the right shows the verbatim prompt + Copy
- [ ] **FR-5**
    - **Given** a signed-out user clicking Create on the detail page
    - **When** they complete OAuth
    - **Then** `/?template=<name>` survives the redirect and opens the existing compose
- [ ] **FR-6**
    - **Given** the shared market card
    - **When** rendered on all three surfaces
    - **Then** the body is the rating-fed FlowStrip; the dashboard teaser previews the catalog's curated order
- [ ] **FR-7**
    - **Given** a template with a `FlowSpec`
    - **When** the modal and the public diagram render
    - **Then** both draw from the same spec (derived, never hand-authored twice)
- [ ] **FR-8**
    - **Given** an unknown slug
    - **When** the detail route loads
    - **Then** a real HTTP 404 is returned
- [ ] **NFR-1**
    - **Given** a request for `meta.json` or `thumb.svg` through the references route
    - **When** resolved
    - **Then** it 404s; only `reference.md` resolves

## Conflicts

None identified yet.

## Open Questions

1. None: behavior is fully determined by the code and its tests.

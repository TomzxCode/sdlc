---
title: "Template Market & Bundles"
status: done
---

# Specification: Template Market & Bundles

## Overview

The market is a file-based, zero-exec template system. `server/templates.ts` builds `TEMPLATES` from an `import.meta.glob` over `skill/templates/*/meta.json`, pairs each folder's optional `thumb.svg` (`?raw`), and merges editorial `rating` from `server/templateRatings.ts`. `server/bundles.ts` builds `BUNDLES` the same way from `skill/bundles/*/meta.json`, listing member template NAMES in display order. Every user-facing surface reads BUNDLES; a template in no bundle is invisible. `listPublicBundles`/`getPublicTemplate` return the same registry minus every inlined thumbnail.

## Architecture

```
skill/templates/<name>/
  meta.json        → server/templates.ts TEMPLATES (name/label/desc/description)
  reference.md     → on-demand route (optional bulky detail)
  thumb.svg        → ?raw pair (dashboard carousel only, never the public market)
  story.md         → "Field notes" (attached ONLY by findPublicTemplate)
skill/bundles/<name>/meta.json → server/bundles.ts BUNDLES (label/tagline/accent/members)
server/templateRatings.ts → TemplateInfo.rating (merged)
lib/templateFlow.tsx       → FLOWS: one FlowSpec per template (nodes + dashboard widgets)
```

Surfaces:

- `routes/templates.tsx` + `templates_.$slug.tsx`: public market + detail (zero auth, SSR).
- `components/TemplateCard.tsx`: ONE card component (`TemplateCard` + `bundleItems`), body = rating-fed `FlowStrip`.
- `components/TemplatesPreview.tsx`: catalog teaser on the dashboard and the pre-login landing (`SignIn`).
- `components/BundleCarousel.tsx`: hero carousel on the dashboard; in-bundle card fan (rows of up to 3).
- `components/ComposeModal.tsx`: handles blank/template/bundle; template/bundle snippets skip the host chooser.
- `components/TemplateFlowDiagram.tsx`: static detail-page diagram derived from the FlowSpec.
- `routes/api.skill.references.$.ts`: serves ONLY `skill/templates/<name>/reference.md`.

## Data Models

- `TemplateInfo`: `name`, `label`, `desc` (one-line card blurb), `description` (paste-prompt task text), optional `reference` presence, `thumb` (optional), `rating` (merged editorial), `hasFlow`/`story` presence (derived).
- `BundleInfo`: `name`, `label`, `tagline`, `accent` (a `--color-<accent>` token), `members` (template names in display order), `individual` (true only for the "Goal Loops" catch-all `others`).
- `Rating`: ease, cadence + mechanism, effect visibility, humanized `schedule`, optional `exitCondition` (closed loops only). Mechanism REUSES the open/closed distinction (the `others` bundle is exactly the closed set).

## API Contracts

### GET /api/skill/references/templates/<name>/reference.md

Static map; only the exact `reference.md` name resolves for a known template folder. `meta.json`/`thumb.svg` are never exposed (pinned by test). Returns the file or 404.

### Public lists (loader data, no auth)

`listPublicBundles()` / `getPublicTemplate(slug)` — the registry minus every inlined `thumb.svg`. Detail resolves BY SLUG (`findPublicTemplate`); unknown slug throws `notFound()`.

## Sequences

### Public detail render

```
GET /templates/<slug> (SSR, no auth)
  findPublicTemplate(slug) → notFound() if unknown
  templateFlowDiagram(name) → static diagram (from FlowSpec, hook-free)
  story.md attached ONLY here (never on list payloads)
  marked (no DOMPurify — trusted repo content, SSR lacks DOM)
  media refs assets/<file> rewritten → /template-assets/<name>/…
  sticky verbatim prompt + Copy
  CTA deep-link /?template=<name>
```

### Create from market

```
/?template=<name> → gated /t/<team> redirect → callbackURL preserves across OAuth
  → DashboardView.openTemplate → EXISTING single-template compose
  (never a parallel creation path)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| File-based registry | `import.meta.glob` over `meta.json` | Zero-exec; adding a template is content + one bundle line |
| Bundle visibility | Every surface reads BUNDLES | No bundle = invisible, pinned by test |
| Slug = folder name | No alias/redirect map | Rename permanently 404s old links; rename only young templates |
| No thumbnails in market | `thumb.svg` stripped from public payloads | The market draws no illustration; detail flow strip is the anchor |
| Trusted markdown | marked without DOMPurify on detail | Repo-authored content; DOMPurify needs a DOM the SSR pass lacks |
| Media in public/ | `public/template-assets/<name>/` | nitro serves `public/` verbatim; Vite `?url` assets 404 in prod |
| One creation path | Detail CTA reuses compose | Never a parallel creation path |
| Accent tokens | Calm `--color-<accent>`, plain `:root`, never red | A category must not read as an error state; Tailwind v4 tree-shakes a var only used in an inline style |

## Risks and Unknowns

1. A template folder rename permanently breaks old share links and `/?template=` deep links — a deliberate trade-off, documented as a Should.
2. `reference.md` route works in prod but vite's static layer 404s `.md` in dev (covered by unit test).
3. Bundle NAME keys must never change (tests key on names); labels/taglines may.

## Out of Scope

- The onboarding Housekeeper template's actual content (owned by onboarding + templates content).
- The daemon skill bundle (`sync-skill.mjs` whitelist) — deliberately excludes templates/bundles.

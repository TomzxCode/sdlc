---
issue: ""
title: "Font Customization"
status: draft
---

# Existing Solutions: Font Customization

## Overview

The codebase already has a mature font customization system with 10 UI font options and 10 monospace font options, CSS custom property injection via the theme generator, FontFace API-based loading, debounced persistence via `appearanceAutoSave.ts`, and a dedicated settings UI in `OpenChamberVisualSettings.tsx`. What the requirements describe (separate monospace/proportional configuration, font size clamping to 50-200% / 9-52px, reset-to-default, global application without restart) are already implemented. The remaining gap is support for custom/arbitrary font families beyond the predefined list, and potential integration with the Google Fonts API to let users browse and select from the full catalog.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/lib/fontOptions.ts`, `fontLoader.ts`, `useAppFontEffects.ts`, `appearanceAutoSave.ts`, `useUIStore.ts`, `OpenChamberVisualSettings.tsx`, `cssGenerator.ts`, `persistence.ts`, `packages/ui/src/lib/theme/cssGenerator.ts` |
| Open-source | Yes | Google Fonts Developer API v2, Google Web Font Loader, CSS Font Loading API (MDN), `fontsource` packages (already a dependency) |
| Commercial / SaaS | Yes | Google Fonts API (free tier, API key required) |
| Standards / protocols | Yes | CSS `@font-face`, CSS Font Loading API (W3C), WOFF2 |
| Reference material | Yes | Google Fonts CSS API v2 docs, MDN CSS Font Loading API |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing OpenChamber font system | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-07, FR-08 | No custom font family input, no Google Fonts catalog browser |
| Google Fonts CSS API v2 | API/Service | Apache 2.0 (fonts), proprietary (API) | Mature | Custom font families from 1,600+ catalog | Requires internet, API key, client-side loading |
| Google Fonts Developer API | API/Service | Proprietary | Mature | Font metadata querying (family list, variants, axes) | Requires API key, rate-limited, metadata only |
| CSS Font Loading API (native) | Standard | W3C | Mature | `FontFace` object loading, `document.fonts` set, status tracking | No catalog discovery, low-level |
| fontsource npm packages | Library | MIT (Open Font License) | Mature | Self-hosted font loading, already used (`@fontsource/ibm-plex-mono`, `@fontsource/ibm-plex-sans` in package.json) | Limited to packaged fonts, no dynamic selection |
| Google Web Font Loader | Library | Apache 2.0 | Maintenance | Provider-agnostic font loading with events | Unmaintained since 2020, TypeScript types outdated |

## Evaluation

### Existing OpenChamber Font System

- **Strengths:** Already implements FR-01 through FR-08 in production. 10 UI fonts + 10 mono fonts with proper CSS custom property injection (`--font-sans`, `--font-mono`), FontFace-based loading (`fontLoader.ts`), debounced persistence via Zustand store subscription (`appearanceAutoSave.ts`), separate `uiFont`/`monoFont` state fields, font size clamped 50-200% with step=5, terminal font size 9-52px, reset buttons, preview-in-select via `fontFamily` style on option labels.
- **Weaknesses:** Only supports predefined font options from `fontOptions.ts`. No custom font family text input. No Google Fonts catalog browser. No font file upload. The existing `terminalFontSize` is already used for terminal-only scaling.
- **Integration effort:** None (already integrated).
- **Cost:** None.
- **Risks:** None.

### Google Fonts CSS API v2

- **Strengths:** Simple CSS-based loading via `<link>` or `@import`. Variable font support with axis ranges (`wght`, `ital`). `font-display` control (`swap`, `fallback`, etc.). `text=` parameter for subset optimization. Supports 1,600+ families.
- **Weaknesses:** Requires internet connectivity for dynamic loading (cached fonts in `@fontsource` cover the offline case for bundled fonts). API key required for Developer API (metadata querying), but CSS API works without key.
- **Integration effort:** Low. Fetch CSS URL and inject a `<link>` or use `FontFace` constructor with the woff2 URL from the Google Fonts CSS response. Existing `fontLoader.ts` pattern can be extended.
- **Cost:** Free (bandwidth for Google Fonts is served from Google's CDN at no charge).
- **Risks:** Privacy concern (Google receives request logs). Not suitable for fully offline/air-gapped deployments.

### CSS Font Loading API

- **Strengths:** Native browser API. No dependencies. `FontFace` objects with `load()` promise, `status` tracking (unloaded/loading/loaded/failed), `document.fonts.ready` for layout-complete detection.
- **Weaknesses:** Low-level. No catalog or discovery. Each font variant requires a separate `FontFace` instance. Error handling is manual.
- **Integration effort:** Low. Existing `fontLoader.ts` already uses `FontFace` constructor for its predefined options.
- **Cost:** None.
- **Risks:** None.

## Recommendation

**Direction:** Adopt and extend

The existing font system already covers all functional requirements. Extend it by:
- Adding a custom font family text input field that accepts any CSS `font-family` value (including web fonts loaded externally)
- Optionally integrating Google Fonts API for a "Browse fonts" dialog that queries the Developer API for the catalog, then loads selected families via the CSS API v2
- Keeping the existing predefined options as quick-select defaults

The Google Fonts integration should be additive: if the user's network is unavailable, the predefined `fontsource`-backed options still work. The custom font text input is the highest-value addition since it unblocks any font the user wants without requiring code changes.

## Sources of Information

- Google Fonts Developer API: `https://developers.google.com/fonts/docs/developer_api`
- Google Fonts CSS API v2: `https://developers.google.com/fonts/docs/css2`
- MDN CSS Font Loading API: `https://developer.mozilla.org/en-US/docs/Web/API/CSS_Font_Loading_API`
- Existing `fontOptions.ts`: 10 UI fonts + 10 mono fonts with FontFace source definitions
- Existing `fontLoader.ts`: `loadUiFont()`/`loadMonoFont()` using `FontFace` constructor + `document.fonts.add()`
- Existing `useAppFontEffects.ts`: Applies `fontFamily` to `document.body.style` and `--font-family-mono` CSS var

## Open Questions

1. Should the Google Fonts API key be user-configured or embedded in the app? (Embedded is simpler but ties to a single quota; user-configured is more private.)
2. Should custom fonts be persisted only as a family name string, or should the full font stack (including fallbacks) be stored?
3. Should the Google Fonts catalog be fetched on demand or pre-cached as a local list updated periodically?

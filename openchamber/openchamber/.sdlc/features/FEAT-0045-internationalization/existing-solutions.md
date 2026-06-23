---
issue: ""
title: "Internationalization (i18n)"
status: draft
---

# Existing Solutions: Internationalization (i18n)

## Overview

OpenChamber already ships a custom i18n system in `packages/ui/src/lib/i18n/` with 8 locales, lazy-loaded TypeScript dictionaries, Zustand store for locale state, browser language persistence via localStorage, and a React context/provider. The requirements doc closely matches what is already built. The question is whether to keep the custom system or migrate to a mature library like react-i18next, FormatJS, or LinguiJS. Given that the custom system is already deeply integrated (~228 `useI18n()` call sites across 100+ components), the retry logic and missing-key fallback are already implemented, and the codebase values minimal dependencies, the recommended direction is to keep and extend the custom system, standardizing the locale-ui-patterns skill as the canonical way to add strings.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/lib/i18n/` — full custom implementation; `packages/ui/src/lib/i18n/messages/` — 16 message files (8 locales x 2 namespaces); settings locale picker in `OpenChamberVisualSettings.tsx`; locale-ui-patterns skill codifies usage |
| Open-source | Yes | `react-i18next` (3.5M/wk, ~6KB gzip), `react-intl`/FormatJS (1.2M/wk, ~17KB gzip), `LinguiJS` (~2KB gzip, compile-time), `next-intl` (457B, Next.js-focused), `typesafe-i18n` (~1KB, SSR-first) |
| Commercial / SaaS | Yes | Locize, SimpleLocalize, L10n.dev — translation management platforms that integrate with i18next/FormatJS |
| Standards / protocols | Yes | ICU Message Format (Unicode CLDR), BCP 47 language tags, `Intl` browser API (DateTimeFormat, NumberFormat, PluralRules) |
| Reference material | Yes | react-i18next docs, FormatJS docs, Mozilla MDN Intl API, Unicode CLDR plural rules |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Custom (existing `packages/ui/src/lib/i18n/`) | Internal | MIT (project) | Production (in use) | FR-01 to FR-08 | FR-05 (retry on load failure has basic catch but no configurable retry count) |
| react-i18next (i18next + react-i18next) | Library | MIT | Mature (10+ years, 3.5M/wk) | FR-01 to FR-08 | Migration cost across 228 call sites; adds ~6KB gzip; namespace plugin model differs from current flat-map pattern |
| FormatJS (react-intl + @formatjs/cli) | Library | MIT | Mature (10+ years, 1.2M/wk) | FR-01 to FR-06, FR-08 | No built-in lazy loading by default; needs custom `@formatjs/cli` extract step; ICU syntax is verbose |
| LinguiJS | Library | MIT | Active (growing, ~2KB gzip) | FR-01, FR-04, FR-06, FR-08 | Compile-time extraction adds build step; smaller ecosystem; requires migration of all dict files |
| Custom (vanilla `Intl` API + ad-hoc patterns) | Build | N/A | N/A | FR-02, FR-06, FR-08 | No lazy loading, no structured dict format, no runtime switching — pre-built custom system already surpasses this |

## Evaluation

### Custom (existing `packages/ui/src/lib/i18n/`)

- **Strengths:** Already integrated across the entire UI with zero additional dependencies. TypeScript dictionaries provide type-safe keys via `I18nKey`. Lazy dynamic `import()` works with Vite's code splitting. Persistence via `localStorage` with a versioned key (`openchamber.i18n.v1`). Runtime switching via Zustand `setLocale` triggers React re-render through `I18nProvider`/`useI18n()`. Fallback to English for missing keys is handled in `formatMessage()`. Retry on load failure uses catch-to-English, though not true retry with backoff. No build step required — edit a `.ts` file, that's all.
- **Weaknesses:** No ICU Message Format support (pluralization must be done with separate keys per count). No built-in number/date formatting (codebase uses ad-hoc `Intl.NumberFormat`/`Intl.DateTimeFormat` calls in components). No translation management integration. Retry logic is a single catch that falls back to English, not a proper retry loop.
- **Integration effort:** None — already fully integrated.
- **Cost:** Zero (MIT, no external dependency).
- **Risks:** Low — the system is simple and proven in production. The main risk is maintainability if new contributors expect a standard library.

### react-i18next (i18next + react-i18next)

- **Strengths:** Largest ecosystem, plugin model (language detection, HTTP backend, caching), ICU add-on available, TypeScript support, SSR support, namespace-based lazy loading, rich interpolation and pluralization.
- **Weaknesses:** Requires migration of ~228 `useI18n()` call sites to `useTranslation()`. Dict format changes from flat TypeScript objects to nested JSON. Adds ~6KB gzip (i18next ~4KB + react-i18next ~2KB). The `i18n.changeLanguage()` imperative API is less compatible with Zustand-driven state. Translation management integrators (Locize) are a paid add-on.
- **Integration effort:** High — full migration of all components and dict files.
- **Cost:** Zero (MIT).
- **Risks:** Medium — migration risk, bundle size increase, and loss of the exact Zustand-driven design that the project's performance rules depend on. The current system ties locale state to Zustand; react-i18next maintains its own internal state, adding a second source of truth.

### FormatJS (react-intl)

- **Strengths:** ICU Message Format standard, built-in date/number/relative time formatting via `Intl` API, strong TypeScript support with message type generation.
- **Weaknesses:** No namespace/lazy loading built-in (must use `@formatjs/cli` or custom dynamic import). ICU syntax is hard to read. Bundle size ~17KB gzip. Migration effort is similar to i18next.
- **Integration effort:** High.
- **Cost:** Zero (MIT).
- **Risks:** Medium — ICU complexity, build step requirement, no built-in lazy loading for this project's Vite setup.

### LinguiJS

- **Strengths:** Compile-time extraction means near-zero runtime overhead (~2KB gzip). TypeScript support. ICU-based message format.
- **Weaknesses:** Requires a build step (`@lingui/cli` extract + compile). Smaller ecosystem than i18next. Migration of all dict files from TypeScript objects to `.po`/`.json` format. The compile-time approach means adding a new locale requires re-running the build.
- **Integration effort:** High.
- **Cost:** Zero (MIT).
- **Risks:** Medium — build process change, smaller community, less battle-tested at this scale.

## Recommendation

**Direction:** Adopt and extend (keep and evolve the custom implementation)

The existing custom i18n system already satisfies FR-01 (8 locales, lazy-loaded), FR-02 (browser detection), FR-03 (persistence), FR-04 (runtime switching), FR-06 (English fallback on missing keys), FR-07 (edit TypeScript files, no formal process), and FR-08 (missing key fallback). FR-05 (retry on load failure) has basic handling but can be improved with a retry wrapper.

The migration cost to any external library is disproportionate to the value gained. The project's performance rules (Zustand referential equality, store splitting) are tightly coupled to how `useI18nStore` works — losing that design would require re-validating render discipline across 100+ components.

Instead, the custom system should be extended with:
- Configurable retry with backoff for locale load failures (FR-05)
- Standardized pluralization pattern using separate keys (`key.zero`/`key.one`/`key.other`) as already enforced by the locale-ui-patterns skill
- A test suite covering all FR acceptance criteria (currently only one test exists)

## Sources of Information

- react-i18next lazy loading pattern: https://react.i18next.com — namespace-based splitting is worth noting as a reference even if not adopted
- FormatJS ICU Message Format: https://formatjs.github.io — the ICU standard for plural/gender/select could influence the key-naming convention
- Mozilla MDN Intl API: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl — already used in the codebase for date/number formatting; the pattern of `Intl.DateTimeFormat(locale, opts)` should continue as the localization approach for dates/numbers rather than building into the i18n system

## Open Questions

1. Should the retry mechanism for failed locale loads use exponential backoff (like the event pipeline) or bounded linear retries?
2. Should pluralization be handled via ICU-style message syntax (requiring a parser) or kept as separate keys enforced by skill rule? The current convention (separate keys) aligns with the locale-ui-patterns skill's anti-grammar-fragment rule.
3. How should number/date formatting be consolidated? Currently ad-hoc `Intl.NumberFormat`/`Intl.DateTimeFormat` calls are scattered in components — should these become shared helpers based on the active locale?

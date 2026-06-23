---
issue: ""
title: "Custom Theming System"
status: draft
---

# Existing Solutions: Custom Theming System

## Overview

OpenChamber already has a mature custom theming system built in-house with 31 built-in themes (light + dark pairs), a CSS custom property generator, VS Code theme import adapter, hot-reload, and file-based custom theme loading from `~/.config/openchamber/themes/`. The existing implementation meets FR-01 through FR-04, FR-06, and FR-08. External libraries like TokiForge, ThemeKit, and AuraFlow CSS offer adjacent functionality but the custom approach is the correct direction given the deep integration with OpenChamber's Tailwind v4 setup, typography system, and component color tokens.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/ui/src/lib/theme/`, `packages/web/server/lib/opencode/theme-runtime.js`, `docs/CUSTOM_THEMES.md`, `vite-theme-plugin.ts` |
| Open-source | Yes | TokiForge, ThemeKit, var-th, AuraFlow CSS, @ninna-ui/core, Style Dictionary, Sassy |
| Commercial / SaaS | No | Theme marketplaces exist but out of scope for requirements |
| Standards / protocols | Yes | CSS custom properties, VS Code color theme JSON format, DTCG design tokens format |
| Reference material | Yes | VS Code theme color reference, Tailwind CSS custom properties |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| OpenChamber built-in theme system | Internal | MIT | Mature | FR-01, FR-02, FR-03, FR-04, FR-06, FR-08 | FR-05 (font/spacing/radius), FR-07 (VS Code import) partial |
| TokiForge | Library | AGPL-3.0 | Active | Runtime theme switching, CSS vars, dark mode | AGPL license incompatible with MIT project, framework-agnostic not needed |
| ThemeKit (@quefep/theme-kit) | Library | MIT | Active | Design tokens, alias resolution, persistence | Over-engineered for CSS-only needs, adds runtime JS weight |
| var-th | Library | MIT | New | Minimal CSS var injection, React provider | Too early, limited token coverage, no syntax colors |
| AuraFlow CSS | Library | MIT | New | 49 drop-in CSS themes | Themes only, no customization or editor import |
| @ninna-ui/core | Library | MIT | Active | CSS custom property presets, Tailwind v4 | Opinionated preset-only, no custom theme loading |
| Style Dictionary | Library | Apache-2.0 | Mature | Build-time token transformation, multi-platform | Build-time only, no runtime theme switching |
| Sassy | Library | MIT | Active | VS Code theme YAML→JSON compiler, variables | VS Code-focused, not general-purpose theming |

## Evaluation

### OpenChamber built-in theme system

- **Strengths:** Already implemented, provides 31 themes via JSON files, generates CSS custom properties, has a VS Code theme adapter, supports hot-reload via `theme-runtime.js`, fully integrated with Tailwind v4 and typography system.
- **Weaknesses:** Font size, spacing, corner radius (FR-05) are only partially implemented via `config` in theme JSON. No import-from-VS-Code UI yet (FR-07) though the adapter at `packages/ui/src/lib/theme/vscode/adapter.ts` exists. No file size validation (NFR-02).
- **Integration effort:** Low (already integrated).
- **Cost:** None (MIT license, built in-house).
- **Risks:** None.

### TokiForge

- **Strengths:** <3KB, framework-agnostic, CLI tooling, TypeScript-first, Figma sync.
- **Weaknesses:** AGPL-3.0 license is incompatible with OpenChamber's MIT license. Framework-agnostic design adds unnecessary abstraction.
- **Integration effort:** High (replace existing system, license change).
- **Cost:** Free but AGPL may require source disclosure.
- **Risks:** License incompatibility with MIT project.

### Style Dictionary

- **Strengths:** Industry standard for design tokens, multi-platform output (CSS, SCSS, iOS, Android), mature ecosystem.
- **Weaknesses:** Build-time only, no runtime theme switching. Adding it would be complementary, not a replacement.
- **Integration effort:** Medium (add as build step alongside existing runtime system).
- **Cost:** None (Apache-2.0).
- **Risks:** None, but does not replace the existing runtime theme system.

### VS Code theme format

- **Strengths:** Well-documented JSON format with `colors`, `tokenColors`, `semanticTokenColors` sections. Used by thousands of themes. Community tools like Sassy and yo generator-code support authoring.
- **Weaknesses:** OpenChamber's theme schema is different from VS Code's. The existing adapter at `packages/ui/src/lib/theme/vscode/adapter.ts` already converts VS Code JSON to OpenChamber format.
- **Integration effort:** Low (adapter already exists).
- **Cost:** None.
- **Risks:** None.

## Recommendation

**Direction: Adopt and extend**

The built-in theme system already covers the core requirements. Extend it to:
- Complete font size, spacing, and corner radius configuration (FR-05) through the existing `theme.config` mechanism in `cssGenerator.ts`.
- Add file size validation (NFR-02) on the server side when loading custom themes.
- Surface the VS Code theme adapter in the UI for importing themes (FR-07).
- Use Style Dictionary as a complementary build-time tool if design token export to other platforms is needed later.

## Sources of Information

- VS Code color theme JSON format: `microsoft/vscode-docs` at `api/extension-guides/color-theme.md`
- Sassy YAML-to-VS-Code compiler: `gesslar/sassy` - reference for import/composition patterns
- `CUSTOM_THEMES.md` at `docs/CUSTOM_THEMES.md` - existing custom theme documentation
- `cssGenerator.ts` at `packages/ui/src/lib/theme/cssGenerator.ts` - existing CSS variable generation
- `vscode/adapter.ts` at `packages/ui/src/lib/theme/vscode/adapter.ts` - existing VS Code theme adapter
- `prColors.ts` at `packages/ui/src/lib/theme/themes/prColors.ts` - PR status color generation

## Open Questions

1. Should font size, spacing, and corner radius be defined in the per-theme JSON or as a separate user settings override that applies to any theme?
2. Should VS Code theme import be a one-time conversion or a live mapping that stays in sync with the source theme?
3. What is the exact threshold for "instant" theme switching (NFR-01) in terms of frame budget?

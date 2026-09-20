---
title: "Docs website"
status: done
---

# Requirements: Docs website

## Overview

OpenCode ships its user documentation as an Astro Starlight site in `packages/web` (package `@opencode-ai/web`), deployed to the docs subdomain on Cloudflare.
English source pages live in `packages/web/src/content/docs/*.mdx`, with per-locale translations under per-locale subdirectories covering 17 locales.
A scheduled agent pipeline (`.github/workflows/docs-update.yml`) keeps the docs in sync with recent commits, and a currently disabled locale pipeline (`.github/workflows/docs-locale-sync.yml`) is intended to propagate English changes to translations.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Readable, searchable, translated usage and configuration docs |
| Contributors | A clear rule for adding docs (new files registered in `astro.config.mjs`) |
| Maintainers | Docs that stay current with code via the agent update pipeline |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall serve the documentation site from `packages/web` using Astro Starlight with sidebar navigation defined in `astro.config.mjs`. |
| FR-2 | Must | The system shall require every new documentation file to be registered in the `astro.config.mjs` sidebar. |
| FR-3 | Must | The system shall keep English source pages in `packages/web/src/content/docs/*.mdx`. |
| FR-4 | Must | The system shall keep translated pages under per-locale subdirectories of `packages/web/src/content/docs` with structure aligned to the English pages. |
| FR-5 | Should | The system shall support 17 locales plus root English, with translated sidebar labels and RTL layout for Arabic. |
| FR-6 | Must | The system shall run a scheduled agent pipeline that reviews recent commits and documents user-facing features and API changes in `packages/web/src/content/docs/*`. |
| FR-7 | Should | The system shall propagate English doc changes to locale docs via translator subagents without modifying the English sources. |
| FR-8 | Should | The system shall provide built-in search, edit links to the `dev` branch, last-updated timestamps, and GitHub and Discord social links. |
| FR-9 | Must | The system shall deploy the site to the docs subdomain from path `packages/web` via the SST Astro construct. |
| FR-10 | Should | The system shall emit `dist/config.json` and `dist/tui.json` at build end via the `configSchema` hook. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Should | Availability | The site shall be served on Cloudflare edge infrastructure via SST. |
| NFR-2 | Should | Usability | The Arabic locale shall render with RTL direction. |
| NFR-3 | Should | Maintainability | Documentation sources shall live alongside code in `packages/web` and follow the existing style and structure. |

## Constraints

- Site base path is `/docs` with server output and the Cloudflare adapter (`imageService: passthrough`).
- The legacy Mintlify starter in `packages/docs` is not referenced by any docs workflow and is out of scope for this feature.
- The locale sync workflow is currently disabled (`if: false` in `docs-locale-sync.yml`).

## Acceptance Criteria

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Docs site serves Starlight navigation
      Given the site is built from packages/web
      When a visitor opens the docs root
      Then the Starlight sidebar shows the Usage, Configure, and Develop groups
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: New page is registered in sidebar config
      Given a new mdx file is added under src/content/docs
      When the docs-update agent finishes its pass
      Then astro.config.mjs contains a sidebar entry for the new page
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: English pages live at the docs root
      Given the content directory src/content/docs
      When the English pages are listed
      Then index, config, providers, cli, tui, and the remaining topic pages exist as top-level mdx files
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Locale pages mirror English structure
      Given an English page such as config.mdx
      When the matching locale directory is inspected
      Then the corresponding translated page exists with aligned structure
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Locales and RTL are configured
      Given astro.config.mjs
      When the locales block is read
      Then root plus 17 locales are defined and ar uses dir rtl
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Scheduled pipeline documents a user-facing change
      Given commits with a user-facing feature land in the lookback window
      When the docs-update workflow runs the docs agent
      Then the relevant pages under packages/web/src/content/docs are updated
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: Locale sync preserves English sources
      Given changed English doc files on dev
      When the locale sync runs with translator subagents
      Then locale pages are updated and no file directly under src/content/docs root is modified
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Docs chrome is present
      Given any rendered docs page
      When the page chrome is inspected
      Then search, an edit link to the dev branch, a last-updated stamp, and GitHub and Discord links are present
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: Site deploys to the docs domain
      Given infra/app.ts
      When the Web construct is read
      Then an SST Astro site points at path packages/web with domain docs plus domain
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Build emits config schemas
      Given a completed astro build
      When the dist directory is inspected
      Then config.json and tui.json exist
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Site runs on Cloudflare via SST
      Given infra/app.ts
      When the Web construct is read
      Then it uses the SST Cloudflare Astro construct
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Arabic pages render right to left
      Given the ar locale page
      When the page is rendered
      Then the document direction is rtl
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Docs stay with code and style
      Given a docs change from the agent pipeline
      When the diff is reviewed
      Then only files under packages/web change and they follow the existing style and structure
    ```

## Conflicts

None identified yet.

## Open Questions

1. Where is the `docs` agent referenced by both workflows defined, since no matching agent file exists under `.opencode/agent/`?
2. Is `packages/docs` (Mintlify starter) formally retired, or is it still published anywhere?
3. Is the locale sync workflow intended to be re-enabled, and what gates that decision?
4. Is content versioning planned, since the Starlight config currently tracks a single version?

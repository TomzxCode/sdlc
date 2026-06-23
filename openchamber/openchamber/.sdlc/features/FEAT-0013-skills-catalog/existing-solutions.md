---
issue: ""
title: "Skills Catalog"
status: draft
---

# Existing Solutions: Skills Catalog

## Overview

The codebase already has a comprehensive skills catalog implementation spanning the server (`packages/web/server/lib/skills-catalog/`, VS Code bridge `packages/vscode/src/skillsCatalog.ts`, and shared UI (`packages/ui/src/components/sections/skills/catalog/`). It supports browsing, searching, and installing skills from Git repositories and the ClawdHub registry, with caching, conflict resolution, skill name validation, and per-scope installation. The recommendation is to adopt the existing implementation with refinements rather than build from scratch or adopt external alternatives.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `packages/web/server/lib/skills-catalog/`, `packages/ui/src/stores/useSkillsStore.ts`, `packages/ui/src/components/sections/skills/`, `packages/vscode/src/skillsCatalog.ts`, `packages/web/server/lib/opencode/skill-routes.js` |
| Open-source | Yes | ClawdHub API, npm registry, OpenClaw skill system, Anthropic skills repo |
| Commercial / SaaS | Yes | GitHub Marketplace, VS Code Extension Marketplace |
| Standards / protocols | Yes | SKILL.md file format with YAML frontmatter, OpenCode skill specification |
| Reference material | Yes | ClawdHub API documentation, OpenCode skill documentation, OpenClaw skill patterns |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing skills catalog (internal) | Internal | MIT | Mature | FR-01 through FR-10, NFR-01, NFR-02 | None significant |
| ClawdHub (community registry) | Registry | MIT | Mature | FR-02, FR-05, FR-10 | Not an installable component; API-only |
| OpenClaw ClawHub | Registry | MIT | Mature | FR-02, FR-05 | Tied to OpenClaw ecosystem |
| npm package registry | Registry | Proprietary | Mature | FR-02, FR-10 | Not skill-specific; no SKILL.md support |

## Evaluation

### Existing Skills Catalog Implementation

- **Strengths:** Dual backend support (web server + VS Code bridge). Built-in curated sources (ClawdHub, Anthropic skills repo). Git repository scanning with recursive SKILL.md discovery. ClawdHub API integration with pagination (max 20 pages), rate limiting, ZIP download, and version resolution. Skill name validation (1-64 chars, lowercase alphanumeric with hyphens). Conflict resolution UI (skip or overwrite per-skill or bulk). Caching with TTL for scan results (entry count + byte limits). Scope-based installation (user or project). Skill file management (read/write/delete supporting files). Settings UI with `SkillsPage`, `SkillsCatalogPage`, `AddCatalogDialog`, `InstallSkillDialog`, `InstallFromRepoDialog`, `InstallConflictsDialog`. i18n for all catalog flows in 7 languages. Supports private repo scanning via SSH identities. WebSocket-free: uses HTTP fetch for catalog data.
- **Weaknesses:** ClawdHub integration exists only in the VS Code bridge path; the web server path uses the `packages/web/server/lib/skills-catalog/` module which is separate. Server-side `skill-routes.js` uses the skills-catalog module but the VS Code bridge has its own parallel implementation.
- **Integration effort:** Low. Already integrated and shipping.
- **Cost:** Free (MIT).
- **Risks:** Low. Feature-rich and production-tested. The duplicate implementation (web server vs VS Code bridge) should be consolidated over time.

### ClawdHub (Community Registry)

- **Strengths:** Public API at `clawhub.ai`. Vector search, versioning (semver), download tracking, stars, security scanning. Open source (MIT). Already integrated.
- **Weaknesses:** API-only; no embeddable UI component. API rate limiting (60 req/min). Skills are OpenCode/OpenClaw-specific.
- **Integration effort:** Already done.
- **Cost:** Free.
- **Risks:** External dependency; API could change. However, the skill format is a simple SKILL.md + zip archive, so local caching provides resilience.

### npm Registry

- **Strengths:** Mature, reliable, CDN-backed. Versioning with semver.
- **Weaknesses:** Not designed for AI agent skills. No SKILL.md metadata concept. No catalog browsing UI for agent skills. No capability/description standardization.
- **Integration effort:** Medium. Would require adapting skill format to npm packages.
- **Cost:** Free for public packages.
- **Risks:** Misalignment with the skill specification. Agents don't use npm to load skills — they read SKILL.md files from disk.

## Recommendation

**Direction:** Adopt

The existing skills catalog implementation is comprehensive and meets all requirements. The ClawdHub integration provides community skill discovery, Git repository scanning provides custom source support, and the UI provides full browsing, search, installation, and management. The main improvement is consolidating the dual implementation paths (web server vs VS Code bridge) into a shared module.

## Sources of Information

- `packages/web/server/lib/skills-catalog/`: Server-side skill scanning, install, caching, and ClawdHub API integration.
- `packages/web/server/lib/skills-catalog/DOCUMENTATION.md`: Module docs with API surface and architecture.
- `packages/web/server/lib/opencode/skill-routes.js`: Server-side API routes for skills catalog endpoints.
- `packages/ui/src/stores/useSkillsStore.ts`: Client-side store for skill CRUD, file management, and config sync.
- `packages/ui/src/components/sections/skills/catalog/`: All catalog UI components (browse, search, install, conflicts).
- `packages/vscode/src/skillsCatalog.ts`: VS Code bridge skills catalog implementation with ClawdHub integration.
- `packages/vscode/src/bridge-config-runtime.ts:547-553`: API bridge wiring for skills catalog.
- ClawdHub API: `https://clawdhub.com/api/v1` (base URL for skill registry).

## Open Questions

1. Should the web server skills-catalog module be extracted into a shared package used by both web and VS Code to eliminate the dual implementation?
2. Should the catalog support a "featured" or "curated" section beyond the current sort-by-downloads from ClawdHub?

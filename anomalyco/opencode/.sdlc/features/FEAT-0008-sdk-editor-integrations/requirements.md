---
title: "SDK & Editor Integrations"
status: done
---

# Requirements: SDK & Editor Integrations

## Overview

OpenCode is consumable beyond its own frontends through a generated TypeScript SDK, a VSCode extension, MCP server integration, and a distributable CLI.
These surfaces let third-party tools, editors, and automation drive OpenCode sessions programmatically.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| SDK consumers | Typed client matching the server API |
| Editor users | First-class VSCode integration |
| MCP users | Compose OpenCode with other MCP-aware agents |
| CLI users | Installable, standalone executable |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a TypeScript SDK generated from the server routes via `./script/generate.ts`. |
| FR-02 | Must | The system shall provide a distributable CLI executable (`opencode`) built from the same entrypoint as `bun dev`. |
| FR-03 | Must | The system shall integrate MCP servers, including a catalog, auth, and an OAuth provider/callback flow. |
| FR-04 | Must | The system shall provide a VSCode editor extension. |
| FR-05 | Should | The system shall produce a single-asset standalone executable via `packages/opencode/script/build.ts --single`. |
| FR-06 | Should | The system shall expose Slack integration via the `packages/slack` package. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Compatibility | The SDK shall stay in lockstep with the server API by regeneration. |
| NFR-02 | Should | Security | MCP OAuth flows shall complete securely with callback handling. |

## Constraints

- The JS SDK lives in `packages/sdk/js`; the VSCode extension in `sdks/vscode`.
- MCP integration lives in `packages/opencode/src/mcp`.
- Regeneration is required after server route or SDK changes.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** the server routes
    - **When** `./script/generate.ts` runs
    - **Then** a typed TypeScript SDK is produced in `packages/sdk/js`
- [ ] **FR-03**
    - **Given** an MCP server requiring OAuth
    - **When** a session connects to it
    - **Then** the OAuth provider and callback flow completes and the server is usable
- [ ] **FR-04**
    - **Given** VSCode with the extension installed
    - **When** the user opens a project
    - **Then** OpenCode sessions are drivable from the editor

## Conflicts

None identified yet.

## Open Questions

1. What is the release and versioning policy for the generated SDK versus the VSCode extension?

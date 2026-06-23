---
title: "Extension and Skills Platform"
status: draft
---

# Requirements: Extension and Skills Platform

## Overview

The extension platform is how pi stays minimal while remaining extensible.
TypeScript extensions register custom tools, commands, event handlers, UI primitives, providers, and autocomplete; skills package on-demand capabilities via the Agent Skills standard; prompt templates offer reusable prompt snippets.
Together they let users and packages reshape nearly every part of the agent without forking the core.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Extension authors | A rich, stable `ExtensionAPI` and clear loading rules |
| Skills authors | A standard `SKILL.md` format and predictable invocation |
| End users | Safe, discoverable ways to add capabilities (install, trust) |
| Maintainers | A small, well-considered hook surface that does not bloat core |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall load TypeScript extensions via a default export `function (pi: ExtensionAPI)` using cached, lazy module loading. |
| FR-02 | Must | The system shall allow extensions to register and replace tools (built-ins included). |
| FR-03 | Must | The system shall allow extensions to register slash commands invoked as `/name`. |
| FR-04 | Must | The system shall provide event handlers for input, tool_call, tool_result, message lifecycle, turn/agent lifecycle, session lifecycle, compaction, provider request/response, project_trust, and resources_discover. |
| FR-05 | Must | The system shall allow extensions to render UI primitives: selectors, confirmations, inputs, notifications, status line, widgets, custom footer/header/editor/overlay, and raw terminal input. |
| FR-06 | Must | The system shall allow extensions to define keyboard shortcuts, CLI flags, autocomplete providers, and message renderers. |
| FR-07 | Must | The system shall allow extensions to perform session control actions (setActiveTools, setModel, setThinkingLevel, abort, compact, fork). |
| FR-08 | Must | The system shall load Agent Skills from `SKILL.md` files (global, project parent-walk, or packages), invoked as `/skill:name`, injected into the system prompt on demand. |
| FR-09 | Must | The system shall load prompt templates (Markdown with `{{variable}}` expansion) invoked as `/templatename`. |
| FR-10 | Must | The system shall load resources from global, project, and package sources with project-trust gating. |
| FR-11 | Should | The system shall support a package manager (`pi install/remove/update/list`) for distributing extensions, skills, prompts, and themes via npm or git. |
| FR-12 | Should | The system shall support custom providers via `~/.pi/agent/models.json` or extensions for custom APIs/OAuth. |
| FR-13 | May | The system shall allow extensions to register custom compaction and summarization behavior. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Project-sourced extensions shall not execute until a project-trust decision is recorded. |
| NFR-02 | Must | Reliability | Extension module loading shall be cached so a module is not re-evaluated per use. |
| NFR-03 | Must | Compatibility | The legacy pi-ai root API used by extensions shall be aliased to `/compat` at runtime so existing extensions keep working. |
| NFR-04 | Should | Maintainability | The hook surface shall be well-considered; new hooks require maintainer discussion to avoid unmaintainable complexity. |
| NFR-05 | Should | Performance | Extension event dispatch shall not block the agent loop on the happy path. |

## Constraints

- Extensions are TypeScript modules loaded via `jiti`.
- Skills follow the external Agent Skills standard (`agentskills.io`).
- New hooks that bloat core are rejected; the bar is "well considered and discussed".

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-02**
    - **Given** an extension calling `pi.registerTool(...)`
    - **When** the agent runs
    - **Then** the custom tool is available and may replace a built-in of the same name.
- [ ] **FR-04**
    - **Given** an extension with a `tool_call` handler
    - **When** a tool is invoked
    - **Then** the handler receives the call and may observe or mutate it.
- [ ] **FR-08**
    - **Given** a `SKILL.md` placed in a discoverable skills directory
    - **When** the user invokes `/skill:name`
    - **Then** the skill content is injected into the system prompt for that session.
- [ ] **FR-10**
    - **Given** an untrusted project with `.pi/` resources
    - **When** the agent starts
    - **Then** project-sourced extensions, skills, and prompts are not loaded until trust is granted.
- [ ] **NFR-01**
    - **Given** a project-sourced extension
    - **When** the project is not trusted
    - **Then** the extension's default export is never executed.
- [ ] **NFR-03**
    - **Given** an extension importing from the pi-ai root
    - **When** loaded after the `/compat` migration
    - **Then** the import resolves to the compat entrypoint without code changes.

## Conflicts

None identified yet.

## Open Questions

1. What is the stabilization criteria for the `ExtensionAPI` (currently documented in a 104KB extensions.md), and which parts are considered stable versus experimental?
2. How should extension-provided permissions/sandboxing hooks interact with the documented external-sandbox patterns?

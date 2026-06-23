---
title: "Extension and Skills Platform"
status: draft
---

# Specification: Extension and Skills Platform

## Overview

Three resource types extend pi: extensions (TypeScript modules), skills (`SKILL.md` packages), and prompt templates (`{{var}}` Markdown).
`DefaultResourceLoader` discovers them from global/project/package sources with trust gating; `ExtensionRunner` dispatches lifecycle and event hooks; skills and templates are injected into the system prompt on demand.

## Architecture

```
DefaultResourceLoader
  discover: global (~/.pi/agent, ~/.agents)
            project (.pi, .agents, AGENTS.md/CLAUDE.md) -- trust gated
            packages (installed)
        |
        v
+--------------------+   cached, lazy (jiti)
| Extension loader   |----> default export (pi: ExtensionAPI)
+---------+----------+
          |
          v
+--------------------+
| ExtensionRunner    |   lifecycle + event dispatch
| (on/emit hooks)    |   (input, tool_call, tool_result,
+--------------------+    message_*, session_*, provider_*, ...)
        |
        v
   AgentSession / InteractiveMode  (consume hooks, expose UI context)

Skills & Prompt Templates
  loaded on demand (/skill:name, /templatename)
  -> injected into system prompt or expanded into user message
```

## Data Models

### ExtensionAPI (excerpt)

| Capability | Method | Description |
|---|---|---|
| Tools | `registerTool`, `defineTool` | Add or replace tools |
| Commands | `registerCommand` | Add slash command `/name` |
| Events | `on(event, handler)` | Subscribe to lifecycle hooks |
| UI | `ExtensionUIContext` | Selectors, confirmations, inputs, widgets, overlays |
| Shortcuts | `ExtensionShortcut` | Register key bindings |
| Flags | `ExtensionFlag` | Register CLI flags |
| Session control | `ExtensionContextActions` | setActiveTools, setModel, compact, fork, abort |

### Event surface (categories)

| Category | Events |
|---|---|
| Input | `input` |
| Agent lifecycle | `before_agent_start`, `agent_start/end`, `turn_start/end` |
| Messages | `message_start/update/end` |
| Tools | `tool_call`, `tool_result` |
| Sessions | `session_start/shutdown`, `session_before_compact/compact/fork/switch/tree` |
| Provider | `before_provider_request`, `after_provider_response` |
| Context | `context`, `resources_discover`, `project_trust`, `user_bash` |

### Skill

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | from `/skill:` invocation | Skill identifier |
| path | string | file path | Location of `SKILL.md` |
| frontmatter | object | optional | Metadata |
| body | string | not null | Markdown injected into prompt |

## API Contracts

### /skill:name

Injects the skill's `SKILL.md` body into the system prompt context for the session.

### /templatename

Expands `{{variable}}` placeholders in the Markdown template into a user message.

### pi.install(name) / pi.remove(name) / pi.update(name)

Package manager operations over npm or git sources, resolving to resource directories (extensions, skills, prompts, themes, models).

## Sequences

### Tool call through extension hooks

```
agent -> tool_call event
  -> beforeToolCall (extension can {block: true})
  -> if not blocked: tool.execute(args)
     -> tool_execution_update events (extensions observe)
  -> afterToolCall (extension can override content/details/isError/terminate)
  -> tool_result event
```

### Resource discovery (trust-gated)

```
DefaultResourceLoader.discover()
  for each source (global, project, package):
    if project source and not trusted: skip
    collect extensions, skills, prompts, themes, context files
  -> resources_discover event (extensions may augment)
  -> registry populated
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Language | TypeScript via jiti | Type-safe, cached, lazy |
| Skills standard | Agent Skills (`SKILL.md`) | Cross-agent interoperability |
| Hook surface | Curated event taxonomy | Power without unbounded core growth |
| Trust model | Project sources gated | Prevent untrusted code execution by default |
| Compat alias | pi-ai root -> `/compat` | Existing extensions keep working |

## Risks and Unknowns

1. The `ExtensionAPI` is large and evolving; breaking changes affect the ecosystem.
2. Event handler ordering and interaction effects across multiple extensions can be hard to predict.
3. Project trust bypass (e.g. via a malicious package source) is a security risk to monitor.

## Out of Scope

- The core built-in tools and agent loop (FEAT-0002, FEAT-0004).
- Session persistence and branching (FEAT-0006).
- LLM provider auth internals (FEAT-0001).

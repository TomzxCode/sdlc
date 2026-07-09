---
title: "Plugin System"
status: draft
---

# Requirements: Plugin System

## Overview

Hermes has two plugin surfaces: general plugins (hooks, tools, CLI subcommands via PluginManager) and provider plugins (model providers, memory providers, context engines, image gen, TTS, transcription, web search, video gen). Plugins can ship in-tree under plugins/ or out-of-tree in ~/.hermes/plugins/ and pip entry points. The plugin system is the primary way to extend Hermes without modifying core files.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Third-party developers | Want to extend Hermes with custom tools, backends, or hooks without modifying core code |
| Power users | Want to install community plugins for additional capabilities |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | Plugins shall be discoverable from ~/.hermes/plugins/, ./.hermes/plugins/, and pip entry points |
| FR-2 | Must | Plugins shall support lifecycle hooks: pre_tool_call, post_tool_call, pre_llm_call, post_llm_call, on_session_start, on_session_end |
| FR-3 | Must | Plugins shall be able to register new tools via ctx.register_tool() |
| FR-4 | Must | Plugins shall be able to register CLI subcommands via ctx.register_cli_command() |
| FR-5 | Must | Model provider plugins shall use a separate lazy discovery system |
| FR-6 | Must | Memory provider plugins shall implement the MemoryProvider ABC |
| FR-7 | Should | PluginManager should support enabling/disabling plugins |
| FR-8 | Should | PluginManager should support plugin dependency resolution |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Isolation | Plugins must not modify core files (run_agent.py, cli.py, gateway/run.py, etc.) |
| NFR-2 | Must | Safety | A failing plugin hook must not crash the agent |
| NFR-3 | Should | Performance | Plugin discovery should complete in under 1 second |

## Constraints

- Plugins register with a `register(ctx)` function called at discovery time
- Model provider plugins must NOT be imported by the general PluginManager (would double-instantiate ProviderProfile)
- New in-tree memory providers and third-party product plugins are not accepted (policy)

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** a plugin installed in ~/.hermes/plugins/myplugin/
    - **When** the agent starts
    - **Then** the plugin is discovered and its register() function is called
- [ ] **FR-2**
    - **Given** a plugin that registers a pre_tool_call hook
    - **When** any tool is about to be called
    - **Then** the hook is invoked before the tool handler
- [ ] **FR-3**
    - **Given** a plugin that registers a new tool
    - **When** agent's tool schemas are collected
    - **Then** the plugin's tool schema appears in the tool definitions
- [ ] **NFR-1**
    - **Given** a plugin that attempts to modify cli.py
    - **When** the plugin is loaded
    - **Then** it must use ctx methods instead, and core files remain unchanged

## Conflicts

None identified yet.

## Open Questions

1. Should there be a plugin marketplace or catalog beyond the current discovery paths?
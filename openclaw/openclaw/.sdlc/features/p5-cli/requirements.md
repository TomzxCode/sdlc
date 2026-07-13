---
title: "Command-Line Interface"
status: done
---

# Requirements: Command-Line Interface

## Overview

The CLI is the primary way users interact with OpenClaw for administration, configuration, and operations. It provides commands for managing plugins, channels, models, sessions, configurations, credentials, and the gateway process itself.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Intuitive, well-documented CLI for daily operations |
| Operators | Scriptable interface for automation and integration |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The CLI shall support starting and stopping the gateway server |
| FR-2 | Must | The CLI shall provide commands for installing, listing, updating, and uninstalling plugins |
| FR-3 | Must | The CLI shall provide commands for managing channel configuration |
| FR-4 | Must | The CLI shall provide commands for viewing and editing configuration |
| FR-5 | Must | The CLI shall provide an onboarding wizard (`openclaw onboard`) for first-time setup |
| FR-6 | Must | The CLI shall provide a doctor command for diagnosing and fixing configuration issues |
| FR-7 | Must | The CLI shall support model configuration and provider authentication |
| FR-8 | Should | The CLI shall support viewing session history |
| FR-9 | Should | The CLI shall support credential management (API keys, auth profiles) |
| FR-10 | Should | The CLI shall provide shell completion (bash, fish, zsh) |
| FR-11 | May | The CLI shall provide a TUI for interactive sessions |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Usability | Help output shall be clear, structured, and include examples |
| NFR-2 | Must | Performance | CLI startup time shall be under 500ms for simple commands |
| NFR-3 | Should | Compatibility | CLI shall work on macOS, Linux, and Windows |

## Constraints

- The CLI binary is a single entry point (`openclaw.mjs`)
- Must work with Node.js 22.19+ (Node 24 recommended)
- Must support both interactive and non-interactive (scripted) modes

## Acceptance Criteria

- [ ] **FR-1**: Given the CLI, when the user runs `openclaw gateway start`, then the gateway process starts
- [ ] **FR-2**: Given the CLI, when the user runs `openclaw plugins list`, then installed plugins are displayed
- [ ] **FR-5**: Given the CLI, when the user runs `openclaw onboard`, then the setup wizard guides through configuration
- [ ] **FR-6**: Given the CLI, when the user runs `openclaw doctor`, then configuration issues are diagnosed
- [ ] **NFR-2**: Given the CLI, when the user runs `openclaw --version`, then the output appears within 500ms

## Conflicts

None identified yet.

## Open Questions

1. Should there be a REST API alternative to CLI commands for remote management?
2. What is the target help text quality standard?

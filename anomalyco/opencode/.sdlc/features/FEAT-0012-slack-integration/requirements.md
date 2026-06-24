---
title: "Slack Integration"
status: draft
---

# Requirements: Slack Integration

## Overview

The Slack Integration (`packages/slack`) connects OpenCode sessions to Slack conversations via a Slack bot built with `@slack/bolt`.
It lets users interact with OpenCode agents directly from Slack channels or DMs, bridging the terminal and collaborative chat environments.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Team users | Run OpenCode from Slack without leaving the chat |
| Slack workspace admins | Configure and manage the Slack bot install |
| Core team | Maintain the Slack integration package independently |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall provide a Slack bot that bridges OpenCode sessions into Slack conversations. |
| FR-02 | Must | The bot shall support sending prompts to OpenCode and receiving responses in Slack. |
| FR-03 | Should | The bot shall support slash commands for common OpenCode actions. |
| FR-04 | Should | The bot shall manage session lifecycle (start, list, reattach) from Slack. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | The bot shall handle Slack API rate limits and reconnection gracefully. |
| NFR-02 | Should | Security | The bot shall authenticate and scope access to authorized Slack users or channels. |

## Constraints

- The package lives at `packages/slack` and uses `@slack/bolt`.
- The bot requires a running OpenCode server or direct access to session runtime.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** the Slack bot is installed in a workspace
    - **When** a user sends a message to the bot
    - **Then** the message is forwarded to OpenCode and the response is returned in Slack
- [ ] **FR-03**
    - **Given** a user types `/opencode <prompt>` in a Slack channel
    - **When** the slash command is triggered
    - **Then** the bot responds with the OpenCode agent's output

## Conflicts

None identified yet.

## Open Questions

1. How should Slack sessions map to OpenCode sessions (1:1, or 1:N per channel)?
2. Should the bot support file uploads from Slack (images, documents)?

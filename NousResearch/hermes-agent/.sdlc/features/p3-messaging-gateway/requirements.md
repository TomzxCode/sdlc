---
title: "Messaging Gateway"
status: draft
---

# Requirements: Messaging Gateway

## Overview

The messaging gateway (gateway/run.py) is an asyncio-based service that runs the agent core across ~25 messaging platforms. Each platform has its own adapter (Telegram, Discord, Slack, Signal, WhatsApp, email, SMS, Matrix, Mattermost, WeChat, DingTalk, Feishu, QQ, IRC, Google Chat, Line, Teams, Simplex, and more) with consistent session lifecycle, slash command dispatch, approval flow, and restart/scale-to-zero support.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Messaging users | Interact with the agent from their preferred chat platform |
| Operators | Run the gateway as a persistent daemon; configure which platforms are active |
| Adapter developers | Easy-to-add platform adapters via a base class and minimal boilerplate |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The gateway shall support running the agent core across multiple messaging platforms simultaneously |
| FR-2 | Must | Each platform adapter shall handle platform-specific authentication, rate limiting, and message formatting |
| FR-3 | Must | The gateway shall support slash commands (/stop, /new, /queue, /status, /approve, /deny) that bypass the running agent |
| FR-4 | Must | The gateway shall support approval flow for potentially destructive agent actions |
| FR-5 | Must | The gateway shall support session management per platform (create, resume, list sessions) |
| FR-6 | Should | The gateway shall support stream dispatch for real-time message delivery |
| FR-7 | Should | The gateway shall support auto-restart and scale-to-zero for serverless operation |
| FR-8 | Should | The gateway shall support message mirroring across platforms |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Concurrency | The gateway shall handle messages from multiple platforms concurrently |
| NFR-2 | Must | Isolation | Each platform's session shall be isolated and not interfere with others |
| NFR-3 | Should | Availability | The gateway should recover from platform adapter crashes without affecting other platforms |

## Constraints

- Token locks prevent two agent profiles from using the same credential
- Gateway config is read from config.yaml (terminal.cwd for working directory, gateway settings)

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** the gateway is running with Telegram and Discord adapters enabled
    - **When** a user sends a message to the Telegram bot and another user sends a message to the Discord bot
    - **Then** both messages are processed independently
- [ ] **FR-2**
    - **Given** a Telegram adapter is configured with a bot token
    - **When** the gateway starts
    - **Then** the Telegram bot connects and shows as online
- [ ] **FR-3**
    - **Given** the agent is processing a request
    - **When** the user sends /stop
    - **Then** the agent loop is interrupted and the user receives confirmation

## Conflicts

None identified yet.

## Open Questions

1. Should there be a standard adapter template/scaffolding tool to reduce boilerplate for new platforms?
---
title: "Slack Integration"
status: done
---

# Specification: Slack Integration

## Architecture

```
Slack ──▶ Slack Bot (packages/slack/, @slack/bolt)
              │
              ▼
      OpenCode Session Runtime ──▶ Agent responses ──▶ Slack
```

The bot listens for events and commands from Slack, translates them into OpenCode session operations, and returns responses to the Slack conversation.

## Data Models

### SlackSessionMapping

| Field | Type | Constraints | Description |
|---|---|---|---|
| slack_channel | text | PK | Slack channel or DM ID |
| opencode_session_id | text | FK, not null | Mapped OpenCode session ID |

## API Contracts

The bot exposes Slack event handlers and slash commands; no public HTTP API beyond what Slack requires.

### Slash commands

- `/opencode <prompt>` — Send a prompt to the active OpenCode session
- `/opencode-sessions` — List active sessions

## Sequences

### Message flow

```
User sends DM to bot
Slack Events API -> bot handler
bot -> OpenCode session.prompt(message)
OpenCode streams response -> bot
bot posts response to Slack conversation
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | @slack/bolt | Official Slack SDK; event, command, and action support |
| Session mapping | Slack channel to OpenCode session ID | Simple 1:1 mapping for predictable behavior |
| Response mode | Ephemeral or in-channel via message metadata | Lets users choose visibility |

## Risks and Unknowns

1. Session-to-channel mapping persistence (in-memory vs database) is not yet specified.
2. Slack's 3000-character message limit may truncate long model responses.

## Out of Scope

- Full TUI-equivalent feature set (see FEAT-0004).
- Multi-user session management in Slack.

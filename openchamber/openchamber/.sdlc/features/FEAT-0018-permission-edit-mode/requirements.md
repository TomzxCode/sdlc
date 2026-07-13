---
title: "Permission / Edit Mode"
status: done
---

# Requirements: Permission / Edit Mode

## Overview

A permission request/response system where the AI asks for user approval before executing potentially dangerous operations (file writes, command execution). Includes per-session auto-accept toggle, edit mode controls, permission cards in chat, and toast notifications for pending permissions.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | Approve or deny AI actions before execution |
| Security-conscious users | Control which operations require approval |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display permission request cards in chat when the AI needs approval. |
| FR-02 | Must | The system shall support approve and deny actions on permission requests. |
| FR-03 | Must | The system shall support per-session auto-accept toggle for permissions. |
| FR-04 | Must | The system shall display toast notifications for pending permissions. |
| FR-05 | Should | The system shall show file write/create tool previews in permission cards. |
| FR-06 | Should | The system shall support auto-approve scoped to session tree (parent auto-accepts for children). |
| FR-07 | Should | The system shall display edit mode with visual color coding. |
| FR-08 | Must | The system shall default new agents to 'allow' as the global permission action, with runtime fallback to 'ask' when no explicit rules are configured. |
| FR-09 | Must | The system shall persist permissions at the agent level via OpenCode config layers and support per-session auto-accept toggling. |

## Acceptance Criteria

- [ ] FR-01: Given an AI tool call requiring permission, a card appears with approve/deny buttons
- [ ] FR-02: Given a permission card, clicking approve grants the action; clicking deny rejects it
- [ ] FR-03: Given auto-accept enabled, permissions are automatically approved
- [ ] FR-04: Given a permission request while the app is in the background, a toast appears
- [ ] FR-05: Given a file write permission, the card shows a preview of the changes
- [ ] FR-06: Given a session tree, enabling auto-accept on the parent session also auto-approves permissions for child sessions
- [ ] FR-07: Given edit mode enabled, the UI applies distinct visual color coding to differentiate it from read-only mode
- [ ] FR-08: Given a new agent with no explicit rules, runtime permission checks fall back to 'ask'; given a new agent's global default, it is set to 'allow'
- [ ] FR-09: Given permission changes for an agent, they persist across sessions via OpenCode config layers; given a session, auto-accept can be toggled independently

## Constraints

- Permissions are configured via OpenCode config layers

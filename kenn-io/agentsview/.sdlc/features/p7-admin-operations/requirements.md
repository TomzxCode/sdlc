---
title: "Admin & Operations"
status: done
---

# Requirements: Admin & Operations

## Overview

The admin and operations features cover secret scanning across session content, remote sync from other machines, export/import capabilities, AI-generated insights from session data, and self-update functionality. These features support day-to-day administration and data portability.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user | Export sessions, import from other tools, scan for leaked secrets |
| Operator | Remote sync from multiple machines, monitor for security issues |
| Security-conscious user | Detect accidentally committed API keys and tokens in session content |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall scan session content for secrets (API keys, tokens, passwords) using rule-based detection |
| FR-2 | Must | The system shall support session export as HTML |
| FR-3 | Must | The system shall support publishing sessions to GitHub Gists |
| FR-4 | Must | The system shall support importing from Claude.ai and ChatGPT exports |
| FR-5 | Must | The system shall support self-update via GitHub release check |
| FR-6 | Must | The system shall support remote sync from other machines via SSH |
| FR-7 | Should | The system shall support AI-generated insights (daily activity summaries, agent analysis) |
| FR-8 | Should | The system shall support session health grades (A-F) |
| FR-9 | Should | The system shall support session starring and pinning |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Security | Secrets scan results are stored locally and not sent externally |

## Acceptance Criteria

- [ ] **FR-1**
    - **Given** session content contains an API key pattern
    - **When** a secret scan is run
    - **Then** the finding is recorded and flagged in the UI
- [ ] **FR-3**
    - **Given** a session
    - **When** "Publish to Gist" is selected
    - **Then** the session is published as a GitHub Gist
- [ ] **FR-6**
    - **Given** a remote host is configured
    - **When** `agentsview sync --host <host>` is run
    - **Then** sessions from the remote host are synced

## Open Questions

1. What secret patterns should be included in the default ruleset?

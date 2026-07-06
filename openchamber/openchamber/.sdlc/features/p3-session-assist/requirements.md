---
title: "Session Assist (Recap and Suggestions)"
status: draft
---

# Requirements: Session Assist

## Overview

A server-side feature that generates a short recap of the AI agent's last reply and one suggested user follow-up after a session goes idle. The recap and suggestion are stored in the session metadata and rendered in the chat UI as a small spacer and tappable chip near the composer. This helps users quickly understand what just happened and what to do next.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Quick context recovery after stepping away from a session |
| Multi-taskers | Understand where each session left off without scrolling up |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall generate a recap of the agent's last reply and one suggested follow-up after a session transitions from busy to idle and stays quiet for 60 seconds. |
| FR-02 | Must | The system shall use the session's own provider/model for generation, falling back to a small model resolution if available. |
| FR-03 | Must | The system shall display the recap in a fixed-height gap under the last message. |
| FR-04 | Must | The system shall display the suggestion as a tappable chip near the composer. |
| FR-05 | Must | The system shall invalidate the recap and suggestion when a new message is sent, preventing stale suggestions. |
| FR-06 | Should | The system shall have a settings toggle to enable/disable session assist generation. |
| FR-07 | Should | The system shall clear the generation timer when the session becomes busy again or the user sends a message. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Performance | Small model generation shall complete within 5 seconds. |
| NFR-02 | Must | Reliability | A small model resolution failure shall not block the session or cause errors. |

## Acceptance Criteria

- [ ] FR-01: Given a session that transitions to idle for 60 seconds, a recap and suggestion are generated.
- [ ] FR-03: Given a generated recap, it appears in the chat UI below the last message.
- [ ] FR-04: Given a generated suggestion, a tappable chip appears near the composer.
- [ ] FR-05: Given a new user message, the recap and suggestion are hidden.
- [ ] FR-06: Given the setting is disabled, no generation occurs and existing payloads are not shown.

## Open Questions

1. Should suggestions be customizable per user or per agent?

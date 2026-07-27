---
title: "Session Goals (Autonomous Multi-Turn Execution)"
status: done
---

# Requirements: Session Goals

## Overview

An autonomous multi-turn execution system where a session works toward a user-defined objective without manual intervention. When a goal is set on a session, the system runs independent loops: the main AI agent works toward the objective while a small-model audit checks each turn for completeness, progress, and budget compliance. Goals persist across server restarts and continue even with the app closed. A goal strip in the UI shows progress with pause/resume controls.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Hands-free AI execution of complex multi-step tasks |
| Power users | Long-running autonomous sessions without constant attention |
| Teams | Auditable AI-driven task completion with progress tracking |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support setting an objective on a session via a goal payload stored under `metadata.openchamber.goal`. |
| FR-02 | Must | The system shall support inline objective text (up to 5000 characters) and external objective files. |
| FR-03 | Must | The system shall execute autonomous auto-continuations toward the objective without user input, capped at a configurable maximum (default 50 turns). |
| FR-04 | Must | The system shall run an independent audit after each auto-continuation using a small model to verify completeness, relevance, and progress. |
| FR-05 | Must | The system shall support goal status transitions: active, paused, blocked, budgetLimited, and complete. |
| FR-06 | Must | The system shall support an optional token budget with tracking of tokens used across segments. |
| FR-07 | Must | The system shall persist goals in session metadata so they survive server restarts. |
| FR-08 | Must | The system shall support pausing and resuming goal execution from the UI. |
| FR-09 | Must | The system shall display a goal progress strip in the chat UI with status, progress, and controls. |
| FR-10 | Must | The system shall stop goal execution when the audit fails consecutively (default 3 strikes) or the budget is exhausted. |
| FR-11 | Should | The system shall support configuring the audit small model independently from the main model. |
| FR-12 | Should | The system shall track token usage per segment and report cumulative consumption. |
| FR-13 | Should | The system shall support session compaction within goal loops while preserving goal metadata. |
| FR-14 | May | The system shall support goal templates with predefined objectives. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Reliability | Goal execution failure shall not corrupt session state or other sessions. |
| NFR-02 | Must | Reliability | Audit unavailability shall be handled gracefully with retry and eventual strike tracking. |
| NFR-03 | Must | Performance | Goal audit calls shall use the small model to minimize cost and latency. |
| NFR-04 | Should | Security | Token budget enforcement shall prevent runaway costs from unbounded execution. |
| NFR-05 | Should | Usability | The goal progress strip shall update within 2 seconds of status changes. |

## Acceptance Criteria

- [ ] FR-01: Given a session, the user sets an objective and the goal is stored in `metadata.openchamber.goal`
- [ ] FR-02: Given an objective file path, the system loads and uses the file content as the objective
- [ ] FR-03: Given an active goal, the system sends auto-continuations until the goal is complete or the turn cap is reached
- [ ] FR-04: Given an auto-continuation response, the audit evaluates it and produces a verdict
- [ ] FR-05: Given a paused goal, no further auto-continuations are sent until resumed
- [ ] FR-06: Given a token budget, the system enforces the limit and transitions to budgetLimited status
- [ ] FR-07: Given a server restart, active goals resume execution
- [ ] FR-08: Given a paused goal, the user can resume it from the UI
- [ ] FR-09: Given a goal strip, the UI displays goal status, progress note, and controls
- [ ] FR-10: Given 3 consecutive audit failures, the goal transitions to blocked status

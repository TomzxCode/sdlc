---
title: "Scheduled Tasks"
status: done
---

# Requirements: Scheduled Tasks

## Overview

Cron-based task scheduling that triggers AI prompts automatically at specified times. Supports locale-aware scheduling, per-task enable/disable, and integration with the desktop quit flow for safe shutdown.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Power users | Automate recurring AI tasks (daily summaries, scheduled reviews) |
| Teams | Schedule regular code review or documentation prompts |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support creating scheduled tasks with cron expressions. |
| FR-02 | Must | The system shall support per-task enable/disable. |
| FR-03 | Must | The system shall support locale-aware scheduling (timezone, weekday names). |
| FR-04 | Must | The system shall execute scheduled tasks by triggering an AI prompt. |
| FR-05 | Should | The system shall provide a task editor dialog with cron visualization. |
| FR-06 | Should | The system shall coordinate with desktop quit flow to prevent task interruption. |
| FR-07 | Must | The system shall silently skip missed scheduled tasks without catch-up; tasks only fire while the server is running. |
| FR-08 | Must | The system shall allow tasks to target specific agents and models via execution configuration. |

## Acceptance Criteria

- [ ] FR-01: Given the scheduled tasks dialog, the user creates a task with a cron expression
- [ ] FR-02: Given a scheduled task, the user can disable it without deleting it
- [ ] FR-03: Given a scheduled task, it respects the configured timezone and locale-aware settings including weekday names
- [ ] FR-04: Given a scheduled task fires, an AI session starts with the configured prompt
- [ ] FR-05: Given the scheduled tasks dialog, a task editor with cron visualization is provided
- [ ] FR-06: Given the desktop app quitting, scheduled task shutdown is coordinated to prevent interruption
- [ ] FR-07: Given a missed scheduled task, it is silently skipped without catch-up; tasks only fire while the server is running
- [ ] FR-08: Given a scheduled task, the user can target a specific agent and model via execution configuration

## Constraints

_No technical constraints remaining._

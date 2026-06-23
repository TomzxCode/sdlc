---
title: "Model Picker"
status: draft
---

# Requirements: Model Picker

## Overview

An organized model selection UI that categorizes available models by provider, supports favoriting/starred models, tracks recently used models, allows hiding unwanted models, and provides search/filter. Model selections persist per-session and per-agent.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| All users | Quickly switch between AI models during conversations |
| Power users | Manage favorites and hide irrelevant models |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall display available models organized by provider. |
| FR-02 | Must | The system shall support favoriting models for quick access. |
| FR-03 | Must | The system shall track recently used models. |
| FR-04 | Must | The system shall allow hiding unwanted models from the picker. |
| FR-05 | Must | The system shall support search/filter across all models. |
| FR-06 | Should | The system shall persist model selection per-session and per-agent. |
| FR-07 | Should | The system shall support favorite-model cycling via keyboard shortcuts. |
| FR-08 | Should | The system shall display model cost indicators and capability icons. |
| FR-09 | Must | The system shall source model capabilities and pricing data from the models.dev API via a server-side proxy, with fallback derivation from OpenCode SDK provider data for unsupported providers. |

## Acceptance Criteria

- [ ] FR-01: Given the model picker, models are grouped by provider with provider logos
- [ ] FR-02: Given a model, clicking the star icon adds it to favorites
- [ ] FR-03: Given the model picker, recently used models appear in a dedicated section
- [ ] FR-04: Given a model, the user can hide it from future display
- [ ] FR-05: Given the model picker, typing filters models by name
- [ ] FR-06: Given a session, the selected model persists when switching away and back; given an agent, the selected model persists across conversations
- [ ] FR-07: Given configured favorites, a keyboard shortcut cycles through them
- [ ] FR-08: Given the model picker, each model displays a cost indicator and capability icons
- [ ] FR-09: Given the model picker, model capabilities and pricing are fetched from the models.dev API; given an unsupported provider, data is derived from OpenCode SDK provider data instead

## Constraints

- Model data is fetched from the models.dev API via a server-side proxy endpoint

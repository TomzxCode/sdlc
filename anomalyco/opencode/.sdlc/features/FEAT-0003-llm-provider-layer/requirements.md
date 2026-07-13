---
title: "LLM Provider Layer"
status: done
---

# Requirements: LLM Provider Layer

## Overview

The LLM Provider Layer lets OpenCode talk to many model providers through a provider-neutral catalog and thin protocol adapters.
Provider/model metadata is data-driven via models.dev, so adding a provider should require little or no code.
It partitions provider-semantic model request options, provider-neutral generation controls, and compatibility wire fields.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Broad provider/model choice; stable behavior across providers |
| Contributors | Add providers via models.dev without code changes |
| Core team | Clean separation between catalog, protocol adapters, and session runner |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall maintain a catalog of models with provider-semantic model request options resolved from models.dev. |
| FR-02 | Must | The system shall partition model request options, generation controls, and compatibility request body fields into separate catalog domains. |
| FR-03 | Must | The system shall encode provider wire fields only in the selected protocol adapter, not in the session runner. |
| FR-04 | Must | The system shall support provider authentication including OAuth flows (e.g. Codex/GitHub Copilot, OpenAI, xAI, Cloudflare, Azure, DigitalOcean, Snowflake Cortex). |
| FR-05 | Must | The system shall map generation controls from the catalog into the LLM package's provider-option namespace. |
| FR-06 | Should | The system shall expose model status (available, deprecated, hidden) so the UI can filter models. |
| FR-07 | Should | The system shall preserve structured tool errors across provider round-trips. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Extensibility | New providers shall be addable via upstream metadata with no code change. |
| NFR-02 | Should | Reliability | Provider errors shall be classified and surfaced as retryable or terminal. |

## Constraints

- Provider support is data-driven through models.dev; contributors must PR models.dev first.
- A shared ingestion adapter partitions legacy and models.dev AI-SDK-shaped options before routing.
- A model/provider switch preserves the current context epoch and conversation history.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** models.dev metadata is available
    - **When** the catalog is built
    - **Then** models and their request options are resolvable per provider
- [ ] **FR-03**
    - **Given** a provider turn
    - **When** the request is encoded
    - **Then** wire encoding happens only in that provider's protocol adapter
- [ ] **FR-04**
    - **Given** a provider requiring OAuth
    - **When** the user authenticates
    - **Then** the flow completes and credentials are stored for that provider
- [ ] **NFR-01**
    - **Given** a new provider added to models.dev
    - **When** metadata is refreshed
    - **Then** the provider is usable without code changes in this repo

## Conflicts

None identified yet.

## Open Questions

1. How should deprecated or hidden models be surfaced to users who pinned them?

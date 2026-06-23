---
title: "LLM Provider Layer"
status: draft
---

# Specification: LLM Provider Layer

## Overview

A provider-neutral catalog holds models, generation controls, and request options.
The session runner maps catalog options into the LLM package's provider-option namespace, and the selected protocol adapter alone encodes provider wire fields.
Provider auth, model status, and structured tool errors are handled in dedicated modules.

## Architecture

```
models.dev metadata ─▶ ingestion adapter (partition legacy + AI-SDK shapes)
                              │
                              ▼
                       Catalog (3 domains)
            ┌──────────────────┼──────────────────────┐
            ▼                  ▼                      ▼
   model request opts    generation controls    compatibility fields
            │                  │                      │
            └────────▶ session runner maps to provider-option namespace
                              │
                              ▼
                  protocol adapter (per provider) ─▶ llm.stream()
                              │
                   auth.ts · model-status.ts · error.ts
```

## Data Models

### catalog_model

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Provider:model identifier |
| provider | text | not null | Owning provider |
| status | enum | not null | available, deprecated, hidden |
| request_options | json | not null | Provider-semantic options |
| generation | json | not null | Provider-neutral generation controls |

## API Contracts

### GET /provider?directory=\<resolve path\> -> Provider

Returns available providers and models for the resolved directory.

| Status | Code | Description |
|---|---|---|
| 200 | OK | Provider list returned |

## Sequences

### Model request resolution

```
session turn -> Catalog.resolve(model, variant)
Catalog -> model request options + generation controls
session runner -> map to provider-option namespace
protocol adapter -> encode wire fields -> llm.stream
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Provider data | models.dev upstream | Minimizes per-provider code |
| Option domains | Split request options, generation controls, compatibility | Keeps provider semantics out of session runner |
| Wire encoding | Protocol adapter only | Single owner of provider wire format |
| Switch behavior | Preserve context epoch and history | Mid-conversation model changes are non-disruptive |

## Risks and Unknowns

1. Legacy and models.dev AI-SDK-shaped options differ and require a partitioning ingestion adapter.
2. Some providers require exact structured tool round-trip payloads, constraining pruning and compaction.

## Out of Scope

- Session execution and provider turn scheduling (see FEAT-0001).
- Plugin-defined providers beyond the catalog (see FEAT-0007).

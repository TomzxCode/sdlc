---
title: "LLM Provider Abstraction"
status: done
---

# Specification: LLM Provider Abstraction

## Overview

`pi-ai` is a provider-centric LLM abstraction.
Each provider owns its model catalog, auth, and stream behavior and delegates to one of a small set of shared wire-protocol ("API") implementations.
A `Models` collection routes by provider, streams flow through a unified `AssistantMessageEventStream`, and SDKs load lazily on first use.

## Architecture

```
Consumer (Agent / SDK)
        |
        v
+-------------------+     routes by provider id
| Models collection |----+ (createModels / builtinProviders)
+-------------------+    |
                         v
              +-------------------+   owns auth + catalog
              |     Provider      |
              +---------+---------+
                        | delegates to
                        v
              +-------------------+   wire protocol
              |  API impl (lazy)  |   (anthropic-messages,
              +---------+---------+    openai-responses, ...)
                        | streams
                        v
              +-------------------+
              | AssistantMessage  |
              |   EventStream     |
              +-------------------+
```

## Data Models

### Provider

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | unique | Provider identifier (e.g. `anthropic`) |
| name | string | not null | Display name |
| baseUrl | string | optional | API base URL |
| auth | ProviderAuth | not null | API key and/or OAuth resolvers |
| models | Model[] | not null | Catalog of models |
| api | ApiFactory | not null | Wire-protocol factory |

### Model

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string | unique per provider | Model identifier |
| provider | string | FK -> Provider.id | Owning provider |
| contextWindow | number | not null | Max context tokens |
| pricing | object | optional | Input/output/cache cost per million tokens |
| reasoning | object | optional | Supported thinking levels and budgets |
| compat | object | optional | Provider compatibility flags |

### AssistantMessageEvent

| Field | Type | Constraints | Description |
|---|---|---|---|
| type | enum | not null | `start`, `text_*`, `thinking_*`, `toolcall_*`, `done`, `error` |
| partial | AssistantMessage | optional | Cumulative message at event time |
| contentIndex | number | optional | Associates delta with a content block |
| stopReason | enum | on done/error | `stop`, `length`, `toolCall`, `error`, `aborted` |

### Tool

| Field | Type | Constraints | Description |
|---|---|---|---|
| name | string | not null | Tool name |
| description | string | not null | LLM-facing description |
| parameters | TSchema (TypeBox) | not null | Serializable, self-validating schema |

## API Contracts

### Models.stream(model, context)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| model | Model | yes | Target model |
| context | Context | yes | System prompt, messages, tools, reasoning level |
| apiKey | ModelAuth | optional | Explicit auth override |

**Response**: an `AssistantMessageEventStream` (async iterable) whose `.result()` resolves to the final `AssistantMessage`.

**Error contract**: failures are encoded as a final event with `stopReason: "error" \| "aborted"` and `errorMessage`; the function never throws.

### Models.refresh()

Resolves the latest catalogs/auth; returns a promise. Synchronous readers (`getModels`/`getModel`) return last-known data without awaiting.

## Sequences

### Streaming a prompt

```
Consumer -> Models: stream(model, context)
Models -> Provider: resolve auth (store first, then ambient)
Provider -> API impl: lazy-load SDK, open stream
API impl -> Consumer: AssistantMessageEventStream
loop: yield start/text_delta/toolcall_delta ... done|error
Consumer awaits stream.result() -> AssistantMessage
```

### OAuth token refresh (double-checked locking)

```
Request -> resolveStoredOAuth: token expired?
  yes -> acquire credentials.modify lock
       -> re-check expiry (another request may have refreshed)
       -> if still expired: refresh once, persist
       -> release lock
  no  -> use cached token (zero locks)
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Routing unit | Provider (not API) | A provider owns auth + catalog; multiple providers share one wire protocol |
| SDK loading | Lazy via `.lazy.ts` wrappers | Keeps import side-effect-free and startup fast |
| Failure model | Encoded in stream | Callers always get a stream object; no try/catch around the call |
| Schema library | TypeBox | JSON-serializable, self-validating, works across providers |
| Sync vs async reads | Sync last-known + explicit `refresh()` | Avoids blocking the agent loop on network |

## Risks and Unknowns

1. The `/compat` entrypoint duplicates the provider-centric API; its removal depends on the coding-agent `ModelManager` migration completing.
2. Generated catalogs depend on live upstream APIs (models.dev, OpenRouter, Vercel); outages during generation could stall releases.
3. Provider-specific compatibility quirks (token counting, cache headers, thinking-level support) require ongoing manual overrides in the generator.

## Out of Scope

- The agent loop and tool execution (FEAT-0002).
- Session persistence, compaction, and branching (FEAT-0006).
- The TUI and interactive experience (FEAT-0003, FEAT-0004).

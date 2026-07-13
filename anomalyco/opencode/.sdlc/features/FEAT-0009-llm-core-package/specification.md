---
title: "LLM Core Package"
status: done
---

# Specification: LLM Core Package

## Architecture

```
Caller ──▶ Route (provider-agnostic interface)
               │
               ▼
        Protocol (wire encoding strategy: chat, responses, messages, gemini)
               │
               ▼
        Endpoint (HTTP transport, streaming, retries)
               │
               ▼
        Auth (credential resolution, token management)
               │
               ▼
        Framing (request/response shaping, tool dispatch)
               │
               ▼
        Provider Adapter (OpenAI, Anthropic, Google, Bedrock, Azure, ...)
```

The package exposes a clean layered architecture where each layer has a single responsibility, and all types are defined via Effect Schema for structural validation.

## Data Models

### LLMRequest

| Field | Type | Constraints | Description |
|---|---|---|---|
| model | text | not null | Provider:model identifier |
| messages | array | not null | Chronological message list |
| tools | array | nullable | Available tool definitions |
| generation | object | nullable | Generation controls (temperature, top_p, etc.) |
| options | object | nullable | Provider-semantic request options |

### LLMResponse

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | text | PK | Response identity |
| content | array | not null | Message content parts |
| tool_calls | array | nullable | Structured tool call list |
| finish_reason | enum | not null | stop, length, tool_calls, error |

## API Contracts

The package exposes an Effect-based `llm.stream(request)` function and internal route/protocol/endpoint/auth modules.
No external HTTP API; consumers call the Effect functions directly.

## Sequences

### Stream a completion

```
Caller -> route.resolve(provider, model)
route -> protocol.chat.encode(request)  (or .responses, .messages, .gemini)
protocol -> endpoint.stream(encoded_request, auth)
endpoint -> stream chunks -> protocol.decode(chunk)
protocol -> structured LLMResponse parts -> caller
```

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Architecture | Route / Protocol / Endpoint / Auth / Framing | Clean separation; each layer independently testable |
| Type system | Effect Schema | Built-in validation, decoding, and JSON serialization |
| Streaming | Pull-based Effect Stream | Composable with Effect's streaming ecosystem |
| Provider data | In-package adapters | No external dependency on models.dev; loaded from package metadata |

## Risks and Unknowns

1. The legacy AI SDK provider path must coexist during gradual migration; double-maintenance burden until migration completes.
2. Provider-specific wire differences (e.g., structured tool round-trip payloads) may constrain the protocol abstraction.

## Out of Scope

- Session runtime integration (see FEAT-0001).
- Provider catalog from models.dev (see FEAT-0003).

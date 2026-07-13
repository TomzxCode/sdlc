---
title: "LLM Provider Abstraction"
status: done
---

# Requirements: LLM Provider Abstraction

## Overview

`pi-ai` provides a single unified API for chat and image generation across 30+ LLM providers, abstracting away differences in wire protocols, authentication, streaming formats, tool-calling schemas, and token/cost accounting.
Consumers (the agent runtime, the coding agent, and third-party SDK users) program against one `Models` collection and one event-stream contract instead of per-provider SDKs.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Agent runtime (pi-agent-core) | A stable `StreamFn` contract and message types to drive the agent loop |
| Coding agent (pi-coding-agent) | Broad provider coverage, automatic auth resolution, and a model catalog |
| SDK / extension authors | A clean public API to register custom providers and models |
| End users | Access to their chosen model and subscription with minimal setup |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall expose a `Models` collection that routes model lookups and streams by owning provider. |
| FR-02 | Must | The system shall support the major wire protocols: Anthropic Messages, OpenAI Responses, OpenAI Completions, Google Generative AI, Google Vertex, Mistral Conversations, and Bedrock Converse Stream. |
| FR-03 | Must | The system shall stream assistant responses as an async-iterable event stream emitting `start`, text/thinking/toolcall deltas, `done`, and `error` events. |
| FR-04 | Must | The system shall encode all stream failures as terminal events with `stopReason: "error" \| "aborted"` and never throw out of a stream. |
| FR-05 | Must | The system shall resolve provider authentication via a credential store first (OAuth or API key), falling back to ambient env-var resolution only when nothing is stored. |
| FR-06 | Must | The system shall support OAuth flows (PKCE and device code) for subscription-based providers. |
| FR-07 | Must | The system shall represent tool definitions and tool calls using TypeBox schemas that are serializable and self-validating. |
| FR-08 | Must | The system shall lazily load provider SDKs on first request rather than at import time. |
| FR-09 | Must | The system shall generate its model catalog (`models.generated.ts`) from live upstream sources (models.dev, OpenRouter, Vercel AI Gateway), filtering to tool-capable models. |
| FR-10 | Should | The system shall track token usage and cost per request. |
| FR-11 | Should | The system shall support cross-provider handoffs, converting thinking blocks from foreign providers into tagged text. |
| FR-12 | Should | The system shall provide per-provider compatibility flags (e.g. `OpenAICompletionsCompat`) auto-detected from baseUrl and overridable per model. |
| FR-13 | Should | The system shall provide a `faux` in-memory provider for deterministic testing. |
| FR-14 | May | The system shall provide an image-generation API (`ImagesModels`) parallel to the chat API. |
| FR-15 | May | The system shall preserve a deprecated `/compat` entrypoint for the legacy global API during migration. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Compatibility | The root `index.ts` shall be side-effect free. |
| NFR-02 | Must | Performance | Synchronous model reads (`getModels`, `getModel`) shall return last-known data without awaiting; `refresh()` shall be the explicit async verb. |
| NFR-03 | Must | Reliability | OAuth token refresh shall use double-checked locking so concurrent requests refresh at most once. |
| NFR-04 | Must | Security | The system shall not silently fall back to ambient auth after a failed stored-credential refresh. |
| NFR-05 | Should | Performance | SDK loading shall not block stream creation; setup may run behind a lazily returned stream. |
| NFR-06 | Should | Maintainability | Provider factories shall be thin wrappers over a shared `createProvider` helper. |

## Constraints

- Only tool-call-capable models are cataloged.
- Generated files (`models.generated.ts`, `*.models.ts`) must never be hand-edited.
- Erasable TypeScript syntax only; ESM only; Node `>=22.19.0`.

## Acceptance Criteria

Every FR and NFR shall have at least one acceptance criterion.

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-01**
    - **Given** a `Models` collection with multiple registered providers
    - **When** a consumer requests a model by `provider/id`
    - **Then** the owning provider resolves the model and its stream behavior.
- [ ] **FR-03**
    - **Given** a configured provider and a prompt
    - **When** the consumer calls the stream function
    - **Then** it receives an `AssistantMessageEventStream` yielding ordered text/thinking/toolcall deltas and a terminal `done` event.
- [ ] **FR-04**
    - **Given** a provider request that fails mid-stream
    - **When** the failure occurs
    - **Then** the stream emits an `error` event with partial content and a `stopReason` of `error` or `aborted` instead of throwing.
- [ ] **FR-05**
    - **Given** a provider with both a stored credential and an ambient env var
    - **When** auth is resolved
    - **Then** the stored credential is used and the env var is ignored.
- [ ] **FR-07**
    - **Given** a tool defined with a TypeBox parameter schema
    - **When** the provider returns a tool call
    - **Then** the arguments are parsed and available for validation without provider-specific handling.
- [ ] **FR-08**
    - **Given** a fresh process importing the root entrypoint
    - **When** no request has been made
    - **Then** no provider SDK (`@anthropic-ai/sdk`, `openai`, etc.) is loaded.
- [ ] **FR-09**
    - **Given** the model generator
    - **When** run via `npm run generate-models`
    - **Then** per-provider `*.models.ts` files and the aggregator `models.generated.ts` are written, containing only tool-capable models.
- [ ] **NFR-01**
    - **Given** a consumer importing the root `index.ts`
    - **When** the import completes
    - **Then** no provider factories, generated catalogs, or OAuth implementations have executed as side effects.
- [ ] **NFR-03**
    - **Given** an expired OAuth token and concurrent requests
    - **When** both attempt to refresh
    - **Then** exactly one network refresh occurs and both requests use the refreshed token.

## Conflicts

None identified yet.

## Open Questions

1. What is the timeline and completion criteria for retiring the `/compat` entrypoint once coding-agent's `ModelManager` migration finishes?
2. Which providers, if any, are considered tier-1 (must-ship) versus community-maintained for the purposes of future feature work?

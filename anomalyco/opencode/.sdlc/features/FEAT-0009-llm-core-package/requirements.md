---
title: "LLM Core Package"
status: draft
---

# Requirements: LLM Core Package

## Overview

The LLM Core Package (`packages/llm`) provides a standalone, Effect Schema-first LLM abstraction that can be used independently of the rest of OpenCode.
It defines a route/protocol/endpoint/auth/framing architecture for provider-agnostic LLM calls, with provider adapters for OpenAI, Anthropic, Google, Bedrock, Azure, and others.
The package publishes as `@opencode-ai/llm` and has no dependency on `packages/opencode` or `packages/core`.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| LLM package consumers | Provider-agnostic LLM calls with a clean schema-first API |
| Core team | Clear separation from the session runtime; independent versioning |
| Provider adapter authors | Stable contract for adding new providers |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The package shall define a route/protocol abstraction that isolates provider wire encoding from the caller. |
| FR-02 | Must | The package shall support multiple provider protocols: chat, responses, messages, and gemini. |
| FR-03 | Must | The package shall include provider adapters for OpenAI, Anthropic, Google, Bedrock, Azure, and other major providers. |
| FR-04 | Must | The package shall implement a tool dispatch mechanism for converting LLM tool calls into bounded results. |
| FR-05 | Must | The package shall use Effect Schema for all type definitions, ensuring structured validation at boundaries. |
| FR-06 | Should | The package shall be publishable as a standalone npm package with no dependency on OpenCode internals. |
| FR-07 | Should | The package shall expose provider auth configuration and credential management. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Extensibility | Adding a new provider shall require only a new adapter module without changing the core protocol. |
| NFR-02 | Must | Correctness | Provider wire encoding shall be deterministic and schema-validated. |
| NFR-03 | Should | Compatibility | The package shall coexist with the legacy AI SDK provider path during migration. |

## Constraints

- The package lives at `packages/llm` and is built with Effect, Effect Schema.
- Provider protocol adapters live alongside the package; no external plugin mechanism for protocols.
- The package must not depend on `packages/opencode` or `packages/core`.

## Acceptance Criteria

- [ ] **FR-01**
    - **Given** a provider protocol is selected
    - **When** a request is encoded
    - **Then** the wire format matches the provider's expected schema
- [ ] **FR-03**
    - **Given** provider adapters for OpenAI, Anthropic, Google, Bedrock, and Azure
    - **When** each is instantiated with valid credentials
    - **Then** a streaming LLM call completes successfully
- [ ] **FR-06**
    - **Given** the package is built
    - **When** published to npm as `@opencode-ai/llm`
    - **Then** consumers can install and use it independently
- [ ] **NFR-01**
    - **Given** a new provider adapter is added
    - **When** it implements the route/protocol contract
    - **Then** no changes to the core protocol or existing adapters are required

## Conflicts

None identified yet.

## Open Questions

1. How should the LLM package migration from the legacy AI SDK path be coordinated across providers?
2. Should provider auth live in this package or remain in `packages/opencode/src/provider/`?

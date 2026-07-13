---
title: "LLM Provider Abstraction"
status: done
---

# Test Plan: LLM Provider Abstraction

## Scope

Covers `pi-ai` provider abstraction, streaming, auth, token tracking, model catalog generation, and cross-provider compatibility. Does not cover agent loop, session, or TUI.

## Unit Tests

Test files under `packages/ai/test/` cover:
- Provider factories and auth resolution (providers.test.ts, oauth-auth.test.ts, oauth-device-code.test.ts, env-api-keys.test.ts, google-vertex-api-key-resolution.test.ts)
- Streaming protocol (stream.test.ts, anthropic-sse-parsing.test.ts, openai-completions-*.test.ts, openai-responses-*.test.ts)
- Tool calling (tool-call-id-normalization.test.ts, tool-call-without-result.test.ts, deferred-tools.test.ts)
- Token/cost tracking (tokens.test.ts, total-tokens.test.ts, cache-retention.test.ts, anthropic-cache-write-1h-cost.test.ts)
- Model catalog (providers.test.ts, firework-models.test.ts, together-models.test.ts, bedrock-models.test.ts, xiaomi-models.test.ts)
- Cross-provider handoff (cross-provider-handoff.test.ts)
- Error handling (error-body.test.ts, provider-error-body-passthrough.test.ts, retry.test.ts, abort.test.ts)
- Image support (image-tool-result.test.ts, images.test.ts, images-models.test.ts)
- Compatibility (compat-env.test.ts, anthropic-eager-tool-input-compat.test.ts, anthropic-temperature-compat.test.ts)
- OAuth flows (oauth-auth.test.ts, oauth-device-code.test.ts, github-copilot-oauth.test.ts, openai-codex-oauth.test.ts, anthropic-oauth.test.ts)
- Lazy loading (lazy-module-load.test.ts)
- Context overflow (context-overflow.test.ts, overflow.test.ts)
- Thinking/reasoning (anthropic-adaptive-thinking-models.test.ts, anthropic-force-adaptive-thinking.test.ts, max-thinking.test.ts, google-thinking-disable.test.ts, mistral-reasoning-mode.test.ts)
- Various provider-specific compat (bedrock-*.test.ts, google-*.test.ts, azure-openai-base-url.test.ts, node-http-proxy.test.ts)

## Integration Tests

E2E tests with live provider credentials (enabled when env vars are present) cover real streaming, auth, and tool-calling flows (anthropic-eager-tool-input-e2e.test.ts, anthropic-long-cache-retention-e2e.test.ts, openai-responses-reasoning-replay-e2e.test.ts, openai-codex-stream.test.ts, bedrock-thinking-payload.test.ts).

## Edge Cases and Failure Scenarios

- Surrogate pairs in messages (unicode-surrogate.test.ts)
- Provider error body passthrough (provider-error-body-passthrough.test.ts, provider-error-body-regression.test.ts)
- Cache retention edge cases (cache-retention.test.ts)
- Empty tool results (openai-responses-empty-tool-result.test.ts)
- Partial JSON cleanup (openai-responses-partial-json-cleanup.test.ts)
- Various compat shims (anthropic-empty-thinking-signature-compat.test.ts, anthropic-tool-name-normalization.test.ts)

## Test Infrastructure

- Faux provider (`providers/faux.ts`) for deterministic, network-free testing
- Model registry with mock/stub providers
- OAuth test server for device code and PKCE flow testing

## Coverage Matrix

| Requirement | Test Files |
|---|---|
| FR-01 (Models collection routing) | providers.test.ts, models-runtime.test.ts |
| FR-02 (Wire protocol support) | stream.test.ts, various anthropic/openai/bedrock/google test files |
| FR-03 (Event stream) | stream.test.ts |
| FR-04 (Failure encoding) | error-body.test.ts, retry.test.ts, abort.test.ts |
| FR-05 (Auth resolution) | oauth-auth.test.ts, env-api-keys.test.ts, compat-env.test.ts |
| FR-06 (OAuth flows) | oauth-auth.test.ts, oauth-device-code.test.ts |
| FR-07 (TypeBox tool schemas) | tool-call-id-normalization.test.ts, validation.test.ts |
| FR-08 (Lazy SDK loading) | lazy-module-load.test.ts |
| FR-09 (Model catalog generation) | providers.test.ts, bedrock-models.test.ts, firework-models.test.ts |
| FR-10 (Token/cost tracking) | tokens.test.ts, total-tokens.test.ts |
| FR-11 (Cross-provider handoff) | cross-provider-handoff.test.ts |
| FR-12 (Compat flags) | various anthropic/openai compat test files |
| FR-13 (Faux provider) | faux-provider.test.ts |
| FR-14 (Image generation) | images.test.ts, images-models.test.ts |
| FR-15 (/compat entrypoint) | compat-env.test.ts |
| NFR-01 (Side-effect free root) | lazy-module-load.test.ts |
| NFR-02 (Sync reads, async refresh) | models-runtime.test.ts |
| NFR-03 (Double-checked OAuth locking) | oauth-auth.test.ts |

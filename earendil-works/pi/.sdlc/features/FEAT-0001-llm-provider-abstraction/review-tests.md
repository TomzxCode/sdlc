---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf83564ffeJkfsdtD7ujGCkN
---

# Review: tests (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

Every test file the plan names exists under `packages/ai/test/`. The drift is in the other direction: the plan does not mention the suites that materially cover parts of the feature.

## Sync drift: 2026-10-19

### The telemetry suites are not referenced
- **Severity:** blocking
- **Evidence:** `packages/ai/test/telemetry.test.ts` exercises `AI_TELEMETRY_SCHEMA`, `observeModelRequest`, span and metric emission, setup failures, and the no-op default. `packages/ai/test/telemetry-options.test.ts` covers the `telemetry` option across the request surfaces and asserts the `telemetryContext` rename has no compatibility alias (`packages/ai/test/telemetry-options.test.ts:75-76`).
- **Artifact says:** The plan has no telemetry line in any section, and the Coverage Matrix has no telemetry row.
- **Required change:** Add both suites to the Unit Tests section and add a Coverage Matrix row for the telemetry requirement.

### The model-type split and catalog-shape suites are not referenced
- **Severity:** blocking
- **Evidence:** `packages/ai/test/model-types.test.ts`, `packages/ai/test/model-catalog-types.test.ts`, `packages/ai/test/classifier-models.test.ts`, and `packages/ai/test/models-entry.test.ts` cover the `Model` / `ImageModel` / `ClassifierModel` split, the typed catalog accessors, and the `./models` entrypoint (`packages/ai/src/types.ts:875-898`, `packages/ai/src/model-catalog.ts`).
- **Artifact says:** The plan mentions `images-models.test.ts` and `models-runtime.test.ts` but not the model-type discrimination suites, and the Coverage Matrix has no row for the model type split.
- **Required change:** Add these four suites and a Coverage Matrix row for the model type split and the `./models` entrypoint.

### The catalog generation integrity suites are not referenced
- **Severity:** blocking
- **Evidence:** `packages/ai/test/model-data-validation.test.ts` exercises the manifest, the schema version, the model-id assertions, and the hydration path of `packages/ai/scripts/model-data.ts`. `packages/ai/test/generate-models-strict.test.ts` runs the generator in an isolated package root and asserts it fails before mutating generated data.
- **Artifact says:** The Coverage Matrix maps FR-09 to "providers.test.ts, bedrock-models.test.ts, fireworks-models.test.ts", which are provider catalog reads, not the generation pipeline.
- **Required change:** Map FR-09 to `model-data-validation.test.ts` and `generate-models-strict.test.ts`, and add them to the Model catalog section of the plan.

### The image and classifier API suites are not referenced
- **Severity:** blocking
- **Evidence:** `packages/ai/test/llama-cpp-classify.test.ts`, `packages/ai/test/openai-decisions.test.ts`, `packages/ai/test/typesafe-system-one.test.ts`, `packages/ai/test/cloudflare-workers-ai-system-one.test.ts`, `packages/ai/test/openrouter-images.test.ts`, `packages/ai/test/pi-messages.test.ts`, and `packages/ai/test/image-model-data.test.ts` are the only coverage of the `KnownImageApi` and `KnownClassifierApi` protocols and of the `pi-messages` chat API (`packages/ai/src/types.ts:61-85`).
- **Artifact says:** The plan's FR-02 row is "stream.test.ts, various anthropic/openai/bedrock/google test files". None of the seven files above is named anywhere in the plan.
- **Required change:** Name these suites in the Unit Tests section and split the FR-02 row so the chat, image, and classifier API families each point at their own suites.

### The event stream suite is not referenced
- **Severity:** blocking
- **Evidence:** `packages/ai/test/event-stream.test.ts` covers `AssistantMessageEventStream` ordering, buffering, and end semantics (`packages/ai/src/utils/event-stream.ts`), which is the contract behind FR-03 and FR-04.
- **Artifact says:** The Coverage Matrix maps FR-03 to "stream.test.ts" and FR-04 to "error-body.test.ts, retry.test.ts, abort.test.ts".
- **Required change:** Add `event-stream.test.ts` to the FR-03 and FR-04 rows and to the Streaming protocol section.

### The per-provider OAuth suites are not referenced
- **Severity:** advisory
- **Evidence:** `packages/ai/test/openai-chatgpt-oauth.test.ts`, `packages/ai/test/openrouter-oauth.test.ts`, `packages/ai/test/xai-oauth.test.ts`, `packages/ai/test/meta-oauth.test.ts`, `packages/ai/test/kimi-coding-oauth.test.ts`, `packages/ai/test/radius-oauth.test.ts`, and `packages/ai/test/oauth-callback-server.test.ts` cover the 9 OAuth-capable providers (`packages/ai/src/auth/oauth/`) and the shared callback server.
- **Artifact says:** The OAuth flows section lists only `oauth-auth.test.ts`, `oauth-device-code.test.ts`, `github-copilot-oauth.test.ts`, `openai-codex-oauth.test.ts`, and `anthropic-oauth.test.ts`. The FR-06 row lists only the first two.
- **Required change:** Add the remaining OAuth suites and point the FR-06 row at them.

### `cross-provider-handoff.test.ts` is filed as a unit test but is a live E2E test
- **Severity:** advisory
- **Evidence:** `packages/ai/test/cross-provider-handoff.test.ts:28-31` imports `completeSimple` from `../src/compat.ts` and calls real providers, gated on the presence of provider credentials.
- **Artifact says:** The plan lists it under "Unit Tests" as "Cross-provider handoff (cross-provider-handoff.test.ts)" and does not list it in the Integration Tests section.
- **Required change:** Move it to the Integration Tests section.

### Other material suites are not referenced
- **Severity:** advisory
- **Evidence:** The following suites exist under `packages/ai/test/` and are absent from the plan: `constrained-sampling.test.ts` (FR-12), `compat-schema.test.ts`, `system-message-replay.test.ts`, `transcript-tool-changes.test.ts`, `transform-messages-cross-model-thinking.test.ts` and `transform-messages-copilot-openai-to-anthropic.test.ts` (FR-11), `provider-retry.test.ts`, `context-estimate.test.ts`, `json-parse.test.ts`, `fetch-option.test.ts`, `model-cost-tiers.test.ts`, `reasoning-options.test.ts`, `sampling-options.test.ts`, `supports-xhigh.test.ts`, `xhigh.test.ts`, `message-types.test.ts`, `lax-message-content.test.ts`, `pre-generation-error.test.ts`, `uuid.test.ts`, `empty.test.ts`, `responseid.test.ts`, `interleaved-thinking.test.ts`, `zen.test.ts`, `google-thinking-level-map.test.ts`, `anthropic-federation.test.ts`, `anthropic-federation-sdk.test.ts`, `qwen-token-plan-models.test.ts`, `zai-coding-plan-models.test.ts`, `baseten-models.test.ts`, and `fireworks-model-generation.test.ts`.
- **Artifact says:** The plan's per-area lists cover a subset of the package's suites and stop there.
- **Required change:** Extend the per-area lists so the plan names every suite that materially covers the feature, and add the missing Coverage Matrix rows for constrained sampling, thinking levels, and model pricing tiers.

## Open questions

- None. Every suite named above exists in `packages/ai/test/`.

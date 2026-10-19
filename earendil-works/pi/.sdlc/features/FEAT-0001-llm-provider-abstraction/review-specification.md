---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf83564ffeJkfsdtD7ujGCkN
---

# Review: specification (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### The Provider data model does not match the `Provider` interface
- **Severity:** blocking
- **Evidence:** `packages/ai/src/models.ts:157-246` — the `Provider` interface has no `models` field and no `api` field. It exposes `id`, `name`, `baseUrl?`, `headers?`, `auth`, the methods `getModels()` (line 179), `getAllModels?()` (line 187), `refreshModels?()` (line 195), `filterModels?()` (line 202), `filterAllModels?()` (line 209), `stream()` (line 215), `streamSimple()` (line 221), `fetchDeferred?()` (line 226), `cancelDeferred?()` (line 231), `generateImages?()` (line 234), and `classify?()` (line 241). The API implementation is supplied to `createProvider()` (`packages/ai/src/models.ts:1016-1058`) and the model carries the api id (`packages/ai/src/types.ts:828`).
- **Artifact says:** The Provider table lists `models | Model[] | not null` and `api | ApiFactory | not null`.
- **Required change:** Replace the Provider table with the interface above: the catalog is a synchronous `getModels()` method, the wire protocol is chosen by `model.api` against the `api`/`images`/`classifiers` maps passed to `createProvider()`, and the optional dynamic-catalog and credential-filter hooks must be listed.

### The Model data model uses the wrong field names and types
- **Severity:** blocking
- **Evidence:** `packages/ai/src/types.ts:825-872` — `BaseModel` carries `id`, `name`, `api`, `provider`, `baseUrl`, `input`, `inputLimits?`, `cost` (type `ModelCost`), `headers?`. `Model` adds `type?: "chat"`, `reasoning: boolean`, `thinkingLevelMap?`, `promptCache?`, `contextWindow`, `maxTokens`, `samplingParams?`, `samplingParamsByThinkingLevel?`, `compat?`. The pricing structure is `ModelCost` (`packages/ai/src/providers/model-schema.ts:96`), and thinking levels are carried by `thinkingLevelMap` and `samplingParamsByThinkingLevel`, not by a `reasoning` object.
- **Artifact says:** The Model table lists `pricing | object | optional` and `reasoning | object | optional | Supported thinking levels and budgets`.
- **Required change:** Rename `pricing` to `cost` and type it `ModelCost`. Change `reasoning` to the boolean it is, and describe `thinkingLevelMap`, `samplingParamsByThinkingLevel`, and `promptCache` as the thinking-level and cache structures. Add the missing `name`, `api`, `baseUrl`, `input`, `maxTokens`, `samplingParams`, and `headers` fields.

### The three model types and the API unions are absent
- **Severity:** blocking
- **Evidence:** `packages/ai/src/types.ts:875-898` defines `ImageModel` (`type: "image"`, with `output: ("text" | "image")[]`), `ClassifierModel` (`type: "classifier"`), and the `ModelTypeMap` / `ModelType` / `AnyModel` types, plus the helpers `getModelType` and `isModelType` in `packages/ai/src/models.ts`. `packages/ai/src/types.ts:61-85` defines `KnownApi` (10 ids), `KnownImageApi` (`openrouter-images`), and `KnownClassifierApi` (4 ids).
- **Artifact says:** The Data Models section defines one flat `Model` type and never mentions image models, classifier models, or the API id unions.
- **Required change:** Add the `Model` / `ImageModel` / `ClassifierModel` split with `ModelTypeMap`, and list the three API unions. The specification must state that the model `type` field selects which `Models` operation accepts the entry.

### The `stopReason` enum does not match the code
- **Severity:** blocking
- **Evidence:** `packages/ai/src/types.ts:474` — `export type StopReason = "pending" | "stop" | "length" | "toolUse" | "error" | "aborted" | "deferred";`. The same seven values are the `stop` attribute values of the telemetry schema (`packages/ai/src/telemetry.ts:19`).
- **Artifact says:** The AssistantMessageEvent table lists `stopReason | enum | on done/error | stop, length, toolCall, error, aborted`.
- **Required change:** Replace the enum with `pending | stop | length | toolUse | error | aborted | deferred`. `toolCall` is not a value; the tool-call stop reason is `toolUse`.

### The `Models` collection surface is mostly undocumented
- **Severity:** blocking
- **Evidence:** `packages/ai/src/models.ts:257-366` defines the `Models` interface with `getProviders`, `getProvider`, `getModels`, `getModel`, `getModelsOfType`, `getModelOfType`, `getAllModels`, `refresh`, `checkAuth`, `getAvailable`, `getAvailableOfType`, `getAllAvailable`, `getAuth`, `login`, `logout`, `stream`, `complete`, `streamSimple`, `completeSimple`, `streamDeferred`, `fetchDeferred`, `cancelDeferred`, `generateImages`, and `classify`. `packages/ai/src/models.ts:1012` exports `createModels()` returning a `MutableModels` (`packages/ai/src/models.ts:368-373`, with `setProvider`, `deleteProvider`, `clearProviders`). `packages/ai/src/models.ts:1061` exports `createProvider()`. `packages/ai/src/models-store.ts:22-26` defines `ModelsStore` and lines 28-40 define `InMemoryModelsStore`, and `CreateModelsOptions` (`packages/ai/src/models.ts:375-379`) accepts `credentials`, `modelsStore`, and `authContext`.
- **Artifact says:** The API Contracts section documents only `Models.stream(model, context)` and `Models.refresh()`. The Architecture diagram names `createModels` and `builtinProviders` in passing but no contract is given.
- **Required change:** Add the collection construction contract (`createModels(options)` returning `MutableModels`, `createProvider(options)` returning `Provider`, `ModelsStore` as the catalog persistence seam, `CreateModelsOptions`), the auth operations (`checkAuth`, `getAuth`, `login`, `logout`), the availability readers (`getAvailable`, `getAvailableOfType`, `getAllAvailable`), the type-scoped readers (`getModelsOfType`, `getModelOfType`, `getAllModels`), and the request operations (`complete`, `streamSimple`, `completeSimple`, `streamDeferred`, `fetchDeferred`, `cancelDeferred`, `generateImages`, `classify`).

### The `Models.refresh()` contract is wrong
- **Severity:** blocking
- **Evidence:** `packages/ai/src/models.ts:287` — `refresh(options?: ModelsRefreshOptions): Promise<ModelsRefreshResult>`. `packages/ai/src/models.ts:560-620` refreshes only providers that implement `refreshModels` (line 566-569), so static built-in providers are no-ops. Provider failures are collected into the returned `errors` map instead of rejecting (lines 597-604, 619), and the result also carries `aborted`. The method does not refresh auth, it only reads the stored credential to decide whether a network fetch may run (line 589).
- **Artifact says:** "Resolves the latest catalogs/auth; returns a promise. Synchronous readers (`getModels`/`getModel`) return last-known data without awaiting."
- **Required change:** State that `refresh()` targets configured dynamic providers only, accepts `providers`, `allowNetwork`, `force`, and `signal`, returns `ModelsRefreshResult` with `aborted` and a per-provider `errors` map instead of rejecting, and does not refresh auth. Keep the statement that the synchronous readers return last-known data.

### The telemetry contract and instrumentation point are missing
- **Severity:** blocking
- **Evidence:** `packages/ai/src/telemetry.ts:63-104` defines `AI_TELEMETRY_SCHEMA` at version 1 with the spans `pi.ai.request` and `pi.ai.poll` (lines 66-67), the events `pi.ai.first_chunk` and `pi.ai.block` (lines 40-54), and the metrics `pi.ai.request.duration`, `pi.ai.first_chunk.duration`, `pi.ai.tokens`, `pi.ai.cost` (lines 70-103). `packages/ai/src/telemetry.ts:120-208` implements `observeModelRequest` as a `LazyStreamObserver`, attached at the `Models` layer only (`packages/ai/src/models.ts:901,922,949`), so direct provider and API calls are not instrumented. The parent span travels in `StreamOptions.telemetry?: TelemetrySpan` (`packages/ai/src/types.ts:159-160`).
- **Artifact says:** The specification has no telemetry section, and the `Models.stream` request table lists only `model`, `context`, and `apiKey`.
- **Required change:** Add a telemetry section covering the schema version, the spans, the events, the metrics, the `Models`-layer instrumentation point, and the content-free attribute policy. Add `telemetry?: TelemetrySpan` to the `Models.stream` request table, and note that the option was renamed from `telemetryContext` with no compatibility alias (`packages/ai/CHANGELOG.md:7`, `packages/ai/test/telemetry-options.test.ts:75-76`).

### The `pi-ai` command line is undocumented
- **Severity:** blocking
- **Evidence:** `packages/ai/package.json:51-53` declares the `pi-ai` binary, and `packages/ai/src/cli.ts:84-118` implements `login [provider]` and `list` over the 9 OAuth-capable providers (`packages/ai/src/cli.ts:10-13`). The credential is written to `auth.json` in the working directory (`packages/ai/src/cli.ts:9,28-30,75-78`).
- **Artifact says:** The specification does not mention a command line.
- **Required change:** Add the CLI to the API contracts: the two commands, the provider list they cover, and the credential file they write.

### The generated catalog pipeline is undocumented
- **Severity:** blocking
- **Evidence:** `packages/ai/scripts/generate-models.ts:3457-3594` writes the gitignored `src/providers/data/<id>.json` plus `.manifest.json` (line 3492, gitignored at `.gitignore:11`), the committed `src/providers/<id>.models.ts` shards (lines 3539-3541), and the committed aggregator `src/models.generated.ts` (lines 3549-3576), which exports `MODELS`, `IMAGE_MODELS`, and `CLASSIFIER_MODELS` (`packages/ai/src/models.generated.ts:47,135,223`). `packages/ai/src/models.generated.ts:1-2` and `AGENTS.md:28` forbid hand edits. `packages/ai/scripts/check-model-data.ts` validates the manifest and the data files, and `packages/ai/package.json` runs `npm run generate-models` at the start of `build`.
- **Artifact says:** The specification has no section on catalog generation, and Risks item 2 only says "Generated catalogs depend on live upstream APIs (models.dev, OpenRouter, Vercel)".
- **Required change:** Add a section describing the three output artifacts, which of them are gitignored and build-time, which are committed, the validation step, and the rule that `models.generated.ts` must never be hand-edited.

### The OAuth refresh sequence omits the validity window
- **Severity:** advisory
- **Evidence:** `packages/ai/src/auth/resolve.ts:102` sets `DEFAULT_OAUTH_MINIMUM_VALIDITY_MS` to five minutes, and `packages/ai/src/auth/resolve.ts:169-175` refreshes whenever the token expires within that window, not only when it is already expired. The refresh itself runs inside a `credentials.modify` transaction (`packages/ai/src/auth/resolve.ts:132-146`), which is the store lock the sequence refers to.
- **Artifact says:** The sequence reads "resolveStoredOAuth: token expired?".
- **Required change:** Say "token expires within five minutes" and name the `credentials.modify` transaction as the lock.

### The `Context` description includes a field it does not have
- **Severity:** advisory
- **Evidence:** `packages/ai/src/types.ts:771-775` — `Context` is `{ systemPrompt?: string; messages: Message[]; tools?: Tool[] }`. The reasoning level is a request option (`packages/ai/src/types.ts:372` `SimpleStreamOptions.reasoning`), not part of the context.
- **Artifact says:** The `Models.stream` request table describes `context` as "System prompt, messages, tools, reasoning level".
- **Required change:** Drop "reasoning level" from the `Context` description.

### The `Models.stream` request table mis-types `apiKey` and omits the request options
- **Severity:** advisory
- **Evidence:** `packages/ai/src/types.ts:161` — `apiKey?: string`. `packages/ai/src/types.ts:157-262` — `ProviderRequestOptions` and `StreamOptions` also carry `signal`, `telemetry`, `fetch`, `env`, `headers`, `timeoutMs`, `maxRetries`, `maxRetryDelayMs`, `onPayload`, `onResponse`, `onProviderStreamEvent`, `temperature`, `samplingParams`, `maxTokens`, `transport`, `cacheRetention`, `sessionId`, `websocketConnectTimeoutMs`, and `metadata`. `packages/ai/src/models.ts:119-122` adds `transformHeaders`.
- **Artifact says:** The request table lists `apiKey | ModelAuth | optional | Explicit auth override`.
- **Required change:** Type `apiKey` as `string` and list the request options that a consumer can set, at least `signal`, `telemetry`, `headers`, `env`, `fetch`, and `transformHeaders`.

## Open questions

- None. Every claim above is answered by the code.

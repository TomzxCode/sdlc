---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eaaf83564ffeJkfsdtD7ujGCkN
---

# Review: requirements (sync drift 2026-10-19)

The artifact drifted from the code during the `/sync-sdlc` full sync on 2026-10-19.

## Sync drift: 2026-10-19

### FR-11 states the opposite of the implemented cross-provider thinking rule
- **Severity:** blocking
- **Evidence:** `packages/ai/src/api/transform-messages.ts:128-138` — a thinking block whose `provider`/`api`/`model` do not match the target model is dropped, not converted. `packages/ai/test/transform-messages-cross-model-thinking.test.ts:40` asserts "does not send another model's readable thinking as text". `packages/ai/CHANGELOG.md` (1.3.0, Changed) records the switch: "Changed model switching to drop thinking blocks from earlier assistant messages produced by a different model, instead of sending them as plain text."
- **Artifact says:** FR-11: "The system shall support cross-provider handoffs, converting thinking blocks from foreign providers into tagged text."
- **Required change:** FR-11 must state that a thinking block produced by a different provider/api/model is dropped from the replayed transcript, while text blocks and tool calls are kept, tool call ids are normalized, and `thoughtSignature` is stripped on foreign tool calls (`packages/ai/src/api/transform-messages.ts:140-165`).

### FR-14 names an API that no longer exists
- **Severity:** blocking
- **Evidence:** `packages/ai/README.md:1862` — "The separate `ImagesModels`/`ImagesProvider` collection that existed briefly (`createImagesModels()`, `createImagesProvider()`, `openrouterImagesProvider()`, `builtinImagesModels()`) is gone: image models now live on the regular provider." No `ImagesModels` symbol exists under `packages/ai/src/`. The live surface is `Models.generateImages` (`packages/ai/src/models.ts:354`) and `Models.getModelOfType("image", ...)` (`packages/ai/src/models.ts:277`).
- **Artifact says:** FR-14: "The system shall provide an image-generation API (`ImagesModels`) parallel to the chat API."
- **Required change:** FR-14 must state that image models are ordinary provider models with `type: "image"` (`packages/ai/src/types.ts:875-879`), reached through `Models.getModelOfType("image", provider, id)` and executed through `Models.generateImages(model, context, options)`, and that a provider declares image support through the `images` map of `createProvider()` (`packages/ai/src/models.ts:1048`).

### No requirement covers the telemetry contract
- **Severity:** blocking
- **Evidence:** `packages/ai/src/telemetry.ts:63-104` defines `AI_TELEMETRY_SCHEMA` at version 1 with spans `pi.ai.request` and `pi.ai.poll` (lines 66-67), events `pi.ai.first_chunk` and `pi.ai.block` (lines 40-54), and metrics `pi.ai.request.duration`, `pi.ai.first_chunk.duration`, `pi.ai.tokens`, `pi.ai.cost` (lines 70-103). `packages/ai/src/models.ts:901,922,949` attach `observeModelRequest` at the `Models` layer for `stream`, `streamSimple`, and `streamDeferred`. `packages/ai/src/telemetry.ts:127,150` read the parent span from `options.telemetry`. The package depends on `@earendil-works/pi-telemetry` (`packages/ai/package.json` dependencies).
- **Artifact says:** The requirements contain no telemetry requirement, and the acceptance criteria list no telemetry criterion.
- **Required change:** Add a requirement (and at least one acceptance criterion) for opt-in request tracing: `AI_TELEMETRY_SCHEMA` version 1, the two spans, the two events, the four metrics, the `Models`-layer instrumentation point, and the rule that no prompt, completion, reasoning, or tool-argument content is recorded (`packages/ai/src/telemetry.ts:40-54`, `packages/ai/README.md:1106`).

### No requirement covers the `pi-ai` command line
- **Severity:** blocking
- **Evidence:** `packages/ai/package.json:51-53` declares `bin: { "pi-ai": "dist/cli.js" }`. `packages/ai/src/cli.ts:84-118` implements `login [provider]` and `list`, and `packages/ai/src/cli.ts:10-13` restricts both to the 9 OAuth-capable providers. `packages/ai/README.md:1818-1820` documents `npx @earendil-works/pi-ai login` and `npx @earendil-works/pi-ai list`.
- **Artifact says:** The requirements contain no requirement for the `pi-ai` binary.
- **Required change:** Add a requirement for the `pi-ai` CLI: `login [provider]` runs the provider's OAuth flow and writes the credential to `auth.json` in the working directory, `list` prints the OAuth-capable providers, and the command surface is limited to those two commands.

### FR-02 omits one implemented wire protocol
- **Severity:** blocking
- **Evidence:** `packages/ai/src/types.ts:79-83` — `KnownClassifierApi` is `typesafe-system-one`, `cloudflare-workers-ai-system-one`, `llama-cpp-classify`, and `openai-decisions`. `packages/ai/src/api/openai-decisions.ts` implements the last one, and `packages/ai/test/openai-decisions.test.ts` covers it.
- **Artifact says:** FR-02 lists "Typesafe System-One, OpenRouter Images, and llama.cpp classification" as the last supported protocols, which is 14 of the 15 implemented APIs.
- **Required change:** FR-02 must include the `openai-decisions` classifier API, and should state the three separate API families (10 chat APIs from `KnownApi` at `packages/ai/src/types.ts:61-71`, 1 image API from `KnownImageApi` at line 75, 4 classifier APIs from `KnownClassifierApi` at lines 79-83).

### FR-09 describes only one of the three generated catalog artifacts
- **Severity:** blocking
- **Evidence:** `packages/ai/scripts/generate-models.ts:3457-3594` writes three artifact groups: the gitignored per-provider JSON under `src/providers/data/` plus `.manifest.json` (line 3492, gitignored at `.gitignore:11`), the committed per-provider shards `src/providers/<id>.models.ts` (lines 3539-3541), and the committed aggregator `src/models.generated.ts` (lines 3549-3576). `packages/ai/src/models.generated.ts:1-2` carries the "auto-generated / Do not edit manually" header, and `AGENTS.md:28` forbids hand edits. `packages/ai/package.json` runs `npm run generate-models` as the first step of `build`.
- **Artifact says:** FR-09: "The system shall generate its model catalog (`models.generated.ts`) from live upstream sources (models.dev, OpenRouter, Vercel AI Gateway), filtering to tool-capable models." The FR-09 acceptance criterion says only "per-provider `*.models.ts` files and the aggregator `models.generated.ts` are written".
- **Required change:** FR-09 and its acceptance criterion must name all three outputs, mark `src/providers/data/` as gitignored and build-time only, and state that `models.generated.ts` and `*.models.ts` must never be hand-edited.

### The provider count in the overview is imprecise
- **Severity:** advisory
- **Evidence:** `packages/ai/src/providers/all.ts:4-46` imports 42 provider factories, and `packages/ai/src/types.ts:87-129` lists the same 42 ids in `KnownProvider`. 9 of them are OAuth-capable (`packages/ai/src/providers/anthropic.ts`, `github-copilot.ts`, `kimi-coding.ts`, `meta.ts`, `openai.ts`, `openai-codex.ts`, `openrouter.ts`, `radius.ts`, `xai.ts`).
- **Artifact says:** The overview says "across 30+ LLM providers".
- **Required change:** State the exact count (42 built-in providers) and, if useful, the 9 OAuth-capable subset.

### FR-05 omits the explicit-override step of the auth order
- **Severity:** advisory
- **Evidence:** `packages/ai/src/auth/resolve.ts:56-68` resolves `options.apiKey` first, then the stored credential (lines 70-87), then ambient sources (lines 89-92).
- **Artifact says:** FR-05: "The system shall resolve provider authentication via a credential store first (OAuth or API key), falling back to ambient env-var resolution only when nothing is stored."
- **Required change:** FR-05 should state the full order: explicit `apiKey` override, then the stored credential, then ambient env vars.

## Open questions

- None. Every claim above is answered by the code.

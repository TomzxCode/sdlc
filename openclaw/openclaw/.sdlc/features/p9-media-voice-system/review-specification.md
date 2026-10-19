---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Media and Voice System specification

## Sync drift: 2026-10-19

### The architecture diagram has no place for media understanding (blocking)

- Evidence: `specification.md:12-30`, `src/media-understanding/` (90 files), `packages/media-understanding-common/` (12 files), `src/media/` (116 files), `src/link-understanding/` (7 files)
- Artifact says: the diagram has exactly two cores, "Media Generation Core" over `src/media-generation`, `src/image-generation`, `src/video-generation`, `src/music-generation`, and "Voice/Audio Core" over `src/tts`, `src/talk`, `src/realtime-transcription`, `src/meeting-bot` (specification.md:12-30).
- Code: a third subsystem exists with its own core, a shared package, and a shared media runtime. The diagram also does not show that `src/media/` is the shared runtime underneath attachment, audio, image, and document handling, nor that `src/link-understanding/` fetches and injects link content into inbound context.
- Blocking: the diagram is the reader's map of the feature, and the feature's own FR-8 has no representation in it.

### The voice call plugin is presented as a provider plugin, not a product surface (blocking)

- Evidence: `specification.md:24-29`, `extensions/voice-call/src/tool-schema.ts:33-67`, `extensions/voice-call/src/call-brief.ts`, `extensions/voice-call/src/call-delivery-runtime.ts`, `extensions/voice-call/src/realtime-call-control.ts`, `extensions/voice-call/src/cli.ts`, `extensions/voice-call/src/config.ts`, `extensions/voice-call/src/manager/`, `extensions/voice-call/src/webhook/`
- Artifact says: the diagram places `extensions/voice-call/` in the "Provider Plugins (ElevenLabs, Deepgram, Azure, ...)" column under "Voice/Audio Core" (specification.md:24-29).
- Code: the voice call plugin is a telephony product with its own agent tool, six Gateway RPC methods, a CLI, a call manager, a webhook and tunnel layer, a realtime call control layer, a per-call brief contract, a call delivery pipeline, and its own configuration blocks. It is not a speech or transcription provider.
- Blocking: a reader would look for a provider adapter where a whole product surface lives.

### The API contracts section omits the tool and RPC surface (blocking)

- Evidence: `specification.md:51-53`, `extensions/voice-call/src/tool-schema.ts:33-67`, `extensions/voice-call/README.md:249-269`, `src/agents/tools/image-generate-tool.ts:264`, `src/agents/tools/video-generate-tool.ts:314`, `src/agents/tools/music-generate-tool.ts:112`, `src/agents/tools/tts-tool.ts:40`
- Artifact says: "Media and voice capabilities are exposed as agent tools through the tool system, not as standalone HTTP endpoints." (specification.md:53)
- Code: the statement is true but now too thin to be useful. The shipped tool surface is `image_generate`, `video_generate`, `music_generate`, `tts`, and the plugin-provided `voice_call` tool with seven actions, plus a family of `voicecall.*` Gateway RPC methods and an `openclaw voicecall` CLI.
- Blocking: the section that should record the public contract names none of it, so the artifact gives a reader no way to know what the surface looks like.

### The `TTSRequest` data model does not match the shipped request types (blocking)

- Evidence: `specification.md:43-49`, `src/tts/provider-types.ts:20-50`, `src/tts/tts-types.ts:12-29`, `src/tts/tts-request.ts:24-40`
- Artifact says: "`TTSRequest` | text | string | not null | Text to synthesize / voice | string | optional | Voice identifier / provider | string | optional | Provider override" (specification.md:45-49).
- Code: there is no `TTSRequest` type. The shipped types are `SpeechSynthesisRequest` in `src/tts/provider-types.ts`, which carries `text`, `cfg`, `providerConfig`, `target` (`audio-file`, `voice-note`, or `telephony`), and directive overrides; and `ResolvedTtsConfig` in `src/tts/tts-types.ts`, which carries `auto`, `mode`, `provider`, `providerSource`, `persona`, `personas`, `summaryModel`, `modelOverrides`, `providerConfigs`, `prefsPath`, `maxTextLength`, `timeoutMs`, and `timeoutMsSource`. Voice selection is a persona or directive concern, not a request field.
- Blocking: the artifact documents a type that does not exist with fields that do not exist.

### The `MediaGenerationRequest` data model does not match the shipped request types (blocking)

- Evidence: `specification.md:36-41`, `src/media-generation/runtime-shared.ts:46-60`, `src/image-generation/types.ts:57-75`, `packages/media-generation-core/src/model-ref.ts`, `grep -rn "MediaGenerationRequest" src/ packages/ extensions/` finds no type declaration
- Artifact says: "`MediaGenerationRequest` | prompt | string | not null / provider | string | optional / options | Record<string, unknown> | optional / stream | boolean | optional" (specification.md:38-41).
- Code: no `MediaGenerationRequest` type exists. The per-capability request types do, starting with `ImageGenerationRequest` in `src/image-generation/types.ts:57-75`, which carries `provider`, `model`, `prompt`, `cfg`, `agentDir`, `authStore`, `timeoutMs`, `count`, `size`, `aspectRatio`, `resolution`, `quality`, `outputFormat`, `background`, `inputImages`, `providerOptions`, and `ssrfPolicy`. The shared generation runtime takes a request with `cfg`, `agentDir`, `modelOverride`, and `autoProviderFallback` and resolves a capability of `image`, `music`, or `video` against a capability model reference. There is no `stream` flag.
- Blocking: the artifact documents a type that does not exist with fields that do not exist.

### The provider plugin lists are incomplete (advisory)

- Evidence: `specification.md:16-29`, `extensions/fish-audio-speech/`, `extensions/gradium/`, `extensions/inworld/`, `extensions/muse/`, `extensions/omlx/`, `extensions/senseaudio/`, `extensions/tts-local-cli/`, `extensions/azure-speech/`, `extensions/teams-meetings/`, `extensions/zoom-meetings/`, `extensions/google-meet/`
- Artifact says: the diagram names Fal, Comfy, Runway, Pixverse, Senseaudio, ElevenLabs, Deepgram, Azure Speech, tts-local-cli, and voice-call (specification.md:16-29).
- Code: the plugin set also includes fish-audio-speech, gradium, inworld, muse, omlx, and the three meeting providers google-meet, zoom-meetings, and teams-meetings. The meeting providers are not represented in the diagram at all, even though `src/meeting-bot` is listed as a core.
- Advisory.

### The technical decision on voice modality does not cover the realtime call path (advisory)

- Evidence: `specification.md:57-61`, `src/talk/talk-session-controller.ts`, `src/talk/exact-speech-protocol.ts`, `extensions/voice-call/src/realtime-voice.runtime.ts`
- Artifact says: "| Voice modality | Talk runtime with session management | Full-duplex voice conversation requires session state |" (specification.md:61).
- Code: the full-duplex conversation also runs through the voice call plugin realtime path, with its own session control, audio pacer, and playback modules under `extensions/voice-call/src/webhook/`.
- Advisory.

### The risk list omits provider and media runtime risks (advisory)

- Evidence: `specification.md:63-66`, `extensions/voice-call/src/tunnel.ts`, `extensions/voice-call/src/webhook-security.ts`, `extensions/voice-call/src/webhook-replay.ts`, `src/media/ffmpeg-exec.ts`, `src/media/ffmpeg-limits.ts`
- Artifact says: the risks are "Quality varies significantly across providers for the same prompt" and "Voice call reliability depends on provider WebSocket stability" (specification.md:65-66).
- Code: the voice call plugin also carries a public webhook surface that needs signature verification, replay protection, and an exposure tunnel, and the media runtime shells out to ffmpeg with explicit limits.
- Advisory.

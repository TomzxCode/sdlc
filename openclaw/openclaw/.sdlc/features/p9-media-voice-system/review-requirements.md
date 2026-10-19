---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Media and Voice System requirements

## Sync drift: 2026-10-19

### FR-6 omits the voice call capability set that shipped (blocking)

- Evidence: `extensions/voice-call/src/call-brief.ts`, `extensions/voice-call/src/call-brief-schema.ts`, `extensions/voice-call/src/call-delivery.ts`, `extensions/voice-call/src/call-delivery-runtime.ts`, `extensions/voice-call/src/realtime-call-control.ts`, `extensions/voice-call/src/webhook/realtime-call-session-control.ts`, `extensions/voice-call/src/tool-schema.ts:33-67`, `extensions/voice-call/src/config.ts`, `extensions/voice-call/README.md:113-223`, `CHANGELOG/2026.10.5.md:10`
- Artifact says: "FR-6 | Must | The system shall support voice call initiation and management through provider integrations" (requirements.md:29).
- Code: the voice call plugin now implements per-call briefs, call reports, live transcript delivery, live steering, inbound callbacks, and voicemail detection, on top of initiation and continuation. The `voice_call` agent tool exposes seven actions (`initiate_call` with a `brief`, `steer_call`, `continue_call`, `speak_to_user`, `send_dtmf`, `end_call`, `get_status`), and the plugin adds six `voicecall.*` Gateway RPC methods, an `openclaw voicecall` CLI, and four new configuration blocks (`reports`, `live`, `callbacks`, `voicemail`) plus `inboundPolicy`. The release notes announce the same set.
- Blocking: a reader would believe voice calls are limited to placing a call and speaking, which misrepresents a user-visible agent tool surface and its configuration contract.

### FR-8 has no implementation inside this feature's scope (blocking)

- Evidence: `.sdlc/sync-meta.yml` p9 code index lists `src/media-generation/`, `src/image-generation/`, `src/video-generation/`, `src/music-generation/`, `src/tts/`, `src/talk/`, `src/realtime-transcription/`, `src/meeting-bot/`, `extensions/elevenlabs/`, `extensions/deepgram/`, `extensions/talk-voice/`, `extensions/voice-call/`, `src/media-understanding/` (90 files), `packages/media-understanding-common/` (12 files), `src/media/` (116 files), `src/link-understanding/` (7 files)
- Artifact says: "FR-8 | Should | The system shall support media understanding (describe, analyze, transcribe media content)" (requirements.md:31) and the overview claims "creation, understanding, and playback of media content through a unified media generation and understanding framework" (requirements.md:10).
- Code: media understanding is implemented in `src/media-understanding/`, its shared types in `packages/media-understanding-common/`, the shared media runtime in `src/media/`, and link fetching in `src/link-understanding/`. None of those paths are in this feature's scope, and no other feature in `.sdlc/features/` claims media understanding.
- Blocking: the requirement is assigned to a feature that does not own the implementation, so the requirement has no verifiable home.
- Boundary note: this is the strongest candidate for a separate new feature directory.

### FR-10 understates the meeting bot subsystem (advisory)

- Evidence: `src/meeting-bot/` (107 files), `src/meeting-bot/node-host.ts`, `src/meeting-bot/browser-controller.ts`, `src/meeting-bot/meeting-modes.ts`, `extensions/google-meet/`, `extensions/zoom-meetings/`, `extensions/teams-meetings/`, `src/state/openclaw-state-schema.sql` tables `meeting_transcript_sessions`, `meeting_transcript_utterances`, `meeting_transcript_summaries`
- Artifact says: "FR-10 | Should | The system shall support meeting bot integration (Google Meet, Zoom, Teams)" (requirements.md:33).
- Code: the meeting bot also owns a browser controller, a node host, meeting modes, and a durable meeting transcript store with speaker-labelled utterances and summaries.
- Advisory: the requirement still holds, but it hides a sizable subsystem.

### FR-5 and FR-1 name only part of the shipped provider set (advisory)

- Evidence: `extensions/fish-audio-speech/`, `extensions/gradium/`, `extensions/inworld/`, `extensions/muse/`, `extensions/omlx/`, `extensions/senseaudio/`, `extensions/tts-local-cli/`, `extensions/azure-speech/`, `extensions/comfy/`, `extensions/fal/`
- Artifact says: "FR-5 | Must | The system shall support text-to-speech (TTS) through multiple providers (ElevenLabs, Azure Speech, system TTS, etc.)" (requirements.md:28) and "FR-1 | Must | The system shall support image generation through multiple AI providers (OpenAI, Stability, Comfy, Fal, etc.)" (requirements.md:24).
- Code: the speech provider list also includes local CLI TTS, a local MLX runtime, and several hosted voice providers. The "etc." already signals a non-exhaustive list, so this is granularity, not a contradiction.
- Advisory.

### FR-9 wake word coverage has moved into the companion apps (advisory)

- Evidence: `apps/swabble/Sources/SwabbleKit/WakeWordGate.swift`, `apps/swabble/README.md:1-3`, `apps/macos/Package.swift:64`, `apps/ios/project.yml:90-91`, `apps/android/app/src/main/java/ai/openclaw/app/voice/VoiceWakeManager.kt`, `src/infra/voicewake.ts`, `src/infra/voicewake-routing.ts`
- Artifact says: "FR-9 | Should | The system shall support voice wake word detection on macOS and iOS" (requirements.md:32).
- Code: the detection itself moved to the companion app tree. The gate is a shared Swift package (`SwabbleKit`) that the macOS and iOS apps consume, and the Android app has its own `VoiceWakeManager`. Core keeps only the trigger vocabulary and routing in `src/infra/voicewake.ts` and `src/infra/voicewake-routing.ts`; `src/talk/` owns no detection.
- Advisory: the requirement is satisfied, but the owning code has moved to the companion app tree, which is FEAT-p7 territory.

### FR-12 streaming progress is now implemented as a background job model (advisory)

- Evidence: `src/agents/tools/media-generate-background.ts`, `src/agents/tools/media-generate-background-shared.ts`, `src/agents/tools/media-generate-background-completion.ts`, `src/agents/tools/generated-media-batch-persistence.ts`
- Artifact says: "FR-12 | Should | The system shall provide streaming progress for long-running media generation tasks" (requirements.md:35).
- Code: long-running generation is handled by a background job owner with batch persistence and completion delivery, which is a different mechanism than in-turn streaming progress.
- Advisory.

### Open question 1 is answered in code (advisory)

- Evidence: `src/agents/tools/media-generate-background.ts`, `src/agents/tools/media-generate-background-shared.ts`, `src/media-generation/runtime-shared.ts`
- Artifact says: "1. What is the exact streaming contract for multi-minute video generation?" (requirements.md:54)
- Code: the contract is a background generation job with persisted batches and a completion callback, and the shared runtime owns provider failover across candidates.
- Advisory: the question should be closed with a pointer to the owning module.

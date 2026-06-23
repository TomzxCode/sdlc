---
issue: ""
title: "Voice Mode"
status: draft
---

# Existing Solutions: Voice Mode

## Overview

A substantial voice mode implementation already exists in the codebase. Server-side TTS routes (`packages/web/server/lib/tts/routes.js`) support OpenAI-compatible TTS and macOS `say` command. STT routes proxy audio to OpenAI-compatible transcription endpoints. Client-side voice infrastructure in `packages/ui/src/lib/voice/` provides browser-speech, WASM Whisper, audio stream, and voice session services. The recommended direction is to document and refine the existing implementation.

## Search Scope

| Source | Searched | Notes |
|---|---|---|
| Internal codebase | Yes | `voice`, `whisper`, `speech`, `tts`, `stt`, `transcri`, `say`, `@xenova/transformers`, `browserVoiceService`, `wasmSttService`, `voiceHooks`, `VoiceSettings` |
| Open-source | Yes | `@xenova/transformers` (Whisper), `faster-whisper`, OpenAI TTS/STT APIs, Web Speech API, macOS `say` command |
| Commercial / SaaS | Yes | OpenAI TTS/STT, ElevenLabs, Google Cloud TTS, Azure Speech |
| Standards / protocols | Yes | Web Speech API (W3C), BCP-47 language codes, W3C Media Capture API, Web Audio API |
| Reference material | Yes | MDN Web Speech API docs, OpenAI API TTS/STT docs, Xenova Transformers docs |

## Candidate Solutions

| Solution | Type | License | Maturity | Covers | Gaps |
|---|---|---|---|---|---|
| Existing internal implementation | Internal | MIT | Production | FR-01, FR-02, FR-04, FR-06 | FR-03 (sync across devices), FR-05 (configurable voice/speed) |
| OpenAI TTS/STT API | API | Proprietary | Mature | FR-02 | NFR-01 (sends data to external service) - excluded by privacy constraint |
| Web Speech API (`SpeechRecognition` + `SpeechSynthesis`) | API | W3C Standard | Mature | FR-01 (browser STT), FR-02 (browser TTS) | FR-06 (BCP-47 support limited), FR-04 (no server-side processing), no Whisper quality |
| ElevenLabs TTS | API | Proprietary | Mature | FR-02 | Excluded by NFR-01 privacy constraint |
| macOS `say` command | System | Apple | Mature | FR-02 | macOS only, limited voices |

## Evaluation

### Existing internal implementation

- **Strengths:** Comprehensive server-side infrastructure: `packages/web/server/lib/tts/routes.js` handles `/api/tts/speak`, `/api/tts/say/speak`, `/api/tts/status`, `/api/stt/transcribe`. Supports OpenAI TTS API, OpenAI-compatible endpoints, and macOS `say` command. `packages/web/server/lib/tts/stt.js` proxies audio to OpenAI-compatible endpoints. Client-side services in `packages/ui/src/lib/voice/` include: `browserVoiceService.ts` (Web Speech API abstraction), `wasmSttService.ts` (local Whisper via `@xenova/transformers`), `audioStreamService.ts`, `voiceHooks.ts`, `voiceSession.ts`, `realtimeClientTools.ts`. UI settings at `packages/ui/src/components/sections/openchamber/VoiceSettings.tsx` provides full configuration UI for provider choice (browser, OpenAI, OpenAI-compatible, say), voice selection, speed/pitch/volume sliders, preview playback, and WASM Whisper model download status. STT settings include BCP-47 language code support (FR-06). Config store at `packages/ui/src/stores/useConfigStore.ts:541-731` manages all voice preferences with localStorage persistence. The `@xenova/transformers` dependency is already in `package.json` at version `^2.17.2`. `@types/dom-speech-recognition` is already in devDependencies.
- **Weaknesses:** Voice mode is currently configurable in settings but the continuous voice conversation mode (always-listening, hands-free) may not be fully wired to the chat composer. FR-05 (configurable TTS voice and speed) is partially implemented via settings UI but may need verification. FR-03 (sync settings across devices) requires server-side storage not yet implemented (settings are in localStorage only). The WASM Whisper models have a significant download size (~1.5GB for large model) that needs user-friendly progress indication.
- **Integration effort:** Low. The services, routes, and UI components already exist and are wired through the settings page.
- **Cost:** Free (MIT). OpenAI TTS/STT API usage costs apply if the user configures OpenAI provider. Local Whisper is free. macOS `say` is free.
- **Risks:** WASM Whisper model download can fail on slow connections or mobile devices. `@xenova/transformers` WebWorker setup has browser compatibility constraints. The `say` command is macOS-only.

### OpenAI TTS/STT API

- **Strengths:** Highest quality voice synthesis and transcription. Supports many voices and languages.
- **Weaknesses:** NFR-01 requires local transcription. OpenAI STT sends audio to external servers. The implementation already supports OpenAI as an optional provider, but the requirement mandates local Whisper as default.
- **Integration effort:** N/A (already integrated as optional provider).
- **Cost:** Usage-based pricing.
- **Risks:** Violates NFR-01 privacy requirement when used for STT.

### Web Speech API (Browser)

- **Strengths:** Zero configuration. Works in any modern browser. Included in PWA. Free.
- **Weaknesses:** Quality is lower than Whisper for STT. Voice selection limited to OS voices. No server-side processing (FR-04). BCP-47 language support varies by browser.
- **Integration effort:** Already integrated via `browserVoiceService.ts`.
- **Cost:** Free.
- **Risks:** Browser-dependent quality. `SpeechRecognition` requires HTTPS (except localhost). `SpeechSynthesis` voice quality varies significantly across platforms.

## Recommendation

**Direction:** Adopt and extend (refine existing implementation)

The existing implementation is comprehensive and already satisfies FR-01, FR-02, FR-04, FR-06. The remaining work is:
- Wire the voice mode controls to the chat composer for hands-free conversation flow
- FR-03: Implement server-side settings sync (or defer to a future session sync feature)
- FR-05: Verify TTS voice and speed settings are fully propagated to the TTS routes
- Ensure NFR-01/NFR-02 privacy constraint: make local Whisper the default and clearly label when external OpenAI STT is used

No new libraries are needed. The `@xenova/transformers` + Web Speech API + macOS `say` combination covers all platforms.

## Sources of Information

- `packages/web/server/lib/tts/routes.js:1-254` — TTS/STT route handlers
- `packages/web/server/lib/tts/stt.js:1-50` — OpenAI-compatible transcription proxy
- `packages/web/server/lib/tts/` — full directory with capability detection
- `packages/ui/src/lib/voice/` — 11 service files covering all voice functionality
- `packages/ui/src/components/sections/openchamber/VoiceSettings.tsx:1-478` — full settings UI
- `packages/ui/src/components/voice/VoiceStatusIndicator.tsx:1-128` — voice state indicator
- `packages/ui/src/stores/useConfigStore.ts:541-731` — voice configuration state
- `packages/ui/src/lib/voice/wasmSttService.ts` — local Whisper via `@xenova/transformers`
- Web Speech API spec: <https://w3c.github.io/speech-api/>
- OpenAI TTS API: <https://platform.openai.com/docs/guides/text-to-speech>
- OpenAI STT API: <https://platform.openai.com/docs/guides/speech-to-text>

## Open Questions

1. Is the continuous voice mode (push-to-talk or always-listening) wired into the chat message send flow, or only available as a settings page configuration?
2. How should voice settings sync across devices (FR-03) without a full user account system?
3. Should the WASM Whisper model be downloaded on-demand when voice mode is activated for the first time, or pre-downloaded during settings configuration?
4. Which model size should be the default (base.en for speed vs large-v3-turbo for accuracy)?

---
title: "Media and Voice System"
status: done
---

# Specification: Media and Voice System

## Architecture

Media generation and voice subsystems are implemented as plugin-based provider integrations under `extensions/` with shared core types in `src/`.

```
Agent Runtime
     │
     ▼
Media Generation Core  ─── Provider Plugins (Fal, Comfy, Runway, ...)
(src/media-generation,    extensions/fal/
 src/image-generation,     extensions/comfy/
 src/video-generation,     extensions/runway/
 src/music-generation)     extensions/pixverse/
                           extensions/senseaudio/
     │
     ▼
Voice/Audio Core      ─── Provider Plugins (ElevenLabs, Deepgram, Azure, ...)
(src/tts, src/talk,       extensions/elevenlabs/
 src/realtime-transcription,  extensions/deepgram/
 src/meeting-bot)            extensions/azure-speech/
                             extensions/tts-local-cli/
                             extensions/voice-call/
```

## Data Models

### MediaGenerationRequest

| Field | Type | Constraints | Description |
|---|---|---|---|
| prompt | string | not null | The generation prompt |
| provider | string | optional | Provider override |
| options | Record<string, unknown> | optional | Provider-specific options |
| stream | boolean | optional | Whether to stream results |

### TTSRequest

| Field | Type | Constraints | Description |
|---|---|---|---|
| text | string | not null | Text to synthesize |
| voice | string | optional | Voice identifier |
| provider | string | optional | Provider override |

## API Contracts

Media and voice capabilities are exposed as agent tools through the tool system, not as standalone HTTP endpoints.

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Provider abstraction | Plugin-based with core abstractions | Enables community provider plugins without core changes |
| Streaming | Core streaming infrastructure for long-running jobs | Users see progress during multi-minute generation |
| Voice modality | Talk runtime with session management | Full-duplex voice conversation requires session state |

## Risks and Unknowns

1. Quality varies significantly across providers for the same prompt
2. Voice call reliability depends on provider WebSocket stability


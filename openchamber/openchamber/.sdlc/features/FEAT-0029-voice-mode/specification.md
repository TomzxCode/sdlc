---
title: "Voice Mode"
status: draft
---

# Specification: Voice Mode

## Overview

Voice input uses `@xenova/transformers` (Whisper model) running server-side for local STT. TTS uses the system `say` command or OpenAI-compatible TTS API. Audio is captured in the browser, sent to the server for transcription, and the resulting text is injected as a chat message.

## Architecture

```
Browser mic capture (Web Audio API)
    |
    v  Audio blob upload
Server (packages/web/server/lib/tts/)
    |
    +---> Whisper via @xenova/transformers (STT)
    |
    +---> say command / OpenAI TTS (TTS output)
    |
    v  Text result
Chat message injection
```

## API Contracts

### POST /api/tts/transcribe

**Request**: Multipart form data with audio file.

**Response (200 OK)**

| Field | Type | Description |
|---|---|---|
| text | string | Transcribed text |

### POST /api/tts/speak

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| text | string | yes | Text to speak |

**Response**: Audio stream (audio/wav or audio/mp3).

## Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| STT engine | Local Whisper via @xenova/transformers | Privacy; no audio data leaves the machine |
| TTS engine | System `say` + OpenAI fallback | Leverages macOS built-in; OpenAI for higher quality |
| Processing location | Server-side | Machine has more resources than browser for Whisper inference |

## Risks and Unknowns

1. Whisper model download size may surprise users on first use
2. Server CPU load during transcription may affect streaming performance

## Out of Scope

- Real-time continuous transcription (push-to-talk only)
- Speaker identification

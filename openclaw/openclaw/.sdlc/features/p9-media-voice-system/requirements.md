---
title: "Media and Voice System"
status: done
---

# Requirements: Media and Voice System

## Overview

OpenClaw supports creation, understanding, and playback of media content through a unified media generation and understanding framework, plus a full voice/audio subsystem spanning TTS, speech recognition, voice calls, meeting bots, and real-time transcription. These capabilities are exposed as agent tools and can be delivered over any channel.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End users | Generate images, video, and music; speak with and listen to the assistant; join meetings |
| Plugin developers | Build provider integrations for media generation and speech services |
| Maintainers | Provider abstraction, streaming, and quality-of-service guarantees |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall support image generation through multiple AI providers (OpenAI, Stability, Comfy, Fal, etc.) |
| FR-2 | Must | The system shall support video generation through provider integrations (Runway, Pixverse, etc.) |
| FR-3 | Must | The system shall support music generation through provider integrations |
| FR-4 | Must | The system shall provide a unified media generation API that abstracts across providers |
| FR-5 | Must | The system shall support text-to-speech (TTS) through multiple providers (ElevenLabs, Azure Speech, system TTS, etc.) |
| FR-6 | Must | The system shall support voice call initiation and management through provider integrations |
| FR-7 | Must | The system shall support real-time transcription of audio input |
| FR-8 | Should | The system shall support media understanding (describe, analyze, transcribe media content) |
| FR-9 | Should | The system shall support voice wake word detection on macOS and iOS |
| FR-10 | Should | The system shall support meeting bot integration (Google Meet, Zoom, Teams) |
| FR-11 | Must | The system shall expose media generation and voice capabilities as agent tools |
| FR-12 | Should | The system shall provide streaming progress for long-running media generation tasks |
| FR-13 | Must | The system shall support configurable provider selection and failover for media and voice |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Compatibility | Media generation output must be deliverable over any supported messaging channel |
| NFR-2 | Should | Performance | Audio/TTS output should begin streaming within 2 seconds |
| NFR-3 | Should | Extensibility | New media and voice providers shall be addable via the plugin system |

## Acceptance Criteria

- [ ] **FR-1**: User sends "generate an image of a cat" and receives a generated image
- [ ] **FR-5**: User asks the assistant to speak and hears audio output on a voice-capable channel
- [ ] **FR-11**: Media generation tools appear in the agent's tool catalog and are invocable

## Open Questions

1. What is the exact streaming contract for multi-minute video generation?


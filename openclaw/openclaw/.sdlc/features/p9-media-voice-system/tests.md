---
title: "Media and Voice System"
status: done
---

# Test Plan: Media and Voice System

## Scope

Unit and integration tests for TTS, talk/voice runtime, media generation provider contracts, and ElevenLabs integration. Voice call E2E and live tests are excluded from this plan.

## Unit Tests

| ID | Description | Source |
|---|---|---|
| TC-1 | TTS text preparation and directives | src/tts/prepare-text.test.ts, src/tts/directives.test.ts |
| TC-2 | TTS provider registry | src/tts/provider-registry.test.ts |
| TC-3 | TTS configuration | src/tts/tts-config.test.ts, src/tts/status-config.test.ts |
| TC-4 | TTS core functionality | src/tts/tts.test.ts, src/tts/tts-core.test.ts |
| TC-5 | OpenAI-compatible speech provider | src/tts/openai-compatible-speech-provider.test.ts |
| TC-6 | Directive number parsing | src/tts/directive-number.test.ts |
| TC-7 | Agent run control for talk | src/talk/agent-run-control.test.ts |
| TC-8 | Agent consult tool | src/talk/agent-consult-tool.test.ts |
| TC-9 | Talk session controller | src/talk/talk-session-controller.test.ts |
| TC-10 | Audio energy detection | src/talk/audio-energy.test.ts |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-20 | Media generation shared runtime | src/media-generation/runtime-shared.test.ts | Provider contracts match |
| TC-21 | Media generation provider capabilities | src/media-generation/provider-capabilities.contract.test.ts | Capabilities match spec |
| TC-22 | ElevenLabs TTS | extensions/elevenlabs/tts.test.ts | TTS returns audio |
| TC-23 | ElevenLabs speech provider | extensions/elevenlabs/speech-provider.test.ts | Speech API works |
| TC-24 | ElevenLabs shared types | extensions/elevenlabs/shared.test.ts | Types are correct |

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-5 (TTS) | TC-1, TC-2, TC-3, TC-4, TC-5, TC-22, TC-23 |
| FR-7 (real-time transcription) | TC-24 |
| FR-10 (voice/talk) | TC-7, TC-8, TC-9, TC-10 |
| FR-1/FR-4 (media generation) | TC-20, TC-21 |


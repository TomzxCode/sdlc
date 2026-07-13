---
title: "Voice Mode"
status: done
---

# Requirements: Voice Mode

## Overview

OpenChamber supports hands-free voice interaction via local Whisper speech-to-text for input and text-to-speech for reading responses aloud. Voice settings sync across devices via the server.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Developers | Hands-free coding assistance while away from keyboard |
| Accessibility users | Voice-driven interaction as an alternative to typing |

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall support speech-to-text input using local Whisper transcription. |
| FR-02 | Must | The system shall support text-to-speech output for reading assistant responses aloud. |
| FR-03 | Should | The system shall sync speech recognition settings across devices via the server. |
| FR-04 | Should | The system shall allow the server transcription to finish processing audio when voice input stops. |
| FR-05 | May | The system shall support configurable TTS voice and speed settings. |
| FR-06 | Must | The system shall accept BCP-47 language codes for STT with auto-detect default, supporting any Whisper-supported language. |

## Non-Functional Requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Privacy | Speech transcription shall run locally; no audio data sent to external services. |
| NFR-02 | Must | Security | Speech transcription shall run locally; no audio data shall be sent to external services. |

## Constraints

- Uses `@xenova/transformers` for local Whisper inference
- TTS uses the `say` command on macOS or equivalent on other platforms
- Audio processing happens server-side to leverage the machine's resources

## Acceptance Criteria

- [ ] FR-01: Given the user speaks into the microphone, the system transcribes the audio locally and inserts it as a chat message
- [ ] FR-02: Given an assistant response, the user can trigger TTS to hear the response read aloud
- [ ] FR-03: Given voice settings changed on one device, the settings are available on another device connected to the same server
- [ ] FR-04: Given audio input stops, the server finishes processing the transcription before returning results
- [ ] FR-05: Given TTS settings, the user can configure the voice and speech speed
- [ ] FR-06: Given a BCP-47 language code in STT settings, the system uses that language for transcription
- [ ] NFR-01: Given voice input, all speech transcription runs locally without sending audio to external services
- [ ] NFR-02: Given voice input, audio data remains local and is never transmitted to external services

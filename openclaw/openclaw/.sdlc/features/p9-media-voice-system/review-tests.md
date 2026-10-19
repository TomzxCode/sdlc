---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Media and Voice System test plan

## Sync drift: 2026-10-19

### TC-21 names a test file that does not exist (blocking)

- Evidence: `src/media-generation/provider-capabilities.contract.test.ts` is absent, `src/media-generation/` contains only `live-test-helpers.test.ts`, `provider-assets.test.ts`, `registry.test.ts`, and `runtime-shared.test.ts`, `src/media-understanding/provider-capability-registry.test.ts` exists, `src/image-generation/capabilities.test.ts` exists, `src/video-generation/capabilities.test.ts` exists, `src/music-generation/capabilities.test.ts` exists
- Artifact says: "| TC-21 | Media generation provider capabilities | src/media-generation/provider-capabilities.contract.test.ts | Capabilities match spec |" (tests.md:32).
- Code: the file was removed. The capability contracts now live per capability in `src/image-generation/capabilities.test.ts`, `src/video-generation/capabilities.test.ts`, and `src/music-generation/capabilities.test.ts`, and a separate provider capability registry with its own tests lives in `src/media-understanding/`.
- Blocking: the plan points a reviewer at a file that cannot be opened, and the replacement lives outside the feature scope.

### The coverage matrix maps FR-7 to a test that proves nothing about it (blocking)

- Evidence: `tests.md:42`, `extensions/elevenlabs/shared.test.ts`, `src/realtime-transcription/websocket-session.test.ts`, `extensions/deepgram/realtime-transcription-provider.test.ts`, `extensions/deepgram/realtime-transcription-provider.cold.test.ts`, `extensions/deepgram/audio.test.ts`
- Artifact says: "| FR-7 (real-time transcription) | TC-24 |" where "TC-24 | ElevenLabs shared types | extensions/elevenlabs/shared.test.ts | Types are correct" (tests.md:35, tests.md:42).
- Code: `extensions/elevenlabs/shared.test.ts` asserts shared type shapes. The real-time transcription coverage is in `src/realtime-transcription/websocket-session.test.ts` and in the Deepgram provider suites, none of which the plan lists.
- Blocking: the matrix directs a reader to a test that cannot fail for a transcription defect.

### The coverage matrix mislabels FR-10 (blocking)

- Evidence: `requirements.md:33`, `tests.md:43`, `src/talk/agent-run-control.test.ts`, `src/talk/agent-consult-tool.test.ts`, `src/talk/talk-session-controller.test.ts`, `src/talk/audio-energy.test.ts`, `src/meeting-bot/` (38 test files)
- Artifact says: "| FR-10 (voice/talk) | TC-7, TC-8, TC-9, TC-10 |" (tests.md:43).
- Code: FR-10 in the requirements is "The system shall support meeting bot integration (Google Meet, Zoom, Teams)" (`requirements.md:33`). TC-7 through TC-10 are talk-runtime tests in `src/talk/`. The meeting bot has 38 test files under `src/meeting-bot/`, plus `extensions/google-meet/`, `extensions/zoom-meetings/`, and `extensions/teams-meetings/`, and none appear in the plan.
- Blocking: the matrix points a reader at the wrong requirement, and the meeting bot requirement has no listed coverage.

### The voice call plugin has 73 test files and none are listed (blocking)

- Evidence: `find extensions/voice-call -name "*.test.ts"` returns 73 files, `extensions/voice-call/src/call-brief.test.ts`, `extensions/voice-call/src/call-delivery.test.ts`, `extensions/voice-call/src/call-delivery-runtime.test.ts`, `extensions/voice-call/src/realtime-call-control.ts`, `extensions/voice-call/src/webhook/realtime-call-control.test.ts`, `extensions/voice-call/src/webhook/realtime-call-session-control.test.ts`, `extensions/voice-call/src/manager.test-harness.ts`
- Artifact says: the scope statement says "Voice call E2E and live tests are excluded from this plan." (tests.md:10) and no voice call file appears in any table.
- Code: the voice call plugin is the largest tested surface in the feature. It has suites for the call brief, call delivery, the delivery runtime, the realtime call control and session control, the manager, the CLI, the allowlist, the tunnel, webhook security, webhook replay, provider discovery, the stale call reaper, and telephony TTS.
- Blocking: a major shipped capability with extensive coverage is absent from the plan.

### The scope statement excludes live tests that are now a separate, labeled family (advisory)

- Evidence: `tests.md:10`, `src/media-generation/live-test-helpers.test.ts`, `src/image-generation/live-test-helpers.test.ts`, `extensions/elevenlabs/elevenlabs.live.test.ts`, `extensions/deepgram/audio.live.test.ts`, `extensions/deepgram/audio-flux.live.test.ts`, `extensions/music-generation-providers.live.test.ts`, `extensions/video-generation-providers.live.test.ts`
- Artifact says: "Voice call E2E and live tests are excluded from this plan." (tests.md:10)
- Code: live tests follow a named `*.live.test.ts` suffix convention across the media and speech providers, so they are separable and labelable rather than a blanket exclusion.
- Advisory.

### The unit test table omits the meeting bot, talk runtime, and background generation suites (advisory)

- Evidence: `src/talk/` (44 test files), `src/meeting-bot/` (38 test files), `src/agents/tools/media-generate-background.test.ts`, `src/agents/tools/media-generate-background-shared.test.ts`, `src/agents/tools/media-generate-background-retention.test.ts`, `src/tts/tts-runtime-routing.test.ts`, `src/tts/tts-preferences.worker.test.ts`, `src/tts/tts-streaming.resources.test.ts`, `src/tts/tts-summary.test.ts`, `src/tts/tts-entry-delivery.test.ts`
- Artifact says: the unit test table lists ten cases (TC-1 through TC-10) across `src/tts/` and `src/talk/` (tests.md:14-25).
- Code: the talk runtime alone has 44 test files, the meeting bot has 38, and the TTS runtime has streaming, preferences, summary, and delivery suites that the table does not name.
- Advisory.

### The ElevenLabs integration rows omit the media understanding provider (advisory)

- Evidence: `extensions/elevenlabs/media-understanding-provider.ts`, `extensions/elevenlabs/media-understanding-provider.test.ts`, `extensions/elevenlabs/capability-catalog.ts`
- Artifact says: the integration test table lists `extensions/elevenlabs/tts.test.ts`, `speech-provider.test.ts`, and `shared.test.ts` (tests.md:33-35).
- Code: the ElevenLabs plugin also ships a media understanding provider with its own test, which is a fourth capability for that plugin and is not listed.
- Advisory.

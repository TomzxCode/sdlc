---
title: "Voice Mode"
status: done
---

# Test Plan: Voice Mode

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | TTS routes work | Text input | Correct audio response |
| TC-2 | Voice preview audio renders | Voice config | Correct playback |

## Test Files

- `packages/web/server/lib/tts/routes.test.js`
- `packages/ui/src/components/sections/openchamber/voicePreviewAudio.test.ts`

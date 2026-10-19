---
title: "Desktop Companion and Voice"
status: done
session_link: http://localhost:10000/?session=ses_sync_sdlc_20261019
---

# Requirements: Desktop Companion and Voice

## Overview

The harness server and the agent runtime must never own a screen, a keyboard, a microphone or a lid.
Every desktop effect that the agent needs (opening a URL, revealing a file, spawning a terminal window, keeping the machine awake, push-to-talk dictation) is brokered to a per-login companion process that runs inside the user's graphical session and answers over a local socket.
A headless or remote server simply has no companion, so the caller falls back to its own local behavior instead of popping a window on the wrong machine.
This feature documents the companion, the desktop-open helpers, the voice subsystem, the `jcode companion` and `jcode dictate` CLI surfaces, and the `/dictate`, `/dictation` and `/voice` TUI commands.
It was reverse-engineered from the existing codebase during an SDLC sync, so it describes already-implemented functionality rather than planned work.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user on a desktop | Agent actions open windows, files and terminals in the session they are actually looking at |
| Remote or headless operator | The server never touches the wrong machine's screen, and every desktop effect degrades to a local fallback |
| Agent runtime and harness | Desktop effects are requested over one small, versioned, local protocol instead of being embedded in the agent loop |
| Voice user | Push-to-talk dictation reaches the focused jcode session, with a visible recording indicator |
| Platform maintainer | Lid-close and power settings are always restored, even after a crash |

## Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Requirement |
|---|---|---|
| FR-1 | Must | The system shall provide a per-login companion process (`jcode companion`) that runs inside the user's graphical session and owns every desktop-only effect: opening URLs and files, revealing paths, spawning terminal windows, the lid-close override, and the global push-to-talk listener. |
| FR-2 | Must | The harness server and the agent runtime shall request desktop effects over a local socket using one JSON request per line answered by one JSON response per line, and shall never open a screen, a keyboard, a microphone or a lid themselves. |
| FR-3 | Must | The companion shall answer a status request with its version, its protocol version, and the list of capabilities it provides on the current platform. |
| FR-4 | Must | The companion shall open a URL or a local path with the desktop's default application, and shall report which opener ran. |
| FR-5 | Must | The companion shall show a local path in the file manager, selecting the file when the platform supports it. |
| FR-6 | Must | The companion shall run a program in a new terminal window in the user's session, preserving the program, the arguments, the working directory, the title, the kind, the session id, and the environment metadata. |
| FR-7 | Must | A caller shall fall back to its own local behavior when no companion answers, so the system still works on a machine with no graphical session. |
| FR-8 | Must | The companion shall engage the lid-close override while a session is working, and shall release it when the work stops, when the activity lease expires, or when the companion exits. |
| FR-9 | Must | The companion shall write the original power settings to a recovery journal before changing them, and shall restore them when the owning process dies, so a killed process cannot leave the machine unable to sleep. |
| FR-10 | Must | The companion shall provide a global push-to-talk listener on Linux that records only while a jcode CLI session is focused, shows a visible recording indicator, and sends the finished transcript to that session. |
| FR-11 | Must | The global push-to-talk listener shall be opt-in through the configured keyboard event devices, and shall be disabled at runtime by a command-line flag or by an environment variable. |
| FR-12 | Must | The companion shall refuse to open the microphone when no visible recording indicator can be shown. |
| FR-13 | Should | The system shall run the configured dictation command and apply the resulting transcript according to the configured mode, either sending it to the focused jcode client or typing it into the focused application. |
| FR-14 | Should | The voice subsystem shall transcribe captured audio with the Nari streaming API, sourcing the audio from either native capture or an external recorder process. |
| FR-15 | Should | The companion shall refresh an installed browser bridge on a periodic schedule, off the browser tool's hot path. |
| FR-16 | May | Opening a URL on the niri compositor shall raise the browser window that handled it. |
| FR-17 | May | The global push-to-talk listener shall share a routing registry with Jcode Desktop, so the most recently focused registrant wins a press. |

## Non-Functional Requirements

Order rows by priority: Must first, then Should, then May.

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-1 | Must | Performance | A companion request shall be answered within the caller's timeout, and a liveness probe shall be answered in under 500 ms. |
| NFR-2 | Must | Privacy | The microphone shall be opened only after an explicit user press, and the capture shall be released on key release, on cancel, on drop, on device failure, on the byte cap, and at the five-minute cap. |
| NFR-3 | Must | Privacy | No audio, transcript, credential, provider error, or response body shall be written to the log, to an error message, or to a notification. |
| NFR-4 | Must | Security | The companion socket shall live in the per-user runtime directory, a request line shall be capped at 64 KiB, and a malformed request shall be answered with an error instead of taking the server down. |
| NFR-5 | Must | Reliability | The power-activity lease shall expire 30 seconds after the last renewal and the override shall be released at the next five-second reconcile tick, and a stale lid override left by a dead owner shall be repaired by the next companion that starts. |
| NFR-6 | Should | Privacy | The system shall check the session lock state before every press and before delivery, and shall refuse to record while the session is locked. |
| NFR-7 | Should | Availability | The system shall keep working with no companion installed, and every voice failure shall map to one specific short user-facing message. |
| NFR-8 | Should | Portability | The companion shall run on Linux, macOS, and Windows, and the reported capability list shall match what the current platform can do. |

## Constraints

- The companion socket path comes from `JCODE_COMPANION_SOCKET`, else `jcode-companion.sock` in the runtime directory.
- The protocol version is `1`, and it is bumped when a request's meaning changes incompatibly.
- Global voice is Linux-only, and the lid override is macOS and Windows only.
- The macOS lid override needs a `sudoers` rule for `pmset`, runs `sudo -n` so it never prompts, and is skipped with a one-time hint when the rule is missing.
- Linux blocks the lid through `systemd-inhibit`, which needs no persistent setting change.
- Voice transcription needs a Nari API key, supplied through `NARI_API_KEY` or `~/.config/jcode/nari.env`.
- The global voice device list comes from `[dictation] global_devices` in `~/.jcode/config.toml`.
- `docs/MESSAGE_VOICE.md` was checked and does not apply, it governs how jcode phrases user-facing messages rather than how voice input works.
- `docs/REMOTE_HANDOFF.md` was checked and does not apply, it is an unimplemented design sketch for moving sessions between hosts.

## Acceptance Criteria

Order criteria by FRs first (sorted by ID), then NFRs (sorted by ID).

- [ ] **FR-1**

    ```gherkin
    @FR-1
    Scenario: Companion owns the desktop effects
      Given a user logged in to a graphical session
      When the companion starts
      Then it binds its local socket and advertises the open, reveal and spawn-terminal capabilities
    ```

- [ ] **FR-2**

    ```gherkin
    @FR-2
    Scenario: Desktop effect travels over the socket
      Given a server with no screen of its own
      When it asks the companion to open a URL
      Then the request is one JSON line and the reply is one JSON line
    ```

- [ ] **FR-3**

    ```gherkin
    @FR-3
    Scenario: Status reports version, protocol and capabilities
      Given a running companion
      When a status request is sent
      Then the reply carries the companion version, protocol version 1, and a capability list
    ```

- [ ] **FR-4**

    ```gherkin
    @FR-4
    Scenario: Opening a URL uses the desktop's own tool
      Given a running companion on a desktop
      When an open request carries a URL
      Then the reply names the opener that ran
    ```

- [ ] **FR-5**

    ```gherkin
    @FR-5
    Scenario: Revealing a path opens the file manager
      Given a running companion and an existing file
      When a reveal request carries that path
      Then the reply names the backend that showed the path
    ```

- [ ] **FR-6**

    ```gherkin
    @FR-6
    Scenario: Spawning a terminal keeps the caller's context
      Given a running companion
      When a spawn-terminal request carries a program, arguments, working directory, title and session id
      Then a new terminal window runs in the user's session with that context
    ```

- [ ] **FR-7**

    ```gherkin
    @FR-7
    Scenario: No companion means a local fallback
      Given no companion is listening on the socket
      When a caller asks to open a URL
      Then the caller opens it with its own local opener instead of failing
    ```

- [ ] **FR-8**

    ```gherkin
    @FR-8
    Scenario: Lid override follows the work
      Given a running companion on macOS or Windows
      When a power-activity request activates and then deactivates the override
      Then the lid close is blocked while active and the original setting is put back afterwards
    ```

- [ ] **FR-9**

    ```gherkin
    @FR-9
    Scenario: A killed owner is repaired by the next process
      Given a companion that was killed while holding the lid override
      When the next companion starts
      Then the original lid setting from the recovery journal is restored
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: Push-to-talk reaches the focused session
      Given a running companion with a configured global device and a focused jcode CLI session
      When the user holds the push-to-talk key and releases it
      Then a recording indicator is shown, the audio is transcribed, and the transcript is sent to that session
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Global voice is opt-in and can be turned off
      Given no global device is configured
      When the companion starts
      Then no global push-to-talk listener is started
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: Recording is refused without an indicator
      Given a press on the push-to-talk key
      And the desktop notification cannot be shown
      Then the microphone is not opened
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Configured dictation applies the configured mode
      Given a dictation command configured to print a transcript
      When the dictate command runs
      Then the transcript is sent to the focused jcode client or typed into the focused application
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Audio is transcribed by the streaming service
      Given a recording opened from native capture or an external recorder
      When the audio is streamed for transcription
      Then a final transcript or a specific failure is reported
    ```

- [ ] **FR-15**

    ```gherkin
    @FR-15
    Scenario: Browser bridge stays current off the hot path
      Given an installed browser bridge
      When the companion's periodic update runs
      Then the bridge is updated without adding a network round trip to a browser action
    ```

- [ ] **FR-16**

    ```gherkin
    @FR-16
    Scenario: The browser window that handled the URL is raised
      Given a niri session with a browser window
      When the companion opens a URL
      Then the browser window that handled the URL is focused
    ```

- [ ] **FR-17**

    ```gherkin
    @FR-17
    Scenario: The most recently focused registrant wins a press
      Given two registrants in the shared routing registry
      When the press-to-talk key is pressed
      Then the most recently focused eligible registrant handles the press
    ```

- [ ] **NFR-1**

    ```gherkin
    @NFR-1
    Scenario: Liveness probe is fast
      Given a running companion
      When a status probe is sent
      Then the reply arrives in under 500 ms
    ```

- [ ] **NFR-2**

    ```gherkin
    @NFR-2
    Scenario: Capture never outlives the press
      Given a user presses the push-to-talk key
      When the key is released, cancelled, or the five-minute cap is reached
      Then the microphone is released and no further audio is captured
    ```

- [ ] **NFR-3**

    ```gherkin
    @NFR-3
    Scenario: Transcripts and keys never leak
      Given a transcription that fails
      When the failure is reported
      Then the message names no audio, no transcript, no key, and no provider response body
    ```

- [ ] **NFR-4**

    ```gherkin
    @NFR-4
    Scenario: A malformed request does not stop the server
      Given a running companion
      When a request line that is not valid JSON arrives
      Then the reply is an error and the server keeps serving later requests
    ```

- [ ] **NFR-5**

    ```gherkin
    @NFR-5
    Scenario: A silent server releases the override
      Given a companion holding the lid override
      When the server stops renewing the activity lease
      Then the 30 second lease expires and the override is released at the next reconcile tick
    ```

- [ ] **NFR-6**

    ```gherkin
    @NFR-6
    Scenario: A locked session is not recorded
      Given a locked desktop session
      When the user presses the push-to-talk key
      Then the press is denied and no audio is captured
    ```

- [ ] **NFR-7**

    ```gherkin
    @NFR-7
    Scenario: Every voice failure has its own message
      Given a missing API key, an exhausted credit balance, a timeout and a missing microphone
      When each failure is reported
      Then each one shows a distinct short message
    ```

- [ ] **NFR-8**

    ```gherkin
    @NFR-8
    Scenario: Capabilities match the platform
      Given a companion running on Linux
      When the status request is answered
      Then the capability list contains voice and does not contain lid
    ```

## Conflicts

None identified.

## Open Questions

None.

---
artifact: requirements
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
---

# Review: Companion Applications requirements

## Sync drift: 2026-10-19

### Platform list omits the Linux and Windows desktop companion (blocking)

- Evidence: `apps/linux/README.md:1-3`, `apps/linux/src-tauri/src/tray.rs`, `apps/linux/src-tauri/src/quickchat.rs`, `apps/linux/src-tauri/src/first_run.rs`, `apps/linux/src-tauri/src/keep_awake.rs`, `apps/linux/src-tauri/src/desktop_node.rs`, `apps/linux/src-tauri/src/native_browser.rs`, `apps/linux/omarchy/manifest.json`
- Artifact says: "Companion applications extend OpenClaw to native platforms: macOS desktop app, iOS app, Android app, and Windows companion." (requirements.md:10)
- Code: `apps/linux/` is a Tauri v2 desktop client that ships for both Linux and Windows. It has a system tray, first-run Gateway setup, a Quick Chat window, an inline browser, desktop sharing through a local node, a keep-awake menu item, an Omarchy bar plugin, and its own release and updater channel.
- The requirements list no functional requirement for this client, so a reader would not know the repository ships a Linux desktop app.
- Blocking: the artifact asserts an incomplete platform list for a user-visible subsystem.

### New native surfaces in `apps/` are unlisted (blocking)

- Evidence: `apps/ios/WatchApp/`, `apps/ios/ActivityWidget/`, `apps/ios/ShareExtension/`, `apps/ios/WatchTests/`, `apps/android/wear/`, `apps/android/wear-shared/`, `apps/swabble/`, `apps/macos-mlx-tts/`, `apps/shared/OpenClawKit/`, `apps/shared/OpenClawWatchRTC/`, `apps/shared/OpenClawMLXTTSProtocol/`
- Artifact says: the platform list is "macOS desktop app, iOS app, Android app, and Windows companion" (requirements.md:10) and the constraints list only iOS, macOS, and Android entries (requirements.md:41-43).
- Code: iOS now ships a watchOS app, a Live Activity widget, and a share extension. Android ships a wear app and a shared wear module. `apps/swabble/` is a macOS wake-word hook daemon that both `apps/macos/Package.swift:64` and `apps/ios/project.yml:90-91` depend on through the shared `SwabbleKit` product. `apps/macos-mlx-tts/` is a local MLX speech helper. `apps/shared/` holds four shared Swift packages that the platform apps depend on.
- Blocking: the platform inventory is materially incomplete, and no requirement covers the watch, widget, share-extension, wear, or wake-word surfaces.

### FR-8 describes a client that is not in this repository (blocking)

- Evidence: `docs/platforms/windows.md:22-25`, `docs/platforms/windows.md:52-60`, `apps/linux/README.md:5-7`, `apps/linux/README.md:114-116`, `find . -name "*.cs" -not -path "*/node_modules/*"` returns 0 files, `find . -name "*.csproj" -not -path "*/node_modules/*"` returns 0 files
- Artifact says: "FR-8 | May | The Windows companion app shall support setup, tray status, chat, node mode, and local MCP mode" (requirements.md:30)
- Code: the Windows Hub is a separate WinUI application maintained in `openclaw/openclaw-windows-node`, and this repository contains no C# or .NET source. The only Windows client in this repository is the Tauri build of `apps/linux/src-tauri/`, which supports setup, tray status, and Quick Chat, plus a narrower desktop-sharing node (`apps/linux/src-tauri/src/desktop_node.rs`). It has no local MCP server mode, and there is no MCP reference anywhere under `apps/`.
- Blocking: the requirement asserts capabilities of an out-of-tree product and names a capability (`local MCP mode`) that no in-tree Windows client implements.

### FR-5 understates the macOS speech surface (advisory)

- Evidence: `apps/macos/Sources/OpenClaw/TalkMLXSpeechSynthesizer.swift:1-50`, `apps/macos/Sources/OpenClaw/AppVoiceRuntime.swift:1-60`, `apps/shared/OpenClawKit/Sources/OpenClawKit/TalkSystemSpeechSynthesizer.swift:1-20`, `apps/macos-mlx-tts/Package.swift:1-50`
- Artifact says: "FR-5 | Must | The macOS app shall support text-to-speech using system voices" (requirements.md:27).
- Code: the macOS app still runs a system speech synthesizer, now owned by the shared Swift package `OpenClawKit`, and it also runs a local MLX neural TTS helper that it spawns as a subprocess, with memory-pressure cancellation and a system-voice fallback path.
- The requirement is not contradicted, but a reader would not know that a second, local speech engine exists.
- Advisory.

### FR-1 uses "system tray" where macOS ships a menu bar (advisory)

- Evidence: `apps/macos/Sources/OpenClaw/MenuBar.swift`, `apps/macos/Sources/OpenClaw/StatusMenuController.swift`, `apps/linux/README.md:638-644`
- Artifact says: "FR-1 | Must | The macOS app shall provide system tray integration with quick access to gateway controls" (requirements.md:23).
- Code: the macOS app is a menu bar app. The repository documentation calls the macOS surface a "menu bar app" and reserves "tray" for the Windows and Linux Tauri clients.
- Advisory: wording only, the capability exists.

### Open question 1 is answered in code (advisory)

- Evidence: `apps/linux/src-tauri/src/quickchat.rs`, `apps/linux/src-tauri/src/quickchat_widgets.rs`, `apps/macos/Sources/OpenClaw/WebChatManager.swift`, `apps/shared/OpenClawKit/Sources/OpenClawChatUI/`, `apps/ios/Sources/Design/ChatProTab.swift`
- Artifact says: "1. Should the companion apps offer full chat functionality or be thin clients?" (requirements.md:59)
- Code: the desktop companion has a native Quick Chat plus the full Control UI dashboard, the macOS app has a WebKit chat surface, and the mobile apps have full chat screens. The thin-client question is settled in favor of both.
- Advisory: the question should be closed rather than left open.

### Constraints omit the Windows and Linux desktop distribution model (advisory)

- Evidence: `apps/linux/README.md:1-3`, `apps/linux/README.md:114-121`, `apps/linux/README.md:688-727`, `docs/platforms/windows.md:9-13`
- Artifact says: the constraints cover only iOS membership, macOS notarization, Android API level, and optionality (requirements.md:41-44).
- Code: the Linux and Windows desktop client has its own signing, updater channels (`linux-stable`, `windows-stable`), Debian and AppImage packaging, and a release request workflow that runs separately from core finalization.
- Advisory: a constraint list that omits a shipped release channel is incomplete, but it does not mislead about behavior.

## Sync drift: 2026-11-16

The 2026-10-19 drift remains present. The artifact is unchanged and the code still exposes the Linux and Windows Tauri client, the watch, widget, share-extension, wear, wake-word, and MLX speech surfaces, and no in-tree C# Windows Hub.

### Browser-based device pairing and pairing notifications are unlisted (advisory)

- Evidence: `src/state/openclaw-state-schema.sql:644-656` defines `device_pairing_browser_requests`, with active consumers `src/infra/device-pairing-browser-code.worker.ts` and `src/gateway/server.browser-pair.test.ts`. `extensions/device-pair/notify.ts` and `extensions/device-pair/index.ts:424-430` add a pairing notification service on a 10-second poll.
- Artifact says: FR-7 (requirements.md:29) covers device pairing only as a generic secure gateway connection, and FR-2 (requirements.md:24) covers push notifications only for assistant messages.
- Code: a browser approval flow lets a user approve a pairing request from a browser using a code, and the device-pair plugin can notify subscribers of pending pairing requests.
- An implemented user-facing behavior is missing from the requirements.
- Advisory.

## Sync drift: 2026-11-23

Fresh comparison against the current code confirms the 2026-10-19 and 2026-11-16 drift remains. The artifact is unchanged at `status: done` and the code still contradicts it. Verdict stays `changes-requested`.

### The platform inventory is still incomplete (blocking)

- Evidence: `apps/linux/README.md:1-3` names the shipped Tauri v2 desktop app for Linux and Windows. The files `apps/linux/src-tauri/src/tray.rs`, `apps/linux/src-tauri/src/quickchat.rs`, `apps/linux/src-tauri/src/gateway.rs`, and `apps/linux/src-tauri/src/updater.rs` are present. The watch, widget, share-extension, wear, wake-word, and MLX speech surfaces exist at `apps/ios/WatchApp/`, `apps/ios/ActivityWidget/`, `apps/ios/ShareExtension/`, `apps/android/wear/`, `apps/swabble/`, `apps/macos-mlx-tts/`, and `apps/shared/OpenClawKit/`.
- Artifact says: requirements.md:10 lists only "macOS desktop app, iOS app, Android app, and Windows companion", and requirements.md:41-43 constrains only iOS, macOS, and Android.
- Code: the in-tree companion set includes the Linux and Windows Tauri client plus six additional native surfaces, none of which has a requirement.
- Blocking: a reader cannot discover shipped platforms from the requirements.

### FR-8 still describes an out-of-tree Windows Hub (blocking)

- Evidence: `docs/platforms/windows.md:22-25` states Windows Hub is maintained in `openclaw/openclaw-windows-node`. A tree search returns 0 `.cs` files and 0 `.csproj` files. The in-tree Windows client is `apps/linux/src-tauri/src/gateway_windows.rs`, `apps/linux/src-tauri/src/cli_windows_tests.rs`, and `apps/linux/src-tauri/src/runtime_action_windows_tests.rs`.
- Artifact says: requirements.md:30 requires setup, tray status, chat, node mode, and local MCP mode of "the Windows companion app".
- Code: no Windows Hub source is in this repository, and the in-tree Tauri client has no local MCP server mode.
- Blocking: the requirement names capabilities of a product that is not built from this tree.

### FR-7 and FR-2 still omit browser pairing and pairing notifications (advisory)

- Evidence: `src/state/openclaw-state-schema.sql:645-656` defines `device_pairing_browser_requests` with consumers `src/infra/device-pairing-browser-code.worker.ts` and `src/gateway/server.browser-pair.test.ts`. `extensions/device-pair/notify.ts` and `extensions/device-pair/notify-state.ts` implement a pairing notification service.
- Artifact says: requirements.md:24 covers push notifications only for assistant messages, and requirements.md:29 covers device pairing generically.
- Code: browser approval of pairing requests and pairing-request notifications are implemented user-facing behaviors.
- Advisory.

### FR-5 and FR-1 wording drift persists (advisory)

- Evidence: `apps/macos/Sources/OpenClaw/TalkMLXSpeechSynthesizer.swift` and `apps/macos-mlx-tts/Package.swift:1-3` show a local MLX speech helper alongside `apps/shared/OpenClawKit/Sources/OpenClawKit/TalkSystemSpeechSynthesizer.swift`. `apps/macos/Sources/OpenClaw/MenuBar.swift` and `StatusMenuController.swift` implement a macOS menu bar.
- Artifact says: requirements.md:27 requires text-to-speech using system voices, and requirements.md:23 calls the macOS surface a system tray.
- Code: a second local speech engine exists, and macOS documentation reserves "tray" for the Windows and Linux Tauri clients.
- Advisory: wording only, the capabilities exist.

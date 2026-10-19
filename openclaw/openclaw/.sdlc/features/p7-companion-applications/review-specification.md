---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Companion Applications specification

## Sync drift: 2026-10-19

### "Linux desktop app" is listed as out of scope but ships in this repository (blocking)

- Evidence: `apps/linux/README.md:1-3`, `apps/linux/src-tauri/src/tray.rs`, `apps/linux/src-tauri/src/quickchat.rs`, `apps/linux/src-tauri/src/first_run.rs`, `apps/linux/src-tauri/src/gateway.rs`, `apps/linux/src-tauri/src/gateway_profiles.rs`, `apps/linux/src-tauri/src/keep_awake.rs`, `apps/linux/src-tauri/src/desktop_node.rs`, `apps/linux/src-tauri/src/native_browser.rs`, `apps/linux/src-tauri/src/updater.rs`, `apps/linux/src-tauri/src/discovery.rs`, `apps/linux/omarchy/manifest.json`
- Artifact says: "## Out of Scope" lists "- Linux desktop app (Linux users use CLI and channels)" (specification.md:73).
- Code: `apps/linux/` is a Tauri v2 desktop application for Linux and Windows. It discovers Gateways over Bonjour, installs the CLI, manages the local Gateway service, opens the Control UI, keeps a system tray, hosts an inline browser, runs a local desktop-sharing node, and publishes its own AppImage and Debian packages.
- Blocking: the artifact states the opposite of what the code does for a shipped user-facing client.

### The Windows platform stack row points at code that is not in this repository (blocking)

- Evidence: `specification.md:29`, `docs/platforms/windows.md:22-25`, `docs/platforms/windows.md:52-60`, `apps/linux/README.md:5-7`, `apps/linux/README.md:114-116`, `apps/linux/src-tauri/src/gateway_windows.rs`, `apps/linux/src-tauri/src/runtime_action_windows_tests.rs`, `apps/linux/src-tauri/src/cli_windows_tests.rs`
- Artifact says: the platform stacks table lists "| Windows | C# (Windows Hub) | .NET |" (specification.md:29), and the risks section says "Windows Hub is in early stages; capabilities may change" (specification.md:69).
- Code: the repository contains no C# or .NET source. The Windows Hub is a separate WinUI application published from `openclaw/openclaw-windows-node` and is not buildable from this tree. The Windows client that this repository does build is the Rust and TypeScript Tauri app in `apps/linux/src-tauri/`.
- Blocking: a reader would believe the Windows companion is implemented in this repository, and would look for `.csproj` and `.cs` files that do not exist.

### The `DevicePairing` data model does not match the state schema (blocking)

- Evidence: `src/state/openclaw-state-schema.sql:576-599`, `src/state/openclaw-state-schema.sql:553-574`, `src/state/openclaw-state-schema.sql:604-616`, `src/state/openclaw-state-schema.sql:644-666`
- Artifact says: the `DevicePairing` table lists `deviceId` (PK), `userId` (not null), `publicKey` (not null), `pairedAt` (not null), `lastSeen` (nullable) (specification.md:35-41).
- Code: pairing is split across five tables. `device_pairing_paired` has `device_id`, `public_key`, `display_name`, `operator_label`, `platform`, `device_family`, `client_id`, `client_mode`, `browser_origin`, `role`, `roles_json`, `scopes_json`, `approved_scopes_json`, `remote_ip`, `tokens_json`, `approved_via`, `node_surface_json`, `pending_node_surface_json`, `created_at_ms`, `approved_at_ms`, `last_seen_at_ms`, and `last_seen_reason`. `device_pairing_pending` holds unapproved requests, `device_bootstrap_tokens` holds setup and redeem profiles, `device_identities` holds the key pair, and `device_auth_tokens` holds the issued per-role tokens. There is no `userId` column and no `pairedAt` column.
- Blocking: the artifact asserts a schema the code contradicts, and it omits the role, scope, and node-surface model that now governs pairing approval.

### The device pairing sequence has the code-generation direction backwards (blocking)

- Evidence: `extensions/device-pair/README.md:9-14`, `extensions/device-pair/index.ts:218-273`, `extensions/device-pair/index.ts:545-629`, `extensions/device-pair/pair-command-approve.ts`, `extensions/device-pair/pair-command-auth.ts`, `src/state/openclaw-state-schema.sql:604-616`
- Artifact says: "App → Gateway: request pairing code / Gateway → User: display pairing code (CLI/Control UI) / User → App: enter pairing code" (specification.md:48-50).
- Code: the Gateway generates the code. An authorized operator runs `/pair` for a setup code or `/pair qr` for a QR code in an authorized chat, the plugin issues a short-lived setup payload recorded in `device_bootstrap_tokens`, and the device then redeems that payload against the Gateway. The device does not ask the Gateway for a code. The CLI and Control UI surfaces the artifact names are the channel DM-pairing approval surfaces (`openclaw pairing list`, `openclaw pairing approve`, and Settings → Channels → DM access requests), not the device setup-code surface.
- Blocking: the sequence is the core pairing contract, and the current code reverses its first hop.

### The architecture diagram omits the Tauri desktop client (blocking)

- Evidence: `specification.md:14-20`, `apps/linux/src-tauri/src/`, `apps/linux/ui/`
- Artifact says: the diagram shows "Companion App (macOS/iOS/Android/Windows) / Gateway Protocol (WebSocket + RPC) / Gateway Server → Agent Runtime" (specification.md:14-20).
- Code: the Tauri client does not speak the Gateway Protocol as its only transport. It also owns a Rust local Gateway supervisor, a CLI installer, a Bonjour discovery client, a native browser, a desktop relay, an updater, and a local Quick Chat that talks to a Gateway over its own WebSocket and local commands.
- Blocking: the diagram is the reader's mental model of the whole feature, and it leaves out one of the two desktop clients.

### The platform stacks table omits Swift, Rust, and TypeScript clients (advisory)

- Evidence: `specification.md:24-29`, `apps/linux/src-tauri/src/main.rs`, `apps/linux/ui/`, `apps/macos/Package.swift:1-20`, `apps/ios/project.yml:1-20`, `apps/android/settings.gradle.kts`
- Artifact says: the table has four rows for macOS, iOS, Android, and Windows (specification.md:24-29).
- Code: the repository also contains a Rust and TypeScript Tauri client, two standalone Swift packages (`apps/swabble/`, `apps/macos-mlx-tts/`), a watchOS app, a Live Activity widget, a share extension, a wear app, and a shared Swift package family under `apps/shared/`.
- Advisory: the table is a summary, but it is now a summary of a smaller codebase than the one in the tree.

### Technical decisions omit the shared Swift package strategy (advisory)

- Evidence: `apps/macos/Package.swift:25-64`, `apps/ios/project.yml:85-92`, `apps/shared/OpenClawKit/`, `apps/shared/OpenClawMLXTTSProtocol/`, `apps/shared/OpenClawWatchRTC/`
- Artifact says: the decisions table covers communication protocol, voice on iOS, voice on Android, and device pairing (specification.md:58-63).
- Code: the macOS and iOS apps now share chat UI, protocol types, native state, the MLX TTS protocol, and the watch RTC layer through local SwiftPM packages under `apps/shared/`, and both depend on the external `Swabble` package for wake-word gating.
- Advisory: the shared-code strategy is a decision a reader would expect to see recorded.

### Risks do not mention the shared-code or wake-word dependencies (advisory)

- Evidence: `specification.md:65-69`, `apps/macos/Package.swift:64`, `apps/ios/project.yml:90-91`
- Artifact says: the risks are Apple platform restrictions, voice I/O quality variance, and Windows Hub maturity (specification.md:67-69).
- Code: both native apps now carry an out-of-tree SwiftPM dependency on `Swabble` for wake-word gating, which is a new supply-chain and platform-availability risk. The `Swabble` package targets macOS 26 for the Speech.framework pipeline, while the shared `SwabbleKit` gate utilities target iOS 17 and macOS 15 (`apps/swabble/README.md:3`, `apps/swabble/README.md:44-45`).
- Advisory.

### `MediaGenerationRequest` and `TTSRequest` are not the current request shapes (advisory)

- Evidence: `src/tts/tts-request.ts`, `src/tts/tts-types.ts`, `src/tts/provider-types.ts`, `src/media-generation/runtime-shared.ts`
- Artifact says: `MediaGenerationRequest` has `prompt`, `provider`, `options`, `stream`, and `TTSRequest` has `text`, `voice`, `provider` (specification.md:36-49).
- Code: neither `MediaGenerationRequest` nor `TTSRequest` exists. The shipped types are `ImageGenerationRequest` in `src/image-generation/types.ts:57-75`, `SpeechSynthesisRequest` in `src/tts/provider-types.ts:44-50`, and `ResolvedTtsConfig` in `src/tts/tts-types.ts:12-29`. The shared generation runtime takes `cfg`, `agentDir`, `modelOverride`, and `autoProviderFallback` in `src/media-generation/runtime-shared.ts`.
- Advisory: data model granularity, not a contradiction of the requirement text.

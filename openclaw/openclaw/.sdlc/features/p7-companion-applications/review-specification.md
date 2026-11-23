---
artifact: specification
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_df5cb8fcdffe6NShEL28nBp8i3
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

## Sync drift: 2026-11-16

The 2026-10-19 drift remains present. The artifact is unchanged and the code still contradicts the out-of-scope claim, the Windows stack row, the DevicePairing table, and the reversed pairing sequence.

### The pairing data model gained three more tables since 2026-10-19 (blocking)

- Evidence: `src/state/openclaw-state-schema.sql:627-635` (`device_pair_setup_completions`), `:637-642` (`device_pairing_join_codes`), `:644-656` (`device_pairing_browser_requests`). Active consumers include `src/infra/device-pairing-join-code.worker.ts`, `src/infra/device-pairing-browser-code.worker.ts`, and `src/infra/device-bootstrap.test.ts`.
- Artifact says: the specification defines a single `DevicePairing` table with five columns (specification.md:33-41).
- Code: pairing now spans at least nine tables, adding join codes, browser approval requests, setup completion receipts, device identities, per-role auth tokens, and gateway-scoped tokens.
- The 2026-10-19 review already flagged the five-table split. The 2026-11-16 snapshot adds three more tables, so the gap has grown.
- Blocking.

### The pairing sequence omits browser approval and notification hops (advisory)

- Evidence: `extensions/device-pair/notify.ts`, `extensions/device-pair/notify-state.ts`, `extensions/device-pair/api.ts`, `extensions/device-pair/doctor-contract-api.ts`, `extensions/device-pair/index.ts:424-430`.
- Artifact says: the pairing sequence (specification.md:47-54) has five hops ending at an authenticated WebSocket connection.
- Code: the device-pair plugin now exposes a notification service that polls every 10 seconds and a public SDK surface, and a browser approval path exists through `device_pairing_browser_requests`.
- Advisory: the 2026-10-19 review already flagged the reversed first hop. The sequence is now missing two more steps.

### The Tauri client gained new runtime responsibilities (advisory)

- Evidence: `apps/linux/src-tauri/src/bundled_runtime.rs`, `deep_links.rs`, `remote_gateway.rs`, `pending_approvals.rs`, `gateway_control_auth.rs`, `desktop_bridge.rs`, `gateway_ws.rs`, `installer.rs`.
- Artifact says: the architecture diagram (specification.md:14-20) shows one generic companion app speaking the Gateway Protocol.
- Code: the Linux and Windows Tauri client now also manages a bundled Gateway runtime, deep links, remote gateways, pending approvals, gateway control auth, and a desktop bridge.
- Advisory: the 2026-10-19 review already flagged the missing Tauri client. Its responsibilities have grown.

## Sync drift: 2026-11-23

Fresh comparison against the current code confirms the 2026-10-19 and 2026-11-16 drift remains. The artifact is unchanged at `status: done` and the code still contradicts it. Verdict stays `changes-requested`.

### Linux is still marked out of scope while the client ships (blocking)

- Evidence: `apps/linux/README.md:1-3` describes a Tauri v2 app for Linux and Windows. The files `apps/linux/src-tauri/src/tray.rs`, `apps/linux/src-tauri/src/first_run.rs`, `apps/linux/src-tauri/src/gateway.rs`, `apps/linux/src-tauri/src/native_browser.rs`, `apps/linux/src-tauri/src/updater.rs`, and `apps/linux/omarchy/manifest.json` are present.
- Artifact says: specification.md:73 lists "- Linux desktop app (Linux users use CLI and channels)" under Out of Scope.
- Code: the desktop app is built and released for Linux with its own tray, first-run setup, Gateway management, inline browser, and updater.
- Blocking: the out-of-scope claim states the opposite of a shipped client.

### The Windows stack row still points at code outside this tree (blocking)

- Evidence: `docs/platforms/windows.md:22-25` places Windows Hub in `openclaw/openclaw-windows-node`. A tree search returns 0 `.cs` and 0 `.csproj` files. The in-tree Windows code is `apps/linux/src-tauri/src/gateway_windows.rs` and `apps/linux/src-tauri/src/runtime_action_windows_tests.rs`.
- Artifact says: specification.md:29 lists "| Windows | C# (Windows Hub) | .NET |", and specification.md:69 calls Windows Hub early stage.
- Code: the buildable Windows companion is Rust and TypeScript Tauri under `apps/linux/src-tauri/`.
- Blocking: a reader would look for C# sources that do not exist.

### The DevicePairing model still contradicts the state schema (blocking)

- Evidence: `src/state/openclaw-state-schema.sql:577-604` defines `device_pairing_paired` with 22 columns including `role`, `roles_json`, `scopes_json`, `approved_scopes_json`, `node_surface_json`, and `approved_at_ms`. Six pairing tables exist at lines 554, 577, 605, 628, 638, and 645.
- Artifact says: specification.md:35-41 defines a single `DevicePairing` table with `deviceId`, `userId`, `publicKey`, `pairedAt`, and `lastSeen`.
- Code: there is no `userId` or `pairedAt` column, and pairing spans `device_pairing_pending`, `device_pairing_paired`, `device_bootstrap_tokens`, `device_pair_setup_completions`, `device_pairing_join_codes`, and `device_pairing_browser_requests`.
- Blocking: the artifact asserts a schema the code contradicts.

### The pairing sequence still reverses code generation (blocking)

- Evidence: `extensions/device-pair/README.md:9-14` documents that an authorized chat runs `/pair` or `/pair qr` and the Gateway issues the setup payload. `extensions/device-pair/pair-command-approve.ts` and `extensions/device-pair/pair-command-auth.ts` implement approval.
- Artifact says: specification.md:48-50 has "App → Gateway: request pairing code" followed by "Gateway → User: display pairing code".
- Code: the Gateway generates the code and the device redeems it; the app never requests a code first.
- Blocking: the first hop of the core pairing contract is wrong.

### The architecture diagram still omits the Tauri client (blocking)

- Evidence: `apps/linux/src-tauri/src/bundled_runtime.rs`, `deep_links.rs`, `remote_gateway.rs`, `desktop_bridge.rs`, `gateway_control_auth.rs`, `pending_approvals.rs`, and `apps/linux/ui/` are present.
- Artifact says: specification.md:14-20 shows one generic companion app speaking only "Gateway Protocol (WebSocket + RPC)".
- Code: the Tauri client also supervises a bundled Gateway runtime, handles deep links and remote gateways, owns a desktop bridge, gates gateway control auth, and tracks pending approvals.
- Blocking: the mental model leaves out one of two desktop clients and its responsibilities.

### The platform stacks and decisions tables omit shared Swift code (advisory)

- Evidence: `apps/macos/Package.swift:24-25` depends on `../shared/OpenClawKit` and `../shared/OpenClawMLXTTSProtocol`. `apps/ios/project.yml:17-19` and `:88-94` depend on `OpenClawKit` and `Swabble`. `apps/shared/` holds `OpenClawKit`, `OpenClawMLXTTSProtocol`, and `OpenClawWatchRTC`.
- Artifact says: specification.md:24-29 lists only four platform rows, and specification.md:58-63 omits the shared-code strategy.
- Code: chat UI, protocol types, native state, MLX TTS protocol, and watch RTC are shared through local SwiftPM packages, with `SwabbleKit` as an external wake-word dependency.
- Advisory.

---
artifact: tests
verdict: changes-requested
reviewed_at: 2026-10-19
session_link: http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA
---

# Review: Companion Applications test plan

## Sync drift: 2026-10-19

### A listed test file no longer exists (blocking)

- Evidence: `test/scripts/ios-pull-gateway-log.test.ts` is absent, `grep -rl "pull-gateway-log" --include="*.ts" --include="*.mjs" --include="*.js" .` returns no match outside `node_modules`
- Artifact says: "| `test/scripts/ios-pull-gateway-log.test.ts` | iOS gateway log retrieval |" (tests.md:25).
- Code: the file was removed and no replacement with the same responsibility exists in `test/scripts/` or `apps/ios/scripts/`. The remaining `apps/ios/scripts/` directory holds only `app-icon-debug-dark.swift` and `app-icon-variants.sh`.
- Blocking: the plan points a reviewer at a file that cannot be opened.

### The native test inventory covers Android only (blocking)

- Evidence: `apps/ios/Tests/` (118 files), `apps/ios/UITests/` (11 files), `apps/ios/WatchTests/` (4 files), `apps/macos/Tests/OpenClawIPCTests/` (294 files), `apps/shared/OpenClawKit/Tests/` (201 files), `apps/swabble/Tests/` (6 files), `apps/macos-mlx-tts/Tests/` (1 file), `apps/linux/tests/` (19 files), `apps/linux/src-tauri/tests/` (5 files), `apps/android/app/src/test/` (278 files), `apps/android/wear/src/test/` (24 files), `apps/android/wear-shared/src/test/` (3 files)
- Artifact says: the native platform test table lists only "| Android | `apps/android/app/src/test/` | JUnit |" and "| Android (wear) | `apps/android/wear/src/test/`, `apps/android/wear-shared/src/test/` | JUnit |" (tests.md:31-34).
- Code: iOS has three XCTest suites including a watchOS suite, macOS has a large Swift suite under `apps/macos/Tests/OpenClawIPCTests/`, the shared Swift package family has its own XCTest suite, and the Tauri desktop client has both Rust tests and Python scenario drivers. The plan names three of the twelve native suite locations in the tree.
- Blocking: the plan understates the native suites, so a reader would not know that the iOS, macOS, shared, and desktop behaviors have native coverage.

### The scope statement excludes macOS testing that now exists (blocking)

- Evidence: `tests.md:10`, `apps/macos/Tests/OpenClawIPCTests/` (294 files), `apps/macos/AGENTS.md:9-15`
- Artifact says: "Does not cover macOS app UI testing or Windows Hub testing outside CI scripts." (tests.md:10)
- Code: `apps/macos/` has a native Swift test target that `apps/macos/AGENTS.md:9-10` tells contributors to build with `swift build --package-path apps/macos --build-system native --build-tests`. It covers app lifecycle, dashboard windows, exec approvals, node permissions, and control UI download behavior.
- Blocking: the scope statement tells a reader the opposite of what the tree contains.

### The coverage matrix claims coverage that does not exist (blocking)

- Evidence: `tests.md:40-45`, `apps/ios/Sources/Push/PushRegistrationManager.swift`, `apps/ios/Sources/Push/PushRelayClient.swift`, `apps/macos/Sources/OpenClaw/MenuBar.swift`, `src/gateway/` device auth tests
- Artifact says: "| FR-1 (macOS tray) | Covered by macOS app build/CI |" and "| FR-2 (iOS push notifications) | Covered by iOS release tests |" (tests.md:40-41).
- Code: the listed iOS test files are release-script tests (version validation, signing, Fastlane gates, release planning). None of them assert push delivery or notification presentation. The macOS tray is a SwiftUI menu bar surface, and a build does not cover it. The real coverage for these behaviors lives in native suites and in Gateway-side tests that the matrix does not name.
- Blocking: the matrix asserts proof that does not exist, which misdirects anyone reviewing whether FR-1 and FR-2 are actually verified.

### The CI and script test table omits most companion release and runtime lanes (advisory)

- Evidence: `test/scripts/android-access-workflow.test.ts`, `test/scripts/android-app-i18n.test.ts`, `test/scripts/android-firebase-distribution.test.ts`, `test/scripts/android-mermaid-assets.test.ts`, `test/scripts/android-perf-scripts.test.ts`, `test/scripts/android-release-artifacts.test.ts`, `test/scripts/android-release-e2e-workflow.test.ts`, `test/scripts/android-release-fastlane-gates.test.ts`, `test/scripts/android-release-wrapper-args.test.ts`, `test/scripts/android-screenshots.test.ts`, `test/scripts/android-store-version.test.ts`, `test/scripts/apple-app-i18n.test.ts`, `test/scripts/apple-build-cache.test.ts`, `test/scripts/apple-release-source-check.test.ts`, `test/scripts/ios-configure-signing.test.ts`, `test/scripts/ios-lifecycle-workflow.test.ts`, `test/scripts/ios-node-e2e.test.ts`, `test/scripts/ios-release-e2e.test.ts`, `test/scripts/ios-release-e2e-build.test.ts`, `test/scripts/ios-release-gateway.test.ts`, `test/scripts/ios-release-screenshot-upload.test.ts`, `test/scripts/ios-release-signing.test.ts`, `test/scripts/ios-release-wrapper-args.test.ts`, `test/scripts/ios-run.test.ts`, `test/scripts/ios-screenshot-evidence.test.ts`, `test/scripts/ios-validate-app-store-ipa.test.ts`, `test/scripts/ios-watch-runtime.test.ts`, `test/scripts/ios-watch-simulator.test.ts`, `test/scripts/linux-app-channel.test.ts`, `test/scripts/linux-updater-manifest.test.ts`, `test/scripts/tauri-workflow.test.ts`, `test/scripts/macos-native-test-launch.test.ts`, `test/scripts/package-mac-app.test.ts`, `test/scripts/codesign-mac-app.test.ts`, `test/scripts/notarize-mac-artifact.test.ts`, `test/scripts/mac-runtime.test.ts`, `test/scripts/watch-node.test.ts`, `test/scripts/watch-pr-ci.test.ts`
- Artifact says: the CI and script test table lists 11 files plus a helper glob (tests.md:14-27).
- Code: the companion-related script tests number in the dozens, including dedicated Linux desktop and Tauri workflow suites that have no counterpart in the plan.
- Advisory: the plan is a partial list, and the omitted lanes are release and packaging lanes rather than behavior lanes.

### The desktop client scenario drivers are not covered (advisory)

- Evidence: `apps/linux/tests/first_run.py`, `apps/linux/tests/gateway_switch.py`, `apps/linux/tests/inline_browser.py`, `apps/linux/tests/quick_chat.py`, `apps/linux/tests/desktop_sharing.py`, `apps/linux/tests/packaged_runtime_smoke.py`, `apps/linux/tests/remote_connection_smoke.py`, `apps/linux/tests/window_chrome.py`, `apps/linux/tests/test_first_run.py`, `apps/linux/tests/test_desktop_sharing_reports.py`, `apps/linux/tests/test_packaged_runtime_smoke.py`
- Artifact says: no desktop client scenario driver appears in the plan (tests.md:8-45).
- Code: the Tauri client has Python drivers that exercise real X11 pointer input, native title bar geometry, Gateway switching, first-run onboarding, inline browser behavior, Quick Chat, and desktop sharing, plus unit tests for the reporting and packaged runtime smoke paths.
- Advisory: a new client surface with substantial test coverage is invisible in the plan.

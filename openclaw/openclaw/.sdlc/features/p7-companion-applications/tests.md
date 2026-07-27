---
title: "Companion Applications"
status: done
---

# Test Plan: Companion Applications

## Scope

Tests cover platform-specific build and release scripts, version validation, and native test suites for Android (Kotlin/JUnit) and iOS (XCTest). Does not cover macOS app UI testing or Windows Hub testing outside CI scripts.

## CI/Script Tests

| File | Description |
|---|---|
| `test/scripts/android-version.test.ts` | Android version validation |
| `test/scripts/android-release-signing.test.ts` | Android release signing verification |
| `test/scripts/android-pin-version.test.ts` | Android version pinning |
| `test/scripts/run-android-gradle.test.ts` | Android Gradle build execution |
| `test/scripts/ios-version.test.ts` | iOS version validation |
| `test/scripts/ios-release-prepare.test.ts` | iOS release preparation |
| `test/scripts/ios-release-plan.test.ts` | iOS release planning |
| `test/scripts/ios-team-id.test.ts` | iOS team ID validation |
| `test/scripts/ios-release-fastlane-gates.test.ts` | iOS Fastlane gate checks |
| `test/scripts/ios-pull-gateway-log.test.ts` | iOS gateway log retrieval |
| `test/scripts/ios-periphery-comment-workflow.test.ts` | iOS Periphery comment workflow |
| `test/helpers/gateway/android-node-capabilities-*.ts` | Android node capabilities test helpers |

## Native Platform Tests

| Platform | Test Location | Framework |
|---|---|---|
| Android | `apps/android/app/src/test/` | JUnit |
| Android (wear) | `apps/android/wear/src/test/`, `apps/android/wear-shared/src/test/` | JUnit |

## Coverage Matrix

| Requirement | Test Coverage |
|---|---|
| FR-1 (macOS tray) | Covered by macOS app build/CI |
| FR-2 (iOS push notifications) | Covered by iOS release tests |
| FR-3 (Android voice I/O) | Covered by Android native tests |
| FR-4 (Gateway connection) | Covered by gateway node capability tests |
| FR-7 (Device pairing) | Covered by gateway auth tests |
| NFR-1 (Secure pairing) | Covered by gateway auth tests |

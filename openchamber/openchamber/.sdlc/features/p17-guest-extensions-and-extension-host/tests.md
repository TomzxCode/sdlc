---
title: "Guest extensions and extension host"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test Plan: Guest extensions and extension host

## Scope

The plan covers the shipped tests for the SDK contract, installation and catalog, capability approval, asset serving, guest services, service roles, extension waits, and the UI host bridge.
It records the tests that exist in `packages/sdk/src`, `packages/web/server/lib/guests`, `packages/web/server/lib/extension-waits`, and `packages/ui/src/lib/guests`.
It does not cover browser end-to-end automation or the OpenCode plugin manager.
The test plan is retrospective: the cases below describe existing files, not new work.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Parse valid manifests in both envelope forms (`packages/sdk/src/parse.test.ts`) | Bare `openchamber` block and `package.json` with `version` and `openchamber` | Parsed contribution and optional semver version. |
| TC-2 | Refuse invalid manifests (`packages/sdk/src/parse.test.ts`) | Bad version, `apiVersion: 2`, junk engine range, escaping entry, bad panel id, invalid capabilities | Specific code such as `invalid-version`, `unsupported-api-version`, `invalid-engines`, `invalid-panel-entry`, or `invalid-capabilities`. |
| TC-3 | Derive requested capabilities (`packages/sdk/src/parse.test.ts`) | Filesystem list, actions with a messages payload, service, integration, waits, marks | Derived grants such as `filesystem`, `conversation`, `service`, `network`, `wake`, and `marks`. |
| TC-4 | Compare host engine versions (`packages/sdk/src/host-version.test.ts`) | Exact, ranged, and junk `engines.openchamber` values | Install is allowed or refused with `host-too-old`. |
| TC-5 | Read wire envelopes (`packages/sdk/src/protocol.test.ts`) | Wrong channel, wrong version, malformed push, and result messages | Only valid `openchamber.sdk` v1 messages pass. |
| TC-6 | Open a guest connection (`packages/sdk/src/host.test.ts`) | Fake `HostFrame`, parent and non-parent message sources | `hello` is posted and `ready` is delivered only from the parent frame. |
| TC-7 | Correlate calls and results (`packages/sdk/src/host.test.ts`) | Matching ids, host error codes, and a silent host | Promise resolves, rejects with `HostRequestError`, or times out. |
| TC-8 | Validate host call payloads (`packages/sdk/src/host.test.ts`) | Oversized compose, bad file path, invalid toast, unadvertised feature | Local rejection without posting, or clamped wire payload. |
| TC-9 | Read wait arguments and wire requests (`packages/sdk/src/waits.test.ts`) | Wait args with optional `undefined`, bad JSON, wrong `v`, malformed entries | Typed args preserved in memory and refused wire bodies return null. |
| TC-10 | Check service provider contracts (`packages/sdk/src/service-providers.test.ts`) | Browser, source-control, notifications, tracker, and quota envelopes | Only declared actions, deadlines, and deeply checked answers are accepted. |
| TC-11 | Check frame policy and scrollbar assets (`packages/sdk/src/frame-policy.test.ts`) | Guest frame policies and scrollbar styles/scripts | Sandbox policy and appended assets match the SDK contract. |
| TC-12 | Compute guest grant scope (`packages/web/server/lib/guests/grant-scope.test.js`) | Filesystem patterns, integration URLs, service exec names and sockets | Sorted scope used for approval and later narrowing. |
| TC-13 | Mint and expire frame grants (`packages/web/server/lib/guests/frame-grants.test.js`) | Grants for two extensions, unknown grant, and idle expiry | One random grant per extension with scoped access and expiry. |
| TC-14 | Guard instance storage (`packages/web/server/lib/guests/storage.test.js`) | Device scope, missing key, stored null, concurrent write and uninstall | Device scope refused, `found` is accurate, and removed namespaces are not recreated. |
| TC-15 | Resolve guest file paths (`packages/web/server/lib/guests/files.test.js`) | Relative path, `~/` path, symlink escape, NUL, backslash, `..` | Project or matched filesystem scope, or `BAD_PATH` without a disk probe where relevant. |
| TC-16 | Track service registry and lifetime (`packages/web/server/lib/guests/service-registry.test.js`, `service-lifetime.test.js`) | Ready failure, idle timeout, keepRunning, schedule | Service states, restarts, and scheduled runs follow the declared policy. |
| TC-17 | Serve the service host API (`packages/web/server/lib/guests/service-host-api.test.js`) | Service bearer, paused guest, session answer and permission calls | Calls are authorized per catalog row and answered with control-service results. |
| TC-18 | Guard proxy and auth store (`packages/web/server/lib/guests/request.test.js`, `auth-store.test.js`) | Changed target, 401 refresh race, token without target | Stale credentials are dropped under lock and the proxy stays on the declared origin. |
| TC-19 | Constrain ZIP inflation (`packages/web/server/lib/guests/extract-zip.test.js`) | Declared size smaller than output, encrypted or parent-path entry | Oversized streams are refused before allocation and unsafe entries are rejected. |
| TC-20 | Answer guest messages in the UI (`packages/ui/src/lib/guests/host-bridge.test.ts`) | Toast, open-url, attach, start-session, service-request, file calls, unknown surface | `okResult` or `errorResult` with the matching id and code. |
| TC-21 | Parse catalog rows defensively (`packages/ui/src/lib/guests/parse.test.ts`) | Unknown value in a known field and a row from a newer server | Field is dropped and the remaining row stays usable. |
| TC-22 | Project extension waits in the UI (`packages/ui/src/sync/extension-waits.test.ts`) | Snapshot and updated event with revision and `waiting` or `waking` states | Client drops stale revisions and renders the session's wait list. |
| TC-23 | Load frame documents and surface clients (`packages/ui/src/lib/guests/surface-client.test.ts`, `frame-url.test.ts`, `useGuestFrameUrl.test.tsx`) | Grant URL, relay document, expired token, frame and ack messages | Correct URL or `srcDoc`, reconnect behavior, and paired frame acknowledgement. |
| TC-24 | Check status controls, popovers, and toasts (`packages/ui/src/lib/guests/status-controls.test.ts`, `popovers.test.ts`, `toast.test.tsx`) | Control publish burst, popover under a dialog, toast button after frame exit | Bounded publishes, safe layering, and buttons that keep their own data. |
| TC-25 | Namespace device storage (`packages/ui/src/lib/guests/device-storage-records.test.ts`) | Runtime, installation id, and guest id combinations | One JSON tuple key per identity with no delimiter ambiguity. |
| TC-26 | Hold sidebar marks (`packages/web/server/lib/guests/marks.test.js`) | Mark from an ended service, token change, same-value set | Stale marks are dropped and an unchanged set spends no budget. |
| TC-27 | Settle deactivation listeners (`packages/web/server/lib/guests/deactivation-listeners.test.js`) | One listener throws after pause | Remaining listeners run and the stored change stands. |
| TC-28 | Register built-ins (`packages/web/server/lib/guests/builtins.test.js`) | Registry entries with reserved ids and declared grants | Built-ins load enabled with only their declared grants and cannot be removed. |
| TC-29 | Apply enterprise policy (`packages/web/server/lib/guests/enterprise.test.js`) | Allowed Git source, local folder setting, ZIP source, policy change | Capabilities are stripped or refused and blocked rows are marked. |
| TC-30 | Check update candidates (`packages/web/server/lib/guests/updates.test.js`) | Newer and older semver `FETCH_HEAD` package, failed fetch | Only newer versions are reported and a failed fetch is not cached. |
| TC-31 | Append guest HTML assets (`packages/web/server/lib/guests/html-styles.test.js`) | HTML with authored CSP, inline script, and mixed-case doctype | Scrollbar assets and color-scheme meta are appended without breaking the document. |
| TC-32 | Run a shared surface session (`packages/web/server/lib/guests/surface.test.js`) | Viewer input, control handoff, resizing, and viewer disconnect | Monotonic frames, one controller, and a queued input that cannot re-take control. |
| TC-33 | Check session-facing contributions (`packages/web/server/lib/guests/session-events.test.js`, `agent-context.test.js`, `instructions.test.js`) | Enabled guest with events, skills, instructions, and plugin folder | Subscriptions, managed config folders, and instructions follow approval and pause state. |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-34 | Install from folder, ZIP, and Git (`packages/web/server/lib/guests/install.test.js`) | Isolated data dir and fixture packages | 201 on install, 200 on replace, duplicate ids refused, copies removed on uninstall. |
| TC-35 | Refuse an unsupported host (`packages/web/server/lib/guests/install.test.js`) | Fixture requiring a newer `engines.openchamber` | `host-too-old` with the required version and no catalog row. |
| TC-36 | Enforce network install rules (`packages/web/server/lib/guests/install.test.js`, `ssh-install.test.js`, `clone-network.test.js`) | Public HTTPS, private redirect, private DNS answer, SSH identity | Pinned HTTPS hops, refused private targets, and no fallback to global auth when an identity is missing. |
| TC-37 | Upload a ZIP body (`packages/web/server/lib/guests/upload.test.js`) | Wrong content type, oversized body, and valid archive | 415 or 413 before reading, or the same result shape as a ZIP path install. |
| TC-38 | List catalog variants (`packages/web/server/lib/guests/catalog.test.js`) | Page-only, status-only, editor-only, background-only, tools-only, and docked fixtures | Each valid shape publishes the right frames and capabilities; invalid shapes are skipped or refused. |
| TC-39 | Complete OAuth (`packages/web/server/lib/guests/oauth.test.js`, `host-session.test.js`) | Pending state, changed target, host Linear descriptor | Stateful callback, `TARGET_CHANGED` when endpoints move, and host access only through a capable tracker. |
| TC-40 | Proxy guest and service requests (`packages/web/server/lib/guests/request.test.js`, `service.test.js`) | Approved guest, paused guest, absent service, and oversized answer | Declared-origin requests succeed; paused, missing, and oversized cases return `DISABLED`, `NO_SERVICE`, and `RESPONSE_TOO_LARGE`. |
| TC-41 | Run extension waits end to end (`packages/web/server/lib/extension-waits/runtime.test.js`) | Approved wait provider and a stub service answering `/waits/start` and `/waits/check` | Start, check, one wake, stop, and a client list that reflects `waiting` and `waking`. |
| TC-42 | Recover from wait failures (`packages/web/server/lib/extension-waits/runtime.test.js`) | Malformed envelope, failing checks, unreadable entry, and racing check runs | Backoff, ended wake after six hours, only the bad wait ends, and one in-flight check per type. |
| TC-43 | Drive a guest session from the UI (`packages/ui/src/lib/guests/start-session.integration.test.ts`) | Loaded catalog, selected session, and host bridge effects | A guest-started session is created with the requested selection and model behavior. |

## End-to-End Tests

No dedicated browser end-to-end test file exists in the source areas for this feature.
Route tests run the Express app in-process with isolated data dirs and loopback supertest, and UI tests drive the host bridge with injected frame effects.

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-44 | A catalog response contains a row this build cannot read. | The row is listed as unreadable and removable and every other row loads. |
| TC-45 | A catalog fetch fails. | The host reports an error instead of an empty catalog and keeps the last shown marks and waits. |
| TC-46 | A wait check answer has a bad envelope. | No wait fires, state does not move, and the type is asked again after doubled backoff. |
| TC-47 | One malformed entry in a valid check batch. | Only that entry's wait ends; the other waits keep their state. |
| TC-48 | A service stays broken for six hours. | The wait ends with an `ended` wake that says why. |
| TC-49 | A frame grant is expired or absent on an older server. | The client mints a fresh grant or falls back to the legacy scoped token, with no runtime credential in the page. |
| TC-50 | A guest is paused between the service request's enabled check and the proxy call. | The stop epoch prevents a spawned process and the call ends with `NO_SERVICE`. |
| TC-51 | Storage exceeds a key, value, count, or namespace cap. | The write is refused and previously stored bytes remain. |
| TC-52 | An archive or file path tries to escape its root. | Symlink, `..`, URL, and parent-path entries are refused before use. |
| TC-53 | Enterprise policy changes after an approval. | The next catalog read strips the refused grants and every proxy refuses them. |
| TC-54 | A timer comes due while the catalog cannot be read. | It is marked fired and its wake waits for the check pass to finish; it is not cancelled. |
| TC-55 | Two starts race at the wait caps. | Both starts hold a reservation and one is refused with 409 instead of evicting a wait. |
| TC-56 | A deactivation listener throws. | The failure is logged and other listeners and the stored change still complete. |

## Test Infrastructure

- SDK and UI tests run through `node ../../scripts/run-isolated-tests.mjs`, invoked by `bun run --cwd packages/sdk test` and `bun run --cwd packages/ui test`.
- Web tests run through `bun run --cwd packages/web test`, which calls `vitest run` and a separate Node test command.
- `packages/web/vitest.config.ts:21` sets isolated data directories, a loopback supertest shim, and a 30-second test timeout.
- Guest tests use fixture packages with built classic-IIFE scripts, temporary data directories, and in-process Express apps.
- Service and wait tests use stub loopback services that answer `/waits/start`, `/waits/check`, and readiness probes.
- Frame tests use the SDK's injectable `HostFrame` so parent, child, and unrelated message sources are distinguishable.
- No real tokens, pairing credentials, or user files are used in the fixtures.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-5, TC-6, TC-11 |
| FR-2 | TC-34, TC-35, TC-36, TC-37, TC-28 |
| FR-3 | TC-1, TC-2, TC-4, TC-38 |
| FR-4 | TC-3, TC-12, TC-29, TC-38, TC-53 |
| FR-5 | TC-13, TC-23, TC-31, TC-49, TC-52 |
| FR-6 | TC-5, TC-6, TC-7, TC-20 |
| FR-7 | TC-8, TC-17, TC-18, TC-20, TC-24, TC-40, TC-43 |
| FR-8 | TC-21, TC-23, TC-24, TC-32, TC-38 |
| FR-9 | TC-16, TC-17, TC-40, TC-50 |
| FR-10 | TC-27, TC-33, TC-56 |
| FR-11 | TC-9, TC-41, TC-42, TC-46, TC-47, TC-48, TC-54, TC-55 |
| FR-12 | TC-22, TC-26, TC-27, TC-41, TC-56 |
| FR-13 | TC-28, TC-29, TC-53 |
| FR-14 | TC-23, TC-38, TC-43 |
| FR-15 | TC-14, TC-18, TC-25, TC-39 |
| FR-16 | TC-30 |
| FR-17 | TC-1, TC-9, TC-10 |
| NFR-1 | TC-12, TC-13, TC-15, TC-18, TC-19, TC-49, TC-52 |
| NFR-2 | TC-21, TC-27, TC-44, TC-45, TC-56 |
| NFR-3 | TC-13, TC-14, TC-19, TC-24, TC-51, TC-55 |
| NFR-4 | TC-1, TC-2, TC-5, TC-21 |
| NFR-5 | TC-27, TC-30, TC-56 |
| NFR-6 | TC-1, TC-5, TC-11, TC-20, TC-33 |

---
title: "Enterprise policy and request security"
status: done
---

# Test Plan: Enterprise policy and request security

## Scope

The tests cover policy file discovery and validation, fail-closed behavior, policy change watching, the public projection, provider and credential route classification, origin decisions, session-cookie slot extraction, frame ancestors, socket upgrade rejection, bind-host classification, and the advertised LAN URL.
The three files in this plan are unit suites that call exported helpers with injected files, environment objects, settings readers, and sockets.
No dedicated integration or end-to-end test file belongs to this feature.
Adjacent suites cover the HTTP handlers, CLI startup refusal, trusted-proxy rate limiting, and app-link trust store, and they are listed under Test Infrastructure rather than counted here.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Enterprise mode is off with no file and no environment switch | Empty machine | Full default policy with enterpriseMode false and source null |
| TC-2 | The environment switch alone turns the mode on | `OPENCHAMBER_ENTERPRISE_MODE=true` | enterpriseMode true, source environment |
| TC-3 | A valid file turns the mode on and carries pins | File with organization, relayUrl, and jev | All three values present and policyError null |
| TC-4 | A governing file ignores user-settable environment pins | File with enterpriseMode true plus relay, Jev, network, and extension variables | Relay and Jev null, network access false, extension list empty |
| TC-5 | Environment pins apply when the file leaves the mode off | No governing file plus relay and network variables | Relay URL and network access read from the environment |
| TC-6 | File values win per field and gaps fill from the environment | File with relayUrl only plus Jev environment variables | File relay URL and environment Jev values |
| TC-7 | A file Jev object is not mixed with environment fields | File Jev URL plus an environment Jev model | Model and API key null |
| TC-8 | Allowed extensions come from the file or the environment | Governing file, file allowlist, and environment-only mode | Each source yields the expected trimmed list |
| TC-9 | Built-in catalog hiding is file-only | File switch, environment switch, and broken file | True from file, false from environment, true when the file is broken |
| TC-10 | OpenCode binary pinning is file-only | File path, environment path, blank path, numeric path | Trimmed file path, null from environment, null when invalid, present in public projection |
| TC-11 | Network access is blocked unless explicitly allowed | Enterprise file, allowing file, environment mode, and broken file | Blocked by default and unblocked only with an explicit allowance |
| TC-12 | Network access is never blocked outside enterprise mode | Empty machine | Blocking predicate false |
| TC-13 | The environment cannot turn a file policy off | File enterpriseMode true plus environment value 0 | enterpriseMode stays true |
| TC-14 | The environment can turn the mode on when the file leaves it off | File enterpriseMode false plus environment value 1 | source is environment |
| TC-15 | Invalid policy files fail closed | Malformed JSON, array, non-boolean switch, non-string relay, Jev without URL | enterpriseMode true, source policy-file, policyError names path, all pins null |
| TC-16 | An unreadable policy file fails closed | Read function raises EACCES | enterpriseMode true and policyError contains the permission error |
| TC-17 | A byte-order mark is stripped before parsing | File text beginning with U+FEFF | organization read successfully and policyError null |
| TC-18 | Unknown policy keys are ignored | File with a future key | enterpriseMode true |
| TC-19 | The public projection hides pinned data | File with relay, Jev URL, model, API key, and organization | Payload contains only the six public fields |
| TC-20 | Policy paths are fixed per platform | darwin, linux, and win32 options | Platform-specific paths with the fixed Windows path first |
| TC-21 | A Windows ProgramData redirect cannot hide a policy | Redirected environment path with a conflicting policy | Fixed path wins and enterpriseMode true |
| TC-22 | Windows falls back to the redirected ProgramData | Only the redirected file exists | enterpriseMode true from the fallback path |
| TC-23 | The watcher ignores unchanged policies | Repeated identical reads across intervals | Change callback never called |
| TC-24 | The watcher fires once on a change and stops cleanly | Read function changes on the third call then stops | One callback, no further reads after stop |
| TC-25 | Provider-connect paths are classified | POST integration connect, credential, and wellknown paths | Each path classified as protected |
| TC-26 | Obfuscated provider paths are still classified | Mixed case, doubled separators, backslashes, percent escapes, semicolon suffixes | Each path classified as protected |
| TC-27 | Unsafe provider paths fail closed | Dot segments and malformed percent escapes | Each path classified as protected |
| TC-28 | MCP sign-in paths are allowed | MCP integration id with oauth and attempt completion | Not classified as a protected provider request |
| TC-29 | Non-MCP integration paths stay protected | MCP id with key or command, malformed attempt id, extra suffix | Each path classified as protected |
| TC-30 | Unrelated methods and paths are left alone | GET, DELETE, session posts, and health checks | Not classified as provider-connect |
| TC-31 | Credential list paths are classified | GET and HEAD variants including case, separators, and escapes | Each path classified as protected |
| TC-32 | Unsafe credential paths fail closed | Dot segments and malformed escapes | Each path classified as protected |
| TC-33 | Non-routed credential paths are left alone | Asset, docs, and encoded separator paths | Not classified as credential-list |
| TC-34 | Credential management methods are left alone | POST, PATCH, and DELETE on credential routes | Not classified as credential-list |
| TC-35 | Packaged client origins are allowed | openchamber-ui://app, capacitor://localhost, https://localhost | Promise resolves true |
| TC-36 | An unknown origin is refused | https://evil.example.com with a LAN host | Promise resolves false |
| TC-37 | A browser HTTPS origin survives a plain forwarded hop | x-forwarded-proto http and matching external host | Promise resolves true |
| TC-38 | A forwarded host does not trust an unrelated origin | Forwarded host plus matching and evil origins | First true, second false |
| TC-39 | The cookie slot for the request port is read | Two cookies for neighboring ports | Token for the request port returned |
| TC-40 | Another port's cookie is not borrowed | Only a cookie for a different port | null returned |
| TC-41 | A bare host uses the bare cookie | Host without an explicit port | Bare token returned |
| TC-42 | No UI session cookie returns null | Cookie header with unrelated cookies | null returned |
| TC-43 | Another loopback port is trusted only in development | Dev page origin against released and development runtimes | False then true, with the environment flags checked |
| TC-44 | Passwordless sockets refuse foreign pages and keep non-browser clients | Foreign origin, other dev port, same host, packaged origin, and no origin | False, false, true, true, true |
| TC-45 | Origin checks are promises on both paths | Packaged fast path and settings-dependent path | Each call returns a Promise before it resolves |
| TC-46 | Frame ancestors contain only allowed sources | Default, development, extra plain origins, wildcard, and directive injection | Expected sources present and injected directive absent |
| TC-47 | Stored origins are validated and read failures are contained | Null, empty, numeric, invalid, valid-with-path, and throwing readers | Only the valid origin adds a candidate, and request-derived candidates survive failures |
| TC-48 | Header arrays and malformed cookie escapes are handled | Array forwarded host, array origin, empty array, array cookie, bad escape | First values used where defined, empty array rejects, raw escape value returned |
| TC-49 | Upgrade rejection writes a response and destroys the socket | Writable socket with 503 and blank reason, then write and destroy failures | Valid HTTP line and body written, socket destroyed, no exception escapes |
| TC-50 | Proven loopback bind hosts are classified as local | localhost, 127.0.0.1, 127.25.1.2, ::1, [::1], and IPv4-mapped loopback | isLoopbackBindHost true and isNetworkExposedBindHost false |
| TC-51 | Wildcard and non-loopback hosts are classified as exposed | Wildcards, LAN, IPv6 link-local, names, numeric oddities, and empty string | isLoopbackBindHost false and isNetworkExposedBindHost true |
| TC-52 | A valid LAN URL reduces to an origin | Trimmed HTTP and HTTPS origins with a trailing slash | Origin returned without warning |
| TC-53 | An unset LAN URL returns null | Empty environment | null returned with no warning |
| TC-54 | A malformed LAN URL is ignored with a warning | Bare address, wrong scheme, path, and query values | null returned and one warning logged per value |

## Integration Tests

No dedicated integration test file belongs to this feature.
The HTTP refusal codes are exercised by `packages/web/server/lib/opencode/provider-source-route.test.js`, and the CLI bind refusal is exercised by `packages/web/bin/cli.test.js`.
The shared origin checker is injected into the terminal, event-stream, dictation, dev-tunnel, spaces, and realtime-proxy suites, which test their own upgrade behavior.

## End-to-End Tests

No dedicated end-to-end test file belongs to this feature.
The settings surface and the app-link trust flow are covered by component and store tests listed under Test Infrastructure.

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-15 | Policy file is not JSON, not an object, or has wrong field types | Fail closed with a policy error and no pins |
| TC-16 | Policy file cannot be read | Fail closed with the error in policyError |
| TC-17 | Policy file has a byte-order mark | Parse successfully |
| TC-21 | Windows ProgramData is redirected to a file with a conflicting policy | Fixed machine path wins |
| TC-24 | Policy polls return the same serialized value | No change callback |
| TC-27 | Provider path contains a dot segment or bad escape | Refuse rather than guess the route |
| TC-32 | Credential path contains a dot segment or bad escape | Refuse rather than guess the route |
| TC-33 | Encoded separator changes the first path segment | Leave the request alone because OpenCode does not route it to the list |
| TC-40 | A browser sends only another port's cookie | Stay unauthenticated for this port |
| TC-44 | A page opens a passwordless socket from a foreign origin | Refuse the upgrade |
| TC-47 | Settings reader throws or returns invalid data | Keep request-derived candidates and fail closed on the untrusted origin |
| TC-48 | Forwarded-host header is an empty array | Reject the promise with TypeError |
| TC-49 | Writing the rejection fails | Still destroy the socket and do not throw |
| TC-51 | Bind host is an unusual numeric or wildcard value | Treat it as network-exposed |
| TC-54 | LAN URL includes a path or query | Ignore it and warn |

## Test Infrastructure

- `packages/web/server/lib/enterprise-mode.test.js` uses vitest with a fake machine helper that injects platform, environment, and file reads.
- `packages/web/server/lib/security/request-security.test.js` uses bun:test with injected settings readers and fake sockets.
- `packages/web/server/lib/security/bind-host.test.js` uses vitest with environment objects and a warning logger spy.
- Vitest fake timers drive the policy watcher without waiting for the 15-second interval.
- Adjacent, not owned here: `packages/web/server/lib/opencode/provider-source-route.test.js` proves the 403 `enterprise_mode` and 403 `credential_list_refused` handlers.
- Adjacent, not owned here: `packages/web/bin/cli.test.js` proves the unauthenticated network-bind refusal.
- Adjacent, not owned here: `packages/web/server/lib/relay/tunnel-host.test.js` proves `rateLimitKey` behavior with trusted proxies and relay provenance.
- Adjacent, not owned here: `packages/ui/src/stores/appLinkTrustStore.test.ts` and `packages/ui/src/components/chat/appLinkConfirmation.test.ts` cover trust list persistence and the confirmation prompt.
- No live policy file, real socket, or external provider is needed.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-20, TC-21, TC-22 |
| FR-2 | TC-1, TC-2, TC-3, TC-4, TC-5, TC-6, TC-13, TC-14 |
| FR-3 | TC-17, TC-18, TC-15 |
| FR-4 | TC-15, TC-16, TC-11 |
| FR-5 | TC-23, TC-24 |
| FR-6 | TC-19, TC-10 |
| FR-7 | TC-25, TC-26, TC-27, TC-28, TC-29, TC-30, TC-31, TC-32, TC-33, TC-34 |
| FR-8 | TC-11, TC-50, TC-51 and the adjacent CLI bind refusal test |
| FR-9 | TC-35, TC-36, TC-37, TC-38, TC-47 |
| FR-10 | TC-44 |
| FR-11 | TC-39, TC-40, TC-41, TC-42, TC-48 |
| FR-12 | TC-46 |
| FR-13 | TC-49 |
| FR-14 | The adjacent `rateLimitKey` suite in `tunnel-host.test.js` |
| FR-15 | The adjacent UI store and webview route consumers, with no dedicated test in these three files |
| FR-16 | The adjacent `appLinkTrustStore.test.ts` and `appLinkConfirmation.test.ts` |
| FR-17 | TC-52, TC-53, TC-54 |
| NFR-1 | TC-19 |
| NFR-2 | TC-47, TC-48, TC-15 |
| NFR-3 | TC-45 |
| NFR-4 | TC-27, TC-32, TC-33 |
| NFR-5 | TC-3, TC-25, TC-35 |
| NFR-6 | The adjacent UI component and i18n conventions, with no dedicated test in these three files |

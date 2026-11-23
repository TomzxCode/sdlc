---
title: "Shared pages and local image grants"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Test plan: Shared pages and local image grants

## Scope

The plan covers the author's card, the server's group and crypto, the relay client, the recipient's open and answer flow, and local image authorization.
It uses the suites present in the two server modules and the UI modules.
Browser automation against a live relay is out of scope, and the relay viewer's own tests live in the website repository.

## Unit tests

| ID | Description | Input | Expected output | Source |
|---|---|---|---|---|
| TC-01 | Host and viewer derive the same auth bytes and hash | 32-byte link key and PIN `482913` | Host auth and auth hash equal a separate browser-style implementation | `packages/web/server/lib/share-pages/crypto.test.js` |
| TC-02 | Document and answer blobs interoperate and stay separate | Sealed document, viewer-sealed answer, wrong AAD and wrong PIN | Viewer opens the document, host opens the answer, wrong AAD or PIN rejects | `packages/web/server/lib/share-pages/crypto.test.js` |
| TC-03 | PIN generation stays uniform in shape | 200 generated PINs | Each matches six digits | `packages/web/server/lib/share-pages/crypto.test.js` |
| TC-04 | Relay calls verify against the relay's own check | Signed create, states and close calls | Verification of timestamp, server id, path, body hash and metadata passes | `packages/web/server/lib/share-pages/relay-client.test.js` |
| TC-05 | State reads batch at the relay limit | 120 share ids | Three `/p/states` calls, 120 states returned | `packages/web/server/lib/share-pages/relay-client.test.js` |
| TC-06 | Relay refusal keeps its status | Mocked 413 response | Rejection carries status 413 | `packages/web/server/lib/share-pages/relay-client.test.js` |
| TC-07 | Relay origin and enterprise policy | WebSocket URLs, settings and environment flags | HTTP origin derived from `/ws`, pinned relay wins, other relays refused in enterprise mode | `packages/web/server/lib/share-pages/relay-client.test.js` |
| TC-08 | Working-day deadline skips weekends | Monday, Thursday, Friday, Saturday and Sunday starts in local time | Two weekdays of elapsed time, with a weekend start counted from Monday 00:00 | `packages/web/server/lib/share-pages/expiry.test.js` |
| TC-09 | Shorter expiry only shortens | Friday 17:00 with 3 hours and with 168 hours | 3 hours moves the deadline earlier, 168 hours keeps the two-working-day deadline | `packages/web/server/lib/share-pages/expiry.test.js` |
| TC-10 | File inspection maps known file errors | `ENOENT`, `EACCES`, `EPERM`, `ELOOP` from `realpath` | `missing` for `ENOENT`, `error` for the others | `packages/web/server/lib/markdown-image-grants/inspect-image.test.js` |
| TC-11 | Unknown inspection failures propagate | Unexpected `Error`, `EIO`, null, undefined, string and number | The same value is rejected unchanged | `packages/web/server/lib/markdown-image-grants/inspect-image.test.js` |
| TC-12 | The `ui` page submitter posts one answer and settles on the viewer reply | Init, submit, second submit, `submit-result` | One message posted, second submit refused while pending and after success | `packages/ui/src/share-document/protocol.test.ts` |
| TC-13 | The submitter refuses what the viewer would | Wrong source, `wantsAnswer: false`, blank summary, saved answer | Viewer's error is passed on, no message is posted, saved answer blocks another | `packages/ui/src/share-document/protocol.test.ts` |
| TC-14 | Share input fields are parsed and validated | Object form, JSON text, no recipients, duplicate names, bad expiry | Parsed field set or a field-specific 400 error | `packages/web/server/lib/share-pages/runtime.test.js` |
| TC-15 | A pasted link is parsed only on an allowed relay | Whole link with key, path prefix, malformed and foreign links | Parsed base, share id and key, or `invalid_link` and `link_not_allowed` | `packages/web/server/lib/share-pages/received.test.js` |

## Integration tests

| ID | Description | Preconditions | Expected outcome | Source |
|---|---|---|---|---|
| TC-16 | Author routes serve group, document, cancel and preview | Group created for a session and call | First GET has null link and PIN, upload returns a link and PIN, second upload is 409, preview returns saved HTML, cancel marks cancelled | `packages/web/server/lib/share-pages/routes.test.js` |
| TC-17 | Unknown call and enterprise refusal | Disabled availability after group creation | 404 for an unknown call, 403 with `code: 'enterprise_mode'` for every route with no relay call | `packages/web/server/lib/share-pages/routes.test.js` |
| TC-18 | Author route bodies stay unchecked until the runtime | Missing body, array body, numeric HTML, numeric title | `html is required` for bad HTML, title falls back to the group title | `packages/web/server/lib/share-pages/routes.test.js` |
| TC-19 | Received route bodies keep inherited and absent values | Register and open with primitive JSON and arrays | Object containers reach the runtime, primitive JSON is 400 | `packages/web/server/lib/share-pages/routes.test.js` |
| TC-20 | Runtime uploads, delivers an answer and closes the share | Two recipients and a fake relay | One sealed upload per recipient, answer synthetic message posted, close called | `packages/web/server/lib/share-pages/runtime.test.js` |
| TC-21 | A failed upload is retried with the first saved document | One recipient's first upload throws | That recipient is `failed`, a later post uploads the saved copy and keeps its source | `packages/web/server/lib/share-pages/runtime.test.js` |
| TC-22 | Race and durability guards around cancel and delivery | Cancel reading a share while a poll collects an answer | Answer submitted in the gap is collected and delivered, and nothing is delivered before the answer and message id are saved | `packages/web/server/lib/share-pages/runtime.test.js` |
| TC-23 | Restart resumes uploads and notifies once per admitted answer | Group with a saved document and `preparing` recipient, then repeated delivery attempts | Upload finishes at start, 409 replay produces no notification | `packages/web/server/lib/share-pages/runtime.test.js` |
| TC-24 | Recipient registers, opens with PIN and answers | Author share held by a fake relay | No key in the registration response, document served, one answer readable by the author | `packages/web/server/lib/share-pages/received.test.js` |
| TC-25 | Received-page refusals and failure states | Five wrong PINs, read-only page, foreign relay, enterprise mode, unreachable relay, malformed state | Locked PIN state, refused answers and links, empty list and 403 routes, state kept on failed read, no redirect followed | `packages/web/server/lib/share-pages/received.test.js` |
| TC-26 | Image grants authorize exact sources with one message fetch | Workspace image, outside image and a missing path in one request | One fetch, no full-file read, `ready` with outside grant for outside paths, `missing` for absent files, encoded directory header | `packages/web/server/lib/markdown-image-grants/routes.test.js` |
| TC-27 | Image grants recognize every stored reference | Inline and reference syntax, balanced parentheses, missing title closure, rendered pages, `openchamber_image` and browser screenshots, spilled action JSON, code fences | Only declared sources are `ready`, syntax in code and other tools is `error`, a page a message does not hold is 404 | `packages/web/server/lib/markdown-image-grants/routes.test.js` |
| TC-28 | Page images respect weight, order and volume | Page of 9 MiB images, 19 images, 400 images and a request for a subset | Images up to 25 MiB are `ready` in page order, the first over budget and all after it are `too-heavy`, large source lists still work | `packages/web/server/lib/markdown-image-grants/routes.test.js` |
| TC-29 | An `html` share document is self-contained and speaks the viewer protocol | Built document mounted with a fake parent and activation | Both default themes present, no external address, one answer posted, viewer refusal and saved answer handled | `packages/ui/src/components/chat/sharePages/shareDocument.test.ts` |
| TC-30 | A `ui` share document carries the program and renderer safely | Program and bundle containing closing script tags and comments | Title escaped, exactly two scripts, original code recovered, no premature script end | `packages/ui/src/components/chat/sharePages/shareDocument.test.ts` |

## End-to-end tests

| ID | Description | Steps | Expected outcome | Source |
|---|---|---|---|---|
| TC-31 | Chat draws only safe local media through grants | Mount assistant message with remote, local and unsafe image schemes, settle, then inspect requests and DOM | Remote images stay links, unsafe schemes stay inert, the local file goes through the grant route after settlement | `packages/ui/src/components/chat/markdown/MarkdownMedia.test.tsx` |
| TC-32 | Media batches at most 12 sources and waits for viewport proximity | Mount 13 images, then each with an intersection observer | No request before settlement, at most 12 unique sources per batch, hidden views abort reads and reconnect | `packages/ui/src/components/chat/markdown/MarkdownMedia.test.tsx` |
| TC-33 | A recipient's viewer over the relay uses no further tunnel reads | Adopt a relay tunnel, mount an assistant image, open its gallery | Image is drawn from the grant path, gallery uses a data URL, tunnel read count unchanged | `packages/ui/src/components/chat/markdown/MarkdownMedia.test.tsx` |
| TC-34 | Failed and credential-bearing media do not leak URLs | Force image and video errors with signed and foreign raw URLs | Safe original links or labels remain, no token appears in markup, foreign URL triggers no auth refresh | `packages/ui/src/components/chat/markdown/MarkdownMedia.test.tsx` |
| TC-35 | Real markdown processing preserves document and assistant assets | Render with `MarkdownContent` and real processing options | Document assets resolve through the raw route, raw HTML stays off, embedded data images stay inline | `packages/ui/src/components/chat/markdown/MarkdownMedia.test.tsx` |

## Edge cases and failure scenarios

| ID | Scenario | Expected behavior |
|---|---|---|
| TC-E01 | A blob is opened with the other purpose's AAD or another PIN | Decryption rejects instead of returning partial data |
| TC-E02 | Two recipients share a case-insensitive label or a label exceeds 60 characters | Share input is refused with a field-specific error |
| TC-E03 | Expiry requested below one hour or past two working days | Minimum rejects, longer value is clamped to the working-day deadline |
| TC-E04 | A grant names a source not referenced by the stored message | The source returns `error` and no file is opened |
| TC-E05 | A workspace symlink points outside the active directory | Canonical containment check rejects the source |
| TC-E06 | A `.mp4` contains PNG bytes or a `.png` symlinks to a clip | Signature check rejects both, so the file is not read as the other media type |
| TC-E07 | An inline destination has an unclosed title or fragment text after the path | Destination parsing returns `error` or strips query and fragment text before resolving |
| TC-E08 | A page request names a call the message does not carry | 404 `Page not found` |
| TC-E09 | A page takes no answer, the send has no click gesture, or the summary is blank | Submit rejects locally and posts nothing |
| TC-E10 | A viewer reply comes from another source or has no source | The pending answer is unchanged and only a real viewer result settles it |
| TC-E11 | A shared page is shown again with a saved answer | The answer is inline before its scripts and another submit is refused |
| TC-E12 | A hidden view completes a stale read after reconnect | The late completion is rejected and a fresh read owns the media |
| TC-E13 | A relay sends a malformed state entry or a 5xx page | The entry is dropped and no local state changes |
| TC-E14 | Enterprise mode changes after a group was created on another relay | Every card route answers 403 and already admitted answers still deliver locally |

## Test infrastructure

- Server suites run under vitest with `supertest` against small Express apps that register only the routes under test.
- Group and received-page stores use temporary directories removed after each test, with POSIX mode checks for owner-only files.
- Relays are fakes holding sealed blobs and state, and UI suites use a signed request verifier written independently in the test.
- OpenCode message fetches are stubbed with `vi.stubGlobal`, and image fixtures include a PNG, an 11 MiB `ftyp` MP4 and EBML WebM bytes.
- UI suites run under `bun:test` with `happy-dom`, React `act`, an intersection observer stub and a relay tunnel fake.
- The crypto test reimplements the browser side of the contract instead of importing the host module, so a drift on either side fails.

## Coverage matrix

| Requirement | Test cases |
|---|---|
| FR-01 | TC-14, TC-16, TC-20 |
| FR-02 | TC-01, TC-03, TC-16, TC-20 |
| FR-03 | TC-29, TC-30, TC-31 |
| FR-04 | TC-01, TC-02, TC-04, TC-20, TC-21 |
| FR-05 | TC-08, TC-09 |
| FR-06 | TC-20, TC-22, TC-23 |
| FR-07 | TC-16, TC-20, TC-22, TC-24 |
| FR-08 | TC-16, TC-17, TC-29 |
| FR-09 | TC-15, TC-24, TC-25 |
| FR-10 | TC-12, TC-13, TC-24, TC-29 |
| FR-11 | TC-26, TC-27, TC-E04, TC-E05 |
| FR-12 | TC-28, TC-32, TC-E08 |
| FR-13 | TC-17, TC-23, TC-25, TC-33 |
| FR-14 | TC-07, TC-17, TC-25, TC-E14 |
| NFR-01 | TC-01, TC-04, TC-16, TC-24, TC-34 |
| NFR-02 | TC-01, TC-02, TC-E01 |
| NFR-03 | TC-04, TC-05, TC-06, TC-25 |
| NFR-04 | TC-10, TC-11, TC-26, TC-E05, TC-E06 |
| NFR-05 | TC-20, TC-22, TC-23 |
| NFR-06 | TC-05, TC-20 |
| NFR-07 | TC-16, TC-24, TC-E13 |
| NFR-08 | TC-29, TC-30, TC-31, TC-35 |

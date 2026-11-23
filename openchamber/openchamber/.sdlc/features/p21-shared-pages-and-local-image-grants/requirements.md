---
title: "Shared pages and local image grants"
status: done
session_link: "sync-sdlc 2026-11-23"
---

# Requirements: Shared pages and local image grants

## Overview

A user can turn part of a session into a shareable page published through the relay with a signed link and a PIN.
Local markdown images need scoped grants so a shared page can include them without exposing unrelated files.
The feature covers the author's card, the recipient's open and answer flow, and the image preparation both sides need.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Session author | Publish a rendered page to named people and see who opened or answered it |
| Recipient | Open a page with a link and PIN, read it with their own agent and send one answer |
| Organization admin | Constrain sharing to a relay the enterprise policy allows |
| Maintainer | Keep keys, links and untrusted content out of the transcript and the relay |

## Functional requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | Must | The system shall let a user ask the agent to publish a `ui` or `html` page to named recipients through `openchamber_render` with `share`. |
| FR-02 | Must | The system shall create one group per tool call and one distinct link and six-digit PIN per recipient. |
| FR-03 | Must | The system shall build a self-contained document with its renderer, styles, default themes and the reader's locale, and no network requests. |
| FR-04 | Must | The system shall seal the document per recipient and upload only ciphertext to the relay, keeping the source for the recipient's agent. |
| FR-05 | Must | The system shall expire a share after two working days in server local time with weekends skipped, and allow the author to shorten it. |
| FR-06 | Must | The system shall deliver a recipient's answer into the originating session as a steered synthetic message with resume, and notify once per admitted answer. |
| FR-07 | Must | The system shall close the relay share after collecting an answer and when a recipient withdraws a link. |
| FR-08 | Must | The author's card shall show recipient status, remaining time, Copy link, Copy PIN, Cancel and an Open action using the server's own copy. |
| FR-09 | Must | A recipient shall open a link and PIN in the app, where their own agent can read the page before they answer. |
| FR-10 | Must | A recipient's Send shall post one sealed answer, and neither the agent nor page scripts may answer without the recipient's gesture. |
| FR-11 | Must | The server shall grant local images only when their exact sources appear in the stored assistant message, a rendered page or a named tool result. |
| FR-12 | Must | The chat shall inline local images into a shared page as data URLs with at most 25 MB of source files per page, in page order. |
| FR-13 | Must | The server shall hold share state, links, PINs and answer keys, while runtimes without an OpenChamber server report sharing unavailable. |
| FR-14 | Should | The system shall restrict sharing and receiving to a pinned relay and answer 403 `enterprise_mode` when policy allows none. |

## Non-functional requirements

| ID | Priority | Category | Requirement |
|---|---|---|---|
| NFR-01 | Must | Security | Link keys, PINs and derived auth bytes shall never appear in logs, tool results, the model transcript or relay requests. |
| NFR-02 | Must | Security | The crypto shall use HKDF-SHA-256 with separate auth and enc info, AES-256-GCM with a version byte and a 12-byte IV, and distinct document and answer AAD. |
| NFR-03 | Must | Security | Relay calls shall be signed over method, path, body hash and metadata, use the relay's signing identity and refuse redirects. |
| NFR-04 | Must | Security | Image grants shall resolve workspace paths after `realpath`, reject symlink escapes, check file signatures and cap images at 10 MiB and video at 1 GiB. |
| NFR-05 | Must | Reliability | An answer and its message id shall be saved before delivery or acknowledgement, with a stable id, bounded retries and resume after restart. |
| NFR-06 | Must | Performance | The poller shall make one batched `/p/states` request per relay per minute with at most 50 share ids per request. |
| NFR-07 | Must | Availability | The stores shall keep at most 100 groups and 100 received pages, write atomically with owner-only modes and move corrupt records aside. |
| NFR-08 | Should | Compatibility | Shared pages shall run in a no-network sandboxed frame with default themes and reader locale across web, desktop and both mobile shells. |

## Acceptance criteria

Every FR and NFR has at least one criterion.

- [ ] **FR-01**

    ```gherkin
    @FR-01
    Scenario: Publish a page to named recipients
      Given a session with a completed `openchamber_render` call carrying a `ui` or `html` page
      When the page's `share` names recipients and the card posts the document
      Then a group exists for that session and call with a kind of `questionnaire` when an answer is expected and `page` otherwise
    ```

- [ ] **FR-02**

    ```gherkin
    @FR-02
    Scenario: One group and one link per recipient
      Given a share request naming two different people
      When the group is created and the document is uploaded
      Then the group id hashes the session and call ids, and each recipient has a distinct share id, 43-character link key and six-digit PIN
    ```

- [ ] **FR-03**

    ```gherkin
    @FR-03
    Scenario: A shared document needs nothing from the network
      Given a `ui` or `html` page with local images
      When the card builds the document
      Then the renderer, stylesheet, default light and dark themes, answer script and inlined images are inside the document and no external address appears in it
    ```

- [ ] **FR-04**

    ```gherkin
    @FR-04
    Scenario: Only ciphertext reaches the relay
      Given a prepared document with source text
      When each recipient's upload runs
      Then the relay receives a sealed blob and metadata with the kind, answer flag, expiry and auth hash, and the link key, PIN and plaintext source stay on the server
    ```

- [ ] **FR-05**

    ```gherkin
    @FR-05
    Scenario: A share expires after two working days
      Given a share created on Friday at 17:00 local time
      When no shorter lifetime is given
      Then its deadline is Tuesday at 17:00, and a `expiresInHours` value only moves the deadline earlier
    ```

- [ ] **FR-06**

    ```gherkin
    @FR-06
    Scenario: An answer wakes the originating session
      Given a recipient has submitted an answer and the poller read it
      When the answer is decrypted and saved
      Then a synthetic message with `delivery: 'steer'`, `resume: true` and a stable message id is posted once and a notification is emitted for an admitted answer
    ```

- [ ] **FR-07**

    ```gherkin
    @FR-07
    Scenario: A collected answer closes the relay share
      Given an answer was delivered or could not be decrypted
      When the close call runs
      Then the relay deletes the page and answer and the recipient is marked `relayClosed`
    ```

    ```gherkin
    @FR-07
    Scenario: Withdrawing a link before an answer
      Given a recipient link is still open
      When the author cancels it
      Then the relay state is read first, an answer submitted in the gap is collected and answered with 409, and otherwise the link is closed and marked `cancelled`
    ```

- [ ] **FR-08**

    ```gherkin
    @FR-08
    Scenario: The card reads status from the server
      Given a group with one recipient in each of `preparing`, `open` and `answered`
      When the card reads the group
      Then it shows those statuses with remaining time, offers Copy link and Copy PIN only for the open link, and Open shows the server's saved HTML rather than the relay link
    ```

- [ ] **FR-09**

    ```gherkin
    @FR-09
    Scenario: A recipient opens a page in the app
      Given a whole share link pasted into the composer on an allowed relay
      When the link lands and the correct PIN is entered
      Then the key goes to the server once, the chip keeps only a keyless link, and the page opens in the context panel or full screen on mobile with its source shown as data to the agent
    ```

- [ ] **FR-10**

    ```gherkin
    @FR-10
    Scenario: One answer from the recipient
      Given a page that expects an answer
      When the recipient presses Send
      Then a sealed answer with data, summary and submission time is posted, a second Send is refused, and page scripts cannot submit without an active user gesture
    ```

- [ ] **FR-11**

    ```gherkin
    @FR-11
    Scenario: Only referenced local images are granted
      Given an assistant message referring to one local image in text and another path that appears nowhere
      When a grant request names both sources
      Then the referenced source is `ready` and the other source is `error`
    ```

    ```gherkin
    @FR-11
    Scenario: Image syntax inside code is not a reference
      Given a message with `![fenced](FENCED)` inside a fence and `![inline](INLINE)` inside inline code
      When a grant request names both sources
      Then both sources return `error` and no file is read
    ```

- [ ] **FR-12**

    ```gherkin
    @FR-12
    Scenario: A page's images fit the weight budget in order
      Given a page naming a 9 MiB image, a missing image, another 9 MiB image and a third 9 MiB image
      When the chat prepares the page
      Then the first three entries are `ready`, `missing` and `ready`, and the third image plus every image after it is `too-heavy`
    ```

- [ ] **FR-13**

    ```gherkin
    @FR-13
    Scenario: Sharing follows the server
      Given web, desktop, hosted mobile and Capacitor mobile clients connected to a server, and a VS Code client with no OpenChamber server
      When each client looks for a shared page
      Then the first four read and upload through their server and the VS Code card reports sharing unavailable
    ```

- [ ] **FR-14**

    ```gherkin
    @FR-14
    Scenario: Enterprise mode without a pinned relay
      Given enterprise mode with no pinned relay URL
      When the card reads a group or posts a document
      Then every share route answers 403 with `code: 'enterprise_mode'`, the card hides links, PINs and preview, and no relay call is made
    ```

- [ ] **NFR-01**

    ```gherkin
    @NFR-01
    Scenario: Secrets stay out of outputs
      Given a created group with a link key and PIN per recipient
      When the tool result, server log and relay request are inspected
      Then none contains a link key, PIN, auth bytes or plaintext document, and only the group file and the card's GET answer carry the link and PIN
    ```

- [ ] **NFR-02**

    ```gherkin
    @NFR-02
    Scenario: Host and viewer derive the same keys
      Given a 32-byte link key and a six-digit PIN
      When the host derives keys and seals a document with the document AAD
      Then the viewer derives the same auth bytes and auth hash and opens the blob, and an answer sealed with the answer AAD opens on the host but a document blob opened with the answer AAD fails
    ```

- [ ] **NFR-03**

    ```gherkin
    @NFR-03
    Scenario: A relay call verifies against its signature contract
      Given a signed create, state or close request
      When the relay verifies method, path, timestamp, server id, body hash and metadata header
      Then the signature passes, and a redirect response is refused rather than followed
    ```

- [ ] **NFR-04**

    ```gherkin
    @NFR-04
    Scenario: Unsafe image files are rejected
      Given a workspace symlink pointing outside the workspace, a plain text file named `.png` and a 12 MiB PNG
      When each is inspected for a grant
      Then all three return `error` and no outside path is opened through a workspace reference
    ```

- [ ] **NFR-05**

    ```gherkin
    @NFR-05
    Scenario: An answer survives a failed delivery
      Given a decrypted answer whose first two synthetic-message attempts fail with a retryable error
      When the runtime retries and the server restarts before a later attempt
      Then the same minted message id is used, at most four attempts run per poll, and delivery resumes from the saved record
    ```

- [ ] **NFR-06**

    ```gherkin
    @NFR-06
    Scenario: One batched state read per relay
      Given 120 open shares on one relay
      When the poller reads their states
      Then three `/p/states` calls are made, each with at most 50 ids, and no call goes to a relay the policy no longer allows
    ```

- [ ] **NFR-07**

    ```gherkin
    @NFR-07
    Scenario: Stores bound their files and survive a corrupt record
      Given 101 finished groups and one malformed group file among valid files
      When the store loads and saves a group
      Then the oldest finished group and its HTML copy are removed, the malformed file is moved aside, the other groups load, and new files are written with mode `0600` in a `0700` directory
    ```

- [ ] **NFR-08**

    ```gherkin
    @NFR-08
    Scenario: A recipient sees default themes in a no-network frame
      Given a shared page in the recipient's app
      When the page is mounted in the sandboxed frame
      Then its stylesheet carries both default themes, follows the reader's system scheme and language, and contains no address that would request a network resource
    ```

## Conflicts

None identified.

## Open questions

1. Account-based verification of the answer's identity is deferred until accounts with known teammates exist.

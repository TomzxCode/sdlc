---
title: "Boards, Projects, and Session Cards"
status: done
session_link: "http://localhost:10000/?session=ses_eab0ae6abffe8Exw5lqWwhTxoA"
---

# Test Plan: Boards, Projects, and Session Cards

## Scope

This plan covers the board layout, board store, board capability validation, board HTTP route, board Gateway methods, the `dashboard` agent tool, the project registry, the project clone and checkout paths, the session progress card, and the shared Workboard contract.
It lists the existing test files that prove each requirement, so the coverage matrix maps a requirement onto the files that already exercise it.

Out of scope:

- The Control UI rendering of boards, project lists, and progress cards (FEAT-p8).
- The widget sandbox host, the content security policy builder, and the sandbox origin allocator (`src/gateway/board-sandbox.ts`).
- The canvas document composition and script validation behind `show_widget` (`src/canvas/`).
- The Workboard plugin's own dispatcher, worker execution, and browser UI; only the shared contract package is covered here.
- End-to-end tests through a live IDE client; the board and project surfaces are exercised through the Gateway method layer instead.

## Unit Tests

| ID | Description | Input | Expected Output |
|---|---|---|---|
| TC-1 | Board layout reorders widgets by position and `after` anchors, including cross-tab moves | A layout with two tabs and widgets at scattered positions | Widgets are densely ordered inside their tab and the moved widget lands after its anchor |
| TC-2 | Board layout rejects a missing anchor and a self anchor | `widget_move` with `after` naming an unknown widget, then `after` naming the moved widget | `BoardValidationError` with code `not_found` and code `invalid_operation` |
| TC-3 | Board layout clamps widget sizes to the grid | A resize to `sizeW` 40 and `sizeH` 40 | Stored size is width 12 and height 20, and the height mode is `fixed` |
| TC-4 | Board layout moves the widgets of a deleted tab to the first remaining tab | A layout with two tabs, the second holding widgets | The widgets keep their order and land on the first tab |
| TC-5 | Board layout refuses to delete the last tab that still holds widgets | A layout with one tab holding one widget | `BoardValidationError` with code `invalid_operation`; deleting an empty last tab succeeds |
| TC-6 | Board layout requires `tabs_reorder` to be an exact permutation | A reorder list with a missing tab and a duplicated tab | `BoardValidationError` with code `invalid_operation` |
| TC-7 | Board layout keeps nested widget metadata caller-owned | A layout operation over a widget that carries extra metadata | The metadata survives the operation and the caller's copy is not mutated in place |
| TC-8 | Capability declaration canonicalizes, deduplicates, and sorts | A declaration with repeated origins and tools | The normalized declaration holds unique, sorted origins and tools |
| TC-9 | Capability declaration refuses an origin set the sandbox CSP cannot carry | Origins that exceed the sandbox host's safe connect-domain limits | `BoardValidationError` with code `invalid_operation` |
| TC-10 | Capability declaration carries the full cron job id contract | An exact `cron.trigger:` capability with a 256 character job id | The capability is accepted and normalized unchanged |
| TC-11 | Manifest codec keeps registered content ownership apart from frame instance metadata | A stored registered widget | The content owner and the frame instance are reported independently |
| TC-12 | Manifest codec ignores invalid persisted frame preferences | A manifest holding an out-of-range preference | The invalid preference is dropped rather than surfaced |
| TC-13 | Manifest codec flags invalid generated name identity metadata | A manifest with a malformed name identity | The widget is reported as an invalid name identity |
| TC-14 | Progress card channel summary counts completed steps | Steps with two of three completed | The summary reports `2/3 complete` and the normalized steps |
| TC-15 | Progress card channel summary falls back to plain text | A card holding only markdown | The summary carries the stripped markdown with the plain explanation format |
| TC-16 | Sessions board contract normalizes column match rules | A column match over observer health, run state, pull request state, and the archived flag | The match is normalized into the contract shape |
| TC-17 | Sessions board contract exposes optional pull request details | A session with no pull request enrichment | The optional details and the rate-limit flag are optional, not required |

## Integration Tests

| ID | Description | Preconditions | Expected Outcome |
|---|---|---|---|
| TC-18 | Sqlite board store keeps content-kind semantics and normalized ordering | A store with an HTML widget, a plugin widget, and an MCP App widget | The snapshot keeps the three content kinds apart and the layout is densely ordered |
| TC-19 | Sqlite board store replaces omitted plugin props without touching unrelated layout state | A board with a plugin widget and a second widget | The plugin widget has empty props and the second widget is unchanged |
| TC-20 | Sqlite board store refuses oversized plugin props and capability declarations | Props over 8 KiB and a declaration over the count limits | Both writes are refused with a `BoardValidationError` |
| TC-21 | Sqlite board store keeps native widget identity across edits and renews it after removal | A board with a native widget | The instance identity survives an edit and changes after a removal and a re-put |
| TC-22 | Sqlite board store requires a fresh grant when an MCP App widget changes servers | A granted MCP App widget | The grant state returns to pending after the server set changes |
| TC-23 | Sqlite board store refuses a delayed grant after a remove and a same-name replacement | A pending grant, then a remove and a replacement put | The delayed grant is refused and the replacement keeps its own grant state |
| TC-24 | Sqlite board store fails closed on a persisted unsafe capability manifest | A manifest persisted before declaration validation | The widget is refused rather than served with an unvalidated declaration |
| TC-25 | Sqlite board store migrates the board tables into an existing v14 database | A database at schema version 14 | The board tables exist after the migration and the store reads them |
| TC-26 | Sqlite board store refuses board writes for a transcript-only placeholder node | A placeholder session node | The write is refused and no board row is created |
| TC-27 | Sqlite board store reads widget bytes only from the canonical per-agent database | A board whose widget lives in a per-agent database | The bytes come from the canonical database and no unregistered agent database is created |
| TC-28 | Sqlite board store requires re-approval for grants stored before byte-frozen semantics | A grant written under the older grant semantics | The widget reports a pending grant and is not served as granted |
| TC-29 | Session actor board store serializes writes without losing widgets | Two concurrent writes against one session actor | Both widgets are present and the read runs outside the write FIFO |
| TC-30 | Session actor board store prepares MCP interaction outside the FIFO and checks source permission at the write | A write whose source permission was revoked | The write is refused and the committed widget is not silently published |
| TC-31 | Session actor board store resets an empty board revision and retains registered documents | A board with registered documents and plugin instances | The documents are retained and the revision resets only when the board is empty |
| TC-32 | Project registry registers, orders, resolves real paths, deduplicates roots, and removes rows | A state store with no registry table | The table appears on first registration, entries are ordered, real paths are resolved, duplicate roots are deduplicated, and removal deletes the row |
| TC-33 | Project registry refuses a path outside a git checkout | A plain directory | The registration is refused with a checkout error |
| TC-34 | Project registry scopes private clone and refresh credentials to the repository origin | A project whose origin is a private host | The credentials go to the recorded origin only |
| TC-35 | Project registry revokes a stale refresh after a removal and an operator re-registration | A refresh in flight across a removal | The stale refresh is refused and the re-registered project is not refreshed by the old owner |
| TC-36 | Project registry classifies authentication failures without returning credential material | A failing private clone | The failure is classified and no credential appears in the error |
| TC-37 | Project clone registration removes the produced checkout after a definite pre-commit failure | A clone that fails before the registry insert | The checkout directory is removed and the registration error is preserved |
| TC-38 | Project clone registration keeps the checkout for an acknowledged registration | A successful clone and registration | The registration is acknowledged and the checkout is retained |
| TC-39 | Project environment keeps Windows state for remove, register, materialize, and refresh | A mocked win32 platform with a changed caller environment | The state directory and supervisor mode survive the caller change for every operation |
| TC-40 | Progress card store creates its lazy table once and retains facts across warm writes | A store with the lazy table present | The table is not recreated and the card content survives a write and a read |
| TC-41 | Progress card store treats a missing lazy table as no card | A store without the progress card table | The read returns no card and the table is not created by the read |
| TC-42 | Progress card store dismisses the card only at its expected revision | A card at revision 3 and a dismiss at revision 2 | The card is not dismissed and still reports revision 3 |
| TC-43 | Progress card store deletes the card when its owning session node is deleted | A card bound to a session node | The card row is gone after the session node is deleted |
| TC-44 | Board gateway methods scope bare boards by explicit owner | A board request without an agent and more than one candidate owner | The request is refused as ambiguous |
| TC-45 | Board gateway methods keep identical global widget notices separate for each owner | The same widget name and payload published for two owners | Each owner gets its own notice |
| TC-46 | Board gateway methods skip prompt confirmation only for an explicitly granted prompt tool | A widget with a granted prompt tool and a widget without | Only the granted widget skips the confirmation |
| TC-47 | Board gateway methods refuse an app-view request for a replaced widget revision | A widget replaced after the client read it | The app-view request is refused |
| TC-48 | Board gateway methods keep zero-tool MCP Apps read-only until an explicit grant | An MCP App with no declared tools | The app view is read-only and an upgrade is refused |
| TC-49 | Board GitHub Actions refuses another repository's grant | A grant for a repository the widget does not own | The grant is refused before any credential is prepared |
| TC-50 | Board GitHub Actions does not follow a redirect to another repository | A run endpoint that redirects elsewhere | The redirect is not followed |
| TC-51 | Board GitHub Actions coalesces successful reads and scopes the cache to the current credentials | Two concurrent reads of the same run | One upstream read happens and the cache entry is scoped to the filters and credentials |
| TC-52 | Board HTTP serves a ticket only through its issuing live Gateway | A ticket presented to a different Gateway | The request is refused |
| TC-53 | Board HTTP rejects garbage and expired tickets before reading the store | A malformed ticket and an expired ticket | Both are refused and the store is not read |
| TC-54 | Board HTTP withholds declared widget bytes until the operator grants them | A pending widget with declared capabilities | The bytes are not served |
| TC-55 | Board HTTP allows GET and HEAD only | A POST to the widget route | The request is refused with a method-not-allowed response |
| TC-56 | Progress card gateway methods round-trip markdown and steps and broadcast the revision | A write of markdown and steps | The card reads back with the same content, invisible Unicode stripped, and the revision is broadcast |
| TC-57 | Progress card gateway methods dismiss only the matching completed revision | A dismiss at a stale revision | The card is not dismissed |
| TC-58 | Progress card refresh deduplicates concurrent refresh bursts with distinct intents | Two concurrent refresh requests | One refresh runs to completion and the second joins it |
| TC-59 | Progress card refresh rejects read-only callers before admitting any turn | A caller without write scope | The refresh is refused and no turn is admitted |
| TC-60 | Project handlers list a normalized configured default repository | A config with a default repository | The listed project carries the normalized default |
| TC-61 | Project handlers expose checkout details only at write scope | A caller with read scope and a caller with write scope | Only the write-scope caller sees the checkout details |
| TC-62 | Project handlers redact credentials and URL suffixes from registered origins | A project whose origin URL carries a token | The response carries the redacted origin |
| TC-63 | Project handlers return INVALID_REQUEST for an unknown project id | A remove for an unknown id | The call returns the typed invalid-request error |
| TC-64 | Project handlers keep a cloned checkout while a duplicate registry row remains | A cloned project with a duplicate row | The checkout is preserved and the duplicate row is the one removed |
| TC-65 | Dashboard tool declares every dashboard action and does not override widget placement | The tool schema | The action list matches the contract and the placement fields are not forced |
| TC-66 | Dashboard tool dispatches through the admitted Gateway and fences replacement or retirement | A dashboard call after the widget was replaced | The call is fenced and the result reports the retired widget |
| TC-67 | Dashboard tool creates a plugin widget through `board.widget.put` | A `widget_put` action with a plugin kind | The plugin widget is created and the content ownership is reported |
| TC-68 | Dashboard tool reports commands as unavailable when no Control UI is connected | A dashboard call with no connected client | The result says the command is unavailable instead of failing |

## End-to-End Tests

| ID | Description | Steps | Expected Outcome |
|---|---|---|---|
| TC-69 | Board approval reuses a reviewed document in a new session but still gates changed bytes and names | Review a document, start a new session, then change the bytes and the name | The unchanged document is reused and the changed bytes and the changed name are gated again |
| TC-70 | Board approval refuses a cached assessment when grant authority is revoked during write admission | Start a write with a cached assessment, then revoke the grant | The write is refused |
| TC-71 | Board widget HTTP serves a widget document in the authorized read turn before a queued removal | Request the document, then queue a removal behind it | The document is served and the removal does not pre-empt the read |
| TC-72 | Progress card refresh keeps a new human message on its own visible turn while a hidden refresh runs | Send a message while a refresh is in flight | The message is delivered as its own turn and the refresh stays hidden |

## Edge Cases and Failure Scenarios

| ID | Scenario | Expected Behavior |
|---|---|---|
| TC-73 | A widget move names both a position and an `after` anchor | `BoardValidationError` with code `invalid_operation` |
| TC-74 | A widget move places a widget after itself | `BoardValidationError` with code `invalid_operation` |
| TC-75 | A tab update carries no changes | `BoardValidationError` with code `invalid_operation` |
| TC-76 | A `tab_create` reuses an existing tab id | `BoardValidationError` with code `conflict` |
| TC-77 | A widget put changes the content kind of an existing widget name | `BoardValidationError` with code `invalid_operation` naming both kinds |
| TC-78 | A generated widget fallback name is already taken | `BoardValidationError` with code `conflict` |
| TC-79 | A generated widget fallback name equals its own preferred name | `BoardValidationError` with code `invalid_operation` |
| TC-80 | A grant is recorded for a widget that is not pending | `BoardValidationError` with code `invalid_operation` |
| TC-81 | A grant names a different widget instance | `BoardValidationError` with code `conflict` |
| TC-82 | A board event payload exceeds 8 KiB | `BoardEventPayloadError`, and no system event is queued |
| TC-83 | The same board event payload repeats inside the 5 second window | The second notice is dropped and the method reports `appended: false` |
| TC-84 | A declared network origin carries a path, query, fragment, credentials, a wildcard, or a trailing dot | `BoardValidationError` with code `invalid_operation` |
| TC-85 | A declared tool name contains an ASCII control character or leading and trailing whitespace | `BoardValidationError` with code `invalid_operation` |
| TC-86 | A plugin widget carries a sandbox capability declaration | `BoardValidationError` with code `invalid_operation` |
| TC-87 | A report widget exceeds the 8 KiB JSON budget | `BoardValidationError` with code `invalid_operation` naming the budget |
| TC-88 | A report table row has a different cell count than the column count | `BoardValidationError` with code `invalid_operation` |
| TC-89 | A website widget URL uses a scheme other than HTTPS or embeds credentials | `BoardValidationError` with code `invalid_operation` |
| TC-90 | A board would hold more than 48 widgets | The write is refused and the board keeps its previous widget count |
| TC-91 | A project path is a file rather than a directory | `ProjectCheckoutError` naming the path |
| TC-92 | A project checkout has no commits | `ProjectCheckoutError` naming the path |
| TC-93 | A project removal fails after the checkout was already deleted | The registration error is preserved and reported |
| TC-94 | A progress card write carries only whitespace markdown | The markdown is treated as absent and the card is cleared |
| TC-95 | Stored progress card steps are not an array, or a step has an unknown status | The stored row is rejected as invalid rather than returned as a card |
| TC-96 | A project add names an unparsable remote URL | The call returns a typed invalid-URL failure |
| TC-97 | A project search surfaces an unexpected upstream error | The error diagnostics are redacted before the response |
| TC-98 | A `projects.list` call races with a replaced config | The default repository from the replaced config is refused |

## Test Infrastructure

- Vitest is the test runner for every file listed here; the suites live next to the code they cover.
- The board and progress card suites use real SQLite databases through the agent and state database helpers, so the schema constraints in the SQL files are exercised directly.
- `src/projects/project-environment.test.ts` forbids opening SQLite and touching the filesystem, so it isolates the lease and environment plumbing from the storage layer.
- `src/gateway/server-methods/projects.test.ts` counts SQLite statements to prove a list call does not fan out into broad reads.
- The project suites shell out to real `git` for the checkout resolution and clone paths, and use a mocked GitHub fetch for remote search.
- The board approval and GitHub Actions suites use a local GitHub Actions server stub, and they assert the no-redirect and wrong-repository cases.
- The Workboard contract suite is a pure unit suite over `@openclaw/workboard-contract` and needs no Gateway.

## Coverage Matrix

| Requirement | Test Cases |
|---|---|
| FR-1 | TC-1, TC-2, TC-4, TC-5, TC-6, TC-7, TC-18, TC-44 |
| FR-2 | TC-5, TC-6, TC-73, TC-74, TC-75, TC-76, TC-78, TC-79 |
| FR-3 | TC-3, TC-20, TC-87, TC-90 |
| FR-4 | TC-8, TC-9, TC-10, TC-20, TC-84, TC-85, TC-86 |
| FR-5 | TC-21, TC-22, TC-23, TC-24, TC-28, TC-30, TC-46, TC-47, TC-48, TC-49, TC-50, TC-54, TC-69, TC-70, TC-80, TC-81 |
| FR-6 | TC-87, TC-88, TC-89 |
| FR-7 | TC-65, TC-66, TC-67, TC-68, TC-77 |
| FR-8 | TC-11, TC-12, TC-13, TC-18, TC-19, TC-21, TC-25, TC-26, TC-27, TC-29, TC-31, TC-44 |
| FR-9 | TC-32, TC-33, TC-37, TC-38, TC-39, TC-91, TC-92, TC-93 |
| FR-10 | TC-34, TC-35, TC-36, TC-37, TC-64, TC-96 |
| FR-11 | TC-14, TC-15, TC-40, TC-41, TC-42, TC-43, TC-56, TC-57, TC-58, TC-59, TC-94, TC-95 |
| FR-12 | TC-45, TC-82, TC-83 |
| FR-13 | TC-60, TC-61, TC-62, TC-63, TC-97, TC-98 |
| FR-14 | TC-16, TC-17 |
| NFR-1 | TC-9, TC-20, TC-24, TC-46, TC-54, TC-84, TC-85, TC-86, TC-88, TC-89 |
| NFR-2 | TC-5, TC-20, TC-28, TC-29, TC-32, TC-37, TC-38, TC-42, TC-51, TC-70, TC-93 |
| NFR-3 | TC-3, TC-20, TC-87, TC-90 |
| NFR-4 | TC-52, TC-53, TC-54, TC-55, TC-71, TC-72, TC-82 |
| NFR-5 | TC-25, TC-32, TC-40, TC-41, TC-43 |
